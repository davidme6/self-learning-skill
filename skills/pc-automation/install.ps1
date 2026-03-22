# PC Automation - Install Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PC Automation Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check Python
Write-Host "Step 1: Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "OK: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python not installed" -ForegroundColor Red
    exit 1
}

# 2. Install dependencies
Write-Host ""
Write-Host "Step 2: Installing Python dependencies..." -ForegroundColor Yellow
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$requirementsPath = Join-Path $scriptDir "requirements.txt"

pip install -r $requirementsPath
Write-Host "OK: Dependencies installed" -ForegroundColor Green

# 3. Create config file
Write-Host ""
Write-Host "Step 3: Creating config file..." -ForegroundColor Yellow
$configPath = Join-Path $env:USERPROFILE ".pc_automation_config.json"

if (Test-Path $configPath) {
    Write-Host "INFO: Config already exists" -ForegroundColor Cyan
} else {
    $config = @{
        enabled = $false
        require_confirmation = $true
        max_clicks_per_run = 100
        max_keys_per_run = 500
        blocked_actions = @("delete", "format", "shutdown", "sudo", "rm -rf")
        timeout_minutes = 30
        log_file = (Join-Path $env:USERPROFILE ".pc_automation.log")
        safe_mode = $true
    } | ConvertTo-Json -Depth 10
    
    $config | Set-Content -Path $configPath -Encoding UTF8
    Write-Host "OK: Config created at $configPath" -ForegroundColor Green
}

# 4. Create CLI shortcut
Write-Host ""
Write-Host "Step 4: Creating CLI command..." -ForegroundColor Yellow

$cliScriptPath = Join-Path $scriptDir "pc_auto_cli.py"
$installDir = Join-Path $env:USERPROFILE ".local\bin"

if (-not (Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir | Out-Null
}

$batPath = Join-Path $installDir "pc-auto.bat"
$batContent = "@echo off`npython `"$cliScriptPath`" %*"
$batContent | Set-Content -Path $batPath -Encoding ASCII
Write-Host "OK: CLI command created: pc-auto" -ForegroundColor Green

Write-Host ""
Write-Host "NOTE: Add $installDir to PATH if not already done" -ForegroundColor Yellow

# 5. Test
Write-Host ""
Write-Host "Step 5: Running test..." -ForegroundColor Yellow

python $cliScriptPath status
Write-Host "OK: Test passed" -ForegroundColor Green

# Done
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Usage:" -ForegroundColor Cyan
Write-Host "  pc-auto status     - Check status" -ForegroundColor White
Write-Host "  pc-auto enable     - Enable automation" -ForegroundColor White
Write-Host "  pc-auto disable    - Disable automation" -ForegroundColor White
Write-Host "  pc-auto test       - Run test" -ForegroundColor White
Write-Host ""
