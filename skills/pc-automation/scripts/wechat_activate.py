#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
激活微信窗口（任意微信相关窗口）
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
import ctypes
import pyautogui

def main():
    print("=" * 60)
    print("激活微信窗口")
    print("=" * 60)
    
    found = False
    
    def callback(hwnd, lparam):
        nonlocal found
        if ctypes.windll.user32.IsWindowVisible(hwnd):
            window_text = ctypes.create_unicode_buffer(256)
            ctypes.windll.user32.GetWindowTextW(hwnd, window_text, 256)
            class_name = ctypes.create_unicode_buffer(256)
            ctypes.windll.user32.GetClassNameW(hwnd, class_name, 256)
            
            # 查找微信窗口（包括无标题的）
            if "WeChat" in class_name.value or "微信" in window_text.value or "WeChat" in window_text.value:
                print(f"\n[找到] 窗口句柄：{hwnd}")
                print(f"       标题：{window_text.value}")
                print(f"       类名：{class_name.value}")
                
                # 获取窗口位置
                rect = ctypes.wintypes.RECT()
                ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
                
                if rect.left == 0 and rect.top == 0 and rect.right == 0 and rect.bottom == 0:
                    print("       [窗口最小化，尝试恢复]")
                    ctypes.windll.user32.ShowWindow(hwnd, 9)  # SW_RESTORE
                else:
                    print(f"       位置：({rect.left}, {rect.top}) - ({rect.right}, {rect.bottom})")
                    
                    # 激活窗口
                    ctypes.windll.user32.SetForegroundWindow(hwnd)
                    time.sleep(0.5)
                    
                    # 如果有标题，计算按钮位置
                    if rect.right > rect.left and rect.bottom > rect.top:
                        width = rect.right - rect.left
                        height = rect.bottom - rect.top
                        
                        if width > 100 and height > 100:  # 确保是主窗口
                            center_x = (rect.left + rect.right) // 2
                            button_y = rect.top + int(height * 0.70)
                            print(f"       [点击] ({center_x}, {button_y})")
                            
                            ctypes.windll.user32.SetCursorPos(center_x, button_y)
                            time.sleep(0.2)
                            pyautogui.click()
                            found = True
                            return False
                
                found = True
                return False
        return True
    
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(callback), 0)
    
    if not found:
        print("\n[未找到] 没有找到可见的微信窗口")
        print("[提示] 微信可能在后台运行，尝试重启微信...")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
