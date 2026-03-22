#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信最终版 - 修复所有问题
"""

import sys
import time
import pyautogui
import pyperclip

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pyautogui.PAUSE = 0.3
pyautogui.FAILSAFE = True


def send_to_contact(contact_name, message):
    print(f"\n{'='*60}")
    print(f"发送：{message}")
    print(f"给：{contact_name}")
    print(f"{'='*60}\n")
    
    # 1. 多次按 Esc 确保在聊天列表
    print("[1] 返回聊天列表...")
    for i in range(5):
        pyautogui.press('esc')
        time.sleep(0.2)
    time.sleep(0.5)
    
    # 2. Ctrl+F 搜索
    print("[2] 打开搜索...")
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
    time.sleep(1.5)
    
    # 5. 选择第一个搜索结果
    print("[5] 选择联系人...")
    # 按 down 箭头选中第一个结果
    pyautogui.press('down')
    time.sleep(0.3)
    # 按回车进入聊天
    pyautogui.press('enter')
    time.sleep(1.5)
    
    # 6. 确认在聊天窗口 - 再按一次回车（如果还在搜索会关闭搜索）
    pyautogui.press('enter')
    time.sleep(0.5)
    
    # 7. 输入消息
    print(f"[6] 输入消息...")
    pyperclip.copy(message)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    
    # 8. 发送
    print("[7] 发送...")
    pyautogui.press('enter')
    time.sleep(0.5)
    
    print(f"\n[OK] 完成！\n")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法：python wechat_final.py <联系人> <消息>")
        sys.exit(1)
    
    contact = sys.argv[1]
    # 修复：跳过脚本路径，只取参数
    message = sys.argv[2] if len(sys.argv) == 3 else " ".join(sys.argv[2:])
    
    success = send_to_contact(contact, message)
    sys.exit(0 if success else 1)
