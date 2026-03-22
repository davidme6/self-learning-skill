#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeChat UI Automation V3 - 最终改进版
使用更可靠的窗口操作和中文输入
"""

import sys
import time
import pyautogui
import pygetwindow as gw
import pyperclip
import keyboard  # 更可靠的键盘模拟

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pyautogui.PAUSE = 0.3
pyautogui.FAILSAFE = True


class WeChatAutomationV3:
    """微信 UI 自动化 V3"""
    
    def __init__(self):
        self.wechat_window = None
    
    def find_wechat_window(self):
        """查找微信窗口"""
        print("[INFO] 正在查找微信窗口...")
        
        windows = gw.getWindowsWithTitle('微信')
        if windows:
            self.wechat_window = windows[0]
            print(f"[OK] 找到微信窗口：{self.wechat_window.title}")
            return True
        
        print("[ERROR] 未找到微信窗口")
        return False
    
    def activate_wechat(self):
        """激活微信窗口"""
        if not self.wechat_window:
            return False
        
        try:
            # 最小化再恢复以确保窗口在前台
            if hasattr(self.wechat_window, 'minimize'):
                self.wechat_window.minimize()
                time.sleep(0.3)
            
            if hasattr(self.wechat_window, 'restore'):
                self.wechat_window.restore()
            elif hasattr(self.wechat_window, 'activate'):
                self.wechat_window.activate()
            
            # 点击窗口中心确保焦点
            center_x = self.wechat_window.left + self.wechat_window.width // 2
            center_y = self.wechat_window.top + 70  # 稍微偏上，避免点到消息区域
            pyautogui.click(center_x, center_y)
            
            time.sleep(0.5)
            print("[OK] 微信窗口已激活")
            return True
        except Exception as e:
            print(f"[ERROR] 激活失败：{e}")
            return False
    
    def send_to_contact(self, contact_name, message):
        """发送消息给联系人"""
        print(f"\n{'='*60}")
        print(f"[START] 发送消息")
        print(f"  联系人：{contact_name}")
        print(f"  消息：{message}")
        print(f"{'='*60}\n")
        
        # 步骤 1: 查找并激活微信
        if not self.find_wechat_window():
            return False
        
        if not self.activate_wechat():
            return False
        
        time.sleep(1)
        
        # 步骤 2: 按 Esc 确保在聊天列表
        print("[ACTION] 返回聊天列表...")
        keyboard.press_and_release('esc')
        time.sleep(0.5)
        
        # 步骤 3: Ctrl+F 聚焦搜索框
        print("[ACTION] 打开搜索 (Ctrl+F)...")
        keyboard.press_and_release('ctrl+f')
        time.sleep(0.5)
        
        # 步骤 4: 输入联系人名字
        print(f"[ACTION] 搜索联系人：{contact_name}...")
        keyboard.press_and_release('ctrl+a')
        time.sleep(0.2)
        keyboard.press_and_release('delete')
        time.sleep(0.2)
        
        pyperclip.copy(contact_name)
        keyboard.press_and_release('ctrl+v')
        time.sleep(1.5)
        
        # 步骤 5: 选择第一个搜索结果 - 改进版
        print("[ACTION] 选择联系人...")
        
        # 多按几次 down 确保选中（微信搜索结果可能需要）
        for i in range(2):
            keyboard.press_and_release('down')
            time.sleep(0.2)
        
        # 按回车进入聊天窗口
        keyboard.press_and_release('enter')
        time.sleep(1.5)  # 多等一会儿，确保聊天窗口加载
        
        # 步骤 6: 确认在聊天窗口 - 按 Esc 测试（在聊天窗口会返回聊天列表）
        # 我们先不按，直接发送
        
        # 步骤 7: 输入并发送消息
        print("[ACTION] 输入消息...")
        pyperclip.copy(message)
        time.sleep(0.3)
        keyboard.press_and_release('ctrl+v')
        time.sleep(0.5)
        
        print("[ACTION] 发送消息...")
        keyboard.press_and_release('enter')
        time.sleep(0.5)
        
        print(f"\n{'='*60}")
        print("[SUCCESS] 消息发送完成！")
        print(f"{'='*60}\n")
        
        return True


def main():
    if len(sys.argv) < 3:
        print("用法：python wechat_ui_auto_v3.py <联系人> <消息>")
        sys.exit(1)
    
    contact = sys.argv[1]
    message = sys.argv[2] if len(sys.argv) == 3 else " ".join(sys.argv[2:])
    
    bot = WeChatAutomationV3()
    success = bot.send_to_contact(contact, message)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
