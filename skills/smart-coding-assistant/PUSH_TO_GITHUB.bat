@echo off
REM 推送到 GitHub 的批处理脚本
REM 使用方法：双击运行或在命令行执行

echo ========================================
echo  推送到 GitHub
echo ========================================
echo.

REM 检查网络连接
echo [1/4] 检查网络连接...
ping -n 2 github.com | find "TTL=" >nul
if %errorlevel% neq 0 (
    echo [ERROR] 无法连接到 GitHub，请检查网络连接
    pause
    exit /b 1
)
echo [OK] 网络连接正常
echo.

REM 检查 Git 状态
echo [2/4] 检查 Git 状态...
git status
if %errorlevel% neq 0 (
    echo [ERROR] Git 状态检查失败
    pause
    exit /b 1
)
echo.

REM 推送
echo [3/4] 推送到 GitHub...
git config --global http.postBuffer 524288000
git push origin main
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] 推送失败，可能是网络问题
    echo.
    echo 建议：
    echo 1. 稍后重试
    echo 2. 使用 GitHub Desktop
    echo 3. 配置 SSH 密钥后使用 SSH 方式
    echo.
    pause
    exit /b 1
)
echo.

REM 验证
echo [4/4] 验证推送...
echo 请访问仓库查看：https://github.com/davidme6/self-learning-skill
echo.
echo [SUCCESS] 推送成功！
echo ========================================
pause
