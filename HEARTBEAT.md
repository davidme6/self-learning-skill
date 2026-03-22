# 健康 Guardian 定时提醒检查

---

## 📱 飞书独立通知（推荐）

**频率：** 每 10 分钟检查一次

**检查命令：**
```bash
python github\davidme6\health-guardian\scripts\feishu_notify.py
```

**工作流程：**
1. 脚本检查当前时间是否有预设提醒
2. 如果有且未发送，直接调用飞书 webhook 发送
3. 不依赖 OpenClaw，独立运行

**配置飞书 webhook：**
1. 编辑 `~/.health_guardian_config.json`
2. 添加 `"feishu_webhook": "你的飞书 webhook URL"`
3. 保存

**设置定时任务：**
```powershell
powershell -ExecutionPolicy Bypass -File "github\davidme6\health-guardian\scripts\setup_feishu_tasks.ps1"
```

---

## 🤖 OpenClaw 心跳检查（备用）

**频率：** 每小时检查一次

**检查命令：**
```bash
python github\davidme6\health-guardian\scripts\notify.py
```

如果有提醒消息，通过 OpenClaw 发送到飞书。

---

## ⏰ 完整提醒时间表

| 时间 | 类型 | 内容 |
|------|------|------|
| 07:00 | 🧴 晨间护肤 | 洁面→保湿→防晒 |
| 07:30 | ☀️ 早安 | 今日计划 |
| 08:00 | 💧 喝水 + 维 C | 250ml + 抗氧化 |
| 10:00 | 💧 喝水 | 250ml |
| 12:00 | 🍽️ 午餐 + 维 E | 豆制品 + 全谷物 |
| 14:00 | 💧 喝水 | 250ml + 绿茶 |
| 16:00 | 💧 喝水 | 250ml + 坚果 |
| 17:00 | 🏃 运动 | 30 分钟有氧/力量 |
| 18:00 | 🍽️ 晚餐 + Omega-3 | 清淡 + Omega-3 |
| 20:00 | 🧘 拉伸 | 10 分钟放松 |
| 21:00 | 🌙 晚间护肤 | 清洁→修复→滋养 |
| 21:30 | 😴 睡前准备 | 关闭电子设备 |
| 22:30 | 💤 入睡 | 保证 7-8 小时 |

---

## 💬 用户可主动查询

直接对我说：
- "健康检查"
- "现在该做什么"
- "喝水提醒"
- "运动时间到了吗"
- "今天健康计划"

---

## ⚙️ 双重保障

1. **飞书独立通知** - 每 10 分钟检查，直接发送
2. **OpenClaw 心跳** - 每小时检查，备用方案

确保你不会错过任何健康提醒！

---

## ✅ 最新状态（23:50 更新）

**定时任务状态：**
```
✅ HealthGuardian-Base - 每 10 分钟
✅ HealthGuardian-Morning - 每天 07:00
✅ HealthGuardian-Meal - 每天 12:00
✅ HealthGuardian-Evening - 每天 18:00
✅ HealthGuardian-Sleep - 每天 21:30
✅ HealthGuardian-Config-Validate - 每天 06:00 验证配置
```

**配置文件：** `C:\Users\Administrator\.health_guardian_config.json`

**备份目录：** `C:\Users\Administrator\.health_guardian_backups\`

**配置验证命令：**
```bash
$env:PYTHONIOENCODING='utf-8'; python C:\Windows\system32\UsersAdministrator.openclawworkspace\github\davidme6\health-guardian\scripts\validate_config.py
```

**手动备份配置：**
```bash
python .../validate_config.py backup
```

**从备份恢复：**
```bash
python .../validate_config.py restore
```

---

## 🛡️ 防护措施

1. **配置验证** - 每天 06:00 自动验证配置编码
2. **自动备份** - 每次验证通过自动备份，保留最近 10 个
3. **自动恢复** - 检测到乱码时自动从最近备份恢复
4. **发送前检查** - 飞书通知发送前验证配置编码

---

*最后更新：2026-03-21 23:50*
