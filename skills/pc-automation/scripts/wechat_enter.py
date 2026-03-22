#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信登录 - 使用键盘操作
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
import pyautogui

def main():
    print("[1/4] 等待窗口稳定...")
    time.sleep(1)
    
    print("[2/4] 按 Tab 键切换焦点...")
    # 通常登录界面 Tab 几次就能到按钮
    for i in range(3):
        pyautogui.press('tab')
        time.sleep(0.3)
    
    print("[3/4] 按回车键确认...")
    pyautogui.press('enter')
    
    time.sleep(2)
    
    print("[4/4] 完成！")
    print("=" * 60)
    print("已尝试键盘操作登录微信")
    print("=" * 60)

if __name__ == "__main__":
    main()
