#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小爪健康检查系统 v1.0
自动监控系统健康状态

功能：
- 检查关键服务
- 自动重启失败服务
- 发送通知
- 记录日志
"""

import os
import time
import json
import subprocess
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ServiceCheck:
    """服务检查"""
    name: str
    check_command: str
    expected_pattern: str = None
    restart_command: str = None
    port: int = None
    status: str = "unknown"
    last_check: str = None
    uptime: str = None
    restart_count: int = 0


class HealthMonitor:
    """健康监控器"""
    
    def __init__(self):
        self.log_file = '/home/admin/.openclaw/workspace/选股结果/health_check.log'
        self.status_file = '/home/admin/.openclaw/workspace/选股结果/service_status.json'
        
        # 定义需要监控的服务
        self.services = [
            ServiceCheck(
                name="OpenClaw Gateway",
                check_command="curl -s -o /dev/null -w '%{http_code}' http://localhost:3003/api/status || echo 'failed'",
                restart_command="openclaw gateway restart",
                port=3003
            ),
            ServiceCheck(
                name="Security System",
                check_command="curl -s http://localhost:3009/health",
                expected_pattern='"status":"healthy"',
                restart_command="node /home/admin/.openclaw/workspace/start_security_system.js",
                port=3009
            ),
            ServiceCheck(
                name="Feishu Bot",
                check_command="pgrep -f 'feishu' || echo 'not running'",
                restart_command="python3 /home/admin/.openclaw/workspace/feishu_bot.py"
            ),
            ServiceCheck(
                name="System CPU",
                check_command="top -b -n 1 | grep 'Cpu(s)' | awk '{print $2}'",
                expected_pattern="^[0-9]",
                port=None
            ),
            ServiceCheck(
                name="System Memory",
                check_command="free -h | grep Mem:",
                expected_pattern="available"
            ),
            ServiceCheck(
                name="Disk Space",
                check_command="df -h /home/admin/.openclaw/workspace | tail -1 | awk '{print $5}'",
                expected_pattern="^[0-9]",
                port=None
            ),
        ]
    
    def check_service(self, service: ServiceCheck) -> Dict:
        """检查单个服务"""
        result = {
            'name': service.name,
            'check_time': datetime.now().isoformat(),
            'status': 'unknown',
            'message': '',
            'needs_restart': False
        }
        
        try:
            # 执行检查命令
            output = subprocess.run(
                service.check_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            output_text = output.stdout.strip()
            
            # 检查端口
            if service.port:
                if output_text in ['200', '000'] or 'failed' in output_text:
                    if output_text == '200':
                        result['status'] = 'healthy'
                        result['message'] = '服务运行正常'
                    else:
                        result['status'] = 'unhealthy'
                        result['message'] = f'HTTP状态码: {output_text}'
                        result['needs_restart'] = True
                else:
                    result['status'] = 'healthy'
                    result['message'] = f'响应正常: {output_text[:50]}'
            
            # 检查命令输出
            else:
                if not output_text:
                    result['status'] = 'unknown'
                    result['message'] = '无输出'
                elif service.expected_pattern:
                    if service.expected_pattern in output_text:
                        result['status'] = 'healthy'
                        result['message'] = f'匹配成功: {output_text[:50]}'
                    else:
                        result['status'] = 'warning'
                        result['message'] = f'不匹配: {output_text[:50]}'
                else:
                    result['status'] = 'healthy'
                    result['message'] = f'输出: {output_text[:50]}'
        
        except subprocess.TimeoutExpired:
            result['status'] = 'error'
            result['message'] = '检查超时'
        except Exception as e:
            result['status'] = 'error'
            result['message'] = f'错误: {str(e)}'
        
        service.last_check = result['check_time']
        service.status = result['status']
        
        return result
    
    def restart_service(self, service: ServiceCheck) -> bool:
        """重启服务"""
        if not service.restart_command:
            return False
        
        try:
            print(f"  🔄 重启 {service.name}...")
            
            output = subprocess.run(
                service.restart_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if output.returncode == 0:
                service.restart_count += 1
                print(f"  ✅ {service.name} 重启成功")
                return True
            else:
                print(f"  ❌ {service.name} 重启失败: {output.stderr}")
                return False
        
        except Exception as e:
            print(f"  ❌ 重启错误: {e}")
            return False
    
    def run_health_check(self, auto_restart: bool = True) -> Dict:
        """执行健康检查"""
        print("\n🏥 小爪健康检查")
        print("=" * 60)
        print(f"⏰ 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        results = {
            'check_time': datetime.now().isoformat(),
            'services': [],
            'summary': {
                'total': len(self.services),
                'healthy': 0,
                'warning': 0,
                'unhealthy': 0,
                'error': 0
            }
        }
        
        for service in self.services:
            print(f"检查 {service.name}...", end=" ")
            
            result = self.check_service(service)
            results['services'].append(result)
            
            # 打印状态
            status_icon = {
                'healthy': '✅',
                'warning': '⚠️',
                'unhealthy': '❌',
                'unknown': '❓',
                'error': '💥'
            }
            icon = status_icon.get(result['status'], '❓')
            print(f"{icon} {result['message']}")
            
            # 更新统计
            results['summary'][result['status']] += 1
            
            # 自动重启
            if result['needs_restart'] and auto_restart and service.restart_command:
                self.restart_service(service)
        
        # 打印总结
        print()
        print("=" * 60)
        print(f"📊 检查总结:")
        print(f"  ✅ 正常: {results['summary']['healthy']}")
        print(f"  ⚠️ 警告: {results['summary']['warning']}")
        print(f"  ❌ 异常: {results['summary']['unhealthy']}")
        print(f"  💥 错误: {results['summary']['error']}")
        
        # 总体状态
        if results['summary']['unhealthy'] > 0 or results['summary']['error'] > 0:
            overall = '⚠️ 需要关注'
        elif results['summary']['warning'] > 0:
            overall = '✅ 基本正常'
        else:
            overall = '🎉 全部正常!'
        
        print(f"\n🎯 总体状态: {overall}")
        print("=" * 60)
        
        # 保存结果
        self.save_status(results)
        self.log_check(results)
        
        return results
    
    def save_status(self, results: Dict):
        """保存状态"""
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    
    def log_check(self, results: Dict):
        """记录日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        log_entry = f"[{timestamp}] "
        log_entry += f"健康:{results['summary']['healthy']} "
        log_entry += f"警告:{results['summary']['warning']} "
        log_entry += f"异常:{results['summary']['unhealthy']} "
        log_entry += f"错误:{results['summary']['error']}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def run_continuous_monitor(self, interval: int = 300, count: int = None):
        """
        持续监控
        
        Args:
            interval: 检查间隔（秒）
            count: 检查次数，None表示无限
        """
        print(f"\n🚀 启动持续监控")
        print(f"  间隔: {interval}秒")
        print(f"  次数: {'无限' if count is None else count}")
        print("  按 Ctrl+C 停止")
        print()
        
        check_count = 0
        
        try:
            while count is None or check_count < count:
                check_count += 1
                print(f"\n[{check_count}] 执行检查...")
                self.run_health_check(auto_restart=True)
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n\n👋 监控已停止")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='小爪健康检查')
    parser.add_argument('--continuous', '-c', action='store_true', help='持续监控')
    parser.add_argument('--interval', '-i', type=int, default=300, help='检查间隔(秒)')
    parser.add_argument('--count', '-n', type=int, default=None, help='检查次数')
    
    args = parser.parse_args()
    
    monitor = HealthMonitor()
    
    if args.continuous:
        monitor.run_continuous_monitor(args.interval, args.count)
    else:
        monitor.run_health_check()


if __name__ == '__main__':
    main()
