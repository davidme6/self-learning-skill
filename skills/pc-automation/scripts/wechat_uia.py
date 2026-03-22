#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 Windows UI Automation 找到并点击微信登录按钮
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
import ctypes
import pyautogui

# 加载 UI Automation 库
try:
    from comtypes import CLSCTX_ALL
    from comtypes.client import CreateObject
    uia_available = True
except:
    uia_available = False
    print("[提示] comtypes 不可用，使用备用方案")

def click_wechat_button():
    """使用 UI Automation 找到并点击按钮"""
    
    if not uia_available:
        print("[备用方案] 尝试多个位置点击...")
        # 微信窗口位置
        window_left = 345
        window_top = 389
        window_width = 296
        window_height = 388
        
        # 尝试多个可能的按钮位置
        positions = [
            (window_left + window_width//2, window_top + int(window_height * 0.65)),
            (window_left + window_width//2, window_top + int(window_height * 0.70)),
            (window_left + window_width//2, window_top + int(window_height * 0.75)),
            (window_left + window_width//2, window_top + int(window_height * 0.60)),
        ]
        
        for i, (x, y) in enumerate(positions):
            print(f"\n尝试位置 {i+1}: ({x}, {y})")
            ctypes.windll.user32.SetCursorPos(x, y)
            time.sleep(0.2)
            pyautogui.click()
            time.sleep(1.5)
        
        print("\n[完成] 已尝试多个位置")
        return
    
    # 使用 UI Automation
    try:
        iuia = CreateObject("UIAutomationCore.CUIAutomation", interface=None, clsctx=CLSCTX_ALL)
        
        # 获取根元素
        root = iuia.GetRootElement()
        
        # 查找微信窗口
        condition = iuia.CreatePropertyCondition(30019, "微信")  # UIA_NamePropertyId = 30019
        
        print("[1/3] 查找微信窗口...")
        wechat_window = root.FindFirst(2, condition)  # TreeScope_Descendants = 2
        
        if not wechat_window:
            print("[错误] 未找到微信窗口")
            return
        
        print("[2/3] 找到微信窗口！")
        
        # 查找按钮
        button_condition = iuia.CreatePropertyCondition(30003, 30000)  # UIA_ControlTypePropertyId = 30003, UIA_ButtonControlTypeId = 30000
        
        print("[3/3] 查找按钮...")
        button = wechat_window.FindFirst(2, button_condition)
        
        if button:
            # 获取按钮位置
            rect = button.CurrentBoundingRectangle
            center_x = (rect.left + rect.right) // 2
            center_y = (rect.top + rect.bottom) // 2
            
            print(f"[找到] 按钮位置：({center_x}, {center_y})")
            
            # 激活窗口
            wechat_window.SetFocus()
            time.sleep(0.5)
            
            # 点击按钮
            ctypes.windll.user32.SetCursorPos(center_x, center_y)
            time.sleep(0.2)
            pyautogui.click()
            
            print("[完成] 已点击按钮！")
        else:
            print("[未找到] 未找到按钮，使用备用方案")
            click_wechat_button_fallback()
            
    except Exception as e:
        print(f"[错误] {e}")
        print("使用备用方案...")
        click_wechat_button_fallback()

def click_wechat_button_fallback():
    """备用方案：尝试多个位置"""
    window_left = 345
    window_top = 389
    window_width = 296
    window_height = 388
    
    # 激活微信窗口
    hwnd = ctypes.c_void_p(329304)
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    time.sleep(0.5)
    
    # 尝试中心位置
    x = window_left + window_width // 2
    y = window_top + int(window_height * 0.68)
    
    print(f"[点击] 位置：({x}, {y})")
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.2)
    pyautogui.click()

def main():
    print("=" * 60)
    print("微信登录 - UI Automation")
    print("=" * 60)
    click_wechat_button()
    print("=" * 60)

if __name__ == "__main__":
    main()
