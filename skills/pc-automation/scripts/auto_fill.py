# 自动填表模板脚本

import sys
import time
from pathlib import Path

script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from config import is_enabled, enable, disable, log_action, confirm_action

def auto_fill_form(form_data):
    """
    自动填写表单
    
    Args:
        form_data: dict, 表单数据
            {
                "fields": [
                    {"type": "click", "x": 100, "y": 200},
                    {"type": "type", "text": "张三"},
                    {"type": "click", "x": 300, "y": 400},
                    {"type": "type", "text": "zhangsan@example.com"},
                ]
            }
    """
    
    if not is_enabled():
        print("❌ 自动化未开启")
        print("💡 请先执行：/pc-auto enable")
        return False
    
    try:
        import pyautogui
    except ImportError:
        print("⚠️ pyautogui 未安装，运行：pip install pyautogui")
        return False
    
    # 生成预览
    preview_lines = ["即将执行的操作:"]
    for i, action in enumerate(form_data.get("fields", []), 1):
        if action["type"] == "click":
            preview_lines.append(f"  {i}. 点击坐标 ({action['x']}, {action['y']})")
        elif action["type"] == "type":
            preview_lines.append(f"  {i}. 输入文本：{action['text'][:30]}...")
        elif action["type"] == "press":
            preview_lines.append(f"  {i}. 按键：{action['key']}")
    
    preview = "\n".join(preview_lines)
    
    if not confirm_action(preview):
        print("❌ 已取消")
        return False
    
    # 执行操作
    print("\n🚀 开始执行...")
    
    for i, action in enumerate(form_data.get("fields", []), 1):
        try:
            if action["type"] == "click":
                pyautogui.click(action["x"], action["y"])
                log_action("click", (action["x"], action["y"]))
                print(f"  ✅ {i}. 点击 ({action['x']}, {action['y']})")
            
            elif action["type"] == "type":
                pyautogui.write(action["text"], interval=0.05)
                log_action("type", action["text"])
                print(f"  ✅ {i}. 输入完成")
            
            elif action["type"] == "press":
                pyautogui.press(action["key"])
                log_action("press", action["key"])
                print(f"  ✅ {i}. 按下 {action['key']}")
            
            time.sleep(0.3)
            
        except Exception as e:
            print(f"  ❌ 步骤 {i} 失败：{e}")
            break
    
    print("\n✅ 执行完成")
    return True

def main():
    # 示例：填写一个简单的表单
    example_form = {
        "fields": [
            {"type": "click", "x": 500, "y": 300},  # 点击姓名输入框
            {"type": "type", "text": "张三"},
            {"type": "press", "key": "tab"},
            {"type": "type", "text": "zhangsan@example.com"},
            {"type": "press", "key": "tab"},
            {"type": "type", "text": "13800138000"},
            {"type": "click", "x": 500, "y": 500},  # 点击提交按钮
        ]
    }
    
    print("📋 自动填表示例")
    print("⚠️ 这是一个示例，实际使用前请修改坐标！")
    print()
    
    # 开启自动化
    if not is_enabled():
        print("开启自动化...")
        enable(timeout_minutes=10)
    
    # 执行
    auto_fill_form(example_form)
    
    # 关闭
    print("\n关闭自动化...")
    disable()

if __name__ == "__main__":
    main()
