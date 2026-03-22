# 即梦 AI 视频全自动化方案

## 问题分析

**即梦 (seedance.ai) 使用 Cloudflare 反机器人保护**，导致：
- ❌ 普通 HTTP 请求被拦截 (403)
- ❌ Playwright/Selenium 本地浏览器被识别
- ❌ 无法直接调用 API（需要登录态 + 签名）

## 解决方案

### 方案 1：Browserbase 云端浏览器（推荐）

**原理**：使用云端真实浏览器 + 住宅 IP 绕过 Cloudflare

**步骤**：
1. 注册 https://browserbase.com/
2. 获取 API Key 和 Project ID
3. 使用 Browserbase SDK 连接远程浏览器
4. 在远程浏览器中执行登录和视频生成操作

**优点**：
- ✅ 绕过 Cloudflare
- ✅ 自动处理验证码
- ✅ 可复用登录态（Cookie 持久化）

**缺点**：
- 💰 需要付费（约 $0.05-0.1/分钟）

---

### 方案 2：即梦官方 API（需申请）

**查询即梦是否有开放 API**：
1. 登录即梦官网
2. 查找"开发者"、"API"、"开放平台"入口
3. 申请 API 权限

**如果有一般会有**：
- 视频生成 API
- 需要 API Key
- 按调用次数计费

---

### 方案 3：半自动化（当前最可行）

**流程**：
1. 你手动登录即梦（1 次）
2. 我帮你写提示词
3. 你复制粘贴生成视频
4. 我帮你批量生成提示词库

**提示词模板**：
```
【场景】{场景描述}
【布局】{物品位置}
【风格】{视觉风格}
【镜头】{运镜方式}
【氛围】{整体感觉}
```

---

## 技术实现（Browserbase 方案）

### 安装依赖
```bash
pip install browserbase playwright
```

### 登录脚本
```python
from browserbase import Browserbase
from playwright.sync_api import sync_playwright
import time

# 初始化
bb = Browserbase(api_key="YOUR_KEY")
session = bb.sessions.create(project_id="YOUR_PROJECT")

# 连接浏览器
browser = p.chromium.connect_over_cdp(session.connect_url)
page = browser.contexts[0].pages[0]

# 登录即梦
page.goto("https://seedance.ai/login")
page.fill('input[type="tel"]', "你的手机号")
page.fill('input[type="password"]', "密码")
page.click('button:has-text("登录")')

# 等待登录完成
time.sleep(5)

# 保存 Cookie 供后续使用
cookies = page.context.cookies()
save_cookies(cookies)
```

### 视频生成脚本
```python
# 加载保存的 Cookie
page.context.add_cookies(load_cookies())

# 进入视频生成页面
page.goto("https://seedance.ai/create")

# 填写提示词
page.fill('textarea[placeholder*="提示词"]', prompt)

# 选择参数
page.select_option('select[name="ratio"]', '16:9')
page.select_option('select[name="duration"]', '5s')

# 点击生成
page.click('button:has-text("生成")')

# 等待完成
time.sleep(60)

# 下载视频
video_url = page.locator('video').get_attribute('src')
download_video(video_url)
```

---

## 下一步行动

1. **确认即梦是否有官方 API** - 你去官网看看有没有"开发者"或"API"入口
2. **注册 Browserbase** - 如果没有 API，用 Browserbase 方案
3. **我先帮你写提示词库** - 你手动生成，同时准备自动化

---

## 提示词库示例

### 收纳游戏场景
```
【场景】整洁的儿童卧室，日式收纳风格，明亮温馨
【布局】左侧白色开放式书架，右侧浅木色双门衣柜，中间米白色地毯
【风格】3D 卡通渲染，皮克斯风格，柔和自然光
【镜头】缓慢推近，从全景到书架特写，4K 高清
【氛围】整洁有序，治愈系，温暖色调
```

### 厨房场景
```
【场景】现代化厨房，白色橱柜，不锈钢台面
【布局】左侧冰箱，中间灶台，右侧水槽，上方吊柜
【风格】写实风格，明亮灯光，干净整洁
【镜头】平移镜头，从左到右展示各区域
【氛围】专业厨房，高效有序
```

---

*最后更新：2026-03-14*
