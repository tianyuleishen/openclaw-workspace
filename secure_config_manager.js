/**
 * Secure Configuration Manager
 * Manages sensitive configuration data securely
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

class SecureConfigManager {
  constructor() {
    this.configDir = path.join(__dirname, 'secure_configs');
    this.encryptionKey = this.getOrCreateEncryptionKey();
    this.configCache = new Map();
    
    // Ensure secure config directory exists
    if (!fs.existsSync(this.configDir)) {
      fs.mkdirSync(this.configDir, { recursive: true });
    }
  }

  /**
   * Get or create encryption key
   */
  getOrCreateEncryptionKey() {
    const keyPath = path.join(__dirname, '.encryption_key');
    
    if (fs.existsSync(keyPath)) {
      return fs.readFileSync(keyPath);
    } else {
      // Generate a new encryption key
      const key = crypto.randomBytes(32); // 256-bit key
      fs.writeFileSync(keyPath, key);
      
      // Set restrictive permissions
      fs.chmodSync(keyPath, '600'); // Owner read/write only
      
      return key;
    }
  }

  /**
   * Encrypt data
   */
  encrypt(data) {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-gcm', this.encryptionKey, iv);
    let encrypted = cipher.update(JSON.stringify(data), 'utf8', 'hex');
    encrypted += cipher.final('hex');
    
    const authTag = cipher.getAuthTag();
    
    return {
      iv: iv.toString('hex'),
      encrypted: encrypted,
      authTag: authTag.toString('hex')
    };
  }

  /**
   * Decrypt data
   */
  decrypt(encryptedData) {
    const iv = Buffer.from(encryptedData.iv, 'hex');
    const authTag = Buffer.from(encryptedData.authTag, 'hex');
    const encrypted = encryptedData.encrypted;
    
    const decipher = crypto.createDecipheriv('aes-256-gcm', this.encryptionKey, iv);
    decipher.setAuthTag(authTag);
    
    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    
    return JSON.parse(decrypted);
  }

  /**
   * Store sensitive configuration securely
   */
  storeConfig(name, configData, options = {}) {
    const encryptedData = this.encrypt(configData);
    const configPath = path.join(this.configDir, `${name}.enc`);
    
    fs.writeFileSync(configPath, JSON.stringify(encryptedData));
    
    // Set restrictive permissions
    fs.chmodSync(configPath, '600'); // Owner read/write only
    
    // Cache the config
    this.configCache.set(name, configData);
    
    console.log(`🔒 Securely stored configuration: ${name}`);
    
    return { success: true, path: configPath };
  }

  /**
   * Retrieve sensitive configuration
   */
  retrieveConfig(name) {
    // Check cache first
    if (this.configCache.has(name)) {
      return this.configCache.get(name);
    }
    
    const configPath = path.join(this.configDir, `${name}.enc`);
    
    if (!fs.existsSync(configPath)) {
      throw new Error(`Configuration ${name} not found`);
    }
    
    const encryptedData = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const decryptedData = this.decrypt(encryptedData);
    
    // Cache the config
    this.configCache.set(name, decryptedData);
    
    return decryptedData;
  }

  /**
   * Update configuration securely
   */
  updateConfig(name, newData) {
    // Retrieve existing config to merge
    let existingData = {};
    
    try {
      existingData = this.retrieveConfig(name);
    } catch (error) {
      // Config doesn't exist yet, start with empty object
      console.log(`📝 Creating new configuration: ${name}`);
    }
    
    // Merge new data with existing
    const mergedData = { ...existingData, ...newData };
    
    // Store the updated config
    return this.storeConfig(name, mergedData);
  }

  /**
   * Remove configuration
   */
  removeConfig(name) {
    const configPath = path.join(this.configDir, `${name}.enc`);
    
    if (fs.existsSync(configPath)) {
      fs.unlinkSync(configPath);
      this.configCache.delete(name);
      console.log(`🗑️  Removed configuration: ${name}`);
      return { success: true };
    }
    
    return { success: false, error: `Configuration ${name} not found` };
  }

  /**
   * List all stored configurations
   */
  listConfigs() {
    const files = fs.readdirSync(this.configDir);
    return files
      .filter(file => file.endsWith('.enc'))
      .map(file => file.replace('.enc', ''));
  }

  /**
   * Rotate encryption key
   */
  rotateEncryptionKey() {
    const oldKey = this.encryptionKey;
    const oldKeyPath = path.join(__dirname, '.encryption_key');
    
    // Generate new key
    const newKey = crypto.randomBytes(32);
    const newKeyPath = path.join(__dirname, '.encryption_key.new');
    
    fs.writeFileSync(newKeyPath, newKey);
    fs.chmodSync(newKeyPath, '600');
    
    // Re-encrypt all configs with new key
    const configNames = this.listConfigs();
    
    for (const configName of configNames) {
      const configData = this.retrieveConfig(configName);
      
      // Temporarily use new key
      this.encryptionKey = newKey;
      this.storeConfig(configName, configData);
      
      // Clear cache to force re-read
      this.configCache.delete(configName);
    }
    
    // Replace old key file with new one
    fs.renameSync(newKeyPath, oldKeyPath);
    
    // Restore new key
    this.encryptionKey = newKey;
    
    console.log('🔄 Encryption key rotated successfully');
    
    return { success: true, configCount: configNames.length };
  }

  /**
   * Get security report
   */
  getSecurityReport() {
    const configs = this.listConfigs();
    const report = {
      timestamp: new Date().toISOString(),
      configCount: configs.length,
      configs: configs,
      encryptionEnabled: true,
      keyRotationRequired: false
    };
    
    return report;
  }
}

// If running directly, demonstrate usage
if (require.main === module) {
  const configManager = new SecureConfigManager();
  
  console.log('🔐 Secure Configuration Manager initialized');
  console.log('📋 Current configurations:', configManager.listConfigs());
  
  // Example usage
  const exampleConfig = {
    apiKeys: {
      moltbook: 'moltbook_sk_2Yfnf5cOudo28BjhWeCQ0w0EJNEBExlK',
      aiBridge: 'enhanced-bridge-key-f409e07f09b88876c3069'
    },
    tokens: {
      tushare: 'YOUR_TUSHARE_TOKEN',
      github: '[REDACTED]'
    },
    secrets: {
      feishuAppSecret: '[REDACTED]'
    }
  };
  
  // Store example config
  configManager.storeConfig('main_secrets', exampleConfig);
  
  // Retrieve and verify
  const retrievedConfig = configManager.retrieveConfig('main_secrets');
  console.log('✅ Retrieved config keys:', Object.keys(retrievedConfig));
  
  console.log('\n📋 Security Report:');
  console.log(JSON.stringify(configManager.getSecurityReport(), null, 2));
  
  console.log('\n🔒 The Secure Configuration Manager is ready to protect sensitive data.');
}

module.exports = SecureConfigManager;

console.log('Secure Configuration Manager module loaded successfully');