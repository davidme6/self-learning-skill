#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOSS 直聘 - 分析推荐岗位
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
from playwright.sync_api import sync_playwright

def analyze_boss_jobs():
    """分析 BOSS 直聘上的岗位"""
    
    print("=" * 60)
    print("BOSS 直聘 - 岗位分析")
    print("=" * 60)
    
    with sync_playwright() as p:
        try:
            # 连接已打开的浏览器
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            page = context.pages[0]
            
            print("\n[1/3] 已连接到 BOSS 直聘页面")
            
            # 等待页面加载
            time.sleep(2)
            
            print("[2/3] 获取岗位列表...")
            
            # 获取所有岗位卡片
            jobs = page.query_selector_all('.job-list-box .job-card-wrapper')
            
            print(f"\n[3/3] 找到 {len(jobs)} 个推荐岗位\n")
            print("=" * 60)
            
            for i, job in enumerate(jobs[:15]):
                try:
                    title_el = job.query_selector('.job-name')
                    company_el = job.query_selector('.company-name')
                    salary_el = job.query_selector('.salary')
                    info_el = job.query_selector('.job-info')
                    
                    if title_el and company_el:
                        title = title_el.inner_text()
                        company = company_el.inner_text()
                        salary = salary_el.inner_text() if salary_el else "面议"
                        info = info_el.inner_text() if info_el else ""
                        
                        print(f"\n{i+1}. {title}")
                        print(f"   公司：{company}")
                        print(f"   薪资：{salary}")
                        print(f"   要求：{info}")
                        
                except Exception as e:
                    continue
            
            print("\n" + "=" * 60)
            print("完成！")
            
        except Exception as e:
            print(f"[错误] {e}")

if __name__ == "__main__":
    analyze_boss_jobs()
