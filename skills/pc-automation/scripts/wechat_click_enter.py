#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用图像识别点击微信"进入微信"按钮
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
import pyautogui

def main():
    print("[1/4] 截取屏幕...")
    screenshot = pyautogui.screenshot()
    screen_width, screen_height = pyautogui.size()
    print(f"    屏幕分辨率：{screen_width} x {screen_height}")
    
    print("\n[2/4] 分析微信窗口位置...")
    # 从之前找到的窗口位置
    # 窗口：(345, 389) - (641, 777)
    # 窗口大小：296 x 388
    
    window_left = 345
    window_top = 389
    window_width = 296
    window_height = 388
    
    print(f"    微信窗口：({window_left}, {window_top})")
    print(f"    窗口大小：{window_width} x {window_height}")
    
    print("\n[3/4] 计算按钮位置...")
    # 绿色按钮在窗口下半部分，大约 65% 的位置
    # 从截图看，按钮在头像下方，大约窗口高度的 65-75% 处
    button_x = window_left + window_width // 2
    button_y = window_top + int(window_height * 0.68)
    
    print(f"    按钮中心位置：({button_x}, {button_y})")
    
    # 按钮大约宽 200 像素，高 50 像素
    button_width = 200
    button_height = 50
    
    print(f"    按钮估计大小：{button_width} x {button_height}")
    
    print("\n[4/4] 点击按钮...")
    # 先移动到按钮位置
    pyautogui.moveTo(button_x, button_y, duration=0.3)
    time.sleep(0.2)
    
    # 点击
    pyautogui.click()
    
    print("=" * 60)
    print("✅ 已点击 [进入微信] 按钮！")
    print(f"   点击位置：({button_x}, {button_y})")
    print("=" * 60)
    
    # 等待一下看效果
    time.sleep(2)
    print("\n[提示] 如果还没登录，可能需要调整位置")

if __name__ == "__main__":
    main()
