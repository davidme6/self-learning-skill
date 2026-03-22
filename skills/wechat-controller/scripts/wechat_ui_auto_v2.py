#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeChat UI Automation V2 - 改进版
使用剪贴板 + 键盘操作，更可靠地发送中文消息
"""

import os
import sys
import time
import pyautogui
import pygetwindow as gw
import pyperclip  # 剪贴板库，支持中文

# 修复 Windows 编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# PyAutoGUI 配置
pyautogui.PAUSE = 0.3
pyautogui.FAILSAFE = True


class WeChatAutomationV2:
    """微信 UI 自动化 V2 - 使用剪贴板发送中文"""
    
    def __init__(self):
        self.wechat_window = None
    
    def find_wechat_window(self):
        """查找微信窗口"""
        print("[INFO] 正在查找微信窗口...")
        
        windows = gw.getWindowsWithTitle('微信')
        if windows:
            self.wechat_window = windows[0]
            print(f"[OK] 找到微信窗口：{self.wechat_window.title}")
            print(f"     位置：({self.wechat_window.left}, {self.wechat_window.top})")
            print(f"     大小：{self.wechat_window.width} x {self.wechat_window.height}")
            return True
        
        print("[ERROR] 未找到微信窗口")
        return False
    
    def activate_wechat(self):
        """激活微信窗口"""
        if not self.wechat_window:
            return False
        
        try:
            # 恢复并激活窗口
            if hasattr(self.wechat_window, 'isMinimized') and self.wechat_window.isMinimized:
                self.wechat_window.restore()
            
            # 尝试不同的激活方法
            if hasattr(self.wechat_window, 'activate'):
                self.wechat_window.activate()
            elif hasattr(self.wechat_window, 'set_focus'):
                self.wechat_window.set_focus()
            else:
                # 备用方案：点击窗口中心
                center_x = self.wechat_window.left + self.wechat_window.width // 2
                center_y = self.wechat_window.top + self.wechat_window.height // 2
                pyautogui.click(center_x, center_y)
            
            time.sleep(0.5)
            print("[OK] 微信窗口已激活")
            return True
        except Exception as e:
            print(f"[ERROR] 激活失败：{e}")
            return False
    
    def send_to_contact(self, contact_name, message):
        """发送消息给联系人（使用剪贴板粘贴中文）"""
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
        
        # 步骤 2: 确保在聊天列表（按 Esc 退出任何当前对话）
        print("[ACTION] 返回聊天列表...")
        pyautogui.press('esc')
        time.sleep(0.5)
        
        # 步骤 3: 聚焦搜索框 (Ctrl+F)
        print(f"[ACTION] 打开搜索 (Ctrl+F)...")
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.5)
        
        # 步骤 4: 清空搜索框并输入联系人名字（使用剪贴板）
        print(f"[ACTION] 搜索联系人：{contact_name}...")
        pyautogui.hotkey('ctrl', 'a')  # 全选
        time.sleep(0.2)
        pyautogui.press('delete')
        time.sleep(0.2)
        
        # 使用剪贴板粘贴中文（更可靠）
        pyperclip.copy(contact_name)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1.5)  # 等待搜索结果
        
        # 步骤 5: 选择第一个搜索结果
        print("[ACTION] 选择联系人...")
        pyautogui.press('down')  # 向下选择第一个结果
        time.sleep(0.3)
        pyautogui.press('enter')  # 确认选择
        time.sleep(1.0)  # 等待聊天窗口加载
        
        # 步骤 6: 聚焦到消息输入框 - 改进版
        print("[ACTION] 聚焦输入框...")
        
        # 方法 1：直接按 Ctrl+V 粘贴（微信会自动聚焦到输入框）
        # 先复制消息到剪贴板
        pyperclip.copy(message)
        time.sleep(0.3)
        
        # 直接粘贴 - 微信在聊天窗口时会自动聚焦到输入框
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        
        # 步骤 7: 发送消息（按回车）
        print("[ACTION] 发送消息...")
        pyautogui.press('enter')
        time.sleep(0.5)
        
        print(f"\n{'='*60}")
        print("[SUCCESS] 消息发送完成！")
        print(f"{'='*60}\n")
        
        return True


def main():
    if len(sys.argv) < 3:
        print("用法：python wechat_ui_auto_v2.py <联系人> <消息>")
        print("\n示例:")
        print('  python wechat_ui_auto_v2.py "马嘉欣" "你好"')
        sys.exit(1)
    
    contact = sys.argv[1]
    message = sys.argv[2] if len(sys.argv) == 3 else " ".join(sys.argv[2:])
    
    bot = WeChatAutomationV2()
    success = bot.send_to_contact(contact, message)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
