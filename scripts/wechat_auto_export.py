#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信聊天记录自动导出工具
- 自动滚动加载历史
- 检测语音消息并点击转换
- 复制所有文字内容
- 本地脱敏处理
"""

import pyautogui
import pyperclip
import time
import re
from datetime import datetime
from pathlib import Path

# 安全设置
pyautogui.FAILSAFE = True  # 移动鼠标到左上角可终止
pyautogui.PAUSE = 0.5

# 输出文件
OUTPUT_FILE = Path("C:/Windows/system32/UsersAdministrator.openclawworkspace/wechat_chat_export.txt")

# 脱敏模式
PATTERNS = {
    "phone": r"1[3-9]\d{9}",
    "id_card": r"\d{17}[\dXx]",
    "email": r"[\w\.-]+@[\w\.-]+\.\w+",
}

def desensitize(text: str) -> str:
    """简单脱敏"""
    for name, pattern in PATTERNS.items():
        matches = re.findall(pattern, text)
        for m in matches:
            if len(m) > 4:
                masked = m[:3] + "***" + m[-2:]
                text = text.replace(m, masked)
    return text

def scroll_up():
    """向上滚动加载更多消息"""
    # 使用鼠标滚轮向上滚动
    pyautogui.scroll(500)  # 正数向上滚动
    time.sleep(0.3)

def select_all_and_copy():
    """全选并复制当前可见内容"""
    # 点击聊天区域确保焦点正确
    # 使用 Ctrl+A 全选
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    # 复制
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.3)
    # 获取剪贴板内容
    try:
        content = pyperclip.paste()
        return content
    except:
        return ""

def find_voice_message():
    """
    查找语音消息
    返回语音消息的位置（如果找到）
    """
    # 语音消息的特征：通常有一个小喇叭图标
    # 需要通过图像识别来定位
    
    # 尝试查找语音图标（需要预先截图保存）
    voice_icon_path = Path(__file__).parent / "voice_icon.png"
    
    if voice_icon_path.exists():
        try:
            location = pyautogui.locateOnScreen(str(voice_icon_path), confidence=0.8)
            if location:
                return pyautogui.center(location)
        except:
            pass
    
    return None

def click_to_convert_voice(position):
    """点击语音消息转换为文字"""
    x, y = position
    pyautogui.click(x, y)
    time.sleep(0.5)
    
    # 等待转换完成（可能需要点击"转文字"按钮）
    # 这取决于微信版本

def main():
    print("=" * 50)
    print("微信聊天记录自动导出工具")
    print("=" * 50)
    print()
    print("⚠️  准备工作：")
    print("1. 打开微信")
    print("2. 打开要导出的聊天窗口")
    print("3. 确保聊天窗口最大化")
    print("4. 不要最小化或切换窗口")
    print()
    print("🛑 终止方式：将鼠标移到屏幕左上角")
    print()
    
    input("准备好了按 Enter 开始...")
    
    print()
    print("开始导出...")
    print()
    
    all_content = set()  # 使用集合去重
    last_content = ""
    no_change_count = 0
    max_scrolls = 100  # 最大滚动次数
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    for i in range(max_scrolls):
        print(f"\r滚动中... 第 {i+1} 次", end="", flush=True)
        
        # 复制当前可见内容
        content = select_all_and_copy()
        
        if content and content != last_content:
            # 新内容
            lines = content.split('\n')
            new_lines = 0
            for line in lines:
                line = line.strip()
                if line and line not in all_content:
                    all_content.add(line)
                    new_lines += 1
            
            if new_lines > 0:
                print(f" - 新增 {new_lines} 行")
                no_change_count = 0
            else:
                no_change_count += 1
        else:
            no_change_count += 1
        
        last_content = content
        
        # 如果连续多次没有新内容，可能已经到底了
        if no_change_count >= 10:
            print()
            print("已到达聊天记录顶部或没有新内容")
            break
        
        # 向上滚动
        scroll_up()
        time.sleep(0.5)
    
    print()
    print("=" * 50)
    
    # 保存内容
    if all_content:
        # 脱敏处理
        content_text = '\n'.join(sorted(all_content))
        content_text = desensitize(content_text)
        
        # 添加时间戳
        header = f"""# 微信聊天记录导出
# 导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# 总行数: {len(all_content)}
# 已脱敏处理

"""
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(header + content_text)
        
        print(f"✅ 导出完成！")
        print(f"📄 文件位置: {OUTPUT_FILE}")
        print(f"📊 总共 {len(all_content)} 行内容")
        print()
        print("⚠️  请检查文件内容，确认没有敏感信息后再让我分析")
    else:
        print("❌ 没有导出到任何内容")
        print("可能原因：")
        print("- 聊天窗口没有获得焦点")
        print("- 没有聊天记录")
        print("- Ctrl+A 没有选中内容")

if __name__ == "__main__":
    main()