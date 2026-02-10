// 安全系统基本使用示例
const SecurityDefense = require('./security_defense');

const security = new SecurityDefense({
  port: 3009,
  features: {
    inputValidation: true,
    threatDetection: true,
    outputFiltering: true,
    behaviorMonitoring: true
  }
});

security.start();

console.log('🛡️ 安全系统已启动，监听端口 3009');
