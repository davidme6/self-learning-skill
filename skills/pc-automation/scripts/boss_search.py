#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOSS 直聘 - 搜索 AI 相关岗位
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
from playwright.sync_api import sync_playwright

def search_boss_jobs():
    """搜索 BOSS 直聘 AI 相关岗位"""
    
    print("=" * 60)
    print("BOSS 直聘 - AI 岗位搜索")
    print("=" * 60)
    
    with sync_playwright() as p:
        # 连接已打开的浏览器
        try:
            # 获取已打开的 BOSS 直聘页面
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            page = context.pages[0]
            
            print("\n[1/4] 已连接到 BOSS 直聘页面")
            
            # 点击搜索框
            print("[2/4] 搜索 AI 相关岗位...")
            page.click('input[placeholder*="搜索"]')
            time.sleep(0.5)
            
            # 清空并输入
            page.fill('input[placeholder*="搜索"]', "AI 销售")
            time.sleep(1)
            
            # 按回车
            page.press('input[placeholder*="搜索"]', 'Enter')
            time.sleep(3)
            
            print("[3/4] 获取岗位列表...")
            
            # 获取岗位信息
            jobs = page.query_selector_all('.job-list-box .job-card-wrapper')
            
            print(f"\n[4/4] 找到 {len(jobs)} 个岗位\n")
            print("=" * 60)
            
            for i, job in enumerate(jobs[:10]):
                try:
                    title_el = job.query_selector('.job-name')
                    company_el = job.query_selector('.company-name')
                    salary_el = job.query_selector('.salary')
                    
                    if title_el and company_el:
                        title = title_el.inner_text()
                        company = company_el.inner_text()
                        salary = salary_el.inner_text() if salary_el else "面议"
                        
                        print(f"{i+1}. {title}")
                        print(f"   公司：{company}")
                        print(f"   薪资：{salary}")
                        print()
                except Exception as e:
                    continue
            
            print("=" * 60)
            print("完成！")
            
        except Exception as e:
            print(f"[错误] {e}")
            print("[提示] 请确保 BOSS 直聘网页已打开")

if __name__ == "__main__":
    search_boss_jobs()
