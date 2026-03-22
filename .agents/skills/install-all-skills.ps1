# Skills 批量安装/更新脚本

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "╔════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Skills 批量安装/更新工具                  ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$DOWNLOADS_DIR = "C:\Users\Administrator\Downloads"
$SKILLS_DIR = "C:\Windows\system32\UsersAdministrator.openclawworkspace\.agents\skills"
$TEMP_DIR = "C:\Users\Administrator\AppData\Local\Temp\skills-install"

# 创建临时目录
if (Test-Path $TEMP_DIR) {
    Remove-Item $TEMP_DIR -Recurse -Force
}
New-Item -ItemType Directory -Path $TEMP_DIR | Out-Null

# 定义要安装的 skills
$skills = @(
    @{Name="nano-banana-pro"; Version="1.0.1"; Action="Install"},
    @{Name="obsidian"; Version="1.0.0"; Action="Install"},
    @{Name="ontology"; Version="1.0.4"; Action="Install"},
    @{Name="self-improving"; Version="1.2.16"; Action="Update"},
    @{Name="caldav-calendar"; Version="1.0.1"; Action="Update"},
    @{Name="slack"; Version="1.0.0"; Action="Update"},
    @{Name="trello"; Version="1.0.0"; Action="Update"},
    @{Name="answeroverflow"; Version="1.0.2"; Action="Update"}
)

$total = $skills.Count
$current = 0

foreach ($skill in $skills) {
    $current++
    Write-Host ""
    Write-Host "[$current/$total] 处理：$($skill.Name) v$($skill.Version) [$($skill.Action)]" -ForegroundColor Yellow
    
    # 查找 ZIP 文件
    $zipPattern = "$($skill.Name)-$($skill.Version)*.zip"
    $zipFile = Get-ChildItem $DOWNLOADS_DIR -Filter $zipPattern | Select-Object -First 1
    
    if (-not $zipFile) {
        Write-Host "  ⚠️  未找到 ZIP 文件：$zipPattern" -ForegroundColor Red
        continue
    }
    
    Write-Host "  ✓ 找到 ZIP: $($zipFile.Name)" -ForegroundColor Green
    
    # 解压到临时目录
    $tempSkillDir = Join-Path $TEMP_DIR $skill.Name
    Expand-Archive -Path $zipFile.FullName -DestinationPath $tempSkillDir -Force
    
    # 检查 SKILL.md
    $skillMd = Join-Path $tempSkillDir "SKILL.md"
    if (-not (Test-Path $skillMd)) {
        Write-Host "  ⚠️  未找到 SKILL.md，跳过" -ForegroundColor Red
        continue
    }
    
    # 读取技能信息
    $skillContent = Get-Content $skillMd -Raw
    $skillName = ""
    $skillVersion = ""
    
    if ($skillContent -match "name:\s*(.+)") {
        $skillName = $matches[1].Trim()
    }
    if ($skillContent -match "version:\s*[`"']?([0-9.]+)[`"']?") {
        $skillVersion = $matches[1].Trim()
    }
    
    Write-Host "  技能名称：$skillName" -ForegroundColor Gray
    Write-Host "  技能版本：$skillVersion" -ForegroundColor Gray
    
    # 检查是否已安装
    $installedPath = Join-Path $SKILLS_DIR $skillName
    
    if (Test-Path $installedPath) {
        Write-Host "  ℹ️  已安装，执行更新..." -ForegroundColor Cyan
        
        # 备份旧版本
        $backupPath = Join-Path $SKILLS_DIR "$($skillName).backup"
        if (Test-Path $backupPath) {
            Remove-Item $backupPath -Recurse -Force
        }
        Move-Item $installedPath $backupPath
        
        # 安装新版本
        Move-Item $tempSkillDir $installedPath
        
        Write-Host "  ✅ 已更新到 v$skillVersion" -ForegroundColor Green
        
        # 删除备份
        Remove-Item $backupPath -Recurse -Force
    } else {
        Write-Host "  ℹ️  新技能，执行安装..." -ForegroundColor Cyan
        
        # 安装
        Move-Item $tempSkillDir $installedPath
        
        Write-Host "  ✅ 已安装 v$skillVersion" -ForegroundColor Green
    }
}

# 清理临时目录
if (Test-Path $TEMP_DIR) {
    Remove-Item $TEMP_DIR -Recurse -Force
    Write-Host ""
    Write-Host "✓ 清理临时文件" -ForegroundColor Green
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ 所有 Skills 处理完成！                  ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# 显示已安装的 skills
Write-Host "已安装/更新的 Skills:" -ForegroundColor Cyan
Get-ChildItem $SKILLS_DIR -Directory | Where-Object { 
    $_.Name -match "nano-banana|obsidian|ontology|self-improving|caldav|slack|trello|answeroverflow" 
} | Select-Object Name, LastWriteTime | Format-Table -AutoSize

Write-Host ""
