#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOSS 直聘 - 简单搜索
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
from playwright.sync_api import sync_playwright

def main():
    print("=" * 60)
    print("BOSS 直聘 - AI 岗位搜索")
    print("=" * 60)
    
    keywords = ["AI 解决方案", "企业数字化", "智能制造", "AI 商务"]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        
        print("\n[1/4] 打开 BOSS 直聘...")
        page.goto("https://www.zhipin.com/qingdao/", wait_until="domcontentloaded")
        time.sleep(5)
        
        for i, kw in enumerate(keywords):
            print(f"\n{'='*50}")
            print(f"[{i+1}/{len(keywords)}] 搜索：{kw}")
            print(f"{'='*50}")
            
            try:
                # 搜索
                page.click('input[placeholder*="搜索"]')
                time.sleep(0.5)
                page.fill('input[placeholder*="搜索"]', kw)
                time.sleep(0.5)
                page.press('input[placeholder*="搜索"]', 'Enter')
                time.sleep(5)
                
                # 获取岗位
                jobs = page.query_selector_all('.job-card-wrapper')
                print(f"\n找到 {len(jobs)} 个岗位\n")
                
                for j, job in enumerate(jobs[:5]):
                    try:
                        title_el = job.query_selector('.job-name')
                        company_el = job.query_selector('.company-name')
                        salary_el = job.query_selector('.salary')
                        
                        if title_el and company_el:
                            title = title_el.inner_text()
                            company = company_el.inner_text()
                            salary = salary_el.inner_text() if salary_el else "面议"
                            
                            print(f"  {j+1}. {title}")
                            print(f"     公司：{company}")
                            print(f"     薪资：{salary}")
                            print()
                    except:
                        continue
                        
            except Exception as e:
                print(f"[错误] {e}")
            
            time.sleep(2)
        
        print("\n" + "=" * 60)
        print("完成！浏览器保持打开")
        print("=" * 60)
        time.sleep(10)
        browser.close()

if __name__ == "__main__":
    main()
