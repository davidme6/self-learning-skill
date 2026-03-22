# 📖 DeepReader 部署说明

## ✅ 已安装

| 技能 | 状态 | 位置 |
|------|------|------|
| **DeepReader** | ✅ 已安装 | `C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\skills\deepreader\` |

---

## 🎯 功能

**自动将网页内容转换为 Markdown 保存到记忆库**

| 支持的平台 | 内容类型 | API Key |
|-----------|---------|---------|
| **Twitter/X** | 推文、线程、个人主页 | ❌ 无需 |
| **Reddit** | 帖子 + 热门评论 | ❌ 无需 |
| **YouTube** | 视频字幕/转录 | ❌ 无需 |
| **任意网页** | 博客、文章、文档 | ❌ 无需 |

---

## 🚀 使用方式

### 自动触发
当消息中包含 URL 时，DeepReader 会自动：
1. 检测 URL
2. 抓取内容
3. 清理格式
4. 保存为 Markdown 到记忆库

### 示例

```
用户：看看这个 https://x.com/user/status/123456

DeepReader 自动抓取 → 保存为 .md 文件 → 存入记忆库
```

---

## 📁 输出格式

保存的文件包含结构化 YAML 头信息：

```markdown
---
title: "Tweet by @user"
source_url: "https://x.com/user/status/123456"
domain: "x.com"
parser: "twitter"
ingested_at: "2026-02-16T12:00:00Z"
content_hash: "sha256:..."
word_count: 350
---

推文正文内容...
```

---

## ⚙️ 配置（可选）

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `DEEPREEDER_MEMORY_PATH` | `../../memory/inbox/` | 保存路径 |
| `DEEPREEDER_LOG_LEVEL` | `INFO` | 日志级别 |

### 创建 .env 文件（可选）

```bash
# 位置：工作区根目录\.env
DEEPREEDER_MEMORY_PATH=C:/Windows/System32/UsersAdministrator.openclawworkspace/memory/deepreader
DEEPREEDER_LOG_LEVEL=DEBUG
```

---

## 📦 文件结构

```
deepreader/
├── SKILL.md              # 技能定义
├── manifest.json         # 配置清单
├── requirements.txt      # Python 依赖
├── __init__.py           # 初始化
├── core/
│   ├── router.py         # URL 路由
│   ├── storage.py        # 存储逻辑
│   └── utils.py          # 工具函数
└── integrations/
    ├── twitter.py        # Twitter 解析
    ├── youtube.py        # YouTube 转录
    ├── reddit.py         # Reddit 解析
    └── generic.py        # 通用网页解析
```

---

## ✅ 优势

| 特点 | 说明 |
|------|------|
| **零 API Key** | 完全免费，无需注册任何服务 |
| **自动触发** | 检测到 URL 自动抓取 |
| **多平台支持** | Twitter/Reddit/YouTube/任意网页 |
| **清理格式** | 输出干净的 Markdown |
| **结构化存储** | YAML 头信息 + 内容 |
| **批量处理** | 支持一次处理多个 URL |

---

## 🔧 依赖

需要 Python 环境（如果还没有）：

```bash
# 安装 Python
https://python.org

# 安装依赖
pip install -r deepreader/requirements.txt
```

---

## 💡 使用场景

- ✅ 保存 Twitter 热门推文到知识库
- ✅ 归档 Reddit 技术讨论
- ✅ 提取 YouTube 视频教程字幕
- ✅ 批量保存博客文章
- ✅ 建立个人知识索引

---

## 🆚 与 Firecrawl 对比

| 功能 | DeepReader | Firecrawl |
|------|-----------|-----------|
| **API Key** | ❌ 无需 | ✅ 需要 |
| **成本** | ✅ 免费 | ⚠️ 500 页/月免费 |
| **自动触发** | ✅ 是 | ❌ 需手动调用 |
| **平台支持** | ✅ Twitter/Reddit/YouTube | ✅ 通用网页 |
| **输出格式** | ✅ Markdown + YAML | ✅ Markdown |
| **防反爬虫** | ⚠️ 基础 | ✅ 高级 |

**建议：** 两者互补使用
- DeepReader：日常 URL 自动抓取（免费）
- Firecrawl：需要防反爬虫的高级场景

---

**部署完成！现在分享 URL 会自动保存到记忆库！** 🚀
