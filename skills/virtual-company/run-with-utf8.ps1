# Fix and run init-offices.ps1 with proper UTF-8 encoding
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$scriptPath = Join-Path $PSScriptRoot "init-offices.ps1"

# Read the script content
$content = Get-Content $scriptPath -Raw -Encoding UTF8

# Verify syntax by creating a script block
try {
    $null = [ScriptBlock]::Create($content)
    Write-Host "Syntax verification passed!" -ForegroundColor Green
} catch {
    Write-Host "Syntax error: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Attempting to fix..." -ForegroundColor Yellow
    
    # Try to identify the problematic lines
    $lines = $content -split "`n"
    Write-Host "Total lines: $($lines.Count)" -ForegroundColor Gray
    
    # Check for issues in each line
    for ($i = 0; $i -lt [Math]::Min($lines.Count, 60); $i++) {
        $line = $lines[$i]
        # Check if line contains Chinese but might have encoding issues
        if ($line -match '[\x{4E00}-\x{9FFF}]' -and $line -match '"[^"]*$') {
            Write-Host "Potential issue at line $($i+1): $($line.Substring(0, [Math]::Min(60, $line.Length)))..." -ForegroundColor Yellow
        }
    }
    exit 1
}

# Run the script
Write-Host ""
Write-Host "Running init-offices.ps1..." -ForegroundColor Cyan
& $scriptPath -DryRun