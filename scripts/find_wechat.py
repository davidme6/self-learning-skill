#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""查找微信安装路径和数据目录"""

import os
import psutil
from pathlib import Path

print("=" * 50)
print("微信路径检测")
print("=" * 50)

# 找微信进程
wechat_procs = []
for proc in psutil.process_iter(['pid', 'name', 'exe']):
    try:
        if 'WeChat' in proc.info['name'] or 'wechat' in proc.info['name'].lower():
            wechat_procs.append(proc.info)
    except:
        pass

if wechat_procs:
    for proc in wechat_procs[:3]:  # 只显示前3个
        print(f"\n进程: {proc['name']}")
        print(f"路径: {proc['exe']}")
else:
    print("未找到微信进程")

# 搜索常见微信数据目录
print("\n" + "=" * 50)
print("搜索微信数据目录")
print("=" * 50)

user = os.environ['USERPROFILE']
search_paths = [
    Path(user) / 'Documents' / 'WeChat Files',
    Path('D:/') / '微信数据',
    Path('D:/'),
]

for sp in search_paths:
    if sp.exists():
        print(f"\n搜索: {sp}")
        for item in sp.rglob('MSG*'):
            if item.is_dir() and 'WMPF' not in str(item):
                print(f"  找到: {item}")
                break

# 检查PyWxDump需要的路径
print("\n" + "=" * 50)
print("PyWxDump 配置")
print("=" * 50)

# 尝试找到微信账号目录
wechat_files = Path(user) / 'Documents' / 'WeChat Files'
if wechat_files.exists():
    for account in wechat_files.iterdir():
        if account.is_dir() and not account.name.startswith('All') and account.name != 'WMPF':
            print(f"账号目录: {account}")