#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 AI Agent Economy生态系统 v7.0
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class AgentService:
    agent_id: str
    name: str
    description: str
    capabilities: List[str]
    price_per_use: float
    rating: float
    usage_count: int
    status: str


@dataclass  
class Transaction:
    tx_id: str
    from_agent: str
    to_agent: str
    service: str
    amount: float
    timestamp: str
    status: str


@dataclass
class UserProfile:
    user_id: str
    preferences: List[str]
    usage_history: List[str]
    trust_score: float


class AIAgentEconomy:
    def __init__(self, data_path: str = "data/agent_economy.json"):
        self.data_path = data_path
        self.services: Dict[str, AgentService] = {}
        self.transactions: List[Transaction] = []
        self.users: Dict[str, UserProfile] = {}
        self._load()
        
    def register_service(self, agent_id: str, name: str, description: str, 
                      capabilities: List[str], price_per_use: float) -> str:
        service = AgentService(
            agent_id=agent_id,
            name=name,
            description=description,
            capabilities=capabilities,
            price_per_use=price_per_use,
            rating=5.0,
            usage_count=0,
            status="active"
        )
        self.services[agent_id] = service
        self._save()
        return agent_id
    
    def discover_services(self, capability: str) -> List[AgentService]:
        return [
            s for s in self.services.values()
            if capability in s.capabilities and s.status == "active"
        ]
    
    def create_payment(self, from_user: str, to_agent: str, 
                     service: str, amount: float) -> str:
        tx_id = hashlib.md5(f"{from_user}{to_agent}{datetime.now()}".encode()).hexdigest()[:16]
        tx = Transaction(
            tx_id=tx_id,
            from_agent=from_user,
            to_agent=to_agent,
            service=service,
            amount=amount,
            timestamp=datetime.now().isoformat(),
            status="pending"
        )
        self.transactions.append(tx)
        self._save()
        return tx_id
    
    def complete_payment(self, tx_id: str) -> bool:
        for tx in self.transactions:
            if tx.tx_id == tx_id:
                tx.status = "completed"
                if tx.to_agent in self.services:
                    self.services[tx.to_agent].usage_count += 1
                self._save()
                return True
        return False
    
    def create_user(self, user_id: str, preferences: List[str]) -> str:
        user = UserProfile(
            user_id=user_id,
            preferences=preferences,
            usage_history=[],
            trust_score=5.0
        )
        self.users[user_id] = user
        self._save()
        return user_id
    
    def get_recommendations(self, user_id: str) -> List[AgentService]:
        if user_id not in self.users:
            return []
        user = self.users[user_id]
        recommendations = []
        for pref in user.preferences:
            for service in self.discover_services(pref):
                recommendations.append(service)
        return recommendations[:5]
    
    def get_market_stats(self) -> Dict:
        total = sum(tx.amount for tx in self.transactions if tx.status == "completed")
        top = sorted(self.services.values(), key=lambda x: x.usage_count, reverse=True)[:5]
        return {
            "total_agents": len(self.services),
            "total_transactions": len(self.transactions),
            "total_volume": total,
            "top_agents": [{"name": a.name, "usage": a.usage_count} for a in top]
        }
    
    def _load(self):
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.services = {k: AgentService(**v) for k, v in data.get('services', {}).items()}
                self.transactions = [Transaction(**t) for t in data.get('transactions', [])]
                self.users = {k: UserProfile(**v) for k, v in data.get('users', {}).items()}
        except:
            pass
    
    def _save(self):
        data = {
            'services': {k: v.__dict__ for k, v in self.services.items()},
            'transactions': [t.__dict__ for t in self.transactions],
            'users': {k: v.__dict__ for k, v in self.users.items()},
            'last_update': datetime.now().isoformat()
        }
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


class OpenClawAgent:
    def __init__(self):
        self.agent_id = "openclaw"
        self.name = "小爪"
        self.capabilities = ["reasoning", "coding", "analysis", "writing", "translation"]
        self.price = 0.01
        self.economy = AIAgentEconomy()
        self._register()
    
    def _register(self):
        self.economy.register_service(
            agent_id=self.agent_id,
            name=self.name,
            description="AI推理助手",
            capabilities=self.capabilities,
            price_per_use=self.price
        )
    
    def offer_service(self, service: str) -> Dict:
        if service in self.capabilities:
            tx_id = self.economy.create_payment(
                from_user="system", to_agent=self.agent_id,
                service=service, amount=self.price
            )
            return {"status": "offered", "service": service, "price": self.price, "tx_id": tx_id}
        return {"status": "failed", "reason": "service not available"}
    
    def get_stats(self) -> Dict:
        return self.economy.get_market_stats()


def demo():
    print("="*70)
    print("🦞 AI Agent Economy生态系统 v7.0")
    print("="*70)
    
    economy = AIAgentEconomy()
    
    print("\n【1. 注册Agent服务】")
    economy.register_service("reasoning_agent", "推理助手", "逻辑推理", ["reasoning", "math"], 0.01)
    economy.register_service("coding_agent", "编程助手", "代码编写", ["coding", "debug"], 0.02)
    print("  ✓ 注册2个服务")
    
    print("\n【2. 创建用户】")
    economy.create_user("user123", ["reasoning", "coding"])
    print("  ✓ 用户创建成功")
    
    print("\n【3. 发现服务】")
    services = economy.discover_services("reasoning")
    print(f"  发现{len(services)}个推理服务")
    
    print("\n【4. 创建支付】")
    tx_id = economy.create_payment("user123", "reasoning_agent", "reasoning", 0.01)
    print(f"  支付: {tx_id}")
    
    print("\n【5. 完成支付】")
    success = economy.complete_payment(tx_id)
    print(f"  {'✓' if success else '✗'}")
    
    print("\n【6. 市场统计】")
    stats = economy.get_market_stats()
    print(f"  Agent: {stats['total_agents']}")
    print(f"  交易: {stats['total_transactions']}")
    print(f"  总额: {stats['total_volume']}")
    
    print("\n"+"="*70)
    print("🦞 OpenClaw接入Economy")
    print("="*70)
    openclaw = OpenClawAgent()
    print(f"\n  Agent: {openclaw.name}")
    print(f"  能力: {', '.join(openclaw.capabilities)}")
    print(f"  价格: {openclaw.price}x402/次")
    result = openclaw.offer_service("reasoning")
    print(f"\n  提供服务: {result}")


if __name__ == "__main__":
    demo()
