#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TuShare Pro API 股票数据接口
基于官方文档: https://tushare.pro/document/2?doc_id=27

功能：
- 获取A股日线行情
- 支持多股票批量提取
- 支持复权数据
"""

import requests
import json
import time
from typing import List, Dict, Optional, Union
from datetime import datetime, timedelta


class TuSharePro:
    """TuShare Pro API 客户端"""
    
    def __init__(self, token: str):
        """
        初始化TuShare客户端
        
        Args:
            token: TuShare Pro API Token
        """
        self.token = token
        self.base_url = 'https://api.tushare.pro'
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
        
    def _request(self, api_name: str, params: Dict = None, 
                  fields: str = None) -> Dict:
        """
        发送API请求
        
        Args:
            api_name: 接口名称
            params: 请求参数
            fields: 返回字段（逗号分隔）
            
        Returns:
            API响应结果
        """
        data = {
            'api_name': api_name,
            'token': self.token,
            'params': params or {},
        }
        
        if fields:
            data['fields'] = fields
            
        max_retries = 3
        for retry in range(max_retries):
            try:
                response = self.session.post(
                    self.base_url, 
                    json=data, 
                    timeout=30
                )
                result = response.json()
                
                if result.get('code') == 0:
                    return {
                        'success': True,
                        'data': result.get('data', {}),
                        'request_id': result.get('request_id')
                    }
                else:
                    return {
                        'success': False,
                        'error': result.get('msg'),
                        'code': result.get('code')
                    }
                    
            except requests.exceptions.RequestException as e:
                if retry < max_retries - 1:
                    time.sleep(1)
                    continue
                return {
                    'success': False,
                    'error': str(e),
                    'code': -1
                }
                
        return {
            'success': False,
            'error': 'Max retries exceeded',
            'code': -1
        }
    
    def get_daily(self, 
                  ts_code: str = None,
                  trade_date: str = None,
                  start_date: str = None,
                  end_date: str = None,
                  fields: str = None) -> Dict:
        """
        获取A股日线行情
        
        官方文档: https://tushare.pro/document/2?doc_id=27
        
        Args:
            ts_code: 股票代码，如 '000001.SZ' 或 '600519.SH'
                     支持多个股票，逗号分隔
            trade_date: 交易日期 (YYYYMMDD)
            start_date: 开始日期 (YYYYMMDD)
            end_date: 结束日期 (YYYYMMDD)
            fields: 返回字段，如 'ts_code,trade_date,open,high,low,close,vol'
            
        Returns:
            {
                'success': True/False,
                'data': [...],
                'count': 数据条数,
                'error': 错误信息
            }
        """
        # 默认字段
        default_fields = 'ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount'
        
        params = {}
        if ts_code:
            params['ts_code'] = ts_code
        if trade_date:
            params['trade_date'] = trade_date
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
            
        result = self._request('daily', params, fields or default_fields)
        
        if result['success']:
            items = result['data'].get('items', [])
            return {
                'success': True,
                'data': items,
                'count': len(items),
                'fields': result['data'].get('fields', [])
            }
        else:
            return result
    
    def get_stock_basic(self, 
                        exchange: str = '',
                        list_status: str = 'L',
                        fields: str = None) -> Dict:
        """
        获取股票基础列表
        
        Args:
            exchange: 交易所代码 SSE/SZSE/BSE (空字符串表示全部)
            list_status: L-上市 D-退市 P-暂停上市
            fields: 返回字段
        """
        default_fields = 'ts_code,symbol,name,area,industry,list_date,delist_date'
        
        params = {
            'exchange': exchange,
            'list_status': list_status
        }
        
        result = self._request('stock_basic', params, fields or default_fields)
        
        if result['success']:
            items = result['data'].get('items', [])
            return {
                'success': True,
                'data': items,
                'count': len(items)
            }
        return result
    
    def get_trade_cal(self,
                       exchange: str = 'SSE',
                       start_date: str = None,
                       end_date: str = None) -> Dict:
        """
        获取交易日历
        
        Args:
            exchange: 交易所代码
            start_date: 开始日期
            end_date: 结束日期
        """
        params = {
            'exchange': exchange,
            'start_date': start_date or '20240101',
            'end_date': end_date or '20241231'
        }
        
        result = self._request('trade_cal', params)
        
        if result['success']:
            items = result['data'].get('items', [])
            return {
                'success': True,
                'data': items,
                'count': len(items)
            }
        return result
    
    def get_index_daily(self, 
                         ts_code: str = '000001.SH',
                         start_date: str = None,
                         end_date: str = None) -> Dict:
        """
        获取指数日线行情
        
        Args:
            ts_code: 指数代码，如 '000001.SH'(上证指数), '399001.SZ'(深证成指)
        """
        params = {'ts_code': ts_code}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
            
        default_fields = 'ts_code,trade_date,open,high,low,close,vol,amount'
        
        result = self._request('index_daily', params, default_fields)
        
        if result['success']:
            items = result['data'].get('items', [])
            return {
                'success': True,
                'data': items,
                'count': len(items)
            }
        return result
    
    def check_token_status(self) -> Dict:
        """
        检查Token状态和积分
        
        Returns:
            Token状态信息
        """
        # 尝试调用接口测试权限
        test_result = self.get_stock_basic(list_status='L')
        
        if test_result['success']:
            return {
                'status': 'active',
                'message': 'Token有效',
                'data_count': test_result.get('count', 0)
            }
        else:
            return {
                'status': 'inactive',
                'message': test_result.get('error', '未知错误'),
                'data_count': 0
            }


def test_connection():
    """测试TuShare连接"""
    print("=" * 60)
    print("🦞 TuShare Pro API 测试")
    print("=" * 60)
    
    # Token
    TOKEN = 'YOUR_TUSHARE_TOKEN'
    
    # 初始化
    pro = TuSharePro(TOKEN)
    
    # 1. 检查Token状态
    print("\n[1] 检查Token状态...")
    status = pro.check_token_status()
    print(f"  状态: {status['status']}")
    print(f"  消息: {status['message']}")
    
    # 2. 获取股票基础列表
    print("\n[2] 获取股票基础列表...")
    stocks = pro.get_stock_basic(list_status='L')
    if stocks['success']:
        print(f"  ✅ 成功获取 {stocks['count']} 只股票")
        print(f"  示例: {stocks['data'][:3]}")
    else:
        print(f"  ❌ 错误: {stocks.get('error')}")
    
    # 3. 获取交易日历
    print("\n[3] 获取2025年1月交易日历...")
    trade_cal = pro.get_trade_cal(
        exchange='SSE',
        start_date='20250101',
        end_date='20250131'
    )
    if trade_cal['success']:
        open_days = sum(1 for item in trade_cal['data'] if item[2] == 1)
        print(f"  ✅ 交易日: {open_days} 天")
    else:
        print(f"  ❌ 错误: {trade_cal.get('error')}")
    
    # 4. 获取指数日线
    print("\n[4] 获取上证指数日线...")
    index_daily = pro.get_index_daily(
        ts_code='000001.SH',
        start_date='20250101',
        end_date='20250210'
    )
    if index_daily['success']:
        print(f"  ✅ 成功获取 {index_daily['count']} 条数据")
        if index_daily['data']:
            latest = index_daily['data'][0]
            print(f"  最新: {latest[1]} 收盘={latest[5]}")
    else:
        print(f"  ❌ 错误: {index_daily.get('error')}")
    
    # 5. 获取个股日线（测试）
    print("\n[5] 获取个股日线...")
    print("  测试股票: 平安银行(000001.SZ), 贵州茅台(600519.SH)")
    
    for ts_code, name in [('000001.SZ', '平安银行'), ('600519.SH', '贵州茅台')]:
        daily = pro.get_daily(
            ts_code=ts_code,
            start_date='20250101',
            end_date='20250131'
        )
        if daily['success']:
            print(f"  {name} ({ts_code}): {daily['count']} 条数据")
        else:
            print(f"  {name}: ❌ {daily.get('error', '权限不足')}")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    test_connection()
