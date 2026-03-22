#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信简单版 - 用最简单的方式发送消息
假设微信已经在正确的聊天窗口
"""

import sys
import time
import pyautogui
import pyperclip

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("微信简单测试 - 请手动打开要发送的聊天窗口")
print("=" * 60)

if len(sys.argv) < 2:
    message = "测试消息 " + time.strftime("%H:%M:%S")
else:
    message = " ".join(sys.argv[1:])  # 跳过脚本路径

print(f"\n准备发送：{message}")
print("\n⚠️  请在 5 秒内切换到微信的正确聊天窗口！")
print("⚠️  确保输入框是空的！")

for i in range(5, 0, -1):
    print(f"  倒计时：{i}...")
    time.sleep(1)

print("\n[ACTION] 粘贴消息...")
pyperclip.copy(message)
time.sleep(0.3)
pyautogui.hotkey('ctrl', 'v')
time.sleep(0.5)

print("[ACTION] 发送...")
pyautogui.press('enter')

print("\n[OK] 完成！")
print("=" * 60)
