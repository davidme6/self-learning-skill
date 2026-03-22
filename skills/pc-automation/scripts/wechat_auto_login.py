#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信自动登录 - 完整版
自动找到微信窗口并点击"进入微信"按钮
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
import ctypes
import pyautogui

def find_and_click_wechat():
    """找到微信窗口并点击登录按钮"""
    
    print("=" * 60)
    print("微信自动登录")
    print("=" * 60)
    
    found_window = None
    
    def callback(hwnd, lparam):
        nonlocal found_window
        
        if ctypes.windll.user32.IsWindowVisible(hwnd):
            window_text = ctypes.create_unicode_buffer(256)
            ctypes.windll.user32.GetWindowTextW(hwnd, window_text, 256)
            class_name = ctypes.create_unicode_buffer(256)
            ctypes.windll.user32.GetClassNameW(hwnd, class_name, 256)
            
            # 查找微信窗口
            if "WeChat" in class_name.value or "微信" in window_text.value:
                print(f"\n[找到] 微信窗口")
                print(f"       句柄：{hwnd}")
                print(f"       标题：{window_text.value}")
                
                # 获取窗口位置
                rect = ctypes.wintypes.RECT()
                ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
                
                # 检查窗口是否最小化
                if rect.left == 0 and rect.top == 0 and rect.right == 0 and rect.bottom == 0:
                    print("       [恢复窗口]")
                    ctypes.windll.user32.ShowWindow(hwnd, 9)
                    time.sleep(0.5)
                    # 重新获取位置
                    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
                
                width = rect.right - rect.left
                height = rect.bottom - rect.top
                
                print(f"       位置：({rect.left}, {rect.top}) - ({rect.right}, {rect.bottom})")
                print(f"       大小：{width} x {height}")
                
                # 激活窗口
                ctypes.windll.user32.SetForegroundWindow(hwnd)
                time.sleep(0.3)
                
                # 计算按钮位置（窗口 70% 处）
                center_x = (rect.left + rect.right) // 2
                button_y = rect.top + int(height * 0.70)
                
                print(f"\n[点击] 按钮位置：({center_x}, {button_y})")
                
                ctypes.windll.user32.SetCursorPos(center_x, button_y)
                time.sleep(0.2)
                pyautogui.click()
                
                found_window = True
                return False
        
        return True
    
    # 枚举所有窗口
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(callback), 0)
    
    if found_window:
        print("\n" + "=" * 60)
        print("✅ 已完成！微信应该已登录")
        print("=" * 60)
        return True
    else:
        print("\n" + "=" * 60)
        print("❌ 未找到微信窗口")
        print("[提示] 微信可能未运行，正在启动...")
        print("=" * 60)
        
        # 启动微信
        import subprocess
        subprocess.Popen("start wechat:", shell=True)
        time.sleep(3)
        
        # 再试一次
        print("\n[重试] 再次查找微信窗口...")
        EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(callback), 0)
        
        if found_window:
            return True
        else:
            print("\n[失败] 仍然未找到微信窗口，请手动检查")
            return False

if __name__ == "__main__":
    find_and_click_wechat()
