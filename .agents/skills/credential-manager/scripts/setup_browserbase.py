#!/usr/bin/env python3
"""
Browserbase 配置向导
帮助用户注册并保存 API Key
"""

import json
import sys
from pathlib import Path

def save_credentials(service, username, password_or_key, extra=None):
    """保存凭证到加密存储"""
    cred_file = Path(__file__).parent.parent / "credentials.json"
    
    creds = {}
    if cred_file.exists():
        with open(cred_file, 'r', encoding='utf-8') as f:
            creds = json.load(f)
    
    creds[service] = {
        "username": username,
        "password": password_or_key,
    }
    if extra:
        creds[service].update(extra)
    
    with open(cred_file, 'w', encoding='utf-8') as f:
        json.dump(creds, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 凭证已保存：{service}")

def main():
    print("=" * 60)
    print("Browserbase 配置向导")
    print("=" * 60)
    print()
    print("步骤 1: 注册 Browserbase")
    print("   访问：https://www.browserbase.com/")
    print("   点击 'Sign Up' 或 'Get Started'")
    print("   使用邮箱或 GitHub 账号注册")
    print()
    print("步骤 2: 获取 API Key")
    print("   登录后进入 Dashboard")
    print("   找到 'API Keys' 或 'Settings'")
    print("   创建新的 API Key")
    print()
    print("步骤 3: 获取 Project ID")
    print("   在 Dashboard 中找到你的 Project ID")
    print("   通常显示在项目列表中")
    print()
    print("=" * 60)
    print("请输入你的 Browserbase 凭证:")
    print("=" * 60)
    
    api_key = input("API Key: ").strip()
    if not api_key:
        print("❌ API Key 不能为空")
        sys.exit(1)
    
    project_id = input("Project ID: ").strip()
    if not project_id:
        print("❌ Project ID 不能为空")
        sys.exit(1)
    
    # 保存凭证
    save_credentials("browserbase", "api_user", api_key, {"project_id": project_id})
    
    print()
    print("=" * 60)
    print("✅ 配置完成！")
    print("=" * 60)
    print()
    print("下一步：运行 jimeng_login_browserbase.py 开始自动化登录")

if __name__ == "__main__":
    main()
