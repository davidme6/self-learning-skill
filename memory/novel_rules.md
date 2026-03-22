# 小说更新规则

## 重要原则（用户明确要求）

**更新完章节后，必须用最新的、最好的版本覆盖旧章节，不要留两个重复的章节！**

### 具体操作：
1. 修复/优化完章节后，直接覆盖原文件
2. 不要保留 `_旧版.txt`、`_backup.txt` 等备份文件
3. 不要创建 `v1`、`v2` 等多版本
4. 每个章节只保留一个文件：`XX 第 X 章 标题.txt`

### 清理步骤：
```bash
# 1. 检查是否有重复
Get-ChildItem "novel/神豪：从消费返利开始当世界首富" -Filter "0*.txt" | Group-Object { $_.Name.Substring(0,2) }

# 2. 删除旧版本
Remove-Item "novel/神豪：从消费返利开始当世界首富/04*.txt" -Force

# 3. 复制新版本
Copy-Item "novel/ch4_fixed.txt" -Destination "novel/神豪：从消费返利开始当世界首富/04 第四章 标题.txt" -Force
```

### 验证：
- 每个章节号（01-99）只能对应一个文件
- 使用 `final_check.py` 脚本验证无重复

---

*最后更新：2026-03-15 00:25*
