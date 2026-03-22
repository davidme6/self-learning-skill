#!/usr/bin/env python3
"""
安全存储凭证 - 使用加密保护敏感信息
用法：python store.py <service> <username> <password>
"""

import sys
import json
import os
import subprocess
from pathlib import Path

# 确保 UTF-8 输出
sys.stdout.reconfigure(encoding='utf-8')

def encrypt_string(text: str) -> str:
    """使用 PowerShell DPAPI 加密字符串"""
    ps_script = f"""
    $secure = ConvertTo-SecureString '{text}' -AsPlainText -Force
    ConvertFrom-SecureString $secure
    """
    result = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    if result.returncode != 0:
        raise Exception(f"加密失败：{result.stderr}")
    return result.stdout.strip()

def store_credential(service: str, username: str, password: str):
    """存储加密凭证"""
    # 创建凭证目录
    cred_dir = Path.home() / ".openclaw" / "credentials"
    cred_dir.mkdir(parents=True, exist_ok=True)
    
    # 加密敏感信息
    encrypted_password = encrypt_string(password)
    encrypted_username = encrypt_string(username)
    
    # 存储加密数据
    cred_file = cred_dir / f"{service}.json.enc"
    data = {
        "service": service,
        "username_enc": encrypted_username,
        "password_enc": encrypted_password
    }
    
    with open(cred_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 设置文件权限（仅当前用户可访问）
    os.chmod(cred_file, 0o600)
    
    print(f"✅ 凭证已安全存储：{service}")
    print(f"   位置：{cred_file}")
    print(f"   ⚠️  密码已加密，不会明文显示")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("用法：python store.py <service> <username> <password>")
        print("示例：python store.py jimeng 13800138000 mypassword123")
        sys.exit(1)
    
    service = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    
    # 安全提示
    print("🔒 正在加密存储凭证...")
    print("   敏感信息不会显示在屏幕上")
    
    store_credential(service, username, password)
