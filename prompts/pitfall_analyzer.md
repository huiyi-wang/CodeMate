# Pitfall 提炼（Markdown + 代码对比）

## 输入

- `experience.md`、`upstream-diff.md`（含代码对比）
- `architecture.md`、git / TODO

代码格式：[code_diff.md](code_diff.md)

## 原则

1. 无证据不立案
2. 由代码引起的坑：**必须**附
   - **`.py` 文件链接`**（如 `[train.py](../basicsr/train.py)`）
   - **问题写法** vs **推荐写法** 代码块
3. secondary：优先 **引用** `upstream-diff.md` 中已有完整 diff 的 `.py`
4. primary：问题 vs 推荐可在同文件不同函数对比

## pitfalls.md 每条 PIT 结构

```markdown
### [PIT-xxx] 标题

| 症状 | … |
| 根因 | … |
| 避坑 | … |
| **涉及文件** | [basicsr/archs/safmn_arch_infer.py](../basicsr/archs/safmn_arch_infer.py) |

#### 代码对比

**问题代码（当前）**
```python
...
```

**推荐写法**
```python
...
```
```

若仅配置/路径类：对比 **修改前默认值** vs **应然写法**。

## 产出

- `pitfalls.md` — 纯 Markdown；≥5 张卡；≥ **3 张** 含代码对比块

## 禁止

空泛 best practice；无代码块的技术坑（除非非代码根因，须说明）
