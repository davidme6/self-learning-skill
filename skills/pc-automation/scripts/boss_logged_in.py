#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOSS 直聘 - 使用用户已登录的浏览器
"""

import sys
import io
import os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
from playwright.sync_api import sync_playwright

def main():
    print("=" * 60)
    print("BOSS 直聘 - 岗位浏览")
    print("=" * 60)
    
    # 用户已登录的 URL
    url = "https://www.zhipin.com/web/geek/jobs?ka=header-jobs"
    
    # 搜索关键词
    keywords = ["AI 解决方案", "企业数字化", "SaaS 大客户", "AI 商务"]
    
    with sync_playwright() as p:
        # 尝试连接已运行的 Chrome/Edge
        print("\n[1/5] 尝试连接已打开的浏览器...")
        
        browser = None
        for port in [9222, 9223, 9224, 9225]:
            try:
                browser = p.chromium.connect_over_cdp(f"http://localhost:{port}")
                print(f"    成功连接到端口 {port}")
                break
            except:
                continue
        
        if not browser:
            print("    未找到已打开的浏览器，启动新浏览器...")
            # 使用用户数据目录，可能保留登录状态
            user_data_dir = os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data")
            try:
                browser = p.chromium.launch_persistent_context(
                    user_data_dir=user_data_dir,
                    headless=False,
                    args=['--no-first-run', '--no-default-browser-check']
                )
                print("    使用 Edge 用户数据启动")
            except Exception as e:
                print(f"    [警告] {e}")
                browser = p.chromium.launch(headless=False)
        
        context = browser.contexts[0] if hasattr(browser, 'contexts') else browser
        page = context.pages[0] if hasattr(context, 'pages') and len(context.pages) > 0 else context.new_page()
        
        print(f"\n[2/5] 打开 BOSS 直聘...")
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(5)
        
        print("[3/5] 等待页面加载...")
        time.sleep(3)
        
        # 搜索岗位
        for kw in keywords:
            print(f"\n{'='*50}")
            print(f"搜索：{kw}")
            print(f"{'='*50}")
            
            try:
                # 找搜索框
                search_box = page.locator('input[placeholder*="搜索"]').first
                search_box.click()
                time.sleep(1)
                search_box.fill(kw)
                time.sleep(1)
                search_box.press('Enter')
                time.sleep(4)
                
                # 获取岗位
                jobs = page.locator('.job-card-wrapper').all()
                count = len(jobs)
                print(f"\n找到 {count} 个岗位\n")
                
                # 显示前 10 个
                for i in range(min(10, count)):
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
        print("完成！浏览器保持打开")
        print("=" * 60)
        
        # 保持浏览器打开
        print("\n[提示] 浏览器保持打开，按 Ctrl+C 关闭")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n关闭浏览器...")
            if hasattr(browser, 'close'):
                browser.close()

if __name__ == "__main__":
    main()
