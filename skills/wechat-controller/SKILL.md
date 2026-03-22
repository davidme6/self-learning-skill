---
name: wechat-controller
description: 微信客户端安全控制技能。仅在用户说出口令时触发：「打开自动化微信」「关闭自动化微信」「检查自动化微信状态」。普通聊天中提到微信不触发。用于安全地启动、关闭、检查微信运行状态，防止误操作。
---

# WeChat Controller - 微信控制技能

## 功能

- 🚀 **启动微信** - 按需启动微信客户端
- ⏹️ **关闭微信** - 优雅关闭微信进程
- 👀 **检查状态** - 查看微信是否正在运行

## 使用方式

### 触发流程

```
用户请求 → 检查是否包含安全口令 → 是 → 执行操作
                      ↓
                     否 → 回复"请说出口令：打开/关闭自动化微信"
```

### 命令行执行

**启动微信**
```bash
python skills/wechat-controller/scripts/wechat_control.py start
```

**关闭微信**
```bash
python skills/wechat-controller/scripts/wechat_control.py stop
```

**检查状态**
```bash
python skills/wechat-controller/scripts/wechat_control.py status
```

## 触发指令

### 安全口令模式（推荐）

用户说以下**精确口令**时才会执行操作：

| 操作 | 触发口令 |
|------|----------|
| 启动微信 | "打开自动化微信" |
| 关闭微信 | "关闭自动化微信" |
| 检查状态 | "检查自动化微信状态" |

### 大白话模式

如果用户用自然语言说（如"帮我开微信"、"把微信关了"），**必须先确认口令**：
- 回复："请说出口令：打开自动化微信"
- 用户说出口令后再执行

### 安全原则

- ⚠️ **不会误触发** - 普通聊天中提到"微信"不会触发
- ⚠️ **需要明确意图** - 必须包含"自动化"关键词
- ⚠️ **全局生效** - 所有 OpenClaw 聊天框都遵循此规则

## 注意事项

- ⚠️ **不会自动启动** - 只在用户明确指令时启动/关闭
- ⚠️ **先找微信路径** - 首次使用会自动搜索微信安装位置
- ⚠️ **优雅关闭** - 使用 taskkill 命令，给微信保存数据的时间

## 配置文件

微信路径会保存在 `~/.wechat_controller_config.json`，格式：
```json
{
  "wechat_path": "C:\\Program Files\\Tencent\\WeChat\\WeChat.exe"
}
```
