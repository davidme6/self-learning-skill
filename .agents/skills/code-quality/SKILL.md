---
name: code-quality
description: 代码质量优化技能。分析生成的代码，优化代码结构、提高代码质量、减少 Bug、提高可维护性。使用场景：生成代码后自动优化，或手动优化现有代码。
---

# Code Quality Skill

## 功能

1. **代码分析**：分析代码结构、逻辑、潜在问题
2. **代码优化**：优化代码结构、提高可读性
3. **Bug 修复**：发现并修复潜在 Bug
4. **性能优化**：优化性能、减少资源消耗
5. **最佳实践**：应用行业最佳实践

## 工作流程

1. 接收代码
2. 静态分析
3. 识别问题
4. 生成优化建议
5. 应用优化

## 优化维度

### 1. 代码结构
```javascript
// 优化前
function draw() {
    // 100 行代码混在一起
}

// 优化后
function draw() {
    drawBackground();
    drawFurniture();
    drawDecorations();
}
```

### 2. 变量命名
```javascript
// 优化前
let x = 100;
let y = 200;

// 优化后
let wardrobeX = 100;
let wardrobeY = 200;
```

### 3. 错误处理
```javascript
// 优化前
ctx.drawImage(img, 0, 0);

// 优化后
if (img && ctx) {
    ctx.drawImage(img, 0, 0);
} else {
    console.error('Image or context not available');
}
```

### 4. 性能优化
```javascript
// 优化前
for (let i = 0; i < items.length; i++) {
    drawItem(items[i]);
}

// 优化后
items.forEach(item => drawItem(item));
```

## 输出格式

```markdown
## 代码质量报告

### 问题识别
1. 问题 1 - 严重程度
2. 问题 2 - 严重程度

### 优化建议
1. 建议 1
2. 建议 2

### 优化后代码
[完整优化后的代码]
```
