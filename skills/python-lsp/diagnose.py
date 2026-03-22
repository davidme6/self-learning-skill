#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python LSP 诊断工具
使用 Pyright 提供代码诊断
"""

import subprocess
import json
import sys
from pathlib import Path


def diagnose(path: str) -> dict:
    """
    使用 Pyright 诊断 Python 代码
    
    Args:
        path: 文件或目录路径
    
    Returns:
        诊断结果字典
    """
    path = Path(path)
    
    if not path.exists():
        return {
            "success": False,
            "error": f"路径不存在: {path}"
        }
    
    # Windows 下使用 npx 或完整路径
    import shutil
    pyright_path = shutil.which("pyright")
    if not pyright_path:
        pyright_path = r"C:\Users\Administrator\AppData\Roaming\npm\pyright.cmd"
    
    # 运行 pyright
    cmd = [pyright_path, str(path), "--outputjson"]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            encoding='utf-8',
            errors='replace'
        )
        
        # 解析 JSON 输出
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            # 如果没有 JSON 输出，尝试从 stderr 解析
            return {
                "success": True,
                "path": str(path),
                "diagnostics": [],
                "raw_output": result.stdout + result.stderr,
                "summary": {
                    "errors": 0,
                    "warnings": 0,
                    "informations": 0
                }
            }
        
        # 提取诊断信息
        diagnostics = []
        summary = data.get("summary", {})
        
        for diag in data.get("generalDiagnostics", []):
            diagnostics.append({
                "file": diag.get("file", ""),
                "line": diag.get("range", {}).get("start", {}).get("line", 0) + 1,
                "column": diag.get("range", {}).get("start", {}).get("character", 0) + 1,
                "severity": diag.get("severity", "unknown"),
                "message": diag.get("message", ""),
                "rule": diag.get("rule", "")
            })
        
        return {
            "success": True,
            "path": str(path),
            "diagnostics": diagnostics,
            "summary": {
                "errors": summary.get("errorCount", 0),
                "warnings": summary.get("warningCount", 0),
                "informations": summary.get("informationCount", 0)
            }
        }
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "诊断超时（60秒）"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def format_report(result: dict) -> str:
    """格式化诊断报告"""
    if not result["success"]:
        return f"❌ 诊断失败: {result.get('error', '未知错误')}"
    
    summary = result["summary"]
    diagnostics = result["diagnostics"]
    
    lines = [
        f"📁 路径: {result['path']}",
        f"📊 总结: {summary['errors']} 错误, {summary['warnings']} 警告, {summary['informations']} 提示",
        ""
    ]
    
    if not diagnostics:
        lines.append("✅ 没有发现问题！")
        return "\n".join(lines)
    
    # 按严重程度分组
    errors = [d for d in diagnostics if d["severity"] == "error"]
    warnings = [d for d in diagnostics if d["severity"] == "warning"]
    infos = [d for d in diagnostics if d["severity"] == "information"]
    
    if errors:
        lines.append("❌ 错误:")
        for d in errors[:10]:  # 最多显示10个
            lines.append(f"  [{d['file']}:{d['line']}:{d['column']}] {d['message']}")
        if len(errors) > 10:
            lines.append(f"  ... 还有 {len(errors) - 10} 个错误")
        lines.append("")
    
    if warnings:
        lines.append("⚠️ 警告:")
        for d in warnings[:5]:
            lines.append(f"  [{d['file']}:{d['line']}:{d['column']}] {d['message']}")
        if len(warnings) > 5:
            lines.append(f"  ... 还有 {len(warnings) - 5} 个警告")
        lines.append("")
    
    if infos:
        lines.append("ℹ️ 提示:")
        for d in infos[:3]:
            lines.append(f"  [{d['file']}:{d['line']}:{d['column']}] {d['message']}")
        if len(infos) > 3:
            lines.append(f"  ... 还有 {len(infos) - 3} 个提示")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # 设置 UTF-8 输出
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    if len(sys.argv) < 2:
        print("用法: python diagnose.py <文件或目录路径>")
        sys.exit(1)
    
    path = sys.argv[1]
    result = diagnose(path)
    print(format_report(result))