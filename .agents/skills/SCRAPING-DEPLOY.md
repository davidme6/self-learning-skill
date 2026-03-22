# 🕷️ Scraping Skills 部署说明

## ✅ 已安装的 Skills

| Skill | 状态 | 功能 |
|-------|------|------|
| **firecrawl-scraping** | ✅ 已安装 | Firecrawl API 网页爬取 |
| **web-scraping** | ⚠️ 部分安装 | 通用爬虫技能（需 Python 环境） |

---

## 🔧 Firecrawl Scraping 使用指南

### 1. 获取 API Key

访问：https://firecrawl.dev/app/api-keys

**免费额度：** 每月 500 credits（约 500 页）

### 2. 配置 API Key

创建 `.env` 文件：

```bash
# 位置：C:\Windows\System32\UsersAdministrator.openclawworkspace\.env
FIRECRAWL_API_KEY=fc-your-api-key-here
```

### 3. 安装 Python 依赖

```bash
# 安装 Python（如果没有）
# 从 https://python.org 下载并安装

# 安装依赖
pip install firecrawl-py python-dotenv requests
```

### 4. 使用示例

```bash
# 简单爬取
python .agents/skills/firecrawl-scraping/scripts/firecrawl_scrape.py "https://example.com"

# 带选项
python .agents/skills/firecrawl-scraping/scripts/firecrawl_scrape.py "https://example.com" --proxy stealth --formats markdown,summary

# 输出到文件
python .agents/skills/firecrawl-scraping/scripts/firecrawl_scrape.py "https://example.com" --output .tmp/result.json
```

---

## 🛡️ 防反爬虫功能

### Firecrawl 内置功能

| 功能 | 说明 |
|------|------|
| **JavaScript 渲染** | 自动处理动态内容 |
| **代理轮换** | 避免 IP 封禁 |
| **验证码解决** | 自动处理 CAPTCHA |
| **请求限速** | 避免被封 |
| **User-Agent 轮换** | 模拟真实浏览器 |

### Proxy 模式

| 模式 | 适用场景 |
|------|---------|
| `basic` | 普通网站，速度快 |
| `stealth` | 反爬虫严格的网站（WSJ、NYT 等） |
| `auto` | 自动选择（推荐） |

---

## 📋 通用 Web Scraping 技能

### 需要的 Python 库

```bash
pip install requests beautifulsoup4 selenium playwright scrapy lxml
playwright install  # 安装浏览器
```

### 功能清单

- ✅ requests + BeautifulSoup：静态网站
- ✅ Selenium/Playwright：动态网站
- ✅ Scrapy：大规模爬取
- ✅ jina AI：智能提取

---

## ⚠️ 注意事项

### 合法合规

- ✅ 遵守 robots.txt
- ✅ 尊重网站服务条款
- ✅ 不要过度请求
- ✅ 仅爬取公开内容
- ❌ 不要绕过付费墙（除非有合法权限）
- ❌ 不要爬取个人隐私数据

### 技术限制

- 需要 Python 环境
- Firecrawl 有免费额度限制
- 大规模爬取需要付费 API

---

## 🚀 快速测试

### 测试 Firecrawl

```bash
# 1. 先设置 API Key
echo "FIRECRAWL_API_KEY=你的 key" > .env

# 2. 安装 Python 依赖
pip install firecrawl-py python-dotenv

# 3. 测试脚本
python .agents/skills/firecrawl-scraping/scripts/firecrawl_scrape.py "https://example.com"
```

### 测试结果

成功的话会输出：
- Markdown 格式内容
- 页面元数据
- 保存的文件路径

---

## 💰 成本说明

| 服务 | 免费额度 | 付费价格 |
|------|---------|---------|
| Firecrawl | 500 credits/月 | $19/月起 |
| 自建爬虫 | 无限 | 时间成本 + 代理费用 |

**建议：** 先用免费额度测试，确定需求后再考虑付费。

---

## 📁 文件位置

```
C:\Windows\System32\UsersAdministrator.openclawworkspace\.agents\skills\
├── firecrawl-scraping/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── firecrawl_scrape.py
│   └── references/
│       ├── single-page.md
│       └── website-crawler.md
├── web-scraping/
│   └── SKILL.md
└── SCRAPING-DEPLOY.md (本文件)
```

---

**下一步：**
1. 获取 Firecrawl API Key
2. 安装 Python（如未安装）
3. 创建 .env 文件
4. 运行测试脚本

**有问题随时问我！** 🚀
