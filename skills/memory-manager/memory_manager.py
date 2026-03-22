#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆管理系统 - 反思 + 对话保存 + 记忆整理
"""

import sys
import io
import os
from datetime import datetime
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 工作区路径
WORKSPACE = r"C:\Windows\system32\UsersAdministrator.openclawworkspace"
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
MEMORY_MD = os.path.join(WORKSPACE, "MEMORY.md")

def get_today_file():
    """获取今天的记忆文件路径"""
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(MEMORY_DIR, f"{today}.md")

def ensure_memory_dir():
    """确保记忆目录存在"""
    if not os.path.exists(MEMORY_DIR):
        os.makedirs(MEMORY_DIR)

def save_conversation(topic, points, decisions=None, todos=None):
    """保存对话记录"""
    ensure_memory_dir()
    
    today_file = get_today_file()
    timestamp = datetime.now().strftime("%H:%M")
    
    content = f"\n## 💬 对话记录 - {timestamp}\n\n"
    content += f"**主题：** {topic}\n\n"
    content += "**要点：**\n"
    for point in points:
        content += f"- {point}\n"
    
    if decisions:
        content += f"\n**决策：** {decisions}\n"
    
    if todos:
        content += f"\n**待办：**\n"
        for todo in todos:
            content += f"- {todo}\n"
    
    content += "\n---\n"
    
    # 追加到文件
    with open(today_file, "a", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 对话已保存：{today_file}")

def daily_reflection(reflection_type="morning"):
    """每日反思"""
    ensure_memory_dir()
    
    today_file = get_today_file()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    reflections = {
        "morning": "早晨",
        "afternoon": "下午",
        "evening": "晚上"
    }
    
    reflection_name = reflections.get(reflection_type, reflection_type)
    
    content = f"\n## 🤔 反思 - {reflection_name} ({timestamp})\n\n"
    content += "### 1. 做得好的\n"
    content += "- [待填写]\n\n"
    content += "### 2. 可以改进的\n"
    content += "- [待填写]\n\n"
    content += "### 3. 学到的新东西\n"
    content += "- [待填写]\n\n"
    content += "### 4. 用户偏好更新\n"
    content += "- [待填写]\n\n"
    content += "### 5. 后续行动\n"
    content += "- [待填写]\n\n"
    content += "---\n"
    
    with open(today_file, "a", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 反思模板已创建：{today_file}")
    print(f"📝 类型：{reflection_name}")

def organize_memory():
    """整理 MEMORY.md"""
    print("📚 开始整理 MEMORY.md...")
    
    # 读取今天的记忆
    today_file = get_today_file()
    if not os.path.exists(today_file):
        print("⚠️ 今天的记忆文件不存在")
        return
    
    with open(today_file, "r", encoding="utf-8") as f:
        today_content = f.read()
    
    # 提取关键信息（简化版，实际应该用 AI 分析）
    key_points = []
    if "决策：" in today_content:
        for line in today_content.split("\n"):
            if "决策：" in line:
                key_points.append(line.strip())
    
    if "用户偏好" in today_content:
        for line in today_content.split("\n"):
            if "用户偏好" in line:
                key_points.append(line.strip())
    
    print(f"📋 提取到 {len(key_points)} 个关键点")
    
    # 更新 MEMORY.md（简化版）
    if os.path.exists(MEMORY_MD):
        with open(MEMORY_MD, "r", encoding="utf-8") as f:
            memory_content = f.read()
        
        # 检查是否已存在
        already_exists = True
        for point in key_points:
            if point not in memory_content:
                already_exists = False
                break
        
        if not already_exists:
            # 追加新内容
            update_section = f"\n## 📅 更新 - {datetime.now().strftime('%Y-%m-%d')}\n\n"
            for point in key_points:
                update_section += f"- {point}\n"
            
            with open(MEMORY_MD, "a", encoding="utf-8") as f:
                f.write(update_section)
            
            print("✅ MEMORY.md 已更新")
        else:
            print("ℹ️ 无新内容需要添加")
    else:
        # 创建新文件
        with open(MEMORY_MD, "w", encoding="utf-8") as f:
            f.write(f"# MEMORY.md - 长期记忆\n\n## 📅 创建于 {datetime.now().strftime('%Y-%m-%d')}\n\n")
        print("✅ MEMORY.md 已创建")

def cleanup_large_files(days=30):
    """清理大型文件（视频等），保留文字和图片"""
    print("🧹 开始清理大型文件...")
    
    media_dir = os.path.join(WORKSPACE, "media")
    if not os.path.exists(media_dir):
        print("ℹ️ 媒体目录不存在")
        return
    
    # 视频目录 - 月清理
    video_dir = os.path.join(media_dir, "videos")
    if os.path.exists(video_dir):
        cleanup_count = 0
        for filename in os.listdir(video_dir):
            filepath = os.path.join(video_dir, filename)
            # 检查文件修改时间
            mtime = os.path.getmtime(filepath)
            days_old = (datetime.now().timestamp() - mtime) / (24 * 3600)
            if days_old > days:
                os.remove(filepath)
                cleanup_count += 1
                print(f"  🗑️ 清理：{filename} ({days_old:.0f}天)")
        print(f"✅ 清理了 {cleanup_count} 个视频文件")
    
    # 图片目录 - 永久保存
    image_dir = os.path.join(media_dir, "images")
    if os.path.exists(image_dir):
        print(f"ℹ️ 图片目录保留，不清理")
    
    # 临时文件目录 - 月清理
    temp_dir = os.path.join(media_dir, "temp")
    if os.path.exists(temp_dir):
        cleanup_count = 0
        for filename in os.listdir(temp_dir):
            filepath = os.path.join(temp_dir, filename)
            mtime = os.path.getmtime(filepath)
            days_old = (datetime.now().timestamp() - mtime) / (24 * 3600)
            if days_old > days:
                os.remove(filepath)
                cleanup_count += 1
        print(f"✅ 清理了 {cleanup_count} 个临时文件")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python memory_manager.py [save|reflect|organize|cleanup]")
        print("  save      - 保存对话")
        print("  reflect   - 每日反思")
        print("  organize  - 整理记忆")
        print("  cleanup   - 清理大型文件（月清理）")
        return
    
    action = sys.argv[1]
    
    if action == "save":
        topic = sys.argv[2] if len(sys.argv) > 2 else "未命名对话"
        points = sys.argv[3:] if len(sys.argv) > 3 else ["待填写"]
        save_conversation(topic, points)
    
    elif action == "reflect":
        reflection_type = sys.argv[2] if len(sys.argv) > 2 else "evening"
        daily_reflection(reflection_type)
    
    elif action == "organize":
        organize_memory()
    
    elif action == "cleanup":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        cleanup_large_files(days)
    
    else:
        print(f"❌ 未知动作：{action}")

if __name__ == "__main__":
    main()
