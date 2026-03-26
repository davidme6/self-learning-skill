# Check file encoding
$filePath = Join-Path $PSScriptRoot "init-offices.ps1"
$bytes = [System.IO.File]::ReadAllBytes($filePath)

Write-Host "First 20 bytes (hex):"
$bytes[0..19] | ForEach-Object { Write-Host ("{0:X2} " -f $_) -NoNewline }
Write-Host ""
Write-Host ""

# Check BOM
if ($bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
    Write-Host "Encoding: UTF-8 with BOM" -ForegroundColor Green
} elseif ($bytes[0] -eq 0xFF -and $bytes[1] -eq 0xFE) {
    Write-Host "Encoding: UTF-16 LE" -ForegroundColor Green
} elseif ($bytes[0] -eq 0xFE -and $bytes[1] -eq 0xFF) {
    Write-Host "Encoding: UTF-16 BE" -ForegroundColor Green
} else {
    Write-Host "Encoding: No BOM detected (likely UTF-8 without BOM or ANSI)" -ForegroundColor Yellow
}

# Read content
$content = [System.IO.File]::ReadAllText($filePath, [System.Text.Encoding]::UTF8)
Write-Host ""
Write-Host "Line count: $($content.Split("`n").Count)"
Write-Host ""

# Check lines 7-10 (param block)
$lines = $content -split "`n"
Write-Host "Lines 7-10 (param block):" -ForegroundColor Cyan
for ($i = 6; $i -lt 10 -and $i -lt $lines.Count; $i++) {
    Write-Host "Line $($i+1): $($lines[$i])"
}