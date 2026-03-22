# 记忆管理系统使用说明

## ✅ 已配置功能

### 1️⃣ 每日自动反思（3 次/天）

| 时间 | 内容 | Cron 任务 |
|------|------|----------|
| **09:00** | 早晨反思 - 回顾昨天，规划今天 | ✅ 记忆反思 - 早晨 09:00 |
| **14:00** | 下午反思 - 上午复盘，调整下午 | ✅ 记忆反思 - 下午 14:00 |
| **21:00** | 晚上反思 - 全天总结，整理记忆 | ✅ 记忆反思 - 晚上 21:00 |

---

### 2️⃣ 对话记录自动保存

**保存策略：**
- ✅ 文字对话 - 全量保存
- ✅ 重要决策 - 提取到 MEMORY.md
- ✅ 代码/脚本 - 保存到 skills/
- ❌ 图片/视频 - 不保存（空间有限）
- ❌ 大型文件 - 不保存

**保存位置：**
```
C:\Windows\system32\UsersAdministrator.openclawworkspace\memory\YYYY-MM-DD.md
```

---

### 3️⃣ MEMORY.md 定期整理

**整理频率：**
- 📅 每天小整理（21:00 反思时）
- 📅 每周大整理（周日晚）
- 📅 每月深度整理（月末）

**整理内容：**
- ✅ 重要决策
- ✅ 用户偏好
- ✅ 长期目标
- ✅ 关键人脉/资源
- ✅ 核心技能/能力

---

## 🔧 手动使用脚本

### 脚本位置：
```
C:\Windows\system32\UsersAdministrator.openclawworkspace\skills\memory-manager\
├── memory_manager.py    # 主脚本
└── PLAN.md              # 设计方案
```

### 使用方法：

#### 1. 保存对话
```powershell
python skills\memory-manager\memory_manager.py save "对话主题" "要点 1" "要点 2" "要点 3"
```

**示例：**
```powershell
python skills\memory-manager\memory_manager.py save "职业讨论" "优先畅联达" "ToAPIs 不错" "薪资 18-30K"
```

#### 2. 每日反思
```powershell
python skills\memory-manager\memory_manager.py reflect [morning|afternoon|evening]
```

**示例：**
```powershell
python skills\memory-manager\memory_manager.py reflect evening
```

#### 3. 整理记忆
```powershell
python skills\memory-manager\memory_manager.py organize
```

---

## 📋 记忆文件结构

### 每日记忆文件（memory/YYYY-MM-DD.md）
```markdown
# YYYY-MM-DD 记忆笔记

## 🎯 用户背景
[用户基本信息]

## 💬 对话记录 - HH:MM
**主题：** [主题]
**要点：**
- [要点 1]
- [要点 2]
**决策：** [决定]
**待办：** [行动]

## 🤔 反思 - 早晨/下午/晚上
### 1. 做得好的
### 2. 可以改进的
### 3. 学到的新东西
### 4. 用户偏好更新
### 5. 后续行动
```

### 长期记忆（MEMORY.md）
```markdown
# MEMORY.md - 长期记忆

## 📅 更新日期
[精华内容]

## 🎯 用户画像
[核心信息]

## 💼 职业方向
[长期目标]

## 🔧 技能/工具
[核心能力]
```

---

## 📊 定时任务状态

查看任务：
```powershell
openclaw cron list
```

任务列表：
```
✅ 记忆反思 - 早晨 09:00 (每天 9 点)
✅ 记忆反思 - 下午 14:00 (每天 14 点)
✅ 记忆反思 - 晚上 21:00 (每天 21 点)
```

---

## 💡 最佳实践

### 1. 对话后自动记录
每次重要对话后，花 1 分钟：
```
- 记录主题
- 提取要点（3-5 个）
- 记录决策
- 记录待办
```

### 2. 反思时认真填写
定时任务触发时，认真回答：
```
- 具体做了什么
- 哪里可以更好
- 学到了什么
- 用户有什么新偏好
```

### 3. 定期整理 MEMORY.md
每周日花 15 分钟：
```
- 读取本周 memory 文件
- 提取关键信息到 MEMORY.md
- 删除过时内容
- 更新用户画像
```

---

## ⚠️ 注意事项

1. **不要保存敏感信息**
   - 密码、密钥、个人隐私
   - 商业机密、合同内容

2. **定期清理**
   - 每月清理一次 memory 文件
   - 删除临时待办、过时信息

3. **备份**
   - 定期备份 MEMORY.md
   - 重要决策单独保存

---

## 🚀 未来改进

- [ ] 自动提取对话要点（AI 分析）
- [ ] 自动关联历史记忆
- [ ] 自动发现用户偏好变化
- [ ] 自动生成绩效报告
- [ ] 支持语音输入

---

*创建时间：2026-03-20 20:45*
*最后更新：2026-03-20 20:45*
