#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
激活微信窗口并带到前台
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
from pywinauto import Application
from pywinauto.findwindows import find_window

def main():
    print("[1/3] 查找微信窗口...")
    
    # 尝试多种方式找到微信窗口
    try:
        # 方式 1：通过进程连接
        app = Application().connect(path="WeChat.exe", timeout=5)
        print("[2/3] 找到微信进程！")
        
        # 获取主窗口
        window = app.window()
        
        # 激活窗口
        print("[3/3] 激活微信窗口...")
        window.set_focus()
        window.set_active()
        
        # 如果最小化了，恢复
        try:
            window.restore()
        except:
            pass
        
        print("=" * 60)
        print("[成功] 微信窗口已激活！")
        print("[提示] 微信应该现在显示在屏幕上了")
        print("=" * 60)
        
    except Exception as e:
        print(f"[错误] {e}")
        print("[提示] 尝试其他方式...")
        
        # 方式 2：使用 Windows API
        import ctypes
        user32 = ctypes.windll.user32
        
        # 枚举所有窗口找微信
        def callback(hwnd, lparam):
            if ctypes.windll.user32.IsWindowVisible(hwnd):
                window_text = ctypes.create_unicode_buffer(256)
                ctypes.windll.user32.GetWindowTextW(hwnd, window_text, 256)
                if "微信" in window_text.value or "WeChat" in window_text.value:
                    print(f"[找到] 窗口标题：{window_text.value}")
                    # 激活窗口
                    ctypes.windll.user32.SetForegroundWindow(hwnd)
                    return False
            return True
        
        ctypes.windll.user32.EnumWindows(callback, 0)
        print("[完成] 已尝试激活微信窗口")

if __name__ == "__main__":
    main()
