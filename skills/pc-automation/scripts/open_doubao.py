# 打开豆包网页并发送"你好"

import sys
import time
from pathlib import Path

script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from config import is_enabled, enable, disable, log_action, confirm_action

def open_doubao():
    """打开豆包网页并发送消息"""
    
    if not is_enabled():
        print("[ERROR] Automation is not enabled")
        print("[INFO] Run: pc-auto enable")
        return False
    
    try:
        import pyautogui
        import webbrowser
    except ImportError as e:
        print(f"[ERROR] Missing dependency: {e}")
        return False
    
    # 操作预览
    preview = """
Operations to execute:
  1. Open browser with Doubao website
  2. Wait for page to load
  3. Find and click input box
  4. Type "你好"
  5. Press Enter to send
"""
    
    print("\n[PREVIEW]")
    print(preview)
    
    confirm = input("Confirm execution? (y/n): ")
    if confirm.lower() != 'y':
        print("[CANCELLED]")
        return False
    
    print("\n[EXECUTING]")
    
    try:
        # 1. 打开豆包网页
        print("  1. Opening Doubao website...")
        webbrowser.open('https://www.doubao.com')
        log_action("open_url", "https://www.doubao.com")
        time.sleep(5)  # 等待页面加载
        
        # 2. 尝试找到输入框并点击（一般网页输入框在页面中下部）
        print("  2. Waiting for page to load...")
        time.sleep(3)
        
        # 3. 使用 Tab 键导航到输入框（通用方法）
        print("  3. Navigating to input box...")
        pyautogui.press('tab')
        time.sleep(0.5)
        log_action("key", "tab")
        
        # 4. 输入"你好"
        print('  4. Typing "你好"...')
        pyautogui.write("你好", interval=0.1)
        log_action("type", "你好")
        time.sleep(1)
        
        # 5. 按 Enter 发送
        print("  5. Sending message...")
        pyautogui.press('enter')
        log_action("key", "enter")
        
        print("\n[SUCCESS] Message sent!")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        return False
    
    finally:
        # 自动关闭
        print("\n[AUTO] Disabling automation...")
        disable()

if __name__ == "__main__":
    open_doubao()
