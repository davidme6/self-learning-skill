#!/usr/bin/env python3
"""
列出已存储的服务（不显示密码）
用法：python list.py
"""

import sys
import json
from pathlib import Path

# 确保 UTF-8 输出
sys.stdout.reconfigure(encoding='utf-8')

def list_credentials():
    """列出所有已存储的服务"""
    cred_dir = Path.home() / ".openclaw" / "credentials"
    
    if not cred_dir.exists():
        print("📭 暂无存储的凭证")
        return
    
    enc_files = list(cred_dir.glob("*.json.enc"))
    
    if not enc_files:
        print("📭 暂无存储的凭证")
        return
    
    print("🔐 已存储的服务：")
    print("-" * 40)
    
    for enc_file in enc_files:
        service = enc_file.stem.replace(".json", "")
        
        # 读取元数据（不解密密码）
        with open(enc_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 只解密用户名用于显示
        import subprocess
        ps_script = f"""
        $secure = ConvertTo-SecureString '{data["username_enc"]}'
        $bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
        [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
        """
        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        username = result.stdout.strip() if result.returncode == 0 else "***"
        
        print(f"  • {service}")
        print(f"    账号：{username}")
        print()
    
    print("-" * 40)
    print(f"共 {len(enc_files)} 个服务")

if __name__ == "__main__":
    list_credentials()
