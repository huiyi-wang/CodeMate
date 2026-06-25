# 代码对比提取（修改前 / 修改后）

所有蒸馏产出以 **Markdown 文档** 为主。对比须 **完整、可核对、可点开源文件**。

---

## 两层分工（secondary 必遵）

| 文档 | 完整性 | 内容 |
|------|--------|------|
| **`upstream-diff.md`** | **全集** | `diff_upstream.py` 列出的每个差异 `.py` **各一节**；**全部 hunk**，不得只挑「重点」漏掉其它差异行 |
| **`experience.md`** | 精华 + **引用** | 按改动簇写动机；每簇 **必须链接** 涉及的 `.py` 与 `upstream-diff` 对应章节；可只贴关键片段，但须写「全文 diff 见 upstream-diff §…」 |
| **`pitfalls.md`** | 问题片段 | 须 **引用** 源文件链接 + 行号；问题/推荐代码对比 |

**原则**：完整 diff 在 `upstream-diff.md`；`experience` / `pitfalls` 不替代全集，但必须 **指回** 文件与全集章节。

---

## 改动文件三类清单（secondary 必出）

**前置条件**：已执行 `fetch_upstream.py`，`_upstream/<short-name>/` 存在。

对比时 **必须先列出** 三类文件，再写各文件 diff。术语与 `diff_upstream.py` / `git diff --name-status` 对齐：

| 类型 | 含义 | `diff_upstream.py` | `git diff --name-status` |
|------|------|--------------------|---------------------------|
| **新增** | 本地有、上游无 | `added` / `only_local` | `A` |
| **删除** | 上游有、本地无 | `deleted` / `only_upstream` | `D` |
| **修改** | 同路径、内容不同 | `modified` | `M` |

生成命令：

```bash
python code-mate-skill/tools/diff_upstream.py \
  --upstream <project>/.distill/_upstream/<name> \
  --local <project> \
  --include basicsr,local_inference,local_convert \
  --out <project>/.distill/_file_inventory.json
```

有 git 时 **仅作交叉核对**（不能代替 `diff_upstream.py`）：

```bash
git diff --name-status upstream/<ref>...HEAD
# A = 新增  D = 删除  M = 修改
```

写入 `upstream-diff.md` 的 **固定结构**（三节缺一不可，某类为空也写「（无）」并注 counts=0）：

```markdown
## 改动文件清单

### 新增文件（added）— 共 N 个

| 文件 | 簇 | 摘要 |
|------|-----|------|
| `local_inference/inference_model.py` | inference | tile 推理入口 |

### 删除文件（deleted）— 共 N 个

| 文件 | 摘要 |
|------|------|
| `scripts/to_onnx/convert_onnx.py` | 本地未保留（或已迁移至 local_convert） |

### 修改文件（modified）— 共 N 个

| 文件 | 簇 | 摘要 |
|------|-----|------|
| `basicsr/archs/safmn_arch.py` | model | 训练 forward 调整 |
```

`experience.md` 开头的改动概览须 **引用** 上述三表的统计：`新增 N / 删除 N / 修改 N`，并链到 `upstream-diff.md#改动文件清单`。

---

## `.py` 文件引用（每个对比节必填）

每个涉及代码的文件，在 MD 标题下 **先贴引用表**，再贴 diff / 代码块：

```markdown
### `basicsr/archs/safmn_arch.py`

| 侧 | 路径 | 链接 |
|----|------|------|
| **本地** | `basicsr/archs/safmn_arch.py` | [打开](../basicsr/archs/safmn_arch.py) |
| **上游** | `.distill/_upstream/SAFMN/basicsr/archs/safmn_arch.py` | [打开](./_upstream/SAFMN/basicsr/archs/safmn_arch.py) |
| **行号** | 本地 `166-201` · 上游 `166-170` | 以下 diff 覆盖 **全部** 差异 hunk |

> 基线：`owner/SAFMN@1a41206` · 变更类型：**修改**（modified）
```

说明：

- 链接路径相对于 **`<project>/.distill/`** 写（本地 `../`，上游 `./_upstream/...`）
- **行号** 与 diff hunk 一致；多个不连续 hunk 写 `45-72, 190-210`
- **禁止** 只有 `` `path:line` `` 文字、没有可点击链接、没有代码/diff 块

---

## 完整 diff 怎么写（modified 文件）

对 **每一个** `modified` 的 `.py`，在 `upstream-diff.md` 放入 **完整 unified diff**（所有 hunk，不截断）：

```bash
git diff --no-index \
  .distill/_upstream/SAFMN/basicsr/archs/safmn_arch.py \
  ../basicsr/archs/safmn_arch.py
```

写入 MD：

````markdown
```diff
--- a/basicsr/archs/safmn_arch.py
+++ b/basicsr/archs/safmn_arch.py
@@ ... @@
-旧行
+新行
（此处为 git diff 的完整输出，不得删减 hunk）
```
````

可选：在完整 `diff` 块之后，再附 **修改前 / 修改后** 对照块（便于阅读），但 **不能只用对照块而省略 diff 中的某些 hunk**。

### only_local → **新增文件（added）**

- **修改前**：`（上游无此文件）`
- **修改后**：贴 **完整文件** 或按函数分段贴全文件内容；顶部链接 `[local_inference/inference_model.py](../local_inference/inference_model.py)`
- 文件 >300 行：按 **类/函数** 分段，**每段须连续覆盖全文件**，段末注 `§2/3`；不得只贴入口而跳过中间逻辑

### only_upstream → **删除文件（deleted）**

- 贴上游完整摘录或完整 diff；本地注 `（本地未引入）`

---

## 何时必须写代码对比

| 场景 | 修改前 | 修改后 |
|------|--------|--------|
| **secondary** modified | `_upstream/` 或 `git show` | 本地；**upstream-diff 用完整 diff** |
| **secondary** 新增 | `（上游无此文件）` | 本地 **完整或分段全覆盖** |
| **primary** 分层 ADR | `git show` / 备选示意 | 当前实现 |
| **pitfall** | 问题写法 + **文件链接** | 推荐写法 + **文件链接** |

无真实代码可引时：**不得编造**；写 `（代码对比缺失：原因）` 并标 `待补`。

---

## 获取修改前 / 修改后

见 [secondary_upstream_diff.md](secondary_upstream_diff.md)、[primary_layer_rationale.md](primary_layer_rationale.md)。

生成完整 diff 的推荐流程：

```bash
# 1. 文件清单
python code-mate-skill/tools/diff_upstream.py --upstream ... --local ...

# 2. 对每个 modified .py 导出完整 diff（可在 .distill/_diffs/ 落盘再嵌入 MD）
mkdir -p <project>/.distill/_diffs
git diff --no-index <upstream>/<file> <local>/<file> \
  > <project>/.distill/_diffs/<file_with_underscores>.diff
```

---

## experience / pitfalls 中的写法

精华节可以短，但 **必须包含**：

1. **`.py` 文件链接**（上表格式，至少本地链接）
2. **指向 upstream-diff 的锚点**：`详见 [upstream-diff §safmn_arch](./upstream-diff.md#basicsrarchssafmn_archpy)`
3. 关键 before/after 或 `diff` 片段（辅助阅读）

```markdown
### 簇：训练 forward vs 部署 SAFMNInfer

| 文件 | 链接 |
|------|------|
| 本地 | [safmn_arch_infer.py](../basicsr/archs/safmn_arch_infer.py) |
| 对照上游 | [safmn_arch.py](../basicsr/archs/safmn_arch.py) · [upstream-diff 全文](./upstream-diff.md#basicsrarchssafmn_archpy) |

**为什么改**：…

（可选：贴 20 行关键对比；读者以 upstream-diff 完整 diff 为准）
```

---

## 篇幅规则（按文档区分）

| 文档 | 规则 |
|------|------|
| **upstream-diff.md** | modified：**完整 diff，无行数上限**；only_local：全文件或分段全覆盖 |
| **experience.md** | 单片段可 ≤60 行；**须链接源文件 + upstream-diff 章节** |
| **pitfalls.md** | 单块 ≤40 行通常够用；**须有文件链接** |

---

## 写入哪份 MD

| 内容 | 文件 |
|------|------|
| **每个差异 .py 的完整 diff + 文件链接** | `upstream-diff.md` |
| 改动簇动机 + 引用 + 精华片段 | `experience.md` |
| 避坑 + 文件链接 + 问题/推荐代码 | `pitfalls.md` |

## 禁止

- `upstream-diff` 只列文件表、不写完整 diff
- 只写「改了 forward」却漏掉同文件其它 hunk
- 只有 `path:line` 或只有表格，**没有** `.py` 可点击链接
- before/after 两段完全相同却声称有改动
- experience 写对比却 **不引用** 对应 `.py` 路径
