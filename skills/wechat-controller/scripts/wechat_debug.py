#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信调试脚本 - 帮助定位界面元素
"""

import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import pyautogui
import time
import pygetwindow as gw

print("=" * 60)
print("微信调试工具 - 定位界面元素")
print("=" * 60)

# 查找微信窗口
windows = gw.getWindowsWithTitle('微信')
if windows:
    wechat = windows[0]
    print(f"\n✓ 找到微信窗口:")
    print(f"  标题：{wechat.title}")
    print(f"  位置：({wechat.left}, {wechat.top})")
    print(f"  大小：{wechat.width} x {wechat.height}")
    print(f"  激活：{wechat.isActive}")
    
    # 微信界面常见元素位置（相对坐标）
    print("\n📍 常见元素位置估算:")
    print(f"  搜索框：({wechat.left + 180}, {wechat.top + 60})")
    print(f"  聊天列表：({wechat.left + 100}, {wechat.top + 150})")
    print(f"  消息输入：({wechat.left + 400}, {wechat.top + 500})")
    print(f"  发送按钮：({wechat.left + 700}, {wechat.top + 500})")
else:
    print("❌ 未找到微信窗口")

print("\n" + "=" * 60)
print("鼠标位置追踪（移动鼠标查看坐标）")
print("按 Ctrl+C 停止")
print("=" * 60)

try:
    while True:
        x, y = pyautogui.position()
        print(f"\r鼠标位置：({x}, {y})    ", end='', flush=True)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n\n调试结束")
