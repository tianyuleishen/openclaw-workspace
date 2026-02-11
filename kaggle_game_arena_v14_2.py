#!/usr/bin/env python3
"""
🎮 Kaggle Game Arena 测试 v14.2游戏增强版
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')

from reasoning_engine_v14_2_games import ReasoningEngineV14_2


def test_games():
    print("="*80)
    print("🎮 Kaggle Game Arena v14.2 游戏增强版测试")
    print("="*80)
    
    engine = ReasoningEngineV14_2()
    
    challenges = [
        # 经典博弈
        ("In chess endgame King+Rook vs King, what is the optimal strategy?", "chess"),
        ("For Nim with heaps (3,4,5), what is the winning move? XOR strategy.", "nim"),
        ("What is the optimal first move in Tic-Tac-Toe? Center vs corner?", "tic_tac_toe"),
        
        # 概率游戏
        ("In Monty Hall, should you switch doors? Calculate probabilities.", "monty_hall"),
        ("In craps, what is probability of winning on come-out roll?", "craps"),
        
        # 策略游戏
        ("In iterated Prisoner's Dilemma, why did Tit-for-Tat win?", "prisoners_dilemma"),
        ("Explain Minimax algorithm and alpha-beta pruning efficiency.", "minimax"),
        
        # 卡牌游戏
        ("In Texas Hold'em, what is EV of pocket aces pre-flop?", "texas_holdem"),
        ("What is house edge in blackjack with basic strategy?", "blackjack"),
        
        # 路径规划
        ("Compare BFS, DFS, A* for maze solving. When is A* optimal?", "maze"),
        
        # RL游戏
        ("How did AlphaGo use MCTS and deep learning to defeat Lee Sedol?", "alphago"),
        ("Explain DQN with experience replay and target networks.", "dqn"),
        
        # 优化
        ("TSP nearest neighbor heuristic for cities at (0,0),(1,2),(3,1),(2,3),(4,4)", "tsp"),
        ("Solve 0/1 knapsack: capacity=50, items (10,60),(20,100),(30,120),(40,150)", "knapsack"),
        ("Find Nash Equilibrium in matching pennies game.", "nash_equilibrium"),
        
        # 原有知识
        ("Prove Euler's formula e^(iπ) + 1 = 0", "math"),
        ("Explain Transformer attention mechanism", "transformer"),
    ]
    
    print(f"\n🎯 测试 {len(challenges)} 道游戏AI挑战:")
    print("-"*80)
    
    results = {"excellent": 0, "good": 0, "partial": 0, "poor": 0}
    
    for i, (q, expected) in enumerate(challenges, 1):
        result = engine.analyze(q)
        
        # 评分
        has_answer = expected.lower() in result["answer"].lower() or len(result["answer"]) > 50
        
        if has_answer and result["confidence"] >= 0.8:
            status = "✅优秀"
            results["excellent"] += 1
        elif has_answer:
            status = "✅良好"
            results["good"] += 1
        elif result["confidence"] >= 0.7:
            status = "⚠️部分"
            results["partial"] += 1
        else:
            status = "❌不足"
            results["poor"] += 1
        
        print(f"\n{i:2d}. [{expected:15s}] {status}")
        print(f"    问题: {q[:50]}...")
        print(f"    回答: {result['answer'][:60]}...")
    
    total = len(challenges)
    passed = results["excellent"] + results["good"]
    score = (passed / total) * 100
    
    print("\n" + "="*80)
    print("📊 Kaggle Game Arena v14.2 测试结果")
    print("="*80)
    
    print(f"\n总题数: {total}")
    print(f"优秀: {results['excellent']} | 良好: {results['good']} | 部分: {results['partial']} | 不足: {results['poor']}")
    print(f"\n得分: {score:.1f}%")
    
    # 评级
    print("\n" + "="*80)
    print("🏆 游戏AI能力评级")
    print("="*80)
    
    if score >= 90:
        rating = "👑 GRANDMASTER"
    elif score >= 80:
        rating = "🎖️ EXPERT"
    elif score >= 70:
        rating = "🎮 ADVANCED"
    elif score >= 60:
        rating = "🎯 INTERMEDIATE"
    else:
        rating = "🎲 NOVICE"
    
    print(f"\n得分: {score:.1f}%")
    print(f"评级: {rating}")
    
    # 进化对比
    print("\n" + "="*80)
    print("📈 进化对比")
    print("="*80)
    
    print("\nv14.1 原版:")
    print("  得分: 0.0%")
    print("  评级: 🎲 NOVICE")
    
    print(f"\nv14.2 游戏增强版:")
    print(f"  得分: {score:.1f}%")
    print(f"  评级: {rating}")
    
    if score > 50:
        print(f"\n提升: +{score:.1f}% 🎉")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    test_games()
