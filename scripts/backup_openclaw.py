#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 完整备份脚本
备份所有配置、记忆、技能、会话
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path

# 配置
WORKSPACE = Path("C:/Windows/system32/UsersAdministrator.openclawworkspace")
CONFIG_DIR = Path.home() / ".openclaw"
BACKUP_DIR = Path.home() / "openclaw_backup"

def create_backup():
    """创建完整备份"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"openclaw_backup_{timestamp}"
    
    print("=" * 50)
    print("OpenClaw 完整备份")
    print("=" * 50)
    print(f"\n备份目录: {backup_path}")
    print()
    
    # 创建备份目录
    backup_path.mkdir(parents=True, exist_ok=True)
    
    # 1. 备份工作目录
    print("1. 备份工作目录（技能、记忆、项目）...")
    workspace_backup = backup_path / "workspace"
    if WORKSPACE.exists():
        shutil.copytree(WORKSPACE, workspace_backup, dirs_exist_ok=True)
        print(f"   ✅ 工作目录已备份")
    
    # 2. 备份配置目录
    print("2. 备份配置目录（模型、网关、会话）...")
    config_backup = backup_path / "openclaw_config"
    if CONFIG_DIR.exists():
        shutil.copytree(CONFIG_DIR, config_backup, dirs_exist_ok=True)
        print(f"   ✅ 配置目录已备份")
    
    # 3. 创建恢复脚本
    print("3. 创建恢复脚本...")
    restore_script = backup_path / "restore.py"
    restore_script.write_text(f'''#!/usr/bin/env python3
"""OpenClaw 恢复脚本"""
import shutil
from pathlib import Path

WORKSPACE = Path("C:/Windows/system32/UsersAdministrator.openclawworkspace")
CONFIG_DIR = Path.home() / ".openclaw"

def restore():
    print("恢复 OpenClaw...")
    
    # 恢复工作目录
    print("1. 恢复工作目录...")
    shutil.copytree("workspace", WORKSPACE, dirs_exist_ok=True)
    
    # 恢复配置目录
    print("2. 恢复配置目录...")
    shutil.copytree("openclaw_config", CONFIG_DIR, dirs_exist_ok=True)
    
    print("\\n✅ 恢复完成！")
    print("请运行: npm install -g openclaw")

if __name__ == "__main__":
    restore()
''', encoding='utf-8')
    print(f"   ✅ 恢复脚本已创建")
    
    # 4. 创建备份信息
    info = {
        "timestamp": timestamp,
        "created_at": datetime.now().isoformat(),
        "workspace_path": str(WORKSPACE),
        "config_path": str(CONFIG_DIR),
        "backup_path": str(backup_path)
    }
    (backup_path / "backup_info.json").write_text(json.dumps(info, indent=2, ensure_ascii=False), encoding='utf-8')
    
    # 5. 计算大小
    total_size = sum(f.stat().st_size for f in backup_path.rglob("*") if f.is_file())
    size_mb = total_size / (1024 * 1024)
    
    print()
    print("=" * 50)
    print(f"✅ 备份完成！")
    print(f"   位置: {backup_path}")
    print(f"   大小: {size_mb:.2f} MB")
    print()
    print("恢复方法：")
    print(f"   1. 复制整个备份目录到新电脑")
    print(f"   2. 在新电脑安装: npm install -g openclaw")
    print(f"   3. 运行: python restore.py")
    print("=" * 50)
    
    return backup_path

if __name__ == "__main__":
    create_backup()