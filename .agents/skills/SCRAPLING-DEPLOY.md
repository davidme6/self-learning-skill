# 🕷️ Scrapling 部署说明

## ✅ 已安装

| 技能 | 状态 | 版本 | 位置 |
|------|------|------|------|
| **scrapling-official** | ✅ 已安装 | v0.4.2 | `.agents\skills\scrapling-official\` |

---

## 🎯 核心功能

**高级网页爬虫 - 绕过反爬虫系统**

| 功能 | 说明 |
|------|------|
| **绕过 Cloudflare** | 自动处理 Turnstile 验证 |
| **隐身浏览** | 无头浏览器 + 防检测 |
| **自适应解析** | 网站更新后自动调整选择器 |
| **蜘蛛框架** | 支持大规模并发爬取 |
| **代理轮换** | 自动代理池管理 |
| **暂停/恢复** | 断点续爬 |

---

## 📦 与其他爬虫技能对比

| 技能 | 优势 | 适用场景 | API Key |
|------|------|---------|---------|
| **DeepReader** | 自动触发 + 免费 | 日常 URL 保存 | ❌ 无需 |
| **Firecrawl** | 简单 + 高质量 | 付费内容/新闻 | ✅ 需要 |
| **Scrapling** | 最强反爬虫 + 本地 | 大规模爬取/定制 | ❌ 无需 |

---

## 🔧 安装依赖

### 方式 1: Python 环境（推荐）

```bash
# 1. 创建虚拟环境
python -m venv scrapling-env

# 2. 激活环境
scrapling-env\Scripts\Activate.ps1

# 3. 安装 Scrapling
pip install "scrapling[all]>=0.4.2"

# 4. 下载浏览器依赖
scrapling install --force
```

### 方式 2: Docker（无需 Python）

```bash
# 拉取镜像
docker pull pyd4vinci/scrapling

# 或
docker pull ghcr.io/d4vinci/scrapling:latest
```

---

## 🚀 CLI 使用示例

### 基础爬取

```bash
# 简单网页 → Markdown
scrapling extract get "https://example.com" article.md

# 保存原始 HTML
scrapling extract get "https://example.com" page.html

# 提取特定元素（CSS 选择器）
scrapling extract get "https://example.com" content.txt -s ".article-body"
```

### 动态网站

```bash
# 需要 JavaScript 渲染
scrapling extract fetch "https://react-app.com" page.md

# 有反爬虫保护（Cloudflare 等）
scrapling extract stealthy-fetch "https://protected-site.com" page.md
```

### 大规模爬取

```bash
# 并发爬取多个 URL
scrapling spider run sitemap.xml --concurrency 10

# 带代理轮换
scrapling spider run urls.txt --proxy-rotate
```

---

## 💻 Python 代码示例

```python
from scrapling import Fetcher

# 基础爬取
fetcher = Fetcher()
response = fetcher.get('https://example.com')
print(response.html)
print(response.css('.title::text').get())

# 绕过 Cloudflare
fetcher = Fetcher(stealth=True)
response = fetcher.get('https://protected-site.com')

# 提取数据
data = {
    'title': response.css('h1::text').get(),
    'content': response.css('.content::text').getall()
}
```

---

## 🆚 三个爬虫技能使用决策树

```
需要爬取 URL 内容？
│
├── 日常 URL 自动保存 → DeepReader（免费 + 自动）
│   - Twitter/Reddit/YouTube
│   - 博客文章
│   - 自动保存到记忆库
│
├── 付费内容/高质量需求 → Firecrawl（stealth 代理）
│   - WSJ/NYT 等付费墙
│   - 需要 API 质量保证
│   - 预算：500 页/月免费
│
└── 大规模/自定义爬取 → Scrapling（本地库）
    - 绕过 Cloudflare 等反爬虫
    - 并发爬取数千页
    - 需要完全控制
    - 预算有限（免费）
```

---

## 📁 文件结构

```
scrapling-official/
├── SKILL.md              # 技能定义
├── LICENSE.txt           # 许可证
├── __init__.py           # 初始化
├── core/
│   ├── fetcher.py        # 抓取器
│   ├── parser.py         # 解析器
│   └── spider.py         # 蜘蛛框架
└── examples/
    ├── basic.py          # 基础示例
    └── advanced.py       # 高级示例
```

---

## ⚠️ 注意事项

### 合法合规
- ✅ 遵守 robots.txt
- ✅ 尊重网站服务条款
- ✅ 控制请求频率
- ❌ 不要用于非法目的

### 技术限制
- 需要 Python 3.10+ 或 Docker
- 首次使用需下载浏览器依赖（约 200MB）
- 大规模爬取需要代理池

---

## 💡 最佳实践

### 1. 选择合适的工具
```
简单网页 → get
动态内容 → fetch
反爬虫保护 → stealthy-fetch
```

### 2. 控制频率
```python
import time
from scrapling import Fetcher

fetcher = Fetcher()
for url in urls:
    response = fetcher.get(url)
    time.sleep(1)  # 限速
```

### 3. 错误处理
```python
try:
    response = fetcher.get(url, timeout=30)
    if response.status_code == 200:
        # 处理成功
    else:
        # 处理失败
except Exception as e:
    print(f"Error: {e}")
```

---

## 🎯 使用场景

| 场景 | 推荐命令 |
|------|---------|
| 保存博客文章 | `scrapling extract get url article.md` |
| 爬取电商价格 | `scrapling extract stealthy-fetch url price.md -s ".price"` |
| 监控新闻更新 | Python 脚本 + 定时任务 |
| 大规模数据采集 | `scrapling spider run urls.txt --concurrency 10` |
| 绕过 Cloudflare | `scrapling extract stealthy-fetch url page.md` |

---

## 📊 性能对比

| 指标 | Scrapling | Firecrawl | DeepReader |
|------|-----------|-----------|------------|
| **速度** | ⚡⚡⚡⚡⚡ | ⚡⚡⚡⚡ | ⚡⚡⚡⚡⚡ |
| **反爬虫** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **成本** | 免费 | 付费 | 免费 |
| **易用性** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **灵活性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

---

**部署完成！现在有三个互补的爬虫工具可用！** 🚀

---

## 📋 总结

| 技能 | 状态 | 用途 |
|------|------|------|
| DeepReader | ✅ 已安装 | 日常 URL 自动保存（免费） |
| Firecrawl | ✅ 已安装 | 高质量爬取（500 页/月免费） |
| Scrapling | ✅ 已安装 | 高级反爬虫（完全免费） |

**三个工具互补，覆盖所有爬取需求！**
