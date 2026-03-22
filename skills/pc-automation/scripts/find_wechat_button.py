#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
截图并找到微信登录按钮位置
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
import pyautogui

def main():
    print("[1/2] 截取屏幕...")
    screenshot = pyautogui.screenshot()
    
    # 保存到临时文件
    screenshot_path = "C:\\Windows\\system32\\UsersAdministrator.openclawworkspace\\skills\\pc-automation\\scripts\\wechat_screenshot.png"
    screenshot.save(screenshot_path)
    print(f"[2/2] 截图已保存：{screenshot_path}")
    
    # 屏幕中心区域（微信窗口通常在这里）
    screen_width, screen_height = pyautogui.size()
    print(f"屏幕分辨率：{screen_width} x {screen_height}")
    
    # 微信登录窗口大约在屏幕中央 600x400 区域
    # 按钮在窗口下半部分
    window_center_x = screen_width // 2
    window_center_y = screen_height // 2
    
    print(f"\n可能的按钮位置：")
    print(f"  位置 1: ({window_center_x}, {window_center_y + 100})")
    print(f"  位置 2: ({window_center_x}, {window_center_y + 120})")
    print(f"  位置 3: ({window_center_x}, {window_center_y + 140})")
    
    print("\n" + "=" * 60)
    print("截图已保存，可以查看按钮的准确位置")
    print("=" * 60)

if __name__ == "__main__":
    main()
