# 合成打工人 - 地狱模式

一款魔性合成类抖音小游戏，难度递增，让人上瘾！

---

## 🎮 游戏特色

- **13 个关卡**，难度逐级递增
- **10 个段位**：从实习生到摸鱼王
- **时间限制**：越往后时间越短
- **道具系统**：洗牌、炸弹、加时
- **连击系统**：快速合成获得额外分数
- **激励机制**：看广告复活、加时

---

## 📁 文件结构

```
merge-worker-pro/
├── index.html      # 游戏主文件
├── game.json       # 抖音小游戏配置
├── game.js         # 平台适配层
├── project.config.json  # 项目配置
└── README.md       # 说明文档
```

---

## 🚀 上传到抖音小游戏

### 第一步：注册抖音小游戏

1. 访问 [抖音开放平台](https://developer.openplatform.toutiao.com/)
2. 注册开发者账号
3. 创建小游戏应用
4. 获取 **AppID**

### 第二步：下载开发者工具

1. 下载 [抖音开发者工具](https://developer.openplatform.toutiao.com/docs/develop/developer-tool/download/developer-tool-update-and-download.html)
2. 安装并登录

### 第三步：导入项目

1. 打开抖音开发者工具
2. 选择「小游戏」→「导入项目」
3. 选择 `merge-worker-pro` 文件夹
4. 填入你的 AppID
5. 点击「导入」

### 第四步：修改配置

编辑 `project.config.json`，填入你的 AppID：

```json
{
    "appid": "你的AppID",
    ...
}
```

### 第五步：测试

1. 在开发者工具中预览
2. 扫码在手机上测试
3. 确认游戏正常运行

### 第六步：提交审核

1. 点击「上传」
2. 填写版本号和说明
3. 在抖音开放平台提交审核
4. 等待审核通过

---

## 💰 变现方式

### 1. 激励视频广告（主要收入）

**场景**：
- 复活时看广告
- 加时时看广告
- 获得额外道具时看广告

**配置**：
1. 在抖音开放平台开通广告
2. 创建激励视频广告位
3. 获取广告位 ID
4. 修改 `game.js` 中的广告位 ID

### 2. Banner 广告

在游戏底部显示 Banner 广告

### 3. 插屏广告

关卡结束时显示插屏广告

---

## ⚠️ 无版权问题

本游戏所有内容均为原创：
- ✅ 表情符号：使用系统自带 emoji，无版权问题
- ✅ 代码：完全原创，无抄袭
- ✅ 音效：未使用（可后续添加免版权音效）

---

## 🔧 自定义修改

### 修改关卡难度

编辑 `index.html` 中的 `LEVELS` 数组：

```javascript
const LEVELS = [
    { targetRank: 3, targetCount: 2, time: 90, spawnRate: 0.7, name: '入门' },
    // 修改参数调整难度
];
```

参数说明：
- `targetRank`: 目标段位（0-9）
- `targetCount`: 需要合成的数量
- `time`: 时间限制（秒）
- `spawnRate`: 生成速率（越小越难）

### 修改段位

编辑 `RANKS` 数组：

```javascript
const RANKS = [
    { emoji: '😊', name: '实习生' },
    // 添加或修改段位
];
```

---

## 📱 测试

直接在浏览器打开 `index.html` 即可测试游戏。

---

## 📄 许可

本项目仅供学习交流使用。

---

*祝你游戏大卖！🎮*