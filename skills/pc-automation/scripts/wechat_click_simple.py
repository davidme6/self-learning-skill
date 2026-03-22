#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单版：点击微信"进入微信"按钮
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
import ctypes
import pyautogui

def click_at(x, y):
    """点击指定位置"""
    # 移动鼠标
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.1)
    # 点击
    pyautogui.click()

def main():
    print("=" * 60)
    print("微信登录 - 点击 [进入微信] 按钮")
    print("=" * 60)
    
    # 微信窗口位置（之前找到的）
    window_left = 345
    window_top = 389
    window_width = 296
    window_height = 388
    
    print(f"\n微信窗口：({window_left}, {window_top})")
    print(f"窗口大小：{window_width} x {window_height}")
    
    # 绿色按钮位置（窗口中心偏下，约 70% 处）
    button_x = window_left + window_width // 2
    button_y = window_top + int(window_height * 0.70)
    
    print(f"\n按钮位置：({button_x}, {button_y})")
    print("\n[3 秒后点击...]")
    
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    # 点击
    click_at(button_x, button_y)
    
    print("\n" + "=" * 60)
    print("✅ 已点击！")
    print("=" * 60)

if __name__ == "__main__":
    main()
