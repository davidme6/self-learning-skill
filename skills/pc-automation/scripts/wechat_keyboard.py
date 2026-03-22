#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信登录 - 使用键盘快捷键
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
import ctypes
import pyautogui

def main():
    print("=" * 60)
    print("微信登录 - 键盘操作")
    print("=" * 60)
    
    # 微信窗口句柄
    hwnd = 329304
    
    print("\n[1/4] 激活微信窗口...")
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    time.sleep(0.5)
    
    print("[2/4] 按空格键（确认按钮）...")
    pyautogui.press('space')
    time.sleep(1)
    
    print("[3/4] 按回车键（备用）...")
    pyautogui.press('enter')
    time.sleep(1)
    
    print("[4/4] 完成！")
    print("=" * 60)
    print("已尝试键盘操作登录微信")
    print("=" * 60)

if __name__ == "__main__":
    main()
