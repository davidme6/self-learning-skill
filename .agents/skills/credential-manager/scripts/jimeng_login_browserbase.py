#!/usr/bin/env python3
"""
即梦自动化登录脚本 - Browserbase 版本
使用 Browserbase 的远程浏览器绕过 Cloudflare 反机器人保护
"""

import subprocess
import json
import sys
from pathlib import Path

def get_credentials(service):
    """从加密存储中获取凭证"""
    cred_script = Path(__file__).parent / "retrieve.py"
    result = subprocess.run(
        [sys.executable, str(cred_script), service],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    if result.returncode != 0:
        print(f"Error: Failed to get credentials: {result.stderr}")
        sys.exit(1)
    return json.loads(result.stdout)

def login_jimeng_browserbase():
    """使用 Browserbase 自动化登录即梦"""
    
    # 获取凭证
    bb_creds = get_credentials("browserbase")
    api_key = bb_creds["password"]  # API Key 存储在 password 字段
    project_id = bb_creds.get("project_id", "")
    
    jimeng_creds = get_credentials("jimeng")
    username = jimeng_creds["username"]
    password = jimeng_creds["password"]
    
    print(f"Browserbase API Key: {api_key[:8]}...")
    print(f"Project ID: {project_id}")
    print(f"Jimeng Username: {username}")
    print()
    
    # 安装 browserbase Python SDK
    print("Installing Browserbase SDK...")
    subprocess.run([sys.executable, "-m", "pip", "install", "browserbase", "-q"], check=True)
    
    # Browserbase 自动化脚本
    playwright_code = f'''
from browserbase import Browserbase
from playwright.sync_api import sync_playwright
import time

# 初始化 Browserbase
bb = Browserbase(api_key="{api_key}")

# 创建会话
print("Creating Browserbase session...")
session = bb.sessions.create(project_id="{project_id}")
session_id = session.id
print(f"Session ID: {{session_id}}")

# 获取 WebSocket 连接 URL
cdp_url = session.connect_url
print(f"CDP URL: {{cdp_url}}")

# 使用 Playwright 连接到远程浏览器
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(cdp_url)
    context = browser.contexts[0]
    page = context.pages[0]
    
    # 打开即梦官网
    print("Opening Jimeng website...")
    page.goto("https://seedance.ai/", wait_until="networkidle")
    time.sleep(3)
    
    # 截图查看当前页面
    page.screenshot(path="jimeng_step1_homepage.png")
    print("Screenshot saved: jimeng_step1_homepage.png")
    
    # 查找登录入口
    print("Looking for login button...")
    
    # 尝试多种登录按钮选择器
    login_selectors = [
        'button:has-text("登录")',
        'button:has-text("Log in")',
        'a:has-text("登录")',
        'a:has-text("Log in")',
        '[class*="login"]',
        '[id*="login"]',
        'nav a[href*="login"]',
        'nav button:has-text("登录")',
    ]
    
    login_clicked = False
    for selector in login_selectors:
        try:
            login_btn = page.locator(selector).first
            if login_btn.is_visible():
                print(f"Found login button: {{selector}}")
                login_btn.click()
                time.sleep(3)
                login_clicked = True
                page.screenshot(path="jimeng_step2_after_login_click.png")
                break
        except Exception as e:
            pass
    
    if not login_clicked:
        print("Login button not found, trying direct login page...")
        page.goto("https://seedance.ai/login", wait_until="networkidle")
        time.sleep(3)
        page.screenshot(path="jimeng_step2_login_page.png")
    
    # 填写账号密码
    print("Filling credentials...")
    
    # 用户名/手机号输入框
    username_selectors = [
        'input[type="tel"]',
        'input[type="text"]',
        'input[name="phone"]',
        'input[name="username"]',
        'input[placeholder*="手机"]',
        'input[placeholder*="phone"]',
        'input[placeholder*="账号"]',
        '#username',
        '#phone',
        '#mobile',
    ]
    
    # 密码输入框
    password_selectors = [
        'input[type="password"]',
        '#password',
        'input[name="password"]',
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
        'button:has-text("Sign in")',
        'button[type="submit"]',
        '[class*="submit"]',
        'button[class*="login"]',
    ]
    
    for selector in submit_selectors:
        try:
            btn = page.locator(selector).first
            if btn.is_visible():
                btn.click()
                print(f"Clicked submit button: {{selector}}")
                break
        except:
            pass
    
    # 等待登录完成
    print("Waiting for login to complete...")
    time.sleep(5)
    
    # 截图查看登录结果
    page.screenshot(path="jimeng_step3_after_submit.png")
    print("Screenshot saved: jimeng_step3_after_submit.png")
    
    # 检查是否登录成功
    current_url = page.url
    print(f"Current URL: {{current_url}}")
    
    # 检查是否有登录成功标志
    success_indicators = [
        'user',
        'profile',
        'account',
        'workspace',
        'create',
    ]
    
    is_logged_in = any(indicator in current_url.lower() for indicator in success_indicators)
    
    if is_logged_in or "/login" not in current_url.lower():
        print("✅ Login appears successful!")
    else:
        print("⚠️  May still be on login page - check screenshots")
    
    # 保持会话 60 秒供检查
    print("Session will remain active for 60 seconds...")
    time.sleep(60)
    
    # 关闭会话
    bb.sessions.close(session_id)
    print(f"Session {{session_id}} closed")
    print("Done!")
'''
    
    # 执行脚本
    result = subprocess.run(
        [sys.executable, "-c", playwright_code],
        capture_output=False,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    
    return result.returncode == 0

if __name__ == "__main__":
    print("=" * 60)
    print("Jimeng Auto Login - Browserbase Edition")
    print("=" * 60)
    print()
    
    try:
        success = login_jimeng_browserbase()
        if success:
            print("\n✅ Login process completed!")
        else:
            print("\n❌ Login failed")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
