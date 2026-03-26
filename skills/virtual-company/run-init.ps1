# Run init-offices.ps1 with correct UTF-8 encoding
param(
    [switch]$DryRun,
    [switch]$Force
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scriptPath = Join-Path $ScriptDir "init-offices.ps1"

# Read with explicit UTF-8 encoding
$content = [System.IO.File]::ReadAllText($scriptPath, [System.Text.Encoding]::UTF8)

# Replace $PSScriptRoot with actual path
$content = $content -replace '\$PSScriptRoot', "'$ScriptDir'"

# Create script block and execute
$scriptBlock = [ScriptBlock]::Create($content)

# Execute with arguments
& $scriptBlock -DryRun:$DryRun -Force:$Force