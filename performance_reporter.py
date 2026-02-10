#!/usr/bin/env python3
"""
性能报告生成器 - 扩展功能 2
自动生成性能报告并分析优化空间
"""

import json
from datetime import datetime

class PerformanceReporter:
    """性能报告生成器"""
    
    def __init__(self):
        self.metrics = []
        
    def add_metric(self, name: str, value: float, unit: str):
        """添加指标"""
        self.metrics.append({
            'name': name,
            'value': value,
            'unit': unit,
            'timestamp': datetime.now().isoformat()
        })
        
    def generate_report(self) -> dict:
        """生成报告"""
        return {
            'timestamp': datetime.now().isoformat(),
            'metrics_count': len(self.metrics),
            'metrics': self.metrics,
            'recommendations': self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> list:
        """生成优化建议"""
        recommendations = []
        
        for metric in self.metrics:
            if 'latency' in metric['name'].lower() and metric['value'] > 10:
                recommendations.append({
                    'type': 'latency',
                    'suggestion': '延迟较高，考虑优化批处理',
                    'priority': 'medium'
                })
            elif 'throughput' in metric['name'].lower() and metric['value'] < 100:
                recommendations.append({
                    'type': 'throughput',
                    'suggestion': '吞吐量较低，考虑增加并发',
                    'priority': 'high'
                })
        
        return recommendations
    
    def save_report(self, filename: str = None):
        """保存报告"""
        if filename is None:
            filename = f"performance_report_{datetime.now().strftime('%Y%m%d')}.json"
        
        report = self.generate_report()
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        return filename

if __name__ == "__main__":
    reporter = PerformanceReporter()
    reporter.add_metric('throughput', 137.42, 'req/s')
    reporter.add_metric('latency', 7.26, 'ms')
    reporter.add_metric('success_rate', 100.0, '%')
    
    report_file = reporter.save_report()
    print("✅ 性能报告生成器已创建")
    print(f"   • 报告文件: {report_file}")
