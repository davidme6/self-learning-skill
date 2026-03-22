#!/usr/bin/env python3
"""
安全读取凭证 - 解密后返回（仅内存中使用）
用法：python retrieve.py <service>
输出：JSON 格式（username, password）
"""

import sys
import json
from pathlib import Path
import subprocess

def decrypt_string(encrypted_text: str) -> str:
    """使用 PowerShell DPAPI 解密字符串"""
    ps_script = f"""
    $secure = ConvertTo-SecureString '{encrypted_text}'
    $bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
    """
    result = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    if result.returncode != 0:
        raise Exception(f"解密失败：{result.stderr}")
    return result.stdout.strip()

def retrieve_credential(service: str) -> dict:
    """读取并解密凭证"""
    cred_file = Path.home() / ".openclaw" / "credentials" / f"{service}.json.enc"
    
    if not cred_file.exists():
        raise FileNotFoundError(f"未找到服务凭证：{service}")
    
    with open(cred_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 解密敏感信息
    username = decrypt_string(data["username_enc"])
    password = decrypt_string(data["password_enc"])
    
    return {
        "service": service,
        "username": username,
        "password": password
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法：python retrieve.py <service>")
        print("示例：python retrieve.py jimeng")
        sys.exit(1)
    
    service = sys.argv[1]
    
    try:
        creds = retrieve_credential(service)
        # 输出 JSON 供其他脚本使用
        print(json.dumps(creds, ensure_ascii=False))
    except FileNotFoundError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        sys.exit(1)
