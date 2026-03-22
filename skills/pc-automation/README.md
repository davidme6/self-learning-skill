# 🤖 PC Automation - 电脑自动化控制技能

**安全可控的电脑自动化** — 通过 Python + pyautogui 实现鼠标键盘控制，带安全开关机制，每次执行需用户明确开启/关闭。

---

## ⚡ 快速开始

### 1. 一键安装

```powershell
cd skills/pc-automation
powershell -ExecutionPolicy Bypass -File install.ps1
```

### 2. 测试运行

```bash
pc-auto test
```

### 3. 开始使用

```bash
# 开启自动化
pc-auto enable

# 执行脚本
python scripts/auto_fill.py

# 完成后关闭
pc-auto disable
```

---

## 🔐 安全机制

### 开关控制

| 命令 | 说明 |
|------|------|
| `pc-auto enable` | 开启自动化（默认 30 分钟后自动关闭） |
| `pc-auto enable -t 60` | 开启 60 分钟 |
| `pc-auto disable` | 手动关闭 |
| `pc-auto status` | 查看状态 |

### 执行流程

```
用户请求 
  → 检查开关状态 
  → 未开启则询问确认 
  → 显示操作预览 
  → 用户确认 
  → 执行 
  → 记录日志 
  → 自动关闭
```

### 安全限制

- ✅ 单次执行最多 100 次点击
- ✅ 单次执行最多 500 次按键
- ✅ 禁止删除、格式化、关机等危险操作
- ✅ 所有操作记录日志（`~/.pc_automation.log`）
- ✅ 按 `Esc` 可随时中断
- ✅ 执行前显示预览
- ✅ 超时自动关闭（默认 30 分钟）

---

## 📚 使用场景

### 场景 1: 自动填表

```python
# 创建你的填表脚本
from scripts.config import is_enabled, enable, log_action
import pyautogui

if not is_enabled():
    enable(timeout_minutes=10)

# 填写表单
pyautogui.click(500, 300)  # 点击姓名框
pyautogui.write("张三", interval=0.1)
pyautogui.press('tab')
pyautogui.write("zhangsan@example.com", interval=0.1)
pyautogui.click(500, 500)  # 点击提交

log_action("form_submit", "联系表单")
```

### 场景 2: 批量操作

```python
# 批量点击/操作
positions = [(100, 200), (200, 200), (300, 200)]

for pos in positions:
    pyautogui.click(pos[0], pos[1])
    log_action("click", pos)
    time.sleep(0.5)
```

### 场景 3: 定时任务

```bash
# 开启 2 小时自动化
pc-auto enable -t 120

# 然后运行你的脚本
python scripts/my_automation.py

# 或者设置定时关闭
# 2 小时后自动关闭，无需手动操作
```

---

## 🛠️ 自定义脚本

### 模板：创建你的自动化脚本

```python
# scripts/my_script.py
import sys
from pathlib import Path

script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from config import is_enabled, enable, disable, log_action, confirm_action
import pyautogui
import time

def main():
    # 1. 检查开关
    if not is_enabled():
        print("❌ 自动化未开启")
        print("💡 运行：pc-auto enable")
        return
    
    # 2. 显示预览
    preview = """
即将执行:
  1. 打开浏览器
  2. 访问网址
  3. 填写表单
  4. 提交
"""
    
    if not confirm_action(preview):
        print("❌ 已取消")
        return
    
    # 3. 执行操作
    try:
        # 你的自动化代码
        pyautogui.hotkey('win', 'd')  # 显示桌面
        log_action("hotkey", "win+d")
        
        # ... 更多操作
        
        print("✅ 完成")
        
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断")
    except Exception as e:
        print(f"❌ 错误：{e}")
    finally:
        # 4. 自动关闭（可选）
        # disable()

if __name__ == "__main__":
    main()
```

---

## 📁 文件结构

```
skills/pc-automation/
├── SKILL.md              # 技能说明
├── README.md             # 使用文档
├── install.ps1           # 安装脚本
├── requirements.txt      # Python 依赖
├── scripts/
│   ├── config.py         # 配置和开关管理
│   ├── pc_auto_cli.py    # CLI 入口
│   ├── test_safe.py      # 安全测试
│   └── auto_fill.py      # 填表示例
└── ...你的脚本
```

---

## ⚠️ 注意事项

1. **首次使用** — 先在测试环境跑，确认无误再用于生产
2. **屏幕分辨率** — 坐标基于当前分辨率，变化需重新校准
3. **不要离开** — 执行时建议在旁边看着，随时可中断
4. **敏感操作** — 涉及金钱、隐私的操作务必仔细检查
5. **日志审计** — 定期查看 `~/.pc_automation.log`

---

## 🆘 常见问题

### Q: 安装后 `pc-auto` 命令不识别？
A: 需要将 `~/.local/bin` 添加到 PATH，或直接用 `python scripts/pc_auto_cli.py`

### Q: 鼠标移动不准确？
A: 检查屏幕分辨率是否变化，重新校准坐标

### Q: 如何查看操作日志？
A: 打开 `~/.pc_automation.log`，每行是一条操作记录

### Q: 如何永久关闭某个危险操作？
A: 编辑 `~/.pc_automation_config.json`，添加到 `blocked_actions` 列表

---

## 📝 配置文件示例

`~/.pc_automation_config.json`:

```json
{
  "enabled": false,
  "require_confirmation": true,
  "max_clicks_per_run": 100,
  "max_keys_per_run": 500,
  "blocked_actions": ["delete", "format", "shutdown", "sudo", "rm -rf"],
  "timeout_minutes": 30,
  "log_file": "C:\\Users\\YourName\\.pc_automation.log",
  "safe_mode": true
}
```

---

*最后更新：2026-03-20*
*版本：v1.0.0*
