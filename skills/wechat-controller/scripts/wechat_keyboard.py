#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信自动化 - 纯键盘版
只用键盘操作，避免鼠标点击位置问题
"""

import sys
import time
import pyautogui
import pyperclip

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pyautogui.PAUSE = 0.3
pyautogui.FAILSAFE = True


def send_message(contact_name, message):
    """纯键盘操作发送消息"""
    print(f"\n{'='*60}")
    print(f"发送：{message}")
    print(f"给：{contact_name}")
    print(f"{'='*60}\n")
    
    # 1. 按 Esc 确保在聊天列表
    print("[1] 返回聊天列表...")
    for i in range(3):
        pyautogui.press('esc')
        time.sleep(0.3)
    time.sleep(0.5)
    
    # 2. Ctrl+F 搜索
    print("[2] 打开搜索 (Ctrl+F)...")
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.5)
    
    # 3. 清空搜索框
    print("[3] 清空搜索框...")
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.press('delete')
    time.sleep(0.2)
    
    # 4. 输入联系人名字
    print(f"[4] 搜索：{contact_name}...")
    pyperclip.copy(contact_name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.5)  # 等待搜索结果
    
    # 5. 按回车选择第一个搜索结果并进入聊天
    print("[5] 选择联系人 (Enter)...")
    pyautogui.press('enter')
    time.sleep(1.5)  # 等待聊天窗口加载
    
    # 6. 再按一次回车确认（某些版本需要）
    pyautogui.press('enter')
    time.sleep(0.5)
    
    # 7. 输入消息
    print(f"[6] 输入消息...")
    pyperclip.copy(message)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    
    # 8. 发送
    print("[7] 发送 (Enter)...")
    pyautogui.press('enter')
    time.sleep(0.5)
    
    print(f"\n[OK] 完成！\n")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法：python wechat_keyboard.py <联系人> <消息>")
        sys.exit(1)
    
    success = send_message(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)
