# 一次开发 — 分层 design rationale + 实现代码

代码摘录规则：[code_diff.md](code_diff.md)

## 前置

- `dev_mode` = primary

---

## Step 0 — 选设计思路来源

```
有 .git 且从项目起点就有完整提交史？
  ├─ 是 → 路径 A：git 历史
  ├─ 否（无 .git）→ 路径 B：架构拆解
  └─ 中途 git init / 首 commit 整树导入 → 路径 C：hybrid（B + A 都要做）
```

| 路径 | 适用 | 设计思路从哪来 |
|------|------|----------------|
| **A — git 历史** | 全程 git | 提交史、patch、迁移 commit |
| **B — 架构拆解** | 无 `.git` | 目录结构、契约、依赖 + 推断 |
| **C — hybrid** | **`git init` 前已开发** | init 前：架构 + 根 commit 快照；init 后：`git log -p` |

在 `meta.json` 记录 `rationale_source`: `git_history` | `architecture` | `hybrid`；`git_coverage`: `full` | `partial` | `none`。

### 判定中途 init

```bash
git rev-list --count HEAD              # 很少 → 可疑
ROOT=$(git rev-list --max-parents=0 HEAD)
git show --stat $ROOT | head           # 首 commit 一次导入大量文件
```

**路径 C 必做两件事**：

1. **架构拆解** + `git show $ROOT:<path>` — init 时「起点」长什么样、为何这样拆（动机可标注推断）
2. **`git log -p $ROOT..HEAD`** — init 之后的设计调整与动机

---

## 路径 A — 有 git：先读历史再写 ADR

在项目根：

```bash
cd <project>

# 1. 总览演进
git log --oneline --graph -20
git log --oneline -- <layer-dir>/          # 如 gateway/、basicsr/

# 2. 某层/文件的设计变迁
git log -p --follow -- <path/to/key.py>    # 带 patch 的演进
git show <commit>:<path>                   # 历史版本作 before

# 3. 双轨/迁移线索
git log --oneline --grep="migrate\|refactor\|gateway" -i

# 4. 热点（谁常改）
git log --oneline -10 -- <path>
```

**从 git 要提取的**：

- 何时引入某层/模块（首个相关 commit）
- 重构前后差异（`git show` / `git diff <old>..<new> -- path`）
- commit message 中的动机（须与代码 patch 交叉验证，不单信 message）
- 双入口并存：旧脚本删除/保留 commit

每层 ADR 的 **修改前** 优先来自 `git show <commit>:path`，不是臆造备选。

---

## 路径 C — 中途 git init（架构 + git 各一段）

1. `architecture.md` — 当前 as-is 全图
2. 根 commit：`ROOT=$(git rev-list --max-parents=0 HEAD)`，`git show $ROOT:<path>` 作 init 起点
3. init 前动机：架构推断，标注 `architecture:推断`；**不假装有提交史**
4. init 后：`git log -p $ROOT..HEAD -- <path>`，ADR 附 `git:<hash>`
5. `experience.md` 分节：`## init 前` / `## init 后`

---

## 路径 B — 无 git：按架构拆解

1. 完成 [architecture_snapshot.md](architecture_snapshot.md) → `architecture.md`
2. 从 manifest `layers` 或 reference 默认层清单选层
3. 从 **当前代码** 反推：模块边界、依赖方向、入口、契约
4. 每层 ADR：**推断** 为何这样设计；备选用 **文字/示意**（标注 `推断，无 git 佐证`）
5. **修改后（当前实现）** 必填真实代码块

无法从架构唯一确定动机时：写「可能原因」+ 证据缺口，**不冒充 git 演进**。

---

## 共用流程

1. `architecture.md`（两路径均要 as-is 地图；路径 A 可叠加 git 热点）
2. 按层填 ADR + 代码块

### 一次开发的「对比」含义

| 对比类型 | 修改前（路径 A） | 修改前（路径 B） | 修改后 |
|----------|------------------|------------------|--------|
| **设计取舍** | `git show` 旧版或 patch 前状态 | 备选方案文字/伪代码 | **当前实现** |
| **演进** | `git show parent:file` | —（标注无历史） | 当前版 |
| **双轨并存** | git 中旧入口文件 | 目录中并存的两套入口 | 主推入口 |

## 每层必答

- 为什么这样设计（路径 A 须尽量有 commit/diff 证据）
- 备选未选及原因
- **修改后（当前实现）** — 必填代码块，`path:line`
- 后果、若重做、证据来源（`git:<hash>` 或 `architecture:推断`）

## 输出

- `experience.md` — 分层 rationale，每层含 **实现代码** 小节
- `architecture.md` — 模块图 + 关键入口 **after** 代码

## 质量门槛

- ≥ **3 层** 有 ADR + **after 代码块**
- 路径 A：≥ **1 层** 有 `git show` 支撑的 before/after
- 路径 B：≥ **1 层** 备选 vs 现状（标注推断）
- 路径 C：**两段都要有** — init 前至少 1 层架构+根 commit 快照；init 后至少 1 层 `git log -p` 演进
- `rationale_source` 写入 `meta.json`

## 禁止

- 有 git 却完全不读历史，只凭当前目录「猜」设计动机
- 无 git 却伪造 `git show` 或虚假 commit 引用
- 只有 ADR 文字、没有 after 代码块
