# PC Automation CLI - 命令行控制入口

import sys
import argparse
from pathlib import Path

script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from config import is_enabled, enable, disable, get_status, get_config, save_config

def cmd_status(args):
    """Check status"""
    print(get_status())
    
    config = get_config()
    print("\nConfiguration:")
    print(f"  Safe mode: {'ON' if config.get('safe_mode') else 'OFF'}")
    print(f"  Require confirmation: {'ON' if config.get('require_confirmation') else 'OFF'}")
    print(f"  Timeout: {config.get('timeout_minutes', 30)} minutes")
    print(f"  Max clicks: {config.get('max_clicks_per_run', 100)}")

def cmd_enable(args):
    """开启自动化"""
    timeout = args.timeout if args.timeout else 30
    enable(timeout_minutes=timeout)

def cmd_disable(args):
    """关闭自动化"""
    disable()

def cmd_config(args):
    """查看/修改配置"""
    config = get_config()
    
    if args.show:
        print("当前配置:")
        for key, value in config.items():
            print(f"  {key}: {value}")
    
    if args.set:
        key, value = args.set.split('=')
        # 类型转换
        if value.lower() == 'true':
            value = True
        elif value.lower() == 'false':
            value = False
        elif value.isdigit():
            value = int(value)
        
        config[key] = value
        save_config(config)
        print(f"✅ 已设置 {key} = {value}")

def cmd_test(args):
    """运行测试"""
    import subprocess
    test_script = script_dir / "test_safe.py"
    subprocess.run([sys.executable, str(test_script)])

def main():
    parser = argparse.ArgumentParser(
        description="PC Automation - 电脑自动化控制",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  pc-auto status          查看状态
  pc-auto enable          开启自动化
  pc-auto enable -t 60    开启 60 分钟
  pc-auto disable         关闭自动化
  pc-auto config --show   查看配置
  pc-auto test            运行测试
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # status
    status_parser = subparsers.add_parser('status', help='查看状态')
    status_parser.set_defaults(func=cmd_status)
    
    # enable
    enable_parser = subparsers.add_parser('enable', help='开启自动化')
    enable_parser.add_argument('-t', '--timeout', type=int, help='超时时间（分钟）')
    enable_parser.set_defaults(func=cmd_enable)
    
    # disable
    disable_parser = subparsers.add_parser('disable', help='关闭自动化')
    disable_parser.set_defaults(func=cmd_disable)
    
    # config
    config_parser = subparsers.add_parser('config', help='配置管理')
    config_parser.add_argument('--show', action='store_true', help='显示配置')
    config_parser.add_argument('--set', help='设置配置 (key=value)')
    config_parser.set_defaults(func=cmd_config)
    
    # test
    test_parser = subparsers.add_parser('test', help='运行测试')
    test_parser.set_defaults(func=cmd_test)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return
    
    args.func(args)

if __name__ == "__main__":
    main()
