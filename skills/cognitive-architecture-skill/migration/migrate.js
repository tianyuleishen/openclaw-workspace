/**
 * Cognitive Architecture Skill Migration System
 * Preserves memory documents during upgrades
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class MigrationSystem {
  constructor(currentVersion, newVersion) {
    this.currentVersion = currentVersion;
    this.newVersion = newVersion;
    this.backupDir = path.join(__dirname, '..', 'backups');
    this.memoryDir = path.join(__dirname, '..', 'memory');
  }

  /**
   * Creates a backup of the current memory system data
   */
  createBackup() {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupPath = path.join(this.backupDir, `backup_${timestamp}`);
    
    console.log(`Creating backup at: ${backupPath}`);
    
    // Create backup directory if it doesn't exist
    if (!fs.existsSync(this.backupDir)) {
      fs.mkdirSync(this.backupDir, { recursive: true });
    }
    
    // Copy memory data to backup
    if (fs.existsSync(this.memoryDir)) {
      this.copyDirectory(this.memoryDir, path.join(backupPath, 'memory'));
    }
    
    // Copy other important data
    const importantFiles = ['memory_system.js', 'reasoning_engine.js', 'coordination_system.js'];
    const backupDataPath = path.join(backupPath, 'data');
    if (!fs.existsSync(backupDataPath)) {
      fs.mkdirSync(backupDataPath, { recursive: true });
    }
    
    for (const file of importantFiles) {
      const filePath = path.join(__dirname, '..', file);
      if (fs.existsSync(filePath)) {
        fs.copyFileSync(filePath, path.join(backupDataPath, file));
      }
    }
    
    // Write backup info
    const backupInfo = {
      timestamp,
      fromVersion: this.currentVersion,
      toVersion: this.newVersion,
      backedUpFiles: fs.readdirSync(this.memoryDir || '.').filter(f => f !== 'migration'),
      backupPath
    };
    
    fs.writeFileSync(path.join(backupPath, 'backup_info.json'), JSON.stringify(backupInfo, null, 2));
    
    console.log(`Backup completed successfully: ${backupPath}`);
    return backupPath;
  }

  /**
   * Copies a directory recursively
   */
  copyDirectory(src, dest) {
    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }
    
    const entries = fs.readdirSync(src);
    
    for (const entry of entries) {
      const srcPath = path.join(src, entry);
      const destPath = path.join(dest, entry);
      
      if (fs.lstatSync(srcPath).isDirectory()) {
        this.copyDirectory(srcPath, destPath);
      } else {
        fs.copyFileSync(srcPath, destPath);
      }
    }
  }

  /**
   * Migrates memory data from old format to new format
   */
  migrateMemoryData() {
    console.log('Starting memory data migration...');
    
    // Preserve existing memory data during upgrade
    const memoryDir = path.join(__dirname, '..', 'memory');
    if (!fs.existsSync(memoryDir)) {
      fs.mkdirSync(memoryDir, { recursive: true });
    }
    
    // Check for existing memory files and preserve them
    const oldMemoryFiles = this.findMemoryFiles();
    
    console.log(`Found ${oldMemoryFiles.length} memory files to preserve`);
    
    // Perform any necessary format conversions
    this.convertMemoryFormats(oldMemoryFiles);
    
    console.log('Memory data migration completed');
  }

  /**
   * Finds all memory-related files that need to be preserved
   */
  findMemoryFiles() {
    const memoryPatterns = [
      '*.json',
      '*.txt',
      '*.mem',
      'memory/**/*',
      'episodes/**/*',
      'long_term/**/*'
    ];
    
    const files = [];
    
    // Look for memory-related directories and files
    const dirsToCheck = [
      path.join(__dirname, '..', 'memory'),
      path.join(__dirname, '..'),
    ];
    
    for (const dir of dirsToCheck) {
      if (fs.existsSync(dir)) {
        const dirFiles = fs.readdirSync(dir);
        for (const file of dirFiles) {
          if (file.includes('memory') || file.includes('episode') || file.includes('long_term')) {
            files.push(path.join(dir, file));
          }
        }
      }
    }
    
    return files;
  }

  /**
   * Converts memory formats if needed for compatibility
   */
  convertMemoryFormats(files) {
    // Placeholder for format conversion logic
    // This would contain specific conversion routines for different memory formats
    console.log('Checking memory format compatibility...');
    
    for (const file of files) {
      try {
        if (file.endsWith('.json')) {
          // Validate and potentially update JSON structure
          const content = JSON.parse(fs.readFileSync(file, 'utf8'));
          
          // Apply any necessary transformations for version compatibility
          const updatedContent = this.updateMemoryStructure(content);
          
          if (JSON.stringify(content) !== JSON.stringify(updatedContent)) {
            fs.writeFileSync(file, JSON.stringify(updatedContent, null, 2));
            console.log(`Updated memory structure in: ${file}`);
          }
        }
      } catch (error) {
        console.warn(`Could not process memory file ${file}:`, error.message);
      }
    }
  }

  /**
   * Updates memory structure for compatibility with new version
   */
  updateMemoryStructure(memoryData) {
    // Example transformation - would be customized based on actual changes
    if (typeof memoryData === 'object' && memoryData !== null) {
      // Add version field if missing
      if (!memoryData.version) {
        memoryData.version = this.newVersion;
      }
      
      // Apply other transformations as needed
      // This is where specific migration logic would go
    }
    
    return memoryData;
  }

  /**
   * Restores data from a backup
   */
  restoreFromBackup(backupPath) {
    console.log(`Restoring from backup: ${backupPath}`);
    
    const backupMemoryPath = path.join(backupPath, 'memory');
    const currentMemoryPath = path.join(__dirname, '..', 'memory');
    
    if (fs.existsSync(backupMemoryPath)) {
      this.copyDirectory(backupMemoryPath, currentMemoryPath);
      console.log('Memory data restored successfully');
    } else {
      console.log('No memory data found in backup');
    }
    
    // Restore other data if needed
    const backupDataPath = path.join(backupPath, 'data');
    if (fs.existsSync(backupDataPath)) {
      const files = fs.readdirSync(backupDataPath);
      for (const file of files) {
        const srcFile = path.join(backupDataPath, file);
        const destFile = path.join(__dirname, '..', file);
        fs.copyFileSync(srcFile, destFile);
      }
    }
  }

  /**
   * Performs the complete migration process
   */
  performMigration() {
    console.log(`Starting migration from ${this.currentVersion} to ${this.newVersion}`);
    
    // Step 1: Create backup
    const backupPath = this.createBackup();
    
    // Step 2: Perform memory data migration
    this.migrateMemoryData();
    
    // Step 3: Update version information
    this.updateVersionInfo();
    
    console.log(`Migration from ${this.currentVersion} to ${this.newVersion} completed successfully`);
    console.log(`Backup available at: ${backupPath}`);
    
    return { success: true, backupPath };
  }

  /**
   * Updates version information in the system
   */
  updateVersionInfo() {
    const versionFile = path.join(__dirname, '..', 'VERSION');
    fs.writeFileSync(versionFile, this.newVersion);
    
    // Update package.json if it exists
    const pkgFile = path.join(__dirname, '..', 'package.json');
    if (fs.existsSync(pkgFile)) {
      const pkg = JSON.parse(fs.readFileSync(pkgFile, 'utf8'));
      pkg.version = this.newVersion;
      fs.writeFileSync(pkgFile, JSON.stringify(pkg, null, 2));
    }
  }
}

// Export the MigrationSystem class
module.exports = MigrationSystem;

// If running directly, perform migration based on arguments
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.error('Usage: node migrate.js <current_version> <new_version>');
    process.exit(1);
  }
  
  const [currentVersion, newVersion] = args;
  const migrator = new MigrationSystem(currentVersion, newVersion);
  
  try {
    const result = migrator.performMigration();
    console.log('Migration completed:', result);
  } catch (error) {
    console.error('Migration failed:', error);
    process.exit(1);
  }
}