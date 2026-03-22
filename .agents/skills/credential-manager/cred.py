#!/usr/bin/env python3
"""
凭证管理命令行工具
用法：
  python cred.py store <service> <username> <password>  - 存储凭证
  python cred.py get <service>                          - 读取凭证
  python cred.py list                                   - 列出服务
  python cred.py delete <service>                       - 删除凭证
"""

import sys
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

def run_script(script: str, args: list = []):
    """运行凭证管理脚本"""
    script_path = SCRIPT_DIR / "scripts" / f"{script}.py"
    cmd = [sys.executable, str(script_path)] + args
    result = subprocess.run(cmd, capture_output=False, text=True, encoding='utf-8')
    return result.returncode

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "store":
        if len(sys.argv) != 5:
            print("用法：python cred.py store <service> <username> <password>")
            sys.exit(1)
        sys.exit(run_script("store", sys.argv[2:]))
    
    elif command == "get":
        if len(sys.argv) != 3:
            print("用法：python cred.py get <service>")
            sys.exit(1)
        sys.exit(run_script("retrieve", sys.argv[2:]))
    
    elif command == "list":
        sys.exit(run_script("list"))
    
    elif command == "delete":
        if len(sys.argv) != 3:
            print("用法：python cred.py delete <service>")
            sys.exit(1)
        sys.exit(run_script("delete", sys.argv[2:]))
    
    else:
        print(f"未知命令：{command}")
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
