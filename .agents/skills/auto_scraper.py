#!/usr/bin/env python3
"""
Auto-Scraper: 智能 URL 检测 + 自动爬取
根据 URL 类型自动选择最佳爬取工具

优先级：
1. DeepReader - 日常 URL（Twitter/Reddit/YouTube/博客）
2. Scrapling - 有反爬虫保护的网站
3. Firecrawl - 付费内容/高质量需求
"""

import sys
import os
import re
from pathlib import Path
from datetime import datetime

# 检测 URL 类型
def detect_url_type(url):
    """根据 URL 判断推荐的爬取工具"""
    
    # DeepReader 支持的网站（免费 + 自动）
    deeprreader_domains = [
        'twitter.com', 'x.com', 't.co',
        'reddit.com', 'old.reddit.com',
        'youtube.com', 'youtu.be',
        'instagram.com', 'tiktok.com'
    ]
    
    # 检查是否是 DeepReader 范围
    for domain in deeprreader_domains:
        if domain in url.lower():
            return 'deeprreader', '社交媒体/视频平台'
    
    # 检查是否有反爬虫保护（常见特征）
    protected_patterns = [
        r'cloudflare',
        r'akamai',
        r'incapsula',
        r'sucuri'
    ]
    
    # 付费内容网站
    paywall_sites = [
        'wsj.com', 'nytimes.com', 'bloomberg.com',
        'ft.com', 'reuters.com', 'medium.com'
    ]
    
    for site in paywall_sites:
        if site in url.lower():
            return 'firecrawl', '付费内容网站'
    
    # 默认：普通网站用 Scrapling
    return 'scrapling', '普通网站'


def scrape_with_deeprreader(url):
    """使用 DeepReader 爬取"""
    print(f"📖 使用 DeepReader 爬取：{url}")
    print("   DeepReader 会自动检测 URL 并保存到记忆库")
    # DeepReader 是自动触发的，这里只是提示
    return True


def scrape_with_scrapling(url, output_file=None):
    """使用 Scrapling 爬取"""
    print(f"🕷️ 使用 Scrapling 爬取：{url}")
    
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f".tmp/scraped_{timestamp}.md"
    
    # 创建输出目录
    Path(output_file).parent.mkdir(exist_ok=True)
    
    # 构建 Scrapling 命令
    cmd = f'scrapling extract get "{url}" "{output_file}"'
    print(f"   执行命令：{cmd}")
    
    try:
        result = os.system(cmd)
        if result == 0:
            print(f"   ✅ 成功保存到：{output_file}")
            return True
        else:
            print(f"   ❌ Scrapling 失败，尝试 stealthy-fetch...")
            # 尝试 stealthy 模式
            cmd = f'scrapling extract stealthy-fetch "{url}" "{output_file}"'
            result = os.system(cmd)
            if result == 0:
                print(f"   ✅ stealthy-fetch 成功保存到：{output_file}")
                return True
            else:
                print(f"   ❌ Scrapling 完全失败")
                return False
    except Exception as e:
        print(f"   ❌ 错误：{e}")
        return False


def scrape_with_firecrawl(url, output_file=None):
    """使用 Firecrawl 爬取"""
    print(f"🔥 使用 Firecrawl 爬取：{url}")
    
    api_key = os.getenv('FIRECRAWL_API_KEY')
    if not api_key:
        print("   ❌ 未设置 FIRECRAWL_API_KEY 环境变量")
        return False
    
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f".tmp/firecrawl_{timestamp}.md"
    
    # 构建 Firecrawl 命令
    cmd = f'python .agents/skills/firecrawl-scraping/scripts/firecrawl_scrape.py "{url}" --output "{output_file}"'
    print(f"   执行命令：{cmd}")
    
    try:
        result = os.system(cmd)
        if result == 0:
            print(f"   ✅ 成功保存到：{output_file}")
            return True
        else:
            print(f"   ❌ Firecrawl 失败")
            return False
    except Exception as e:
        print(f"   ❌ 错误：{e}")
        return False


def auto_scrape(urls):
    """自动检测 URL 并选择合适的工具爬取"""
    
    print("=" * 60)
    print("🤖 Auto-Scraper 智能爬取")
    print("=" * 60)
    
    results = {
        'deeprreader': 0,
        'scrapling': 0,
        'firecrawl': 0,
        'success': 0,
        'failed': 0
    }
    
    for url in urls:
        url = url.strip()
        if not url:
            continue
        
        print(f"\n📍 分析 URL: {url}")
        
        # 检测 URL 类型
        tool, reason = detect_url_type(url)
        print(f"   类型：{reason}")
        print(f"   推荐工具：{tool}")
        
        # 根据类型选择工具
        if tool == 'deeprreader':
            success = scrape_with_deeprreader(url)
            results['deeprreader'] += 1
        elif tool == 'scrapling':
            success = scrape_with_scrapling(url)
            results['scrapling'] += 1
        elif tool == 'firecrawl':
            success = scrape_with_firecrawl(url)
            results['firecrawl'] += 1
        else:
            print(f"   ❌ 未知工具：{tool}")
            success = False
        
        if success:
            results['success'] += 1
        else:
            results['failed'] += 1
    
    # 输出统计
    print("\n" + "=" * 60)
    print("📊 爬取统计")
    print("=" * 60)
    print(f"   DeepReader:  {results['deeprreader']} 个")
    print(f"   Scrapling:   {results['scrapling']} 个")
    print(f"   Firecrawl:   {results['firecrawl']} 个")
    print(f"   ✅ 成功：{results['success']} 个")
    print(f"   ❌ 失败：{results['failed']} 个")
    print("=" * 60)
    
    return results['failed'] == 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法：python auto_scraper.py <URL1> [URL2] [URL3] ...")
        print("\n示例:")
        print("  python auto_scraper.py https://example.com")
        print("  python auto_scraper.py https://x.com/user/status/123 https://reddit.com/r/python")
        sys.exit(1)
    
    urls = sys.argv[1:]
    success = auto_scrape(urls)
    sys.exit(0 if success else 1)
