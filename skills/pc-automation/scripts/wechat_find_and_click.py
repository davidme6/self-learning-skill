#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查找当前微信窗口并激活
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
import ctypes

def enum_windows_callback(hwnd, results):
    if ctypes.windll.user32.IsWindowVisible(hwnd):
        window_text = ctypes.create_unicode_buffer(256)
        ctypes.windll.user32.GetWindowTextW(hwnd, window_text, 256)
        if window_text.value:
            if "微信" in window_text.value or "WeChat" in window_text.value:
                results.append((hwnd, window_text.value))
    return True

def main():
    print("=" * 60)
    print("查找微信窗口")
    print("=" * 60)
    
    results = []
    
    def callback(hwnd, lparam):
        if ctypes.windll.user32.IsWindowVisible(hwnd):
            window_text = ctypes.create_unicode_buffer(256)
            ctypes.windll.user32.GetWindowTextW(hwnd, window_text, 256)
            if window_text.value:
                if "微信" in window_text.value or "WeChat" in window_text.value:
                    print(f"\n[找到] 窗口：{window_text.value}")
                    print(f"       句柄：{hwnd}")
                    
                    # 获取窗口位置
                    rect = ctypes.wintypes.RECT()
                    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
                    print(f"       位置：({rect.left}, {rect.top}) - ({rect.right}, {rect.bottom})")
                    
                    width = rect.right - rect.left
                    height = rect.bottom - rect.top
                    print(f"       大小：{width} x {height}")
                    
                    # 计算按钮位置（绿色按钮通常在窗口 70% 处）
                    center_x = (rect.left + rect.right) // 2
                    button_y = rect.top + int(height * 0.70)
                    print(f"       按钮估计：({center_x}, {button_y})")
                    
                    # 激活窗口
                    ctypes.windll.user32.SetForegroundWindow(hwnd)
                    time.sleep(0.5)
                    
                    # 点击
                    import pyautogui
                    ctypes.windll.user32.SetCursorPos(center_x, button_y)
                    time.sleep(0.2)
                    pyautogui.click()
                    print(f"       [已点击]")
                    
        return True
    
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(callback), 0)
    
    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
