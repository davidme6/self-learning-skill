#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打开微信网页版并保持浏览器打开
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from playwright.sync_api import sync_playwright
import time

def main():
    print("[1/4] 启动浏览器...")
    with sync_playwright() as p:
        # 启动浏览器（保持打开）
        browser = p.chromium.launch(
            headless=False,  # 显示浏览器窗口
            args=['--start-maximized']
        )
        
        print("[2/4] 创建页面...")
        page = browser.new_page()
        
        print("[3/4] 访问微信网页版...")
        page.goto("https://wx.qq.com/", wait_until="domcontentloaded")
        
        print("[4/4] 等待扫码登录...")
        print("=" * 60)
        print("[手机] 请用手机微信扫码登录")
        print("[时钟] 等待 90 秒...")
        print("=" * 60)
        
        # 等待 90 秒让用户扫码登录
        time.sleep(90)
        
        # 检查是否登录成功
        try:
            current_url = page.url
            if "wx.qq.com" in current_url and "cgi-bin/mmwebwx-bin/webwxinit" not in current_url:
                print("[成功] 检测到已登录！")
            else:
                print("[等待] 时间到，浏览器保持打开状态")
        except Exception as e:
            print(f"[提示] 检查状态：{e}")
        
        print("=" * 60)
        print("[提示] 浏览器保持打开，你可以继续使用微信")
        print("[退出] 按 Ctrl+C 或关闭浏览器窗口退出")
        print("=" * 60)
        
        # 保持浏览器打开，等待用户操作
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[退出] 正在关闭浏览器...")
            browser.close()
            print("[完成] 已退出")

if __name__ == "__main__":
    main()
