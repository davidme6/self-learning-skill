#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信测试 - 简单测试发送功能
"""

import sys
import time
import pyautogui
import pygetwindow as gw
import pyperclip

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

print("=" * 60)
print("微信测试 - 手动测试发送")
print("=" * 60)

# 1. 找到微信窗口
windows = gw.getWindowsWithTitle('微信')
if not windows:
    print("[ERROR] 未找到微信窗口")
    sys.exit(1)

wechat = windows[0]
print(f"\n[OK] 找到微信窗口：{wechat.title}")
print(f"     位置：({wechat.left}, {wechat.top})")
print(f"     大小：{wechat.width} x {wechat.height}")

# 2. 激活窗口
print("\n[ACTION] 激活窗口...")
if hasattr(wechat, 'activate'):
    wechat.activate()
time.sleep(1)

# 3. 测试：直接粘贴到当前焦点
print("\n[ACTION] 测试粘贴...")
test_message = "【测试消息】" + str(time.strftime("%H:%M:%S"))
pyperclip.copy(test_message)
time.sleep(0.3)

print(f"准备发送：{test_message}")
print("\n⚠️  接下来 3 秒，请确保微信在正确的聊天窗口！")
time.sleep(3)

# 粘贴
pyautogui.hotkey('ctrl', 'v')
time.sleep(0.5)

# 发送
print("[ACTION] 发送...")
pyautogui.press('enter')

print("\n[OK] 测试完成！")
print("=" * 60)
