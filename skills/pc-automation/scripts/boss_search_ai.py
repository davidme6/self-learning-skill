#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOSS 直聘 - 搜索 AI 解决方案岗位
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
from playwright.sync_api import sync_playwright

def search_jobs():
    """搜索岗位"""
    
    print("=" * 60)
    print("BOSS 直聘 - 搜索 AI 相关岗位")
    print("=" * 60)
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            page = context.pages[0]
            
            print("\n[1/5] 已连接到页面")
            
            # 点击搜索框
            print("[2/5] 点击搜索框...")
            page.click('input[placeholder*="搜索职位、公司"]')
            time.sleep(0.5)
            
            # 输入搜索词
            print("[3/5] 搜索'AI 解决方案'...")
            page.fill('input[placeholder*="搜索职位、公司"]', "AI 解决方案")
            time.sleep(1)
            
            # 按回车
            page.press('input[placeholder*="搜索职位、公司"]', 'Enter')
            time.sleep(3)
            
            print("[4/5] 获取岗位列表...")
            
            # 获取岗位
            jobs = page.query_selector_all('.job-list-box .job-card-wrapper')
            
            print(f"\n[5/5] 找到 {len(jobs)} 个岗位\n")
            print("=" * 60)
            
            for i, job in enumerate(jobs[:15]):
                try:
                    title_el = job.query_selector('.job-name')
                    company_el = job.query_selector('.company-name')
                    salary_el = job.query_selector('.salary')
                    location_el = job.query_selector('.job-location')
                    
                    if title_el and company_el:
                        title = title_el.inner_text()
                        company = company_el.inner_text()
                        salary = salary_el.inner_text() if salary_el else "面议"
                        location = location_el.inner_text() if location_el else ""
                        
                        print(f"\n{i+1}. {title}")
                        print(f"   公司：{company}")
                        print(f"   薪资：{salary}")
                        print(f"   地点：{location}")
                        
                except Exception as e:
                    continue
            
            print("\n" + "=" * 60)
            print("完成！")
            
        except Exception as e:
            print(f"[错误] {e}")
            print("[提示] 请确保 BOSS 直聘页面已打开")

if __name__ == "__main__":
    search_jobs()
