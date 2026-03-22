#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信自动化 - 鼠标点击版
搜索后用鼠标点击联系人，确保进入聊天窗口
"""

import sys
import time
import pyautogui
import pygetwindow as gw
import pyperclip

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pyautogui.PAUSE = 0.3
pyautogui.FAILSAFE = True


class WeChatClick:
    def __init__(self):
        self.wechat_window = None
    
    def find_and_activate(self):
        """找到并激活微信窗口"""
        windows = gw.getWindowsWithTitle('微信')
        if not windows:
            print("[ERROR] 未找到微信窗口")
            return False
        
        self.wechat_window = windows[0]
        print(f"[OK] 找到微信窗口")
        
        # 激活窗口
        if hasattr(self.wechat_window, 'activate'):
            self.wechat_window.activate()
        
        # 点击窗口确保焦点
        cx = self.wechat_window.left + self.wechat_window.width // 2
        cy = self.wechat_window.top + 100
        pyautogui.click(cx, cy)
        time.sleep(0.5)
        
        print("[OK] 窗口已激活")
        return True
    
    def send_to_contact(self, contact_name, message):
        """发送消息"""
        print(f"\n{'='*60}")
        print(f"发送：{message}")
        print(f"给：{contact_name}")
        print(f"{'='*60}\n")
        
        if not self.find_and_activate():
            return False
        
        # 按 Esc 返回聊天列表
        print("[1] 返回聊天列表...")
        pyautogui.press('esc')
        time.sleep(0.5)
        
        # Ctrl+F 搜索
        print("[2] 打开搜索...")
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.5)
        
        # 输入联系人名字
        print(f"[3] 搜索：{contact_name}...")
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyperclip.copy(contact_name)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1.5)
        
        # 点击搜索结果（搜索框下方约 120 像素）
        print("[4] 点击联系人...")
        search_box_x = self.wechat_window.left + 200
        search_box_y = self.wechat_window.top + 70
        
        # 搜索结果通常在搜索框下方
        click_x = search_box_x
        click_y = search_box_y + 100
        
        print(f"    点击位置：({click_x}, {click_y})")
        pyautogui.click(click_x, click_y)
        time.sleep(1.5)
        
        # 确认在聊天窗口后发送
        print("[5] 发送消息...")
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')
        
        print(f"\n[OK] 完成！\n")
        return True


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法：python wechat_click.py <联系人> <消息>")
        sys.exit(1)
    
    bot = WeChatClick()
    success = bot.send_to_contact(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)
