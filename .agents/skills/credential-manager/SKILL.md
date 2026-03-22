# Credential Manager - 安全凭证管理

安全存储和管理敏感信息（账号、密码、API Key 等），使用加密保护用户隐私。

## 安全原则

1. **加密存储** - 所有敏感信息必须加密后存储
2. **最小暴露** - 只在需要时解密，用完立即清理
3. **不记录日志** - 敏感操作不写入日志或记忆
4. **用户授权** - 每次访问敏感信息需用户确认

## 加密方式（Windows）

使用 PowerShell 的 `SecureString` 和 DPAPI：

```powershell
# 加密字符串
$secure = ConvertTo-SecureString "plain_text_password" -AsPlainText -Force
$encrypted = ConvertFrom-SecureString $secure
# $encrypted 可安全存储到文件

# 解密字符串
$secure = ConvertTo-SecureString $encrypted_string
$plain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
)
# 使用后立即清除变量
```

## 存储位置

敏感数据存储在：`~/.openclaw/credentials/`

文件结构：
```
~/.openclaw/credentials/
├── jimeng.json.enc    # 即梦账号（加密）
├── github.json.enc    # GitHub Token（加密）
└── ...
```

## 使用命令

### 存储凭证
```powershell
python skills/credential-manager/scripts/store.py <service> <username> <password>
```

### 读取凭证
```powershell
python skills/credential-manager/scripts/retrieve.py <service>
```

### 删除凭证
```powershell
python skills/credential-manager/scripts/delete.py <service>
```

### 列出服务（不显示密码）
```powershell
python skills/credential-manager/scripts/list.py
```

## 自动化流程

当需要登录网站时：

1. **检查是否已存储凭证**
   ```bash
   python skills/credential-manager/scripts/retrieve.py jimeng
   ```

2. **如未存储，提示用户输入**
   - 用户输入后加密存储
   - 不显示在聊天记录中

3. **使用凭证登录**
   - 解密后直接填入浏览器
   - 不在日志中保留明文

4. **清理内存**
   - 使用后立即清除变量
   - 不写入会话历史

## 最佳实践

- ✅ 使用加密文件存储
- ✅ 每次使用前确认
- ✅ 用完清理内存变量
- ✅ 不记录敏感操作到 MEMORY.md
- ❌ 不要明文存储密码
- ❌ 不要在聊天记录中显示密码
- ❌ 不要将密码写入日志

## 示例：即梦登录

```bash
# 1. 存储账号（只需做一次）
python skills/credential-manager/scripts/store.py jimeng "手机号" "密码"

# 2. 自动化登录时使用
$creds = python skills/credential-manager/scripts/retrieve.py jimeng
# 返回 JSON: {"username": "...", "password": "..."}

# 3. 浏览器自动填充
browse fill "#username" $creds.username
browse fill "#password" $creds.password
browse click "#login-btn"
```

---

*安全第一，便利第二。宁可多一步确认，不要泄露用户隐私。*
