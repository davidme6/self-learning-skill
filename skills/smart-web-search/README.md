# 🌐 Smart Web Search - 智能搜索切换

> 根据查询内容**自动选择最优搜索引擎**，无需手动指定。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)

---

## 🚀 快速开始

### 安装

```bash
# 通过 ClawHub 安装（发布后）
clawhub install smart-web-search

# 或手动安装
git clone https://github.com/davidme6/openclaw-skills.git
cp -r openclaw-skills/skills/smart-web-search ~/.openclaw/skills/
```

### 使用

直接使用自然语言搜索，**自动判断最优引擎**：

```
"搜索 XXX"
"search for XXX"
"帮我找一下 XXX"
"find XXX"
"上网查 XXX"
```

---

## 🧠 智能判断逻辑

### 自动选择规则

| 查询类型 | 自动使用 | 引擎 |
|---------|---------|------|
| 🇨🇳 中文内容 | CN Web Search | 360/搜狗/必应中文 |
| 🌍 英文内容 | DuckDuckGo | DDG Lite |
| 🇨🇳 国内话题（微信、淘宝等） | CN Web Search | 搜狗微信/360 |
| 🌍 国际话题（GitHub、Stack Overflow） | DuckDuckGo | DDG/Qwant |

### 示例

```
用户：搜索一下英伟达的最新财报
→ 自动使用：360 搜索

用户：search for latest AI news
→ 自动使用：DuckDuckGo

用户：帮我找找关于人工智能的公众号文章
→ 自动使用：搜狗微信搜索

用户：find Python tutorials on GitHub
→ 自动使用：DuckDuckGo
```

---

## 🔧 技术实现

### 国内引擎（CN Search）

```
主引擎：
- 360 搜索：https://m.so.com/s?q=查询
- 搜狗微信：https://weixin.sogou.com/weixin?type=2&query=查询
- 必应中文：https://cn.bing.com/search?q=查询

备选：
- 搜狗网页：https://www.sogou.com/web?query=查询
```

### 国际引擎（DuckDuckGo）

```
主引擎：
- DuckDuckGo Lite：https://lite.duckduckgo.com/lite/?q=query

备选：
- Qwant：https://www.qwant.com/?q=query&t=web
- Startpage：https://www.startpage.com/do/search?q=query
- 必应英文：https://www.bing.com/search?q=query
```

---

## 📋 特性

- ✅ **零配置** - 无需 API Key，全部免费
- ✅ **智能切换** - 自动判断语言和内容类型
- ✅ **双引擎支持** - 国内 + 国际全覆盖
- ✅ **自动重试** - 主引擎失败自动切换备用
- ✅ **隐私友好** - 不追踪用户数据
- ✅ **快速响应** - 直接抓取搜索结果页

---

## 🛠️ 技能结构

```
smart-web-search/
├── SKILL.md          # 技能清单（Agent 读取）
├── _meta.json        # 元数据（ClawHub 需要）
├── README.md         # 本文档
└── tools/            # 工具脚本（可选）
```

---

## 📊 引擎对比

| 引擎 | 地区 | 免费 | API Key | 中文结果 | 英文结果 |
|------|------|------|---------|---------|---------|
| 360 搜索 | 🇨🇳 | ✅ | ❌ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| 搜狗微信 | 🇨🇳 | ✅ | ❌ | ⭐⭐⭐⭐⭐ | ⭐ |
| 必应中文 | 🇨🇳 | ✅ | ❌ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| DuckDuckGo | 🌍 | ✅ | ❌ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Qwant | 🌍 | ✅ | ❌ | ⭐⭐ | ⭐⭐⭐⭐ |

---

## 🔒 安全说明

- ✅ **无外部依赖** - 仅使用内置 `web_fetch` 工具
- ✅ **无 API Key** - 不需要任何凭证
- ✅ **无数据收集** - 不存储用户搜索记录
- ✅ **开源透明** - 代码完全公开可审查

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发环境

```bash
git clone https://github.com/davidme6/openclaw-skills.git
cd openclaw-skills/skills/smart-web-search
# 编辑 SKILL.md 或其他文件
# 测试后提交 PR
```

### 提交规范

- 清晰的提交信息
- 遵循现有代码风格
- 添加必要的测试（如适用）
- 更新文档

---

## 📝 更新日志

### v1.0.0 (2026-03-17)

- ✅ 初始版本发布
- ✅ 支持国内/国际智能切换
- ✅ 集成 360、搜狗、DuckDuckGo 等引擎
- ✅ 自动语言判断
- ✅ 零配置使用

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🔗 相关链接

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [ClawHub 技能市场](https://clawhub.ai)
- [GitHub 仓库](https://github.com/davidme6/openclaw-skills)
- [Discord 社区](https://discord.gg/clawd)

---

## 💬 反馈

遇到问题或有建议？

- 🐛 [提交 Issue](https://github.com/davidme6/openclaw-skills/issues)
- 💡 [讨论区](https://github.com/davidme6/openclaw-skills/discussions)
- 📧 联系作者

---

*Made with ❤️ by Jarvis for OpenClaw Community*
