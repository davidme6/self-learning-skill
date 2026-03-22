# 打开豆包网页并发送消息 - 优化版 PowerShell

param(
    [string]$url = "https://www.doubao.com",
    [string]$message = "你好"
)

$ErrorActionPreference = "Stop"

Write-Host "[INFO] Starting Doubao automation (Optimized)..." -ForegroundColor Cyan
Write-Host "[INFO] URL: $url" -ForegroundColor Cyan
Write-Host "[INFO] Message: $message" -ForegroundColor Cyan
Write-Host ""

try {
    # 1. 打开浏览器（使用 Edge）
    Write-Host "  1. Opening Edge browser..." -ForegroundColor Yellow
    $edge = New-Object -ComObject MSEdge.Application
    $edge.Visible = $true
    $edge.Navigate($url)
    Start-Sleep -Seconds 5
    
    # 2. 等待页面加载
    Write-Host "  2. Waiting for page load..." -ForegroundColor Yellow
    Start-Sleep -Seconds 3
    
    # 3. 使用 COM 自动化直接操作（比 SendKeys 快）
    Write-Host "  3. Finding input element..." -ForegroundColor Yellow
    
    # 尝试多种选择器定位输入框
    $selectors = @(
        "textarea[placeholder*='输入']",
        "textarea[placeholder*='消息']",
        "textarea",
        "input[type='text']",
        "[contenteditable='true']",
        ".input-box",
        "#chat-input"
    )
    
    $inputElement = $null
    foreach ($selector in $selectors) {
        try {
            $element = $edge.Document.querySelector($selector)
            if ($element) {
                $inputElement = $element
                Write-Host "     Found: $selector" -ForegroundColor Green
                break
            }
        } catch {
            continue
        }
    }
    
    if ($inputElement) {
        # 4. 直接设置值（比逐字符快 10 倍）
        Write-Host "  4. Setting message value..." -ForegroundColor Yellow
        $inputElement.value = $message
        Start-Sleep -Milliseconds 500
        
        # 5. 触发输入事件（让页面知道有输入）
        Write-Host "  5. Triggering input event..." -ForegroundColor Yellow
        $event = $edge.Document.createEvent("HTMLEvents")
        $event.initEvent("input", $true, $false)
        $inputElement.dispatchEvent($event)
        
        # 6. 点击发送按钮
        Write-Host "  6. Finding send button..." -ForegroundColor Yellow
        $sendButton = $edge.Document.querySelector("button[class*='send'], .send-btn, [aria-label*='发送']")
        
        if ($sendButton) {
            $sendButton.click()
            Write-Host "     Send button clicked!" -ForegroundColor Green
        } else {
            # 没找到发送按钮就按 Enter
            Write-Host "     No send button, pressing Enter..." -ForegroundColor Yellow
            $wshell = New-Object -ComObject wscript.shell
            $wshell.SendKeys("{ENTER}")
        }
        
        Write-Host ""
        Write-Host "[SUCCESS] Message sent!" -ForegroundColor Green
        
    } else {
        Write-Host "[ERROR] Could not find input box" -ForegroundColor Red
        Write-Host "[INFO] Falling back to keyboard method..." -ForegroundColor Yellow
        
        # 回退到键盘方式
        $wshell = New-Object -ComObject wscript.shell
        Start-Sleep -Seconds 2
        
        # Tab 导航
        for ($i = 0; $i -lt 15; $i++) {
            $wshell.SendKeys("{TAB}")
            Start-Sleep -Milliseconds 100
        }
        
        # 输入消息（一次性，不是逐字符）
        $wshell.SendKeys($message)
        Start-Sleep -Seconds 1
        $wshell.SendKeys("{ENTER}")
        
        Write-Host "[SUCCESS] Sent via keyboard fallback" -ForegroundColor Green
    }
    
} catch {
    Write-Host "[ERROR] $_" -ForegroundColor Red
    Write-Host "[INFO] Exception occurred" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[DONE] Automation complete" -ForegroundColor Cyan
