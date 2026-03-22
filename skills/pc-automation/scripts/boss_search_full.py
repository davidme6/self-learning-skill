#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOSS 直聘 - 搜索 AI 岗位并分析
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
import json
from playwright.sync_api import sync_playwright

def search_and_analyze():
    """搜索并分析 AI 岗位"""
    
    print("=" * 60)
    print("BOSS 直聘 - AI 岗位搜索与分析")
    print("=" * 60)
    
    # 搜索关键词（根据用户需求：AI+ 制造业/企业客户/能积累资源）
    keywords = [
        "AI 解决方案",
        "AI 大客户",
        "企业数字化",
        "智能制造",
        "AI 商务",
        "工业互联网",
        "SaaS 大客户",
        "AI 营销"
    ]
    
    results = []
    
    with sync_playwright() as p:
        # 尝试连接已打开的浏览器
        browser = None
        for port in [9222, 9223, 9224, 9225]:
            try:
                browser = p.chromium.connect_over_cdp(f"http://localhost:{port}")
                print(f"\n✅ 连接到浏览器端口 {port}")
                break
            except:
                continue
        
        if not browser:
            print("\n⚠️ 未找到已打开的浏览器，启动新浏览器...")
            browser = p.chromium.launch(headless=False)
        
        context = browser.contexts[0]
        page = context.pages[0] if len(context.pages) > 0 else context.new_page()
        
        # 打开 BOSS 直聘
        print("\n[1/8] 打开 BOSS 直聘...")
        page.goto("https://www.zhipin.com/qingdao/?ka=header-home", wait_until="domcontentloaded")
        time.sleep(5)
        
        for i, kw in enumerate(keywords):
            print(f"\n{'='*50}")
            print(f"[{i+1}/{len(keywords)}] 搜索：{kw}")
            print(f"{'='*50}")
            
            try:
                # 搜索
                search_box = page.locator('input[placeholder*="搜索"]').first
                search_box.click()
                time.sleep(0.5)
                search_box.fill(kw)
                time.sleep(0.5)
                search_box.press('Enter')
                time.sleep(4)
                
                # 获取岗位
                jobs = page.locator('.job-card-wrapper').all()
                count = len(jobs)
                print(f"\n找到 {count} 个岗位")
                
                if count == 0:
                    continue
                
                # 获取前 5 个岗位详情
                for j in range(min(5, count)):
                    try:
                        job = jobs[j]
                        title = job.locator('.job-name').inner_text().strip()
                        company = job.locator('.company-name').inner_text().strip()
                        salary = job.locator('.salary').inner_text().strip() if job.locator('.salary').count() > 0 else "面议"
                        location = job.locator('.job-location').inner_text().strip() if job.locator('.job-location').count() > 0 else ""
                        experience = job.locator('.job-info li').nth(0).inner_text().strip() if job.locator('.job-info li').count() > 0 else ""
                        
                        job_data = {
                            "keyword": kw,
                            "title": title,
                            "company": company,
                            "salary": salary,
                            "location": location,
                            "experience": experience
                        }
                        results.append(job_data)
                        
                        print(f"\n  {j+1}. {title}")
                        print(f"     公司：{company}")
                        print(f"     薪资：{salary}")
                        print(f"     地点：{location}")
                        print(f"     经验：{experience}")
                        
                    except Exception as e:
                        continue
                        
            except Exception as e:
                print(f"[错误] {e}")
            
            time.sleep(2)
        
        # 保存结果
        print("\n" + "=" * 60)
        print(f"共找到 {len(results)} 个岗位")
        print("=" * 60)
        
        # 保存到文件
        with open("boss_jobs_result.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print("\n结果已保存到：boss_jobs_result.json")
        
        # 保持浏览器打开
        print("\n[提示] 浏览器保持打开，按 Ctrl+C 关闭")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n关闭浏览器...")
            browser.close()

if __name__ == "__main__":
    search_and_analyze()
