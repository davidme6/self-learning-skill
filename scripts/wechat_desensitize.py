#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信聊天记录脱敏脚本
在本地处理，不上传任何数据
"""

import re
import json
import os
from pathlib import Path
from datetime import datetime

# 敏感信息正则模式
PATTERNS = {
    "phone": [
        r"1[3-9]\d{9}",  # 手机号
        r"\d{3,4}-\d{7,8}",  # 座机
    ],
    "id_card": [
        r"\d{17}[\dXx]",  # 身份证号
    ],
    "bank_card": [
        r"\d{16,19}",  # 银行卡号（需进一步确认）
    ],
    "address": [
        r"(省|市|区|县|路|街|号|楼|室|幢|栋|单元|小区|花园|广场|大厦)[\w\d\-#]+",
    ],
    "email": [
        r"[\w\.-]+@[\w\.-]+\.\w+",
    ],
    "url": [
        r"https?://[^\s]+",
    ],
    "qq": [
        r"QQ[：:]\s*\d{5,11}",
        r"qq号[是为]?\s*\d{5,11}",
    ],
    "wechat": [
        r"微信[号：:]\s*[\w\-]+",
        r"微信号[是为]?\s*[\w\-]+",
    ],
}

# 不需要脱敏的关键词（避免误伤）
WHITELIST = [
    "110", "119", "120", "12345", "12306",  # 公共服务号码
    "12315", "12319", "12320", "12348",
]


def desensitize_text(text: str) -> tuple:
    """
    脱敏文本
    返回: (脱敏后的文本, 脱敏统计)
    """
    stats = {key: 0 for key in PATTERNS}
    result = text
    
    for category, patterns in PATTERNS.items():
        for pattern in patterns:
            matches = re.findall(pattern, result)
            for match in matches:
                # 检查白名单
                if match in WHITELIST:
                    continue
                
                # 银行卡号需要确认长度
                if category == "bank_card" and len(match) < 16:
                    continue
                
                # 脱敏处理
                if category == "phone":
                    # 保留前3后4
                    if len(match) == 11:
                        masked = match[:3] + "****" + match[-4:]
                    else:
                        masked = "***" + match[-4:] if len(match) > 4 else "***"
                elif category == "id_card":
                    # 保留前6后4
                    masked = match[:6] + "********" + match[-4:]
                elif category == "bank_card":
                    # 保留前4后4
                    masked = match[:4] + "****" + match[-4:]
                elif category == "email":
                    # 保留首字母和域名
                    parts = match.split("@")
                    if len(parts) == 2:
                        name = parts[0]
                        if len(name) > 2:
                            masked = name[0] + "***@" + parts[1]
                        else:
                            masked = "***@" + parts[1]
                    else:
                        masked = "***@***.***"
                elif category == "url":
                    masked = "[链接已脱敏]"
                elif category == "address":
                    # 地址只保留省市区
                    masked = re.sub(r"(省|市|区|县).*", r"\1***", match)
                else:
                    # 其他情况用星号替换中间部分
                    if len(match) > 4:
                        masked = match[:2] + "***" + match[-2:]
                    else:
                        masked = "***"
                
                result = result.replace(match, masked)
                stats[category] += 1
    
    return result, stats


def process_file(input_path: str, output_path: str) -> dict:
    """
    处理单个文件
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    
    if not input_path.exists():
        return {"success": False, "error": f"文件不存在: {input_path}"}
    
    # 读取文件
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        # 尝试其他编码
        try:
            with open(input_path, "r", encoding="gbk") as f:
                content = f.read()
        except Exception as e:
            return {"success": False, "error": f"无法读取文件: {e}"}
    
    # 脱敏处理
    desensitized, stats = desensitize_text(content)
    
    # 写入输出文件
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(desensitized)
    
    total_masked = sum(stats.values())
    
    return {
        "success": True,
        "input": str(input_path),
        "output": str(output_path),
        "stats": stats,
        "total_masked": total_masked,
    }


def process_directory(input_dir: str, output_dir: str) -> dict:
    """
    处理整个目录
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    
    if not input_dir.exists():
        return {"success": False, "error": f"目录不存在: {input_dir}"}
    
    results = []
    total_stats = {key: 0 for key in PATTERNS}
    
    # 处理所有文件
    for file_path in input_dir.rglob("*"):
        if file_path.is_file() and file_path.suffix in [".txt", ".json", ".csv", ".html"]:
            rel_path = file_path.relative_to(input_dir)
            output_path = output_dir / rel_path
            
            result = process_file(file_path, output_path)
            results.append(result)
            
            if result["success"]:
                for key, count in result["stats"].items():
                    total_stats[key] += count
    
    return {
        "success": True,
        "input_dir": str(input_dir),
        "output_dir": str(output_dir),
        "files_processed": len(results),
        "total_stats": total_stats,
        "total_masked": sum(total_stats.values()),
        "details": results,
    }


if __name__ == "__main__":
    import sys
    
    print("=" * 50)
    print("微信聊天记录脱敏工具")
    print("⚠️  所有处理均在本地进行，不上传任何数据")
    print("=" * 50)
    print()
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  处理文件: python wechat_desensitize.py <输入文件> [输出文件]")
        print("  处理目录: python wechat_desensitize.py <输入目录> <输出目录>")
        print()
        print("示例:")
        print("  python wechat_desensitize.py chat.txt chat_masked.txt")
        print("  python wechat_desensitize.py C:\\wechat_export C:\\wechat_masked")
        sys.exit(1)
    
    input_path = sys.argv[1]
    
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        # 自动生成输出路径
        p = Path(input_path)
        output_path = p.parent / f"{p.stem}_desensitized{p.suffix}"
    
    print(f"输入: {input_path}")
    print(f"输出: {output_path}")
    print()
    
    # 判断是文件还是目录
    if Path(input_path).is_dir():
        result = process_directory(input_path, output_path)
    else:
        result = process_file(input_path, output_path)
    
    if result["success"]:
        print("✅ 脱敏完成!")
        print()
        print("📊 脱敏统计:")
        for key, count in result.get("stats", result.get("total_stats", {})).items():
            if count > 0:
                print(f"  - {key}: {count} 处")
        print(f"  总计: {result.get('total_masked', 0)} 处敏感信息已脱敏")
        print()
        print(f"📁 输出文件: {result.get('output', result.get('output_dir', ''))}")
    else:
        print(f"❌ 处理失败: {result.get('error', '未知错误')}")