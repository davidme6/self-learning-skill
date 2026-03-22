# Python LSP 诊断技能

使用 Pyright 提供 Python 代码诊断功能。

✅ **已安装并可用**

## 功能

- **代码诊断**：检测语法错误、类型错误、未定义变量等
- **快速分析**：无需运行代码即可发现问题
- **JSON 输出**：结构化诊断结果

## 使用方法

直接对我说：
```
帮我检查这个 Python 文件有没有问题：path/to/file.py
```

或：
```
诊断 Python 项目 path/to/project
```

## 示例

```
用户：帮我检查 main.py 有没有问题
助手：[调用 pyright 诊断，返回错误和警告]
```

## 诊断类型

| 类型 | 说明 |
|------|------|
| `error` | 语法错误、类型错误、未定义变量 |
| `warning` | 潜在问题、未使用变量 |
| `information` | 代码风格建议 |

## 技术实现

- 使用 Pyright 1.1.408 作为 LSP 服务器
- 通过 `--outputjson` 获取结构化诊断
- 自动检测 Windows 下的 pyright 路径

## 依赖

- Python 3.8+ ✅
- pyright 1.1.408 ✅