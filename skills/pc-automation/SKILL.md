# PC Automation - 电脑自动化控制技能

## 🎯 功能描述

通过 Python + pyautogui 实现电脑自动化控制（鼠标、键盘、窗口操作），**带安全开关机制** — 每次执行需用户明确开启/关闭。

## ⚙️ 安装部署

### 1. 安装依赖

```bash
pip install pyautogui pygetwindow pillow opencv-python
```

### 2. 配置安全开关

编辑配置文件 `~/.pc_automation_config.json`：

```json
{
  "enabled": false,
  "require_confirmation": true,
  "max_clicks_per_run": 100,
  "blocked_actions": ["delete", "format", "shutdown"],
  "log_file": "~/.pc_automation.log"
}
```

### 3. 测试运行

```bash
python skills/pc-automation/scripts/test_safe.py
```

---

## 🔐 安全机制

### 开关控制

| 命令 | 说明 |
|------|------|
| `/pc-auto enable` | 开启自动化（需确认） |
| `/pc-auto disable` | 关闭自动化 |
| `/pc-auto status` | 查看当前状态 |
| `/pc-auto run <script>` | 执行脚本（需已开启） |

### 执行流程

```
用户请求 → 检查开关状态 → 未开启则询问确认 → 开启后执行 → 执行完自动关闭
```

### 安全限制

- ✅ 单次执行最多 100 次点击/按键
- ✅ 禁止删除、格式化、关机等危险操作
- ✅ 所有操作记录日志
- ✅ 随时可按 `Esc` 中断
- ✅ 执行前显示预览（要做什么）

---

## 📚 使用示例

### 示例 1: 自动填表

```bash
# 请求
帮我自动填写这个表单，姓名张三，邮箱 zhangsan@example.com

# 我会
1. 询问是否开启自动化
2. 显示要执行的操作预览
3. 你确认后执行
4. 执行完自动关闭
```

### 示例 2: 批量点击

```bash
# 请求
帮我批量点赞这 10 个视频

# 我会
1. 写脚本定位每个视频点赞按钮
2. 显示操作列表
3. 你确认后执行
```

### 示例 3: 定时任务

```bash
# 请求
每 30 分钟帮我检查一下这个页面有没有更新

# 我会
1. 创建定时脚本
2. 设置开关超时（比如 2 小时后自动关闭）
3. 你确认后启动
```

---

## 🛠️ 脚本示例

### 基础脚本模板

```python
# skills/pc-automation/scripts/auto_fill.py
import pyautogui
import time
from config import check_enabled, log_action

def main():
    # 检查开关
    if not check_enabled():
        print("❌ 自动化未开启，请先执行 /pc-auto enable")
        return
    
    try:
        # 预览操作
        print("📋 即将执行:")
        print("  1. 点击坐标 (100, 200)")
        print("  2. 输入 '张三'")
        print("  3. 点击坐标 (300, 400)")
        
        confirm = input("确认执行？(y/n): ")
        if confirm.lower() != 'y':
            print("❌ 已取消")
            return
        
        # 执行操作
        log_action("click", (100, 200))
        pyautogui.click(100, 200)
        time.sleep(0.5)
        
        log_action("type", "张三")
        pyautogui.write("张三", interval=0.1)
        time.sleep(0.5)
        
        log_action("click", (300, 400))
        pyautogui.click(300, 400)
        
        print("✅ 执行完成")
        
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断")
    finally:
        # 自动关闭
        print("🔒 自动化已关闭")

if __name__ == "__main__":
    main()
```

---

## 📁 文件结构

```
skills/pc-automation/
├── SKILL.md              # 技能说明
├── scripts/
│   ├── test_safe.py      # 安全测试脚本
│   ├── auto_fill.py      # 自动填表模板
│   ├── auto_click.py     # 自动点击模板
│   └── config.py         # 配置和开关逻辑
└── requirements.txt      # Python 依赖
```

---

## ⚠️ 注意事项

1. **首次使用** — 先在测试环境跑，确认无误再用于生产
2. **屏幕分辨率** — 坐标基于当前分辨率，分辨率变化需重新校准
3. **不要离开** — 执行时建议在旁边看着，随时可中断
4. **敏感操作** — 涉及金钱、隐私的操作务必仔细检查
5. **日志审计** — 定期查看 `~/.pc_automation.log` 回顾操作记录

---

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install pyautogui pygetwindow pillow

# 2. 测试
python skills/pc-automation/scripts/test_safe.py

# 3. 开启自动化
/pc-auto enable

# 4. 执行任务
/pc-auto run auto_fill

# 5. 完成后自动关闭（或手动）
/pc-auto disable
```

---

*最后更新：2026-03-20*
