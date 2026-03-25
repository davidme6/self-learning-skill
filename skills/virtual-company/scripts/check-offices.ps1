# check-offices.ps1
# 虚拟公司 - 检查所有成员办公室状态
# 用法: pwsh check-offices.ps1

param(
    [switch]$Repair  # 自动修复失效的办公室
)

$configPath = Join-Path $PSScriptRoot "..\team-config.json"
$sessionsPath = Join-Path $PSScriptRoot "..\.team-sessions.json"

Write-Host "🔍 检查虚拟公司状态..." -ForegroundColor Cyan
Write-Host "=" * 50

# 读取配置
$config = Get-Content $configPath | ConvertFrom-Json
$sessions = if (Test-Path $sessionsPath) { Get-Content $sessionsPath | ConvertFrom-Json } else { @{teams=@{}} }

$totalMembers = 0
$activeSessions = 0
$inactiveSessions = 0

foreach ($teamKey in $config.teams.PSObject.Properties.Name) {
    $team = $config.teams.$teamKey
    Write-Host "`n🏢 $($team.name)" -ForegroundColor Cyan
    
    foreach ($memberKey in $team.members.PSObject.Properties.Name) {
        $member = $team.members.$memberKey
        $totalMembers++
        
        # 检查 session 是否存在
        $sessionKey = if ($sessions.teams.$teamKey.members.$memberKey.sessionKey) { 
            $sessions.teams.$teamKey.members.$memberKey.sessionKey 
        } else { 
            $null 
        }
        
        if ($sessionKey) {
            Write-Host "  ✅ $($member.name): 活跃 [$($member.model)]" -ForegroundColor Green
            $activeSessions++
        } else {
            Write-Host "  ❌ $($member.name): 未创建" -ForegroundColor Red
            $inactiveSessions++
        }
    }
}

Write-Host "`n" + "=" * 50
Write-Host "📊 统计:" -ForegroundColor Cyan
Write-Host "  总成员数: $totalMembers"
Write-Host "  活跃办公室: $activeSessions" -ForegroundColor Green
Write-Host "  未创建: $inactiveSessions" -ForegroundColor $(if ($inactiveSessions -gt 0) { "Red" } else { "Green" })

if ($inactiveSessions -gt 0 -and $Repair) {
    Write-Host "`n🔧 自动修复模式..." -ForegroundColor Yellow
    & "$PSScriptRoot\init-offices.ps1" -Force
} elseif ($inactiveSessions -gt 0) {
    Write-Host "`n💡 提示: 运行 init-offices.ps1 创建缺失的办公室" -ForegroundColor Yellow
}