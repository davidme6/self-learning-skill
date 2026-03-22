# 🔐 Credential Manager - 凭证安全管理系统

## 功能

安全存储和管理敏感信息（账号、密码、API Key 等），使用 Windows DPAPI 加密保护。

## 安全特性

- ✅ **加密存储** - 使用 Windows DPAPI 加密，只有你的用户账号能解密
- ✅ **不显示明文** - 存储时不显示密码，读取时仅输出 JSON
- ✅ **文件权限** - 加密文件仅当前用户可访问（600 权限）
- ✅ **用完即清** - 解密后在内存中使用，不保留历史记录

## 使用方法

### 存储凭证
```bash
python .agents/skills/credential-manager/cred.py store <服务名> <账号> <密码>
```

示例（即梦）：
```bash
python .agents/skills/credential-manager/cred.py store jimeng 13800138000 your_password
```

### 读取凭证
```bash
python .agents/skills/credential-manager/cred.py get <服务名>
```

输出（JSON 格式，供脚本使用）：
```json
{"service": "jimeng", "username": "13800138000", "password": "your_password"}
```

### 列出所有服务
```bash
python .agents/skills/credential-manager/cred.py list
```

### 删除凭证
```bash
python .agents/skills/credential-manager/cred.py delete <服务名>
```

## 存储位置

```
C:\Users\Administrator\.openclaw\credentials\
├── jimeng.json.enc    # 即梦账号（加密）
└── ...
```

## 与浏览器自动化配合使用

```bash
# 1. 先存储凭证（只需一次）
python .agents/skills/credential-manager/cred.py store jimeng 13800138000 mypassword

# 2. 自动化登录时读取
$creds = python .agents/skills/credential-manager/cred.py get jimeng

# 3. 浏览器自动填充（脚本中处理）
# browse fill "#username" $creds.username
# browse fill "#password" $creds.password
```

## 安全提醒

- ⚠️ 不要将密码告诉任何人（包括在聊天记录中）
- ⚠️ 使用此系统存储后，删除聊天记录中的密码消息
- ⚠️ 定期检查和清理不需要的凭证
- ⚠️ 如怀疑泄露，立即删除并修改密码

---

*安全是习惯，不是选项。*
