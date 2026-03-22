# 即梦自动化登录方案

## 问题

本地没有安装 Chrome 浏览器，`browse` CLI 无法启动。

## 解决方案

### 方案 A：安装 Chrome（推荐）

```powershell
# 下载 Chrome 安装程序
Invoke-WebRequest -Uri "https://dl.google.com/chrome/install/latest/chrome_installer.exe" -OutFile "$env:TEMP\chrome_installer.exe"

# 静默安装
Start-Process -FilePath "$env:TEMP\chrome_installer.exe" -ArgumentList "/silent /install" -Wait
```

### 方案 B：配置 Browserbase（远程浏览器）

1. 注册 Browserbase: https://browserbase.com/
2. 获取 API Key 和 Project ID
3. 设置环境变量：
   ```bash
   $env:BROWSERBASE_API_KEY="your_api_key"
   $env:BROWSERBASE_PROJECT_ID="your_project_id"
   ```

### 方案 C：使用 Edge（需要修改 browse 配置）

Edge 已安装在：`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`

但 browse CLI 默认使用 Chrome，需要配置。

## 当前状态

- ✅ 账号已加密存储：`jimeng` (18516982443)
- ❌ 浏览器不可用（缺少 Chrome）
- ⏸️ 等待浏览器配置完成

## 下一步

选择方案 A/B/C 后继续自动化登录流程。
