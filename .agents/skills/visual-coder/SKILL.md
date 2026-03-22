---
name: visual-coder
description: 视觉代码生成技能。根据文字描述或参考图，生成高质量的 Canvas/WebGL 渲染代码。专长于游戏场景、UI 界面、数据可视化等视觉内容的代码实现。
---

# Visual Coder Skill

## 专长领域

1. **Canvas 2D 渲染**
   - 游戏场景绘制
   - UI 界面绘制
   - 数据可视化

2. **CSS 布局**
   - Flexbox
   - Grid
   - 响应式布局

3. **动画效果**
   - CSS Animation
   - Canvas Animation
   - Transition

## 代码质量标准

### 1. 清晰的结构
```javascript
class Scene {
    constructor() {
        this.canvas = null;
        this.ctx = null;
        this.objects = [];
    }

    init() { /* 初始化 */ }
    draw() { /* 绘制 */ }
    update() { /* 更新 */ }
}
```

### 2. 配置驱动
```javascript
const CONFIG = {
    wardrobe: {
        x: 0.02,
        y: 0.05,
        width: 0.28,
        height: 0.5,
        color: '#8B4513'
    }
};
```

### 3. 可复用组件
```javascript
function drawRect(x, y, w, h, color, borderColor) {
    // 通用绘制函数
}
```

## 输出保证

1. **一次做对**：理解准确，代码准确
2. **高质量**：结构清晰，注释完整
3. **可维护**：易于修改和扩展
4. **无 Bug**：经过逻辑验证

## 工作流程

1. 理解需求（文字/图片）
2. 提取关键信息
3. 设计代码结构
4. 生成代码
5. 自我验证
6. 输出最终代码
