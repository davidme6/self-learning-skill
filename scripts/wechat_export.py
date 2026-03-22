#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""微信聊天记录导出"""

import pyautogui
import pyperclip
import time
import re
import winsound
from datetime import datetime
from pathlib import Path

OUTPUT_FILE = Path("C:/Windows/system32/UsersAdministrator.openclawworkspace/chat_export.txt")
MAX_SCROLLS = 200

def beep(times=1):
    """发出声音提示"""
    for _ in range(times):
        winsound.Beep(1000, 300)  # 频率1000Hz，持续300ms
        time.sleep(0.2)

def mask(text):
    text = re.sub(r'1[3-9]\d{9}', lambda m: m.group()[:3]+'****'+m.group()[-2:], text)
    text = re.sub(r'\d{17}[\dXx]', lambda m: m.group()[:6]+'********'+m.group()[-4:], text)
    return text

pyautogui.FAILSAFE = True

print("=" * 50)
print("微信聊天记录自动导出工具")
print("=" * 50)
print()
print("步骤：")
print("1. 打开微信 PC 版")
print("2. 打开对象的聊天窗口")
print("3. 把聊天窗口最大化")
print("4. 用鼠标点击一下聊天区域")
print()
print("终止：把鼠标移到左上角")
print()

input("准备好了按 Enter...")

# 开始提示 - 2声
print()
print("🔔 开始导出...")
beep(2)

all_lines = set()
last_hash = ""
no_new = 0

for i in range(MAX_SCROLLS):
    screen_width, screen_height = pyautogui.size()
    pyautogui.click(screen_width // 4, screen_height // 2)
    time.sleep(0.2)
    
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.3)
    
    try:
        content = pyperclip.paste()
    except:
        content = ""
    
    content_hash = str(hash(content))
    if content_hash != last_hash:
        lines = [l.strip() for l in content.split('\n') if l.strip()]
        new_count = 0
        for line in lines:
            if line not in all_lines:
                all_lines.add(line)
                new_count += 1
        
        if new_count > 0:
            print(f"\r滚动 {i+1} 次 - 新增 {new_count} 行 (共 {len(all_lines)} 行)", end="", flush=True)
            no_new = 0
        else:
            no_new += 1
    else:
        no_new += 1
    
    last_hash = content_hash
    
    if no_new >= 15:
        print()
        print("到达顶部")
        break
    
    pyautogui.scroll(300)
    time.sleep(0.4)

# 结束提示 - 3声
beep(3)
print()
print("🔔 导出结束")

if all_lines:
    text = mask('\n'.join(sorted(all_lines)))
    header = f"# 微信聊天记录\n# 时间: {datetime.now()}\n# 行数: {len(all_lines)}\n\n"
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(header + text)
    
    print("=" * 50)
    print(f"✅ 完成！文件: {OUTPUT_FILE}")
    print(f"共 {len(all_lines)} 行")
    print("=" * 50)
else:
    print("❌ 没有导出内容，请检查聊天窗口")

input("\n按 Enter 退出...")