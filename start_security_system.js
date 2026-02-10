#!/usr/bin/env node

/**
 * OpenClaw Security Defense System Startup Script
 * Initializes and starts the security defense system
 */

const fs = require('fs');
const path = require('path');

console.log('🚀 Starting OpenClaw Security Defense System...');

// Check if required modules exist
const requiredFiles = [
  './security_defense.js',
  './integrate_security_defense.js'
];

for (const file of requiredFiles) {
  if (!fs.existsSync(path.join(__dirname, file))) {
    console.error(`❌ Required file missing: ${file}`);
    process.exit(1);
  }
}

try {
  // Import the security integration module
  const SecurityIntegration = require('./integrate_security_defense');
  
  // Create and start the security integration
  const securityIntegration = new SecurityIntegration();
  const status = securityIntegration.start();
  
  // Save the security integration instance globally
  global.securityIntegration = securityIntegration;
  
  console.log('\n✅ OpenClaw Security Defense System started successfully!');
  console.log('\n🛡️  Security Features Active:');
  console.log('   • Input validation and threat detection');
  console.log('   • Context isolation');
  console.log('   • Output filtering');
  console.log('   • Behavior monitoring');
  console.log('   • Security violation logging');
  console.log('   • Anomaly detection');
  
  // Create a simple health check endpoint
  const http = require('http');
  
  const server = http.createServer((req, res) => {
    if (req.url === '/health') {
      res.writeHead(200, {'Content-Type': 'application/json'});
      res.end(JSON.stringify({
        status: 'healthy',
        service: 'OpenClaw Security Defense System',
        timestamp: new Date().toISOString(),
        features: {
          inputValidation: true,
          threatDetection: true,
          outputFiltering: true,
          behaviorMonitoring: true,
          logging: true
        }
      }));
    } else if (req.url === '/status') {
      res.writeHead(200, {'Content-Type': 'application/json'});
      res.end(JSON.stringify(securityIntegration.getStatus()));
    } else {
      res.writeHead(404, {'Content-Type': 'text/plain'});
      res.end('Not found');
    }
  });
  
  const PORT = 3009; // Security system monitoring port
  server.listen(PORT, () => {
    console.log(`\n📊 Security monitoring server running on port ${PORT}`);
    console.log(`   Health check: http://localhost:${PORT}/health`);
    console.log(`   Status: http://localhost:${PORT}/status`);
  });
  
  // Set up graceful shutdown
  process.on('SIGTERM', () => {
    console.log('\n🛑 Shutting down OpenClaw Security Defense System...');
    server.close(() => {
      console.log('✅ Security Defense System shut down gracefully');
      process.exit(0);
    });
  });
  
  process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down OpenClaw Security Defense System...');
    server.close(() => {
      console.log('✅ Security Defense System shut down gracefully');
      process.exit(0);
    });
  });
  
  console.log('\n🎯 The OpenClaw Security Defense System is now protecting the AI agent environment.');
  console.log('   Security measures are active and monitoring for potential threats.');

} catch (error) {
  console.error('❌ Failed to start OpenClaw Security Defense System:', error);
  process.exit(1);
}