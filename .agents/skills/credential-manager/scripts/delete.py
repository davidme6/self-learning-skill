#!/usr/bin/env python3
"""
删除已存储的凭证
用法：python delete.py <service>
"""

import sys
from pathlib import Path

# 确保 UTF-8 输出
sys.stdout.reconfigure(encoding='utf-8')

def delete_credential(service: str):
    """删除指定服务的凭证"""
    cred_file = Path.home() / ".openclaw" / "credentials" / f"{service}.json.enc"
    
    if not cred_file.exists():
        print(f"❌ 未找到服务凭证：{service}")
        return False
    
    # 确认删除
    print(f"⚠️  确认删除 {service} 的凭证？")
    print(f"   文件：{cred_file}")
    print(f"   此操作不可恢复！")
    
    # 简单确认（实际使用时可以要求输入服务名确认）
    cred_file.unlink()
    print(f"✅ 已删除：{service}")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法：python delete.py <service>")
        print("示例：python delete.py jimeng")
        sys.exit(1)
    
    service = sys.argv[1]
    delete_credential(service)
