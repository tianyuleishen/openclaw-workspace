#!/usr/bin/env python3
"""
AI 论文搜索工具 v2.1 (稳定版)
支持 ArXiv、GitHub、Papers With Code 搜索
"""

import urllib.request
import json
import re
import ssl
from datetime import datetime

# 颜色定义
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'


def print_section(title: str):
    """打印章节标题"""
    print(f"\n{BOLD}{CYAN}═══ {title} ═══{RESET}\n")


def create_context():
    """创建 SSL 上下文"""
    return ssl._create_unverified_context()


def search_arxiv_robust(query: str = "AI", max_papers: int = 5) -> list:
    """ArXiv 搜索 - 稳定版"""
    categories = {
        'AI': 'cat:cs.AI',
        'ML': 'cat:cs.LG', 
        'NLP': 'cat:cs.CL'
    }
    
    all_papers = []
    
    for cat_name, cat_query in categories.items():
        if len(all_papers) >= max_papers:
            break
            
        url = f"http://export.arxiv.org/api/query?search_query={cat_query}&start=0&max_items={max_papers}"
        
        try:
            with urllib.request.urlopen(url, timeout=10, context=create_context()) as response:
                content = response.read().decode('utf-8')
            
            entries = re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL)
            
            for entry in entries[:max_papers]:
                title = re.search(r'<title>(.*?)</title>', entry)
                link = re.search(r'<id>(.*?)</id>', entry)
                published = re.search(r'<published>(.*?)</published>', entry)
                
                if title:
                    paper = {
                        'title': title.group(1).strip().replace('\n', ' ')[:70],
                        'link': link.group(1).strip() if link else "",
                        'date': published.group(1)[:10] if published else "",
                        'source': f'ArXiv/{cat_name}'
                    }
                    
                    if paper['title'] not in [p['title'] for p in all_papers]:
                        all_papers.append(paper)
                        
        except Exception as e:
            continue
    
    return all_papers[:max_papers]


def search_github_robust(query: str = "AI machine learning", max_repos: int = 5) -> list:
    """GitHub 搜索 - 稳定版"""
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&per_page={max_repos}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Python-AI-Search'})
        with urllib.request.urlopen(req, timeout=10, context=create_context()) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        repos = []
        for repo in data.get('items', [])[:max_repos]:
            repos.append({
                'name': repo['full_name'],
                'stars': repo['stargazers_count'],
                'description': repo.get('description', '')[:80],
                'url': repo['html_url'],
                'language': repo.get('language', 'N/A')
            })
        
        return repos
    except Exception as e:
        return []


def search_pwc_robust(topic: str = "machine learning", max_papers: int = 5) -> list:
    """Papers With Code 搜索 - 稳定版"""
    try:
        url = f"https://paperswithcode.com/api/v1/papers?q={topic}&page=1&items={max_papers}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Python'})
        with urllib.request.urlopen(req, timeout=10, context=create_context()) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        papers = []
        for paper in data.get('results', [])[:max_papers]:
            papers.append({
                'title': paper.get('title', '')[:70],
                'url': f"https://paperswithcode.com{paper.get('url', '')}",
                'year': paper.get('year', 'N/A')
            })
        
        return papers
    except Exception as e:
        return []


def display_papers(papers: list, source: str):
    """显示论文列表"""
    print(f"{GREEN}📚 {source} 论文:{RESET}")
    
    if not papers:
        print("  ⚠️  暂时无法获取，请稍后再试")
        print(f"  🔗 访问: https://arxiv.org/list/cs.AI/recent\n")
        return
    
    for i, paper in enumerate(papers, 1):
        print(f"  {i}. {paper['title']}...")
        if 'date' in paper:
            print(f"     📅 {paper['date']}")
        if 'url' in paper:
            print(f"     🔗 {paper['url'][:50]}...")
        print()


def display_repos(repos: list):
    """显示仓库列表"""
    print(f"{YELLOW}⭐ GitHub AI 热门仓库:{RESET}")
    
    if not repos:
        print("  ⚠️  暂时无法获取，请稍后再试")
        print(f"  🔗 访问: https://github.com/search?q=AI+machine+learning\n")
        return
    
    for i, repo in enumerate(repos, 1):
        print(f"  {i}. {BOLD}{repo['name']}{RESET}")
        print(f"     ⭐ {repo['stars']:,} | 💻 {repo['language']}")
        print(f"     📝 {repo['description']}...")
        print()


def display_quick_links():
    """显示常用链接"""
    print_section("📌 常用链接")
    links = [
        ("ArXiv AI", "https://arxiv.org/list/cs.AI/recent"),
        ("Papers With Code", "https://paperswithcode.com/"),
        ("Google Scholar", "https://scholar.google.com/scholar?q=AI+papers"),
        ("Semantic Scholar", "https://www.semanticscholar.org/"),
    ]
    
    for name, url in links:
        print(f"  • {GREEN}{name}{RESET}: {url}")


def main():
    """主函数"""
    print(f"{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}🔍 AI 论文搜索工具 v2.1 (稳定版){RESET}")
    print(f"{BOLD}{'='*60}{RESET}")
    
    # ArXiv
    print_section("ArXiv AI 论文")
    papers = search_arxiv_robust("AI", max_papers=5)
    display_papers(papers, "ArXiv")
    
    # GitHub
    print_section("GitHub AI 仓库")
    repos = search_github_robust("AI machine learning papers", max_repos=5)
    display_repos(repos)
    
    # Papers With Code
    print_section("Papers With Code")
    pwcpapers = search_pwc_robust("machine learning", max_papers=5)
    display_papers(pwcpapers, "Papers With Code")
    
    # 常用链接
    display_quick_links()
    
    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    main()
