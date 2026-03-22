#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeChat Controller - 微信控制脚本
功能：启动、关闭、检查微信运行状态
"""

import os
import sys
import json
import subprocess
import psutil
from pathlib import Path

# 修复 Windows 命令行编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 配置文件路径
CONFIG_FILE = Path.home() / ".wechat_controller_config.json"

# 常见微信安装路径
COMMON_PATHS = [
    r"C:\Program Files (x86)\Tencent\WeChat\WeChat.exe",
    r"C:\Program Files\Tencent\WeChat\WeChat.exe",
    r"C:\Users\{}\AppData\Local\Programs\Tencent\WeChat\WeChat.exe".format(os.getlogin() if hasattr(os, 'getlogin') else "Administrator"),
    os.path.expanduser(r"~\AppData\Local\Tencent\WeChat\WeChat.exe"),
    os.path.expanduser(r"~\AppData\Roaming\Tencent\WeChat\WeChat.exe"),
]


def load_config():
    """加载配置文件"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_config(config):
    """保存配置文件"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def find_wechat_path():
    """搜索微信安装路径"""
    config = load_config()
    
    # 先检查配置文件
    if config.get("wechat_path") and os.path.exists(config["wechat_path"]):
        return config["wechat_path"]
    
    # 检查常见路径
    for path in COMMON_PATHS:
        if os.path.exists(path):
            print(f"✓ 找到微信：{path}")
            save_config({"wechat_path": path})
            return path
    
    # 搜索整个系统（较慢）
    print("正在搜索微信安装位置...")
    search_paths = [
        r"C:\Program Files",
        r"C:\Program Files (x86)",
        os.path.expanduser(r"~\AppData\Local"),
        os.path.expanduser(r"~\AppData\Roaming"),
    ]
    
    for base_path in search_paths:
        if not os.path.exists(base_path):
            continue
        try:
            for root, dirs, files in os.walk(base_path):
                if "WeChat.exe" in files:
                    path = os.path.join(root, "WeChat.exe")
                    print(f"✓ 找到微信：{path}")
                    save_config({"wechat_path": path})
                    return path
        except (PermissionError, OSError):
            continue
    
    return None


def is_wechat_running():
    """检查微信是否正在运行"""
    for proc in psutil.process_iter(['name', 'pid']):
        try:
            if proc.info['name'] and 'WeChat.exe' in proc.info['name']:
                return True, proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False, None


def start_wechat():
    """启动微信"""
    wechat_path = find_wechat_path()
    
    if not wechat_path:
        print("❌ 未找到微信安装路径，请先安装微信")
        print("下载地址：https://weixin.qq.com/")
        return False
    
    # 检查是否已在运行
    running, pid = is_wechat_running()
    if running:
        print(f"ℹ️ 微信已在运行中 (PID: {pid})")
        return True
    
    # 启动微信
    try:
        subprocess.Popen([wechat_path], 
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        print("✓ 微信已启动")
        return True
    except Exception as e:
        print(f"❌ 启动失败：{e}")
        return False


def stop_wechat():
    """关闭微信"""
    running, pid = is_wechat_running()
    
    if not running:
        print("ℹ️ 微信未运行")
        return True
    
    try:
        # 先尝试优雅关闭
        proc = psutil.Process(pid)
        proc.terminate()
        
        # 等待进程结束
        try:
            proc.wait(timeout=5)
            print("✓ 微信已关闭")
            return True
        except psutil.TimeoutExpired:
            # 如果超时，强制结束
            proc.kill()
            print("✓ 微信已强制关闭")
            return True
    except psutil.NoSuchProcess:
        print("ℹ️ 微信已关闭")
        return True
    except Exception as e:
        # 备用方案：使用 taskkill
        try:
            subprocess.run(["taskkill", "/F", "/IM", "WeChat.exe"], 
                          capture_output=True)
            print("✓ 微信已关闭")
            return True
        except Exception as e2:
            print(f"❌ 关闭失败：{e2}")
            return False


def status_wechat():
    """检查微信状态"""
    running, pid = is_wechat_running()
    
    if running:
        print(f"✓ 微信正在运行 (PID: {pid})")
        
        # 获取更多信息
        try:
            proc = psutil.Process(pid)
            mem = proc.memory_info().rss / 1024 / 1024  # MB
            cpu = proc.cpu_percent()
            print(f"  内存占用：{mem:.1f} MB")
            print(f"  CPU 占用：{cpu:.1f}%")
        except:
            pass
        return True
    else:
        print("✗ 微信未运行")
        return False


def main():
    if len(sys.argv) < 2:
        print("用法：python wechat_control.py <command>")
        print("命令：start | stop | status")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "start":
        success = start_wechat()
        sys.exit(0 if success else 1)
    elif command == "stop":
        success = stop_wechat()
        sys.exit(0 if success else 1)
    elif command == "status":
        status_wechat()
        sys.exit(0)
    else:
        print(f"未知命令：{command}")
        print("用法：python wechat_control.py <start|stop|status>")
        sys.exit(1)


if __name__ == "__main__":
    main()
