#!/usr/bin/env python3
"""
即梦自动化登录脚本
使用 Playwright 自动登录即梦网站
"""

import subprocess
import json
import sys
from pathlib import Path

# 确保 UTF-8 输出
sys.stdout.reconfigure(encoding='utf-8')

def get_credentials():
    """从加密存储中获取即梦账号"""
    cred_script = Path(__file__).parent / "retrieve.py"
    result = subprocess.run(
        [sys.executable, str(cred_script), "jimeng"],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    if result.returncode != 0:
        print(f"Error: Failed to get credentials: {result.stderr}")
        sys.exit(1)
    return json.loads(result.stdout)

def login_jimeng():
    """自动化登录即梦"""
    creds = get_credentials()
    username = creds["username"]
    password = creds["password"]
    
    print(f"Logging in to Jimeng...")
    print(f"   Username: {username}")
    
    # Playwright 自动化脚本
    playwright_code = f'''
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    # 启动浏览器
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    # 打开即梦官网 (seedance.ai)
    print("Opening Jimeng website...")
    page.goto("https://seedance.ai/", wait_until="networkidle")
    time.sleep(2)
    
    # 尝试找到登录按钮并点击
    print("Looking for login button...")
    
    # 可能的登录按钮选择器
    login_selectors = [
        'button:has-text("登录")',
        'a:has-text("登录")',
        '[class*="login"]',
        '[id*="login"]',
        'button:has-text("Log in")',
        'a:has-text("Log in")',
    ]
    
    login_btn = None
    for selector in login_selectors:
        try:
            login_btn = page.locator(selector).first
            if login_btn.is_visible():
                print(f"Found login button: {{selector}}")
                break
            login_btn = None
        except:
            login_btn = None
    
    if login_btn:
        login_btn.click()
        time.sleep(2)
    else:
        print("Login button not found, trying direct login page...")
        page.goto("https://seedance.ai/login", wait_until="networkidle")
        time.sleep(2)
    
    # 填写账号密码
    print("Filling credentials...")
    
    # 可能的用户名输入框
    username_selectors = [
        'input[type="tel"]',
        'input[type="text"]',
        'input[name="phone"]',
        'input[placeholder*="手机"]',
        'input[placeholder*="phone"]',
        '#username',
        '#phone',
    ]
    
    # 可能的密码输入框
    password_selectors = [
        'input[type="password"]',
        '#password',
    ]
    
    # 填写用户名
    for selector in username_selectors:
        try:
            field = page.locator(selector).first
            if field.is_visible():
                field.fill("{username}")
                print(f"Filled username: {{selector}}")
                break
        except:
            pass
    
    # 填写密码
    for selector in password_selectors:
        try:
            field = page.locator(selector).first
            if field.is_visible():
                field.fill("{password}")
                print(f"Filled password: {{selector}}")
                break
        except:
            pass
    
    # 点击登录按钮
    print("Submitting login...")
    submit_selectors = [
        'button:has-text("登录")',
        'button:has-text("Log in")',
        'button[type="submit"]',
        '[class*="submit"]',
    ]
    
    for selector in submit_selectors:
        try:
            btn = page.locator(selector).first
            if btn.is_visible():
                btn.click()
                print(f"Clicked login button: {{selector}}")
                break
        except:
            pass
    
    # 等待登录完成
    print("Waiting for login to complete...")
    time.sleep(5)
    
    # 检查是否登录成功
    current_url = page.url
    print(f"Current URL: {{current_url}}")
    
    # 截图保存
    screenshot_path = "jimeng_login_result.png"
    page.screenshot(path=screenshot_path)
    print(f"Screenshot saved: {{screenshot_path}}")
    
    # 保持浏览器打开 30 秒供检查
    print("Browser will close in 30 seconds...")
    time.sleep(30)
    
    browser.close()
    print("Done!")
'''
    
    # 执行 Playwright 脚本
    result = subprocess.run(
        [sys.executable, "-c", playwright_code],
        capture_output=False,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    
    return result.returncode == 0

if __name__ == "__main__":
    print("Jimeng Auto Login")
    print("=" * 40)
    
    try:
        success = login_jimeng()
        if success:
            print("\\nLogin completed!")
        else:
            print("\\nLogin failed")
            sys.exit(1)
    except Exception as e:
        print(f"\\nError: {e}")
        sys.exit(1)
