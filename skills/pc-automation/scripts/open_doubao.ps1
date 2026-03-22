# 打开豆包网页并发送消息 - PowerShell 版本

param(
    [string]$url = "https://www.doubao.com",
    [string]$message = "你好"
)

Write-Host "[INFO] Starting Doubao automation..." -ForegroundColor Cyan
Write-Host "[INFO] URL: $url" -ForegroundColor Cyan
Write-Host "[INFO] Message: $message" -ForegroundColor Cyan
Write-Host ""

# 1. 打开浏览器
Write-Host "  1. Opening browser..." -ForegroundColor Yellow
Start-Process $url
Start-Sleep -Seconds 5

# 2. 等待页面加载
Write-Host "  2. Waiting for page to load..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# 3. 激活浏览器窗口
Write-Host "  3. Activating browser window..." -ForegroundColor Yellow
$wshell = New-Object -ComObject wscript.shell
$wshell.AppActivate("豆包")
Start-Sleep -Milliseconds 500

# 4. 使用 Tab 键导航到输入框
Write-Host "  4. Navigating to input box..." -ForegroundColor Yellow
for ($i = 0; $i -lt 10; $i++) {
    $wshell.SendKeys("{TAB}")
    Start-Sleep -Milliseconds 200
}

# 5. 输入消息
Write-Host "  5. Typing message..." -ForegroundColor Yellow
foreach ($char in $message.ToCharArray()) {
    $wshell.SendKeys($char)
    Start-Sleep -Milliseconds 100
}

Start-Sleep -Seconds 1

# 6. 按 Enter 发送
Write-Host "  6. Sending message..." -ForegroundColor Yellow
$wshell.SendKeys("{ENTER}")

Write-Host ""
Write-Host "[SUCCESS] Done!" -ForegroundColor Green
