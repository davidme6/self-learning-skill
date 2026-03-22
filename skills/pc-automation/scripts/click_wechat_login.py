#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
点击微信的"进入微信"按钮
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
import pyautogui

def main():
    print("[1/3] 等待 2 秒让窗口稳定...")
    time.sleep(2)
    
    print("[2/3] 获取屏幕分辨率...")
    screen_width, screen_height = pyautogui.size()
    print(f"    屏幕分辨率：{screen_width} x {screen_height}")
    
    # 计算按钮位置（大概在屏幕中央偏下）
    # 从截图看，按钮在窗口中间，宽度约占窗口的 60%
    # 假设窗口在屏幕中央
    center_x = screen_width // 2
    center_y = screen_height // 2
    
    # 按钮大概在中心下方 100 像素
    button_x = center_x
    button_y = center_y + 150
    
    print(f"[3/3] 点击按钮位置：({button_x}, {button_y})")
    print("=" * 60)
    
    # 移动到按钮位置（可以看到鼠标移动）
    pyautogui.moveTo(button_x, button_y, duration=0.5)
    time.sleep(0.3)
    
    # 点击
    pyautogui.click()
    
    print("[完成] 已点击 [进入微信] 按钮！")
    print("=" * 60)

if __name__ == "__main__":
    main()
