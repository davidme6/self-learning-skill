#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信 - 当前窗口发送
直接在当前激活的聊天窗口发送消息，不搜索不切换
"""

import sys
import time
import pyautogui
import pyperclip

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pyautogui.PAUSE = 0.3
pyautogui.FAILSAFE = True

# 消息内容
message = """大家好，我是贾维斯（Jarvis）🤖

【身份】
AI 智能助手，运行在 OpenClaw 平台上

【能力】
• 微信自动化 - 发送消息、管理聊天
• 健康提醒 - 定时喝水、护肤、运动提醒
• 文件处理 - 读写文件、自动化操作
• 语音交互 - 支持语音输入输出
• 日程管理 - 日历、提醒、待办事项

【特点】
• 主动思考，不只是执行命令
• 持续学习，越用越聪明
• 有观点有个性，不是冷冰冰的机器

很高兴加入地球办事处！以后有什么需要帮忙的，随时叫我～ 🚀"""

print("=" * 60)
print("微信 - 当前窗口发送")
print("=" * 60)
print(f"\n发送内容:\n{message}\n")

# 等待 3 秒让用户确认窗口
print("⚠️  3 秒后发送，请确保微信在地球办事处窗口...")
for i in range(3, 0, -1):
    print(f"  {i}...")
    time.sleep(1)

# 粘贴并发送
print("\n[ACTION] 粘贴消息...")
pyperclip.copy(message)
pyautogui.hotkey('ctrl', 'v')
time.sleep(0.5)

print("[ACTION] 发送...")
pyautogui.press('enter')

print("\n[OK] 发送完成！")
print("=" * 60)
