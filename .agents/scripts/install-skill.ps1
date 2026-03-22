# Skill 安装部署脚本
# 用法：.\install-skill.ps1 -ZipPath "C:\path\to\skill-x.x.x.zip"

param(
    [Parameter(Mandatory=$true)]
    [string]$ZipPath,
    
    [string]$SkillsDir = "C:\Windows\system32\UsersAdministrator.openclawworkspace\.agents\skills"
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Skill 安装部署工具" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 验证文件存在
if (-not (Test-Path $ZipPath)) {
    Write-Host "❌ 错误：文件不存在 - $ZipPath" -ForegroundColor Red
    exit 1
}
Write-Host "✓ 找到 ZIP 文件：$ZipPath" -ForegroundColor Green

# 2. 创建临时目录
$zipName = [System.IO.Path]::GetFileNameWithoutExtension($ZipPath)
$tempDir = Join-Path $env:TEMP "skill-install-$zipName"
$null = New-Item -ItemType Directory -Path $tempDir -Force
Write-Host "✓ 创建临时目录：$tempDir" -ForegroundColor Green

# 3. 解压文件
Write-Host "⏳ 解压中..." -ForegroundColor Yellow
Expand-Archive -Path $ZipPath -DestinationPath $tempDir -Force

# 4. 检查 SKILL.md
$skillMd = Join-Path $tempDir "SKILL.md"
if (-not (Test-Path $skillMd)) {
    Write-Host "❌ 错误：未找到 SKILL.md 文件" -ForegroundColor Red
    Remove-Item -Path $tempDir -Recurse -Force
    exit 1
}
Write-Host "✓ 找到 SKILL.md" -ForegroundColor Green

# 5. 读取 skill 信息
$skillName = $null
$skillVersion = "unknown"
$skillDescription = ""

Get-Content $skillMd | ForEach-Object {
    if ($_ -match "^name:\s*(.+)") { $skillName = $matches[1].Trim() }
    if ($_ -match "^version:\s*[`"']?([0-9.]+)[`"']?") { $skillVersion = $matches[1].Trim() }
    if ($_ -match "^description:\s*(.+)") { $skillDescription = $matches[1].Trim() }
}

if (-not $skillName) {
    # 从文件名推断
    $skillName = $zipName -replace '-\d+\.\d+\.\d+$', ''
}

Write-Host "✓ Skill 名称：$skillName" -ForegroundColor Green
Write-Host "✓ 版本：$skillVersion" -ForegroundColor Green

# 6. 检查是否已安装
$installPath = Join-Path $SkillsDir $skillName
if (Test-Path $installPath) {
    Write-Host "⚠️  技能已存在，将覆盖安装" -ForegroundColor Yellow
}

# 7. 安装技能
Write-Host "⏳ 安装中..." -ForegroundColor Yellow
Copy-Item -Path $tempDir -Destination $installPath -Recurse -Force
Write-Host "✓ 安装完成：$installPath" -ForegroundColor Green

# 8. 清理临时文件
Remove-Item -Path $tempDir -Recurse -Force
Write-Host "✓ 清理临时文件" -ForegroundColor Green

# 9. 验证安装
$installedFiles = Get-ChildItem -Path $installPath -Recurse -File | Measure-Object | Select-Object -ExpandProperty Count
Write-Host "✓ 安装文件数：$installedFiles" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ✅ 安装成功！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Skill 信息:"
Write-Host "  名称：$skillName"
Write-Host "  版本：$skillVersion"
Write-Host "  描述：$skillDescription"
Write-Host "  位置：$installPath"
Write-Host ""
