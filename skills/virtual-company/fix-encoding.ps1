# Fix encoding helper
$sourcePath = Join-Path $PSScriptRoot "init-offices.ps1"
$targetPath = Join-Path $PSScriptRoot "init-offices-fixed.ps1"

# The correct script content with UTF-8 BOM
$utf8BOM = New-Object System.Text.UTF8Encoding $true
$content = @'
# ============================================================
# 虚拟公司办公室初始化脚本 v1.4.2
# 功能：为所有成员创建独立的子窗口（办公室）
# 命名格式：{团队名} - {角色}办公室
# ============================================================

param(
    [switch]$DryRun,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

# 配置文件路径
$ConfigPath = Join-Path $PSScriptRoot "team-config.json"
$StatePath = Join-Path $PSScriptRoot "office-state.json"

# 加载配置
if (-not (Test-Path $ConfigPath)) {
    Write-Error "找不到配置文件: $ConfigPath"
    exit 1
}

$Config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
Write-Host "📋 加载配置: $($Config.name) v$($Config.version)" -ForegroundColor Cyan
Write-Host "📊 总成员数: $($Config.totalMembers)" -ForegroundColor Cyan
Write-Host ""

# 加载现有状态（如果存在）
$ExistingOffices = @{}
if (Test-Path $StatePath) {
    $ExistingOffices = Get-Content $StatePath -Raw | ConvertFrom-Json
}

# 收集所有成员信息
$AllMembers = @()

# CEO
$AllMembers += [PSCustomObject]@{
    Team = "CEO"
    Role = "马云"
    OfficeName = "CEO 办公室"
    Model = $Config.ceo.model
    Description = $Config.ceo.description
    Number = $Config.ceo.number
}

# CEO 秘书
$AllMembers += [PSCustomObject]@{
    Team = "CEO秘书办公室"
    Role = "CEO 秘书"
    OfficeName = "CEO 秘书办公室"
    Model = $Config.ceoSecretary.model
    Description = $Config.ceoSecretary.description
    Number = $Config.ceoSecretary.number
}

# 各团队成员
foreach ($TeamKey in $Config.teams.PSObject.Properties.Name) {
    $Team = $Config.teams.$TeamKey
    $TeamName = $Team.name
    
    foreach ($MemberKey in $Team.members.PSObject.Properties.Name) {
        $Member = $Team.members.$MemberKey
        $AllMembers += [PSCustomObject]@{
            Team = $TeamName
            Role = $Member.name
            OfficeName = $Member.officeName
            Model = $Member.model
            Description = $Member.description
            Number = $Member.number
        }
    }
}

Write-Host "🏢 准备创建 $($AllMembers.Count) 个办公室..." -ForegroundColor Yellow
Write-Host ""

if ($DryRun) {
    Write-Host "🔍 [DRY-RUN] 将创建以下办公室：" -ForegroundColor Magenta
    Write-Host ""
    $AllMembers | ForEach-Object {
        Write-Host "  📍 $($_.OfficeName)" -ForegroundColor White
        Write-Host "     团队: $($_.Team) | 角色: $($_.Role) | 模型: $($_.Model)" -ForegroundColor Gray
    }
    Write-Host ""
    Write-Host "✅ Dry-run 完成，未创建实际办公室" -ForegroundColor Green
    exit 0
}

# 创建办公室状态
$OfficeState = @{}
$CreatedCount = 0
$SkippedCount = 0
$ErrorCount = 0

Write-Host "🚀 开始创建办公室..." -ForegroundColor Green
Write-Host ""

foreach ($Member in $AllMembers) {
    $OfficeName = $Member.OfficeName
    
    # 检查是否已存在
    if ($ExistingOffices.$OfficeName -and -not $Force) {
        Write-Host "  ⏭️  跳过（已存在）: $OfficeName" -ForegroundColor DarkGray
        $SkippedCount++
        $OfficeState.$OfficeName = $ExistingOffices.$OfficeName
        continue
    }
    
    try {
        # 生成唯一 Session ID
        $SessionId = "agent:main:office:$($Member.Number.ToLower())"
        
        # 创建办公室记录
        $OfficeRecord = @{
            sessionKey = $SessionId
            officeName = $OfficeName
            team = $Member.Team
            role = $Member.Role
            model = $Member.Model
            description = $Member.Description
            number = $Member.Number
            createdAt = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss+08:00")
            status = "created"
        }
        
        $OfficeState.$OfficeName = $OfficeRecord
        $CreatedCount++
        
        Write-Host "  ✅ 创建: $OfficeName" -ForegroundColor Green
        Write-Host "     📍 Session: $SessionId" -ForegroundColor DarkGray
        Write-Host "     🤖 模型: $($Member.Model)" -ForegroundColor DarkGray
        
    } catch {
        Write-Host "  ❌ 失败: $OfficeName - $_" -ForegroundColor Red
        $ErrorCount++
    }
}

# 保存状态
$OfficeState | ConvertTo-Json -Depth 10 | Set-Content $StatePath -Encoding UTF8

Write-Host ""
Write-Host "📊 初始化完成！" -ForegroundColor Cyan
Write-Host "   ✅ 创建: $CreatedCount" -ForegroundColor Green
Write-Host "   ⏭️  跳过: $SkippedCount" -ForegroundColor Yellow
Write-Host "   ❌ 失败: $ErrorCount" -ForegroundColor Red
Write-Host ""
Write-Host "📁 状态文件: $StatePath" -ForegroundColor Gray

# 输出使用说明
Write-Host ""
Write-Host "📖 使用方法：" -ForegroundColor Cyan
Write-Host "   精确调用: '让软件开发团队的产品经理分析需求'" -ForegroundColor White
Write-Host "   团队调用: '搞钱特战队的技术专家看这个方案'" -ForegroundColor White
Write-Host "   CEO调用: '叫CEO来汇报工作'" -ForegroundColor White
Write-Host "   秘书调用: 'CEO秘书帮我做个PPT'" -ForegroundColor White
Write-Host ""
Write-Host "💡 提示：" -ForegroundColor Yellow
Write-Host "   - 使用 -DryRun 预览将创建的办公室" -ForegroundColor Gray
Write-Host "   - 使用 -Force 强制重新创建已存在的办公室" -ForegroundColor Gray
Write-Host "   - 运行 check-offices.ps1 -Repair 可自动恢复" -ForegroundColor Gray
'@

# Write with UTF-8 BOM
[System.IO.File]::WriteAllText($sourcePath, $content, $utf8BOM)

Write-Host "File written with UTF-8 BOM encoding" -ForegroundColor Green

# Verify by running
Write-Host ""
Write-Host "Verifying syntax..." -ForegroundColor Yellow
try {
    $null = [ScriptBlock]::Create($content)
    Write-Host "Syntax OK!" -ForegroundColor Green
} catch {
    Write-Host "Syntax Error: $_" -ForegroundColor Red
}