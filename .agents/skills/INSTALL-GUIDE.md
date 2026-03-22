# Skill 安装部署指南

## 快速安装流程

### 方式 1：使用自动化脚本（推荐）

```powershell
# 1. 安全检查（可选但推荐）
powershell -ExecutionPolicy Bypass -File ".agents\scripts\vet-skill.ps1" -SkillPath "C:\path\to\skill-folder"

# 2. 安装 Skill
powershell -ExecutionPolicy Bypass -File ".agents\scripts\install-skill.ps1" -ZipPath "C:\path\to\skill-x.x.x.zip"
```

### 方式 2：手动安装

```powershell
# 1. 解压 ZIP 文件
Expand-Archive -Path "skill-x.x.x.zip" -DestinationPath "C:\temp\skill-temp"

# 2. 复制到 skills 目录
Copy-Item -Path "C:\temp\skill-temp" -Destination ".agents\skills\skill-name" -Recurse -Force

# 3. 清理临时文件
Remove-Item -Path "C:\temp\skill-temp" -Recurse -Force
```

## 标准流程

### Step 1: 下载 Skill
从 ClawHub、GitHub 或其他来源下载 Skill ZIP 文件

### Step 2: 安全检查（使用 skill-vetter）
```powershell
# 解压到临时目录
Expand-Archive -Path "skill.zip" -DestinationPath "C:\temp\skill-check"

# 运行安全检查
powershell -ExecutionPolicy Bypass -File ".agents\scripts\vet-skill.ps1" -SkillPath "C:\temp\skill-check"
```

**检查项目：**
- 🚨 远程脚本执行（curl | bash）
- ⚠️ eval()/exec() 使用
- ⚠️ Base64 解码
- ⚠️ 敏感文件访问（~/.ssh, ~/.aws）
- ⚠️ 核心记忆文件引用（MEMORY.md 等）
- ⚠️ 硬编码凭证
- ⚠️ 外部网络请求

### Step 3: 安装
```powershell
powershell -ExecutionPolicy Bypass -File ".agents\scripts\install-skill.ps1" -ZipPath "skill.zip"
```

### Step 4: 验证
```powershell
# 检查是否安装成功
ls .agents\skills\skill-name

# 查看 SKILL.md
cat .agents\skills\skill-name\SKILL.md
```

### Step 5: 配置（如需要）
某些 Skill 需要配置 API 密钥或环境变量：
- 检查 SKILL.md 中的 "Requirements" 或 "Configuration" 部分
- 在 `~/.openclaw/openclaw.json` 中添加配置
- 或设置系统环境变量

## 已安装 Skills

| Skill | 版本 | 状态 | 说明 |
|-------|------|------|------|
| api-gateway | 1.0.69 | ✅ Active | 100+ API 网关代理（Maton.ai） |
| skill-vetter | 1.0.0 | ✅ Active | 安全检查工具 |

## 脚本说明

### install-skill.ps1
**功能：** 自动化 Skill 安装
**参数：**
- `-ZipPath` (必需): ZIP 文件路径
- `-SkillsDir` (可选): Skills 目录，默认使用工作区目录

**示例：**
```powershell
.\install-skill.ps1 -ZipPath "C:\Downloads\my-skill-1.0.0.zip"
```

### vet-skill.ps1
**功能：** 安全检查，识别潜在风险
**参数：**
- `-SkillPath` (必需): Skill 文件夹路径

**输出：**
- 🟢 低风险：无警告，可安全安装
- 🟡 中风险：少量警告，审查后可安装
- 🔴 高风险：发现红旗或大量警告，需人工审查

**示例：**
```powershell
.\vet-skill.ps1 -SkillPath "C:\temp\skill-to-check"
```

## 风险等级说明

| 等级 | 含义 | 操作 |
|------|------|------|
| 🟢 LOW | 无风险 | 直接安装 |
| 🟡 MEDIUM | 少量警告 | 审查警告内容后决定 |
| 🔴 HIGH | 发现红旗或多项警告 | 人工审查或拒绝安装 |
| ⛔ EXTREME | 严重安全问题 | 禁止安装 |

## 常见问题

### Q: 安装后 Skill 不生效？
A: 可能需要重启 OpenClaw Gateway：
```powershell
openclaw gateway restart
```

### Q: 如何卸载 Skill？
A: 直接删除对应文件夹：
```powershell
Remove-Item -Path ".agents\skills\skill-name" -Recurse -Force
```

### Q: 如何查看已安装的所有 Skills？
A: 
```powershell
ls .agents\skills -Directory | Select-Object Name
```

## 最佳实践

1. ✅ **始终先检查后安装** - 使用 vet-skill.ps1 进行安全检查
2. ✅ **从可信来源下载** - 优先选择 ClawHub 官方或高星仓库
3. ✅ **定期更新** - 保持 Skills 为最新版本
4. ✅ **记录变更** - 在 memory 文件中记录安装的 Skills
5. ✅ **最小权限** - 只授予必要的权限

## 安全提示

⚠️ **永远不要安装：**
- 要求提供 SSH/AWS 凭证的 Skill
- 包含混淆代码的 Skill
- 请求 sudo/管理员权限的 Skill
- 来源不明且无审查记录的 Skill

---

*最后更新：2026-03-15*
