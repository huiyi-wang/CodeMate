# 二次开发 — 必须先 clone 上游，再 diff

**铁律**：`dev_mode=secondary` 时：

1. **第一步必须** `git clone` 官方上游到 `<project>/.distill/_upstream/<short-name>/`（用 [fetch_upstream.py](../tools/fetch_upstream.py)）
2. **修改前**代码只许来自该目录下的真实文件（或 `git show upstream/<ref>:path` 交叉核对）
3. **禁止**未 clone 就写 `upstream-diff.md`、禁止用 README/目录猜测冒充 upstream

> 本地已有 `.git`、已 `git fetch upstream` **不能代替 clone**。`git diff` 看不见未跟踪新增、本地删除的上游文件、以及与 `origin` 同 commit 时的工作区改动。

代码对比格式：[code_diff.md](code_diff.md)  
工具：[fetch_upstream.py](../tools/fetch_upstream.py)、[diff_upstream.py](../tools/diff_upstream.py)

---

## Step 0 — 门禁：clone 上游（必做）

在 **gitlab 根目录**（含 `code-mate-skill/tools/`）执行：

```bash
python code-mate-skill/tools/fetch_upstream.py \
  --repo <owner/name> \
  --ref <tag|branch|commit> \
  --out <project>/.distill/_upstream/<short-name>
```

示例（SAFMN）：

```bash
python code-mate-skill/tools/fetch_upstream.py \
  --repo owner/SAFMN \
  --ref main \
  --out SAFMN/.distill/_upstream/SAFMN
```

**成功标准**：

- 目录 `<project>/.distill/_upstream/<short-name>/` 存在且为完整上游树
- stdout JSON：`{"ok": true, "commit": "...", "path": "..."}`
- 将 `commit`、`clone_path` 写入 `meta.json` 与 `upstream-diff.md` §基线

**已有合法 clone**（`manifest.upstream.local_path` 或 `_upstream/` 已存在）：

```bash
cd <clone-path> && git rev-parse HEAD
# 与锁定 ref 一致 → 可复用，不必重复 fetch；否则重新 fetch_upstream
```

**失败时**：`upstream.resolved: false`，不得编造 before；降级 `primary` + README 说明。

---

## Step 1 — 树级 diff（必做）

```bash
python code-mate-skill/tools/diff_upstream.py \
  --upstream <project>/.distill/_upstream/<short-name> \
  --local <project> \
  --include basicsr,local_inference \
  --exclude TensorRT-8.6.1.6,.distill \
  --out <project>/.distill/_file_inventory.json
```

JSON → `upstream-diff.md` 三节（见 [code_diff.md §改动文件三类清单](code_diff.md)）：

| JSON | MD 章节 |
|------|---------|
| `added` / `only_local` | **新增文件** |
| `deleted` / `only_upstream` | **删除文件** |
| `modified` | **修改文件** |

**这是权威清单**；后续 git `--name-status` 仅作交叉校验，不能替代。

---

## Step 2 — 文件 hunk（必做）

对 **每一个** `modified` 文件：

```bash
git diff --no-index \
  <project>/.distill/_upstream/<short-name>/<file> \
  <project>/<file>
```

对 **added**：修改前写 `（上游无此文件）`，修改后贴本地文件。  
对 **deleted**：修改前贴 `_upstream/` 摘录，修改后写 `（本地未引入）`。

**before 代码块摘录规则**：从 `_upstream/<short-name>/<file>` 按行号复制，禁止手打。

---

## Step 3 — 本地 git 补充（可选，不代替 Step 0–2）

本地有 `.git` 时，**在 clone + 树级 diff 完成后**追加：

```bash
cd <project>
git remote -v
# 若无 upstream remote，可添加（与 clone 并行，非替代）
git remote add upstream https://github.com/<owner>/<repo>.git
git fetch upstream <ref> --depth 1

# 交叉校验：已提交相对上游（看不见 untracked）
git diff --name-status upstream/<ref>...HEAD

# 单文件已提交 hunk（可选，与 --no-index 对照）
git diff upstream/<ref>...HEAD -- <file>

# 取片段核对
git show upstream/<ref>:<path>
```

**用途**：

| git 命令 | 补充什么 |
|----------|----------|
| `git log -p` | init **后**改动动机（hybrid） |
| `git diff upstream/...HEAD` | 与 `_file_inventory.json` 交叉验证 |
| `git show upstream/<ref>:path` | 核对 before 摘录是否与 clone 一致 |

**禁止**：仅用 `git diff`、跳过 Step 0 clone。

---

## Step 4 — hybrid（中途 `git init`）

判定：

```bash
git merge-base upstream/<ref> HEAD    # 无输出 → hybrid
```

**必做三件事**（clone 仍不可省）：

1. Step 0 `fetch_upstream.py`
2. Step 1 `diff_upstream.py`（覆盖 init 前 + 整体相对上游）
3. `git log -p $(git rev-list --max-parents=0 HEAD)..HEAD`（init 后演进）

`meta.json`：`baseline_method: hybrid`，`git_coverage: partial`。

---

## Step 5 — 代码对比写入 MD

**顺序**：§基线（含 clone 路径 + commit）→ §改动文件清单（三表）→ §代码对比全集。

对每一个差异文件：

1. `upstream-diff.md` 建节 + 双端文件链接
2. 贴完整 `git diff --no-index` 或 before/after 双块
3. `experience.md` 按簇写动机，链接 upstream-diff 锚点

聚类：preprocess / model / training / deploy / integration …

---

## Step 6 — 动机与产出

- `upstream-diff.md` — clone 路径、commit、三表、完整 diff；hybrid 加 `## init 后（git 演进）`
- `experience.md` — 每簇动机 + 内嵌对比
- `pitfalls.md` — 相关 PIT + 代码

---

## 质量门槛

- [ ] `_upstream/<short-name>/` 存在且 `fetch_upstream.py` commit 已写入 meta
- [ ] `_file_inventory.json` 存在；三表 counts 与 JSON 一致
- [ ] **每个** added / deleted / modified 在 upstream-diff 有记录
- [ ] 修改类文件有 `git diff --no-index` 或等价 before/after 双块
- [ ] before 代码可追溯到 `_upstream/` 具体路径+行号
- [ ] experience ≥3 改动簇；每簇链接 upstream-diff
- [ ] hybrid：clone 全量 diff **与** init 后 `git log` 均有内容

## 禁止

- **未 clone 上游**就写 secondary 蒸馏产物
- 本地有 `.git` 就只跑 `git diff`、不跑 `diff_upstream.py`
- 用 README 冒充 upstream 文件
- 只有表格、没有完整 diff 或 `.py` 链接
- `baseline_method` 仅填 `git_local` 而无 `_upstream/` 目录
