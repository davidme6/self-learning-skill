# 安全测试脚本 - 测试自动化控制是否正常工作

import sys
import time
from pathlib import Path

# 添加脚本目录到路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from config import is_enabled, enable, disable, get_status, log_action, confirm_action

def test_status():
    """测试状态检查"""
    print("📊 测试 1: 检查状态")
    print(get_status())
    print()

def test_enable_disable():
    """测试开关"""
    print("📊 测试 2: 开关测试")
    
    print("开启自动化...")
    enable(timeout_minutes=5)
    print(f"状态：{get_status()}")
    
    time.sleep(1)
    
    print("\n关闭自动化...")
    disable()
    print(f"状态：{get_status()}")
    print()

def test_safe_move():
    """测试安全移动（只移动鼠标，不点击）"""
    print("📊 测试 3: 安全移动测试")
    
    if not is_enabled():
        print("❌ 自动化未开启，先开启")
        enable(timeout_minutes=5)
    
    try:
        import pyautogui
        
        # 获取屏幕尺寸
        screen_width, screen_height = pyautogui.size()
        
        print(f"屏幕分辨率：{screen_width}x{screen_height}")
        print("鼠标将在屏幕四个角移动（不点击）...")
        
        # 预览
        preview = f"""
即将执行:
  1. 移动到左上角 (50, 50)
  2. 移动到右上角 ({screen_width-50}, 50)
  3. 移动到右下角 ({screen_width-50}, {screen_height-50})
  4. 移动到左下角 (50, {screen_height-50})
  5. 回到中心 ({screen_width//2}, {screen_height//2})
"""
        
        if not confirm_action(preview):
            print("❌ 已取消")
            return
        
        # 执行
        positions = [
            (50, 50),
            (screen_width - 50, 50),
            (screen_width - 50, screen_height - 50),
            (50, screen_height - 50),
            (screen_width // 2, screen_height // 2),
        ]
        
        for i, pos in enumerate(positions, 1):
            print(f"  {i}. 移动到 {pos}")
            pyautogui.moveTo(pos[0], pos[1], duration=0.5)
            log_action("move", pos)
            time.sleep(0.3)
        
        print("✅ 测试完成")
        
    except ImportError:
        print("⚠️ pyautogui 未安装，运行：pip install pyautogui")
    except Exception as e:
        print(f"❌ 测试失败：{e}")
    
    print()

def test_safe_type():
    """测试安全输入"""
    print("📊 测试 4: 安全输入测试")
    
    if not is_enabled():
        print("❌ 自动化未开启")
        return
    
    try:
        import pyautogui
        
        preview = """
即将执行:
  1. 输入测试文本："Hello, 贾维斯！"
  2. 按 Enter 键
"""
        
        if not confirm_action(preview):
            print("❌ 已取消")
            return
        
        print("⚠️ 请确保光标在安全位置（如记事本）")
        time.sleep(3)
        
        pyautogui.write("Hello, 贾维斯！", interval=0.1)
        log_action("type", "Hello, 贾维斯！")
        
        pyautogui.press('enter')
        log_action("key", "enter")
        
        print("✅ 输入完成")
        
    except ImportError:
        print("⚠️ pyautogui 未安装")
    except Exception as e:
        print(f"❌ 测试失败：{e}")
    
    print()

def main():
    print("=" * 50)
    print("🤖 PC Automation - 安全测试")
    print("=" * 50)
    print()
    
    test_status()
    test_enable_disable()
    test_safe_move()
    # test_safe_type()  # 需要用户手动确认，可选
    
    print("=" * 50)
    print("✅ 所有测试完成")
    print("=" * 50)
    print()
    print("📝 日志文件位置：~/.pc_automation.log")
    print("⚙️ 配置文件位置：~/.pc_automation_config.json")
    print()

if __name__ == "__main__":
    main()
