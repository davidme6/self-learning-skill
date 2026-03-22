#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeChat UI Automation - 微信界面自动化
功能：模拟鼠标键盘操作微信客户端，实现自动聊天
"""

import os
import sys
import time
import subprocess
import pyautogui
import pygetwindow as gw
from pathlib import Path

# uiautomation 作为可选依赖
try:
    import uiautomation as auto
    HAS_UIA = True
except ImportError:
    HAS_UIA = False

# 修复 Windows 命令行编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 禁用 pyautogui 的安全暂停（生产环境建议保留）
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True  # 鼠标移到屏幕角落可紧急停止


class WeChatAutomation:
    """微信 UI 自动化类"""
    
    def __init__(self):
        self.wechat_window = None
        self.search_box = None
        self.message_input = None
        
    def find_wechat_window(self):
        """查找微信窗口"""
        print("🔍 正在查找微信窗口...")
        
        # 方法 1：通过窗口标题查找
        windows = gw.getWindowsWithTitle('微信')
        if windows:
            self.wechat_window = windows[0]
            print(f"✓ 找到微信窗口：{self.wechat_window.title}")
            return True
        
        # 方法 2：通过 UI 自动化查找（如果可用）
        if HAS_UIA:
            control = auto.WindowControl(ClassName='WeChatMainWndForPC')
            if control.Exists(0, 1):
                self.wechat_window = control
                print("✓ 找到微信窗口（UI Automation）")
                return True
        
        print("❌ 未找到微信窗口，请先打开微信")
        return False
    
    def activate_wechat(self):
        """激活微信窗口"""
        if not self.wechat_window:
            return False
        
        try:
            # 恢复窗口（如果最小化）
            if hasattr(self.wechat_window, 'restore'):
                self.wechat_window.restore()
            
            # 激活窗口
            if hasattr(self.wechat_window, 'set_focus'):
                self.wechat_window.set_focus()
            else:
                self.wechat_window.activate()
            
            time.sleep(0.5)
            print("✓ 微信窗口已激活")
            return True
        except Exception as e:
            print(f"❌ 激活窗口失败：{e}")
            return False
    
    def search_contact(self, contact_name):
        """搜索联系人 - 改进版"""
        print(f"🔍 搜索联系人：{contact_name}")
        
        # 方法 1：先尝试点击搜索框（微信顶部搜索框）
        # 使用 Tab 键导航到搜索框
        for i in range(3):
            pyautogui.press('tab')
            time.sleep(0.2)
        
        # 方法 2：直接按 Ctrl+F 聚焦搜索框
        pyautogui.hotkey('ctrl', 'f', interval=0.3)
        time.sleep(0.5)
        
        # 清除现有内容（如果有）
        pyautogui.hotkey('ctrl', 'a', interval=0.2)
        time.sleep(0.2)
        
        # 输入联系人名字
        pyautogui.write(contact_name, interval=0.15)
        time.sleep(1.5)  # 等待搜索结果加载
        
        print(f"✓ 已搜索：{contact_name}")
        return True
    
    def select_first_contact(self):
        """选择搜索结果中的第一个联系人 - 改进版"""
        # 方法 1：按向下箭头选择第一个结果
        pyautogui.press('down')
        time.sleep(0.3)
        
        # 按回车确认选择
        pyautogui.press('enter')
        time.sleep(1.0)  # 等待聊天窗口加载
        
        print("✓ 已选择联系人")
        return True
    
    def send_message(self, message):
        """发送消息"""
        print(f"📤 发送消息：{message}")
        
        # 输入消息
        pyautogui.write(message, interval=0.05)
        time.sleep(0.3)
        
        # 按回车发送
        pyautogui.press('enter')
        time.sleep(0.5)
        
        print("✓ 消息已发送")
        return True
    
    def send_to_contact(self, contact_name, message):
        """完整流程：搜索联系人并发送消息 - 改进版"""
        print(f"\n{'='*50}")
        print(f"🚀 开始发送消息给：{contact_name}")
        print(f"{'='*50}\n")
        
        # 1. 查找微信窗口
        if not self.find_wechat_window():
            print("❌ 步骤 1 失败：未找到微信窗口")
            return False
        
        # 2. 激活窗口
        if not self.activate_wechat():
            print("❌ 步骤 2 失败：无法激活窗口")
            return False
        
        time.sleep(1)  # 等待窗口激活
        
        # 3. 聚焦到聊天列表（按 Esc 确保在聊天列表）
        pyautogui.press('esc')
        time.sleep(0.3)
        
        # 4. 搜索联系人
        if not self.search_contact(contact_name):
            print("❌ 步骤 4 失败：搜索失败")
            return False
        
        time.sleep(1)  # 等待搜索结果
        
        # 5. 选择联系人（向下箭头 + 回车）
        if not self.select_first_contact():
            print("❌ 步骤 5 失败：选择联系人失败")
            return False
        
        time.sleep(1)  # 等待聊天窗口加载
        
        # 6. 确认在聊天窗口（按 Tab 到输入框）
        for i in range(3):
            pyautogui.press('tab')
            time.sleep(0.2)
        
        # 7. 发送消息
        if not self.send_message(message):
            print("❌ 步骤 7 失败：发送消息失败")
            return False
        
        print(f"\n{'='*50}")
        print("✅ 完成！")
        print(f"{'='*50}\n")
        return True
    
    def test_ui(self):
        """测试 UI 自动化基础功能"""
        print("\n🧪 开始测试 UI 自动化...\n")
        
        # 测试 1：查找微信窗口
        print("测试 1: 查找微信窗口")
        if not self.find_wechat_window():
            print("❌ 测试失败：未找到微信窗口\n")
            return False
        print("✓ 测试通过\n")
        
        # 测试 2：激活窗口
        print("测试 2: 激活微信窗口")
        if not self.activate_wechat():
            print("❌ 测试失败：无法激活窗口\n")
            return False
        print("✓ 测试通过\n")
        
        print("✅ 所有基础测试通过！\n")
        return True


def main():
    if len(sys.argv) < 2:
        print("用法：python wechat_ui_auto.py <command> [args]")
        print("\n命令:")
        print("  test                    - 测试 UI 自动化")
        print("  send <联系人> <消息>     - 发送消息给联系人")
        print("  status                  - 检查微信状态")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    auto_bot = WeChatAutomation()
    
    if command == "test":
        success = auto_bot.test_ui()
        sys.exit(0 if success else 1)
    
    elif command == "send":
        if len(sys.argv) < 4:
            print("❌ 用法：python wechat_ui_auto.py send <联系人> <消息>")
            sys.exit(1)
        
        contact = sys.argv[2]
        message = " ".join(sys.argv[3:])
        success = auto_bot.send_to_contact(contact, message)
        sys.exit(0 if success else 1)
    
    elif command == "status":
        success = auto_bot.find_wechat_window()
        sys.exit(0 if success else 1)
    
    else:
        print(f"❌ 未知命令：{command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
