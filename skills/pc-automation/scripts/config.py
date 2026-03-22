# PC Automation - 配置和开关管理

import json
import os
from datetime import datetime
from pathlib import Path

# 配置文件路径
CONFIG_PATH = Path.home() / ".pc_automation_config.json"
LOG_PATH = Path.home() / ".pc_automation.log"

# 默认配置
DEFAULT_CONFIG = {
    "enabled": False,
    "require_confirmation": True,
    "max_clicks_per_run": 100,
    "max_keys_per_run": 500,
    "blocked_actions": ["delete", "format", "shutdown", "sudo", "rm -rf"],
    "timeout_minutes": 30,  # 自动关闭超时
    "log_file": str(LOG_PATH),
    "safe_mode": True,  # 安全模式：执行前显示预览
}

def get_config():
    """读取配置"""
    if not CONFIG_PATH.exists():
        # 创建默认配置
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Failed to read config: {e}")
        return DEFAULT_CONFIG.copy()

def save_config(config):
    """保存配置"""
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def is_enabled():
    """检查自动化是否开启"""
    config = get_config()
    
    # 检查超时
    if config.get("enabled"):
        enabled_at = config.get("enabled_at")
        timeout = config.get("timeout_minutes", 30)
        
        if enabled_at:
            enabled_time = datetime.fromisoformat(enabled_at)
            elapsed = (datetime.now() - enabled_time).total_seconds() / 60
            
            if elapsed > timeout:
                print(f"⏰ 自动化已超时（{timeout}分钟），自动关闭")
                disable()
                return False
    
    return config.get("enabled", False)

def enable(timeout_minutes=30):
    """Enable automation"""
    config = get_config()
    config["enabled"] = True
    config["enabled_at"] = datetime.now().isoformat()
    config["timeout_minutes"] = timeout_minutes
    save_config(config)
    
    print(f"[OK] Automation enabled")
    print(f"[INFO] Will auto-disable in {timeout_minutes} minutes")
    print(f"[INFO] Press Esc to interrupt")
    return True

def disable():
    """Disable automation"""
    config = get_config()
    config["enabled"] = False
    config["enabled_at"] = None
    save_config(config)
    
    print("[OK] Automation disabled")
    return True

def get_status():
    """Get status"""
    config = get_config()
    
    if not config.get("enabled"):
        return "[DISABLED] Automation is off"
    
    enabled_at = config.get("enabled_at")
    timeout = config.get("timeout_minutes", 30)
    
    if enabled_at:
        enabled_time = datetime.fromisoformat(enabled_at)
        elapsed = (datetime.now() - enabled_time).total_seconds() / 60
        remaining = max(0, timeout - elapsed)
        
        return f"[ENABLED] Automation is on ({remaining:.1f} min remaining)"
    
    return "[ENABLED] Automation is on"

def log_action(action_type, details):
    """记录操作日志"""
    config = get_config()
    log_file = Path(config.get("log_file", LOG_PATH))
    
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "action": action_type,
        "details": str(details)
    }
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

def is_blocked(action):
    """检查操作是否被禁止"""
    config = get_config()
    blocked = config.get("blocked_actions", [])
    return action.lower() in [b.lower() for b in blocked]

def confirm_action(preview_text):
    """确认操作"""
    config = get_config()
    
    if not config.get("require_confirmation", True):
        return True
    
    print("\n📋 操作预览:")
    print(preview_text)
    print()
    
    confirm = input("确认执行？(y/n): ")
    return confirm.lower() == 'y'

# 安全提示
SAFE_MODE_WARNING = """
⚠️ 安全模式已启用
- 所有操作将被记录
- 危险操作将被阻止
- 按 Esc 可随时中断
"""
