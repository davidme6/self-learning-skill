#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOSS 直聘 - 简单搜索
"""

import sys
import io
import os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
from playwright.sync_api import sync_playwright

def main():
    print("=" * 60)
    print("BOSS 直聘 - 搜索 AI 岗位")
    print("=" * 60)
    
    keywords = ["AI 解决方案", "企业数字化", "SaaS 大客户"]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        
        page.goto("https://www.zhipin.com/", wait_until="domcontentloaded")
        print("\n[等待] 页面加载中...")
        time.sleep(5)
        
        for kw in keywords:
            print(f"\n{'='*50}")
            print(f"搜索：{kw}")
            print(f"{'='*50}")
            
            try:
                # 搜索
                page.fill('input[placeholder*="搜索"]', kw)
                time.sleep(1)
                page.press('input[placeholder*="搜索"]', 'Enter')
                time.sleep(4)
                
                # 获取岗位
                jobs = page.query_selector_all('.job-card-wrapper')
                print(f"\n找到 {len(jobs)} 个岗位\n")
                
                for i, job in enumerate(jobs[:8]):
                    try:
                        title = job.query_selector('.job-name')
                        company = job.query_selector('.company-name')
                        salary = job.query_selector('.salary')
                        
                        if title and company:
                            print(f"{i+1}. {title.inner_text()}")
                            print(f"   公司：{company.inner_text()}")
                            print(f"   薪资：{salary.inner_text() if salary else '面议'}")
                            print()
                    except Exception as e:
                        continue
                        
            except Exception as e:
                print(f"[错误] {e}")
            
            time.sleep(2)
        
        print("\n" + "=" * 60)
        print("完成！")
        time.sleep(10)
        browser.close()

if __name__ == "__main__":
    main()
