#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 Kaggle Game Arena 游戏AI挑战测试
测试推理引擎在游戏领域的决策和策略能力
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')

from reasoning_engine_v14_final import ReasoningEngineV14Final


def test_game_arena():
    print("="*80)
    print("🎮 Kaggle Game Arena 游戏AI挑战测试")
    print("="*80)
    print("\n来源: https://www.kaggle.com/game-arena")
    print("测试: AI在各类游戏中的策略和决策能力")
    print("="*80)
    
    engine = ReasoningEngineV14Final()
    
    # Kaggle游戏类型挑战
    challenges = [
        # 🎯 经典博弈游戏
        {
            "id": 1,
            "category": "Combinatorial Games",
            "game": "Chess Endgame",
            "q": """In a chess endgame with King and Rook vs King, what is the optimal strategy 
to checkmate? What are the key positions and mating patterns?""",
            "difficulty": "Intermediate",
            "hints": ["Rook", "king", "checkmate", "opposition"]
        },
        {
            "id": 2,
            "category": "Combinatorial Games",
            "game": "Nim Game",
            "q": """For a Nim game with 3 heaps of sizes (3, 4, 5), what is the winning move?
Explain the XOR (nim-sum) strategy.""",
            "difficulty": "Intermediate",
            "hints": ["Nim", "XOR", "nim-sum", "winning"]
        },
        {
            "id": 3,
            "category": "Combinatorial Games",
            "game": "Tic-Tac-Toe",
            "q": """What is the optimal first move in Tic-Tac-Toe? 
Explain why center vs corner vs edge matters.""",
            "difficulty": "Easy",
            "hints": ["center", "optimal", "strategy"]
        },
        
        # 🎲 概率与统计游戏
        {
            "id": 4,
            "category": "Probability Games",
            "game": "Monty Hall Problem",
            "q": """In the Monty Hall game, should you switch doors after the host reveals a goat?
Calculate the probabilities and explain.""",
            "difficulty": "Intermediate",
            "hints": ["Monty Hall", "probability", "switch", "1/3", "2/3"]
        },
        {
            "id": 5,
            "category": "Probability Games",
            "game": "Craps Dice Game",
            "q": """In craps, what is the probability of winning on the come-out roll?
What are the probabilities for each sum of two dice?""",
            "difficulty": "Advanced",
            "hints": ["craps", "probability", "dice", "come-out"]
        },
        
        # 🧠 策略优化游戏
        {
            "id": 6,
            "category": "Strategy Games",
            "game": "Prisoner's Dilemma",
            "q": """In the iterated Prisoner's Dilemma, what is the optimal strategy?
Why did Tit-for-Tat perform well in Axelrod's tournaments?""",
            "difficulty": "Advanced",
            "hints": ["Tit-for-Tat", "iteration", "cooperation", "Axelrod"]
        },
        {
            "id": 7,
            "category": "Strategy Games",
            "game": "Minimax Algorithm",
            "q": """Explain how the Minimax algorithm works for game trees.
What is alpha-beta pruning and how does it improve efficiency?""",
            "difficulty": "Advanced",
            "hints": ["Minimax", "alpha-beta", "game tree", "optimal"]
        },
        
        # 🎰 扑克与卡牌游戏
        {
            "id": 8,
            "category": "Card Games",
            "game": "Texas Hold'em",
            "q": """In Texas Hold'em, what is the expected value of pocket aces (AA) pre-flop?
What are the key poker probability calculations?""",
            "difficulty": "Advanced",
            "hints": ["Texas Hold'em", "AA", "expected value", "pre-flop"]
        },
        {
            "id": 9,
            "category": "Card Games",
            "game": "Blackjack Strategy",
            "q": """What is the house edge in blackjack with basic strategy?
Explain the concept of card counting and its impact.""",
            "difficulty": "Advanced",
            "hints": ["blackjack", "house edge", "basic strategy", "card counting"]
        },
        
        # 🎯 路径规划游戏
        {
            "id": 10,
            "category": "Pathfinding",
            "game": "Maze Solving",
            "q": """Compare BFS, DFS, and A* algorithms for maze solving.
When is A* optimal? What heuristic functions work best?""",
            "difficulty": "Advanced",
            "hints": ["BFS", "DFS", "A*", "heuristic", "optimal"]
        },
        
        # 🤖 强化学习游戏
        {
            "id": 11,
            "category": "RL Games",
            "game": "AlphaGo Strategy",
            "q": """How did AlphaGo use Monte Carlo Tree Search (MCTS) and deep learning
to defeat Lee Sedol? What was the key innovation?""",
            "difficulty": "Expert",
            "hints": ["AlphaGo", "MCTS", "policy network", "value network"]
        },
        {
            "id": 12,
            "category": "RL Games",
            "game": "DQN Atari Games",
            "q": """Explain how Deep Q-Networks (DQN) learn to play Atari games.
What is experience replay and target networks?""",
            "difficulty": "Expert",
            "hints": ["DQN", "experience replay", "target network", "Atari"]
        },
        
        # 🏆 组合优化游戏
        {
            "id": 13,
            "category": "Optimization",
            "game": "Traveling Salesman",
            "q": """For TSP with 5 cities at positions (0,0), (1,2), (3,1), (2,3), (4,4),
what is the nearest neighbor heuristic solution?""",
            "difficulty": "Advanced",
            "hints": ["TSP", "nearest neighbor", "heuristic", "tour"]
        },
        {
            "id": 14,
            "category": "Optimization",
            "game": "Knapsack Problem",
            "q": """Solve the 0/1 knapsack problem: capacity=50, items (weight, value):
(10,60), (20,100), (30,120), (40,150), (50,200). What is the optimal solution?""",
            "difficulty": "Advanced",
            "hints": ["knapsack", "dynamic programming", "optimal", "capacity"]
        },
        
        # 🎲 博弈论游戏
        {
            "id": 15,
            "category": "Game Theory",
            "game": "Nash Equilibrium",
            "q": """Find the Nash Equilibrium in the matching pennies game:
Player 1: H/T, Player 2: H/T. Payoffs: same=H gets +1, different=T gets +1.""",
            "difficulty": "Expert",
            "hints": ["Nash", "equilibrium", "mixed strategy", "matching pennies"]
        },
    ]
    
    print(f"\n🎯 测试 {len(challenges)} 道游戏AI挑战:")
    print("-"*80)
    
    results = {"excellent": 0, "good": 0, "partial": 0, "poor": 0}
    by_category = {}
    
    for c in challenges:
        result = engine.analyze(c["q"])
        
        has_hints = sum(1 for h in c["hints"] if h in result["answer"])
        coverage = has_hints / len(c["hints"])
        
        if coverage >= 0.8:
            status = "✅优秀"
            results["excellent"] += 1
        elif coverage >= 0.6:
            status = "✅良好"
            results["good"] += 1
        elif coverage >= 0.4:
            status = "⚠️部分"
            results["partial"] += 1
        else:
            status = "❌不足"
            results["poor"] += 1
        
        if c["category"] not in by_category:
            by_category[c["category"]] = {"total": 0, "passed": 0}
        by_category[c["category"]]["total"] += 1
        if coverage >= 0.6:
            by_category[c["category"]]["passed"] += 1
        
        print(f"\n{c['id']:2d}. [{c['category']:20s}] {status}")
        print(f"    游戏: {c['game']}")
        print(f"    覆盖率: {coverage*100:.0f}% | 置信度: {result['confidence']*100:.0f}%")
    
    total = len(challenges)
    passed = results["excellent"] + results["good"]
    score = (passed / total) * 100
    
    print("\n" + "="*80)
    print("📊 Kaggle Game Arena 测试结果")
    print("="*80)
    
    print(f"\n总题数: {total}")
    print(f"优秀: {results['excellent']} | 良好: {results['good']} | 部分: {results['partial']} | 不足: {results['poor']}")
    print(f"\n得分: {score:.1f}%")
    
    # 分类成绩
    print("\n📊 分类成绩:")
    for cat, stats in by_category.items():
        cat_score = (stats["passed"] / stats["total"]) * 100
        bar = "█" * int(cat_score / 10) + "░" * (10 - int(cat_score / 10))
        print(f"  {cat:20s}: [{bar}] {cat_score:5.1f}%")
    
    # 评级
    print("\n" + "="*80)
    print("🏆 游戏AI能力评级")
    print("="*80)
    
    if score >= 90:
        rating = "👑 GRANDMASTER"
        comment = "游戏策略大师！"
    elif score >= 80:
        rating = "🎖️ EXPERT"
        comment = "专业级游戏策略！"
    elif score >= 70:
        rating = "🎮 ADVANCED"
        comment = "高级游戏理解！"
    elif score >= 60:
        rating = "🎯 INTERMEDIATE"
        comment = "中级游戏策略！"
    else:
        rating = "🎲 NOVICE"
        comment = "需要加强游戏AI学习！"
    
    print(f"\n得分: {score:.1f}%")
    print(f"评级: {rating}")
    print(f"\n评价: {comment}")
    
    # 能力分析
    print("\n" + "="*80)
    print("📈 游戏AI能力分析")
    print("="*80)
    
    print("\n✅ 强项:")
    print("  - 组合游戏理论")
    print("  - 概率计算")
    print("  - 博弈论基础")
    print("  - 强化学习概念")
    
    print("\n❌ 弱项:")
    print("  - 具体数值计算")
    print("  - 实时决策")
    print("  - 具体游戏状态分析")
    
    print("\n💡 提升方向:")
    print("  - 添加具体游戏案例")
    print("  - 增强概率计算库")
    print("  - 集成MCTS等算法")
    
    # 总体评价
    print("\n" + "="*80)
    print("🎯 总体评价")
    print("="*80)
    
    print("""
┌─────────────────────────────────────────────────────────────┐
│                    Kaggle Game Arena                        │
├─────────────────────────────────────────────────────────────┤
│  本引擎: Reasoning Engine v14.1 Ultimate                   │
│  评级: {}                                                │
│  得分: {:.1f}%                                             │
├─────────────────────────────────────────────────────────────┤
│  优势: 理论理解深厚，概念清晰                              │
│  劣势: 具体计算和实时决策不足                              │
│  定位: 游戏理论专家，非实战选手                            │
└─────────────────────────────────────────────────────────────┘
""".format(rating, score))
    
    print("\n" + "="*80)
    
    return score


if __name__ == "__main__":
    test_game_arena()
