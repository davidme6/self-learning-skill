# Skill Vetter - Security Check Tool
# Usage: .\vet-skill.ps1 -SkillPath "C:\path\to\skill"

param(
    [Parameter(Mandatory=$true)]
    [string]$SkillPath
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  Skill Vetter - Security Check Tool" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Validate path
if (-not (Test-Path $SkillPath)) {
    Write-Host "ERROR: Path does not exist - $SkillPath" -ForegroundColor Red
    exit 1
}

# Read SKILL.md
$skillMd = Join-Path $SkillPath "SKILL.md"
if (-not (Test-Path $skillMd)) {
    Write-Host "ERROR: SKILL.md not found" -ForegroundColor Red
    exit 1
}

$skillContent = Get-Content $skillMd -Raw
$skillName = ""
$skillVersion = ""

$skillContent | ForEach-Object {
    if ($_ -match "name:\s*(.+)") { $skillName = $matches[1].Trim() }
    if ($_ -match "version:\s*[`"']?([0-9.]+)[`"']?") { $skillVersion = $matches[1].Trim() }
}

Write-Host "Target: $skillName v$skillVersion" -ForegroundColor Yellow
Write-Host "Path: $SkillPath" -ForegroundColor Yellow
Write-Host ""

# Red flag checks
$redFlags = @()
$warnings = @()

Write-Host "Starting security scan..." -ForegroundColor Cyan
Write-Host ""

# Check all files
$files = Get-ChildItem -Path $SkillPath -Recurse -File -Include *.md,*.py,*.js,*.ts,*.json,*.sh,*.ps1,*.bat

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $relativePath = $file.FullName.Replace($SkillPath, "").TrimStart('\')
    
    # Red flag checks
    if ($content -match "curl.*\|.*bash" -or $content -match "wget.*\|.*bash") {
        $redFlags += "[$relativePath] Pipes remote script to bash"
    }
    
    if ($content -match "eval\s*\(") {
        $warnings += "[$relativePath] Uses eval() - review input source"
    }
    
    if ($content -match "exec\s*\(") {
        $warnings += "[$relativePath] Uses exec() - review input source"
    }
    
    if ($content -match "base64\.decode" -or $content -match "atob\s*\(") {
        $warnings += "[$relativePath] Uses base64 decode - review purpose"
    }
    
    if ($content -match "\.ssh|\.aws|\.config" -and $content -match "read|open") {
        $warnings += "[$relativePath] Accesses sensitive config files"
    }
    
    if ($content -match "MEMORY\.md|USER\.md|SOUL\.md|IDENTITY\.md") {
        $warnings += "[$relativePath] References core memory files"
    }
    
    if ($content -match "password|secret|token|key" -and $content -match "=\s*[`"'][^`"']+[`"']") {
        $warnings += "[$relativePath] May contain hardcoded credentials"
    }
    
    if ($content -match "requests\.post|urllib\.request" -and $content -match "http://(?!localhost|127\.0\.0\.1)") {
        $warnings += "[$relativePath] Contains external HTTP requests"
    }
}

# Output results
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

if ($redFlags.Count -gt 0) {
    Write-Host "RED FLAGS FOUND ($($redFlags.Count)):" -ForegroundColor Red
    foreach ($flag in $redFlags) {
        Write-Host "  - $flag" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "RECOMMENDATION: DO NOT INSTALL" -ForegroundColor Red
    exit 1
} else {
    Write-Host "No critical red flags found" -ForegroundColor Green
}

Write-Host ""

if ($warnings.Count -gt 0) {
    Write-Host "WARNINGS ($($warnings.Count)):" -ForegroundColor Yellow
    foreach ($warn in $warnings) {
        Write-Host "  - $warn" -ForegroundColor Yellow
    }
    Write-Host ""
} else {
    Write-Host "No warnings" -ForegroundColor Green
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Risk assessment
if ($redFlags.Count -eq 0 -and $warnings.Count -eq 0) {
    Write-Host "Risk Level: LOW" -ForegroundColor Green
    Write-Host "Recommendation: SAFE TO INSTALL" -ForegroundColor Green
} elseif ($redFlags.Count -eq 0 -and $warnings.Count -le 3) {
    Write-Host "Risk Level: MEDIUM" -ForegroundColor Yellow
    Write-Host "Recommendation: Review warnings, then install" -ForegroundColor Yellow
} else {
    Write-Host "Risk Level: HIGH" -ForegroundColor Red
    Write-Host "Recommendation: Manual review required" -ForegroundColor Yellow
}

Write-Host ""
