#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信数据库读取工具
"""

import sqlite3
from pathlib import Path

WECHAT_DATA_DIR = Path("D:/WeChat Files")

def main():
    print("=" * 50)
    print("微信数据库读取工具")
    print("=" * 50)
    
    if not WECHAT_DATA_DIR.exists():
        print(f"❌ 微信数据目录不存在: {WECHAT_DATA_DIR}")
        return
    
    print(f"✅ 微信数据目录: {WECHAT_DATA_DIR}")
    
    # 列出账号
    print("\n📱 发现的微信账号：")
    accounts = []
    for account_dir in WECHAT_DATA_DIR.iterdir():
        if account_dir.is_dir() and account_dir.name.startswith("wxid_"):
            msg_dir = account_dir / "Msg" / "Multi"
            msg_files = list(msg_dir.glob("MSG*.db")) if msg_dir.exists() else []
            accounts.append((account_dir.name, len(msg_files)))
            print(f"  - {account_dir.name} ({len(msg_files)} 个消息库)")
    
    print("\n" + "=" * 50)
    print("⚠️  数据库已加密，需要密钥")
    print("=" * 50)
    print("""
🔑 获取密钥方法：

方法 1: wxdump ui（推荐）
   1. 右键 PowerShell -> 以管理员身份运行
   2. 输入: wxdump ui
   3. 打开浏览器显示的地址
   4. 在界面查看密钥和导出

方法 2: 手动复制（最简单）
   1. 打开微信聊天窗口
   2. 滚动加载历史
   3. Ctrl+A 全选 -> 复制
   4. 粘贴到 txt 文件
   5. 我来脱敏处理
""")

if __name__ == "__main__":
    main()