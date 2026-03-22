---
name: smart-web-search
description: Smart Web Search v3.1 - Intelligent search with Baidu (China) and Google (International) as primary engines. Real-time news, ad filtering, content de-toxication, multi-engine aggregation. Auto-detects query language for accurate results.
version: 3.1.0
author: Jarvis
triggers:
  - search
  - find
  - web search
  - real-time news
  - latest news
  - today news
  - latest
  - verified search
  - safe search
  - filter ads
  - no ads
  - search with Baidu
  - search with Google
---

# 🌐 Smart Web Search v3.1

**Primary Engines**: Baidu (China) + Google (International)

**Core Features**:
- ✅ **Real-time Search** - Today/24h/7d/30d time filtering
- ✅ **Time Filtering** - Specify search time range
- ✅ **Multi-engine Aggregation** - Search 3-5 engines simultaneously
- ✅ **Smart De-duplication** - Auto-filter duplicate content
- ✅ **AI Summaries** - Auto-generated key insights
- ✅ **Ad Filtering** - Auto-detect and filter ads/promotions
- ✅ **Content De-toxication** - Filter spam, fake news, misinformation
- ✅ **Baidu Integration** - China's largest search engine (Primary)
- ✅ **Google Integration** - World's most accurate engine (Primary)

Auto-selects optimal search engine based on query content.

---

## 🧠 Intelligent Detection Logic

### Use **Baidu Search** (China) When:
- 🇨🇳 Query contains Chinese characters
- 🇨🇳 Searching China-related topics (WeChat, Taobao, Baidu, etc.)
- 🇨🇳 Searching Chinese companies/people/events
- 🇨🇳 Searching Chinese policies/news/regulations

### Use **Google Search** (International) When:
- 🌍 Query is pure English
- 🌍 Searching international topics (GitHub, Stack Overflow, Reddit, etc.)
- 🌍 Searching foreign companies/people/events
- 🌍 Searching technical docs/academic papers/international news

---

## 🔧 Tool Calls

### Domestic Search (Chinese Queries)

**Primary Engine (Baidu):**
```
web_fetch(url="https://www.baidu.com/s?wd=query", extractMode="text", maxChars=15000)
```

**Advanced Search:**
```
# Exact match
web_fetch(url="https://www.baidu.com/s?wd=\"exact+keyword\"", extractMode="text", maxChars=15000)

# Exclude site
web_fetch(url="https://www.baidu.com/s?wd=keyword+-site:zhihu.com", extractMode="text", maxChars=15000)

# File type
web_fetch(url="https://www.baidu.com/s?wd=keyword+filetype:pdf", extractMode="text", maxChars=15000)
```

**Real-time News:**
```
# Latest 24 hours
web_fetch(url="https://www.baidu.com/s?wd=query+2026-03-17&src=news", extractMode="text", maxChars=15000)

# Latest 7 days
web_fetch(url="https://www.baidu.com/s?wd=query+this+week&src=news", extractMode="text", maxChars=15000)
```

**Backup Engines** (by priority):
1. **360 Search**: `https://m.so.com/s?q=query`
2. **Sogou WeChat**: `https://weixin.sogou.com/weixin?type=2&query=query`
3. **Bing CN**: `https://cn.bing.com/search?q=query`
4. **Sogou Web**: `https://www.sogou.com/web?query=query`
5. **Toutiao**: `https://www.toutiao.com/search/?keyword=query`

**Baidu Advantages**:
- ✅ Largest Chinese index (trillions of pages)
- ✅ Best localization for China
- ✅ Fastest update speed (minute-level)
- ✅ Advanced search syntax support
- ✅ Integrated with Baidu Baike, Zhidao, Tieba

### International Search (English Queries)

**Primary Engine (Google via Startpage):**
```
web_fetch(url="https://www.startpage.com/do/search?q=query", extractMode="text", maxChars=15000)
```

**Direct Google** (if accessible):
```
web_fetch(url="https://www.google.com/search?q=query", extractMode="text", maxChars=15000)
```

**Real-time News:**
```
# Latest 24 hours
web_fetch(url="https://www.startpage.com/do/search?q=query+2026-03-17", extractMode="text", maxChars=15000)

# Latest 7 days
web_fetch(url="https://www.startpage.com/do/search?q=query+this+week", extractMode="text", maxChars=15000)
```

**Backup Engines** (by priority):
1. **DuckDuckGo**: `https://lite.duckduckgo.com/lite/?q=query`
2. **DuckDuckGo News**: `https://duckduckgo.com/?q=query&ia=news`
3. **Qwant**: `https://www.qwant.com/?q=query&t=web`
4. **Bing EN**: `https://www.bing.com/search?q=query`
5. **Brave Search**: `https://search.brave.com/search?q=query`

**Google Advantages**:
- ✅ World's largest index (hundreds of billions of pages)
- ✅ Most advanced search algorithm
- ✅ Richest academic resources
- ✅ Best multi-language support
- ✅ Powerful advanced search features

---

## 📋 Usage Examples

### Chinese Queries

**Basic Search**:
```
User: Search NVIDIA latest financial report
→ Auto-use: Baidu Search
→ Time range: Auto-detect "latest" → 7 days
```

**Real-time News**:
```
User: Today March 17 latest news
→ Auto-use: Baidu News Search
→ Time range: 2026-03-17 (today)
→ Extra parameter: &src=news
```

**WeChat Articles**:
```
User: Find WeChat articles about AI
→ Auto-use: Sogou WeChat Search
→ Search type: WeChat official accounts
```

**Specified Time**:
```
User: Search AI news last 24 hours
→ Auto-use: Baidu Search + time filter
→ Time range: 2026-03-16 to 2026-03-17
```

### English Queries

**Basic Search**:
```
User: search for latest AI news
→ Auto-use: Google (via Startpage)
→ Time range: Auto-detect "latest" → 7 days
```

**Real-time News**:
```
User: today news March 17 2026
→ Auto-use: Google News
→ Time range: 2026-03-17 (today)
```

**Technical Content**:
```
User: find Python tutorials on GitHub
→ Auto-use: Google
→ Priority sources: GitHub, Stack Overflow
```

**Specified Time**:
```
User: latest tech news this week
→ Auto-use: Google
→ Time parameter: this week
```

### Mixed Queries

**International Company**:
```
User: Tesla TSLA stock price today
→ Priority: Google (international company)
→ Backup: Baidu (Chinese results)
```

**China Product**:
```
User: WeChat how to export data
→ Priority: Baidu (domestic product)
→ Backup: Google (English tutorials)
```

### Real-time Search (v3.1 Recommended)

**Today's News**:
```
"Search today March 17 AI news"
"NVIDIA latest news (24 hours)"
"latest AI news today March 17"
"2026-03-17 AI latest news"
```

**This Week**:
```
"Search this week AI news"
"AI latest news this week"
"Last 7 days AI updates"
```

---

## 🎯 Search Strategy v3.1

### Step 1: Language Detection
- Contains Chinese characters → Baidu (China)
- Pure English/Latin → Google (International)
- Mixed language → Judge by topic

### Step 2: Topic Detection
- China companies/products/policies → Baidu
- International companies/tech/academic → Google
- News/current events → Dual-engine parallel

### Step 3: Time Detection
**Auto-recognize time keywords**:
- "Today", "今日", "today" → 2026-03-17
- "Yesterday", "昨天" → 2026-03-16
- "Last 24h", "最近 24 小时" → Past 24 hours
- "This week", "本周" → Current week
- "Latest", "最新" → 7 days
- "This month", "本月" → 30 days

**No time keyword** → Default 30 days

### Step 4: Safety Detection
```
1. Detect if query involves sensitive topics
   - Medical/health → Enable strict de-tox
   - Finance/investment → Enable scam filter
   - News → Enable fake news filter

2. Set filter level
   - Normal search → Standard filter
   - "Verified", "safe" → Strict filter
   - "Academic", "research" → Authoritative source priority
```

### Step 5: Engine Selection
**Domestic Priority**:
1. **Baidu** (Largest Chinese engine) - PRIMARY
2. **360 Search** (General)
3. **360 News** (Real-time news)
4. **Sogou WeChat** (Official accounts)
5. **Bing CN** (Backup)
6. **Toutiao** (Breaking news)

**International Priority**:
1. **Google via Startpage** (Most accurate) - PRIMARY
2. **DuckDuckGo** (Privacy)
3. **DuckDuckGo News** (News)
4. **Qwant** (European)
5. **Bing EN** (Backup)
6. **Brave Search** (Privacy)

### Step 6: Multi-engine Aggregation
**Search 3 engines simultaneously**:
```
Primary: Baidu/Google
Backup 1: 360/Qwant
Backup 2: Bing
```

**Merge Strategy**:
- Collect top 10 results from each
- De-duplicate (URL + title similarity)
- Filter ads and toxic content
- Sort by time descending
- Keep 5-8 best results

### Step 7: Search + Fetch
1. Search 3 engines simultaneously
2. Merge and de-duplicate results
3. Filter ads (auto-detect)
4. De-toxicate (verify sources)
5. Select 3-5 most relevant URLs
6. Fetch detailed content with web_fetch
7. Generate AI summary

---

## ⚠️ Best Practices

### For Latest Information
```
✅ "Search today March 17 XXX news"
✅ "XXX latest news (24 hours)"
✅ "latest XXX news today"
❌ "Search XXX" (no time range, may return old news)
```

### For High Accuracy
```
✅ "March 17 2026 XXX latest news"
✅ "XXX + 2026-03-17"
✅ "XXX breaking news"
❌ "XXX news" (unclear time range)
```

### For Safe Search
```
✅ "Search vaccine info (verified)"
✅ "XXX safe search"
✅ "verified XXX info"
❌ Direct search for medical/finance (may encounter misinformation)
```

### For Baidu Search
```
✅ "Search with Baidu XXX"
✅ "XXX site:baidu.com"
✅ "XXX filetype:pdf"
```

### For Google Search
```
✅ "Search with Google XXX"
✅ "XXX site:github.com"
✅ "XXX filetype:pdf"
```

---

## 🛡️ Ad Filtering

### Auto-detect Ads

**Ad Characteristics**:
```python
Ad Labels = [
    "广告", "推广", "Sponsored", "Ad", "Promoted",
    "竞价排名", "品牌展示", "商业推广"
]

Ad Positions = [
    "Top of results", "Right sidebar", "Bottom recommendations",
    "Related searches", "Guess you want"
]
```

### Filtering Rules

**1. Label Filtering**:
```
✅ Keep: Organic search results
❌ Filter: Results marked as "Ad", "Sponsored", "广告", "推广"
```

**2. Position Filtering**:
```
✅ Keep: Natural results (middle positions)
❌ Filter: Top 3, right sidebar, bottom recommendations
```

**3. Domain Filtering**:
```
❌ Filter domains blacklist:
- Known ad farms
- Low-quality content sites
- Content scrapers

✅ Priority domains whitelist:
- Government sites (.gov.cn)
- Educational institutions (.edu)
- Mainstream media
- Known tech companies
```

### Usage Examples

**Enable Ad Filtering**:
```
"Search AI news (filter ads)"
"search AI news (no ads)"
"XXX clean search"
```

**Filter Results**:
```
Raw results: 20 items
Ad count: 6 items (30%)
After filter: 14 items (100% organic)
```

---

## 🧪 Content De-toxication

### Toxin Detection

**Content Toxin Types**:

| Type | Characteristics | Action |
|------|----------------|--------|
| 🗑️ Spam | Duplicate, keyword stuffing | Filter |
| 📢 Clickbait | "Shocking", "Must-see", "#1" | Down-rank |
| 📰 Fake News | No source, no author, no date | Filter |
| 💊 Medical Rumors | Folk remedies, miracle cures, 100% cure rate | Filter + Warning |
| 💰 Financial Scams | High returns, guaranteed profit, insider info | Filter + Warning |
| 🔞 Inappropriate | Adult, violence, gambling | Filter |
| 🎭 Deepfakes | AI-generated fake content | Mark + Warning |

### De-tox Algorithm

**1. Source Verification**:
```python
Trusted Sources = [
    "Government sites", "Mainstream media", "Academic journals",
    "Known company websites", "Authoritative organizations"
]

if Source not in Trusted Sources:
    Credibility Score -= 30%
```

**2. Content Quality Assessment**:
```python
Quality Metrics = [
    "Has author", "Has date", "Has source citations",
    "Clear logic", "Verifiable data"
]

if Quality Score < 60:
    Mark as "Low Quality"
```

**3. Fact-checking**:
```python
# Cross-verify multiple sources
if Only single source reports:
    Mark as "Unverified"

if Multiple authoritative sources confirm:
    Credibility += 50%
```

**4. Sentiment Analysis**:
```python
if Contains extreme emotion words > 10:
    Mark as "Sensational content"
    Credibility -= 40%
```

### Warning System

**Warning Levels**:

| Level | Icon | Trigger | Action |
|-------|------|---------|--------|
| 🟢 Trusted | ✅ | Authoritative + verified | Normal display |
| 🟡 Questionable | ⚠️ | Single source/medium quality | Mark display |
| 🟠 Suspicious | ❗ | Low quality/clickbait | Down-rank + Warning |
| 🔴 Toxic | 🚫 | Fake/scam | Filter + Warning |

### Usage Examples

**Enable De-toxication**:
```
"Search vaccine info (verified)"
"search vaccine info (de-toxic)"
"XXX safe search"
"XXX filter misinformation"
```

**De-tox Results**:
```
Raw results: 20 items
Toxic content: 5 items (25%)
  - Fake info: 2 items
  - Clickbait: 2 items
  - Low quality: 1 item
After filter: 15 items (100% trusted)
```

---

## 📊 Engine Comparison

| Engine | Region | Free | API Key | Accuracy | Features |
|--------|--------|------|---------|----------|----------|
| Baidu | 🇨🇳 China | ✅ | ❌ | ⭐⭐⭐⭐⭐ | Largest Chinese index |
| Google | 🌍 Global | ✅ | ❌ | ⭐⭐⭐⭐⭐ | Most accurate globally |
| 360 Search | 🇨🇳 China | ✅ | ❌ | ⭐⭐⭐⭐ | Safe & clean |
| DuckDuckGo | 🌍 Global | ✅ | ❌ | ⭐⭐⭐⭐ | Privacy-focused |
| Startpage | 🌍 Global | ✅ | ❌ | ⭐⭐⭐⭐⭐ | Google results + privacy |
| Qwant | 🌍 Europe | ✅ | ❌ | ⭐⭐⭐⭐ | European engine |
| Bing CN | 🇨🇳 China | ✅ | ❌ | ⭐⭐⭐⭐ | Stable & reliable |
| Bing EN | 🌍 Global | ✅ | ❌ | ⭐⭐⭐⭐ | Stable backup |

---

## 🚀 Quick Start

### Basic Search
```
"Search XXX"
"search for XXX"
"Help me find XXX"
"find XXX"
```

### Real-time Search (v3.1 Recommended)

**Get Today's Latest**:
```
"Search today March 17 XXX news"
"XXX latest news (24 hours)"
"latest XXX news today March 17"
"2026-03-17 XXX latest news"
```

**Get This Week**:
```
"Search this week XXX news"
"XXX latest news this week"
"Last 7 days XXX updates"
```

### Safe Search (v3.1 New)

**De-toxic Search**:
```
"Search vaccine info (verified)"
"XXX safe search"
"verified XXX info"
"XXX filter misinformation"
```

**Filter Ads**:
```
"Search XXX (filter ads)"
"XXX no ads"
"XXX clean search"
```

### Specify Engine

**Use Baidu**:
```
"Search with Baidu XXX"
"XXX site:baidu.com"
```

**Use Google**:
```
"Search with Google XXX"
"XXX site:github.com"
```

### Advanced Search

**Specify Time Range**:
```
"Search March 16-17 2026 XXX"
"XXX news from 2026-03-16 to 2026-03-17"
```

**Specify Source**:
```
"Search WeChat articles about XXX"
"find XXX on GitHub"
"search XXX on Reddit"
```

---

## 📊 v3.1 Changelog

### New Features
- ✅ Baidu as primary China engine (was 360)
- ✅ Google as primary International engine (via Startpage)
- ✅ Advanced search syntax support
- ✅ Real-time search (today/24h/7d/30d)
- ✅ Multi-engine aggregation (3 engines)
- ✅ Smart de-duplication (>80% similarity filter)
- ✅ AI summaries (key insights)
- ✅ Time keyword auto-recognition
- ✅ News source priority (real-time news engines)

### Improvements
- ✅ Domestic engines: 3 → 6 (+100%)
- ✅ International engines: 3 → 6 (+100%)
- ✅ Timeout optimization (15s auto-skip)
- ✅ Cache optimization (30min/real-time exception)
- ✅ Result ranking (time descending)
- ✅ Accuracy improvement (Baidu + Google)
- ✅ Safety improvement (ad filter + de-tox)
- ✅ All documentation in English

### Engine Updates
**Domestic New**:
- ✅ Baidu (Primary - Largest Chinese engine)
- ✅ Toutiao (Breaking news)

**International New**:
- ✅ Google via Startpage (Primary - Most accurate)
- ✅ Brave Search (Privacy)

---

## 🔮 Roadmap (v4.0)

- [ ] Vertical search (academic/images/videos/products)
- [ ] AI summary upgrade (multi-language)
- [ ] Search subscription (RSS push)
- [ ] Custom search engines
- [ ] Search history analysis
- [ ] Batch search (multi-keyword parallel)
- [ ] Fact-check API integration
- [ ] Multi-modal search (text+image)

---

*Last updated: 2026-03-17 14:50*  
*Version: v3.1.0*  
*Status: ✅ Production Ready*
*Primary Engines: Baidu (China) + Google (International)*
