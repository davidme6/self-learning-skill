#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOSS 直聘 - 使用现有浏览器会话搜索岗位
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
import subprocess
from playwright.sync_api import sync_playwright

def search_with_existing_browser():
    """使用已打开的浏览器搜索"""
    
    print("=" * 60)
    print("BOSS 直聘 - 岗位搜索")
    print("=" * 60)
    
    # 搜索关键词列表
    keywords = [
        "AI 解决方案",
        "AI 大客户", 
        "企业数字化",
        "SaaS 大客户",
        "AI 商务"
    ]
    
    with sync_playwright() as p:
        # 启动新浏览器（因为无法连接到现有会话）
        print("\n[1/4] 启动浏览器...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        page = context.new_page()
        
        print("[2/4] 打开 BOSS 直聘...")
        page.goto("https://www.zhipin.com/", wait_until="domcontentloaded")
        time.sleep(3)
        
        print("[3/4] 搜索岗位...\n")
        
        for keyword in keywords:
            print(f"\n{'='*40}")
            print(f"搜索：{keyword}")
            print(f"{'='*40}")
            
            try:
                # 找搜索框
                search_box = page.locator('input[placeholder*="搜索"]').first
                search_box.fill(keyword)
                time.sleep(0.5)
                search_box.press('Enter')
                time.sleep(3)
                
                # 获取岗位列表
                jobs = page.locator('.job-card-wrapper').all()
                
                print(f"\n找到 {len(jobs)} 个岗位\n")
                
                # 显示前 10 个
                for i in range(min(10, len(jobs))):
                    try:
                        job = jobs[i]
                        title = job.locator('.job-name').inner_text()
                        company = job.locator('.company-name').inner_text()
                        salary = job.locator('.salary').inner_text()
                        location = job.locator('.job-location').inner_text()
                        
                        print(f"{i+1}. {title}")
                        print(f"   公司：{company}")
                        print(f"   薪资：{salary}")
                        print(f"   地点：{location}")
                        print()
                    except:
                        continue
                        
            except Exception as e:
                print(f"[错误] {e}")
            
            time.sleep(2)
        
        print("\n" + "=" * 60)
        print("完成！浏览器保持打开，你可以继续浏览")
        print("=" * 60)
        
        # 保持浏览器打开
        print("\n[提示] 浏览器保持打开状态，按 Ctrl+C 关闭")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n关闭浏览器...")
            browser.close()

if __name__ == "__main__":
    search_with_existing_browser()
