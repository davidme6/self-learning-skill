#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 Windows UI 自动化点击微信登录按钮
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
import ctypes
from ctypes import wintypes

def find_window_by_title(title):
    """查找窗口"""
    EnumWindows = ctypes.windll.user32.EnumWindows
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible
    
    def callback(hwnd, lparam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            if length > 0:
                buffer = ctypes.create_unicode_buffer(length + 1)
                GetWindowText(hwnd, buffer, length + 1)
                if title in buffer.value:
                    print(f"[找到] 窗口：{buffer.value} (hwnd={hwnd})")
                    # 激活窗口
                    ctypes.windll.user32.SetForegroundWindow(hwnd)
                    time.sleep(0.5)
                    # 获取窗口位置
                    rect = ctypes.wintypes.RECT()
                    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
                    width = rect.right - rect.left
                    height = rect.bottom - rect.top
                    center_x = (rect.left + rect.right) // 2
                    center_y = (rect.top + rect.bottom) // 2
                    print(f"窗口位置：({rect.left}, {rect.top}) - ({rect.right}, {rect.bottom})")
                    print(f"窗口大小：{width} x {height}")
                    print(f"窗口中心：({center_x}, {center_y})")
                    
                    # 按钮通常在中心下方
                    button_y = rect.top + int(height * 0.65)
                    print(f"按钮估计位置：({center_x}, {button_y})")
                    
                    # 点击
                    import pyautogui
                    pyautogui.click(center_x, button_y)
                    print("[完成] 已点击！")
                    return False
        return True
    
    EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(callback), 0)

def main():
    print("[1/3] 查找微信窗口...")
    
    # 尝试多个可能的窗口标题
    titles = ["微信", "WeChat", "登录"]
    
    for title in titles:
        print(f"\n[2/3] 搜索包含 '{title}' 的窗口...")
        find_window_by_title(title)
        time.sleep(1)
    
    print("\n[3/3] 完成！")

if __name__ == "__main__":
    main()
