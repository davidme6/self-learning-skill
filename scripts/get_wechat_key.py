#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动获取微信密钥并解密数据库
"""

import os
import sys
import ctypes
from pathlib import Path

# 添加 PyWxDump 路径
try:
    from pywxdump import get_wx_info, decrypt_merge
except ImportError:
    print("请先安装 pywxdump: pip install pywxdump")
    sys.exit(1)

print("=" * 50)
print("微信数据库解密工具")
print("=" * 50)

# 微信数据路径
wechat_data_dir = Path("D:/WeChat Files")
account_dir = wechat_data_dir / "wxid_9096610966122"

print(f"\n账号目录: {account_dir}")

# 检查是否以管理员权限运行
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("\n⚠️  请以管理员身份运行此脚本！")
    print("   右键点击 PowerShell -> 以管理员身份运行")
    sys.exit(1)

# 尝试获取微信信息
print("\n正在获取微信信息...")

try:
    # 尝试不同的获取方式
    from pywxdump.api.rjson import get_wechat_db
    
    # 获取当前登录的微信信息
    result = get_wechat_db()
    print(f"结果: {result}")
    
except Exception as e:
    print(f"获取失败: {e}")
    print("\n尝试备用方法...")
    
    try:
        # 备用方法：直接读取内存
        from pywxdump.analyzer.dat_analyzer import DatAnalyzer
        
        print("请确保微信正在运行...")
        
    except Exception as e2:
        print(f"备用方法也失败: {e2}")

print("\n" + "=" * 50)
print("如果以上方法都失败，请尝试：")
print("1. 确保微信正在运行")
print("2. 以管理员身份运行")
print("3. 或者手动复制聊天记录（最安全）")
print("=" * 50)