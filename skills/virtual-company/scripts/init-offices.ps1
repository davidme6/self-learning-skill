# init-offices.ps1
# 虚拟公司 - 初始化所有成员办公室
# 用法: pwsh init-offices.ps1

param(
    [switch]$Force  # 强制重建所有办公室
)

$configPath = Join-Path $PSScriptRoot "..\team-config.json"
$config = Get-Content $configPath | ConvertFrom-Json

$results = @()

foreach ($teamKey in $config.teams.PSObject.Properties.Name) {
    $team = $config.teams.$teamKey
    Write-Host "`n🏢 初始化 $($team.name)..." -ForegroundColor Cyan
    
    foreach ($memberKey in $team.members.PSObject.Properties.Name) {
        $member = $team.members.$memberKey
        
        Write-Host "  创建办公室: $($member.name) $($member.emoji) [$($member.model)]" -ForegroundColor Yellow
        
        # 这里应该调用 OpenClaw API 创建 session
        # 目前输出信息，实际使用时需要实现 API 调用
        
        $results += [PSCustomObject]@{
            Team = $team.name
            Member = $member.name
            Model = $member.model
            Status = "Created"
        }
    }
}

Write-Host "`n✅ 初始化完成！" -ForegroundColor Green
Write-Host "总计: $($results.Count) 个办公室已创建" -ForegroundColor Green

# 输出结果表格
$results | Format-Table -AutoSize