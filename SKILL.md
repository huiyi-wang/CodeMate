---
name: code-mate
description: >-
  码伴 CodeMate — onboarding assistant for new algorithm engineers. Distill code
  project experience into Markdown with before/after snippets. Training/inference/
  engineering repos; secondary MUST clone upstream first. Use for 码伴、新人算法工程师、
  接手仓库、项目经验、踩坑、upstream diff、pre-flight pitfalls.
---

# 码伴 · CodeMate

**新人算法工程师的代码仓库小助手** — 陪你读懂项目、对比上游、躲开坑。

- **绿场 / 自研** → 看「为什么这样设计」（分层 ADR + 实现代码）
- **改开源 / fork** → 看「相对上游改了什么、为什么改」（clone 上游 + 代码对比）
- **开工前** → 读 `pitfalls.md`，先躲 L0/L1 硬坑

从代码库蒸馏 **可复用的项目经验**；每条须能指导下次怎么做，不是目录复述。

**设计初衷**（迭代基础，见 [reference.md](reference.md)）：

0. **服务新人** — 默认读者是刚接手的算法工程师；术语能简则简，关键处给代码与路径
1. **先分型** — 训练 / 推理 / 工程，镜头与深度不同
2. **再分代际** — 一次开发 vs 二次开发，蒸馏路径不同
3. **经验可执行** — 每条须能指导下次怎么做，不是目录复述
4. **无证据不立案** — 推测标 `待验证`；架构乱更要扫
5. **产出全是 Markdown** — 主交付为 `.md` 文件（**直接 `experience.md`，不用 `experience.md.draft`**），须含修改前/后代码块

**可选配置**：[scan-manifest.yaml](scan-manifest.yaml)（`projects` 可留空；对话给路径即可）  
**后续规划**：[TODO.md](TODO.md)（待补提示词、工具、自动化）  
**模板**：[OUTPUT-TEMPLATES.md](OUTPUT-TEMPLATES.md)  
**分类细则**：[reference.md](reference.md)  
**代码对比**：[prompts/code_diff.md](prompts/code_diff.md)  
**镜头**：[prompts/](prompts/)

---

## 1. 决策总览

```
指定项目
  ├─ Step 0: project_type（主类型 + 可选副类型）
  │     training | inference | engineering
  ├─ Step 1: dev_mode
  │     primary（一次开发）| secondary（二次开发 / fork）
  ├─ Step 2: 选路径
  │     secondary → **先 clone 上游到 `.distill/_upstream/`**（必做）→ diff →（可选 git 补 init 后）→ 代码对比
  │     primary   → 设计思路（git / 架构 / **中途 init 则两者都做**）+ 逐层 ADR
  ├─ Step 3: 类型镜头（training / inference / engineering）
  ├─ Step 4: 提炼 pitfalls + experience 总则
  └─ Step 5: 写 .distill 草稿 → 用户确认
```

manifest 的 `projects` **可选**。已登记且与证据一致时直接采用；否则按 [prompts/classify.md](prompts/classify.md) 从目录/README 推断并 **向用户确认**。

---

## 2. 产物模型（Markdown 为主）

**主交付均为 `.md` 文件**；`meta.json` 仅作分类/统计索引，不含经验正文。

```
<project>/.distill/
  README.md                 # 索引：各文档链接 + 扫描摘要（推荐）
  _upstream/<short-name>/   # secondary 必做：fetch_upstream.py 克隆的上游树
  _file_inventory.json      # secondary：diff_upstream.py 三类清单（推荐）
  architecture.md           # as-is 地图 + 关键入口代码（after）
  experience.md             # ★ 主交付：动机 + 修改前/后代码
  upstream-diff.md          # secondary：diff 清单 + 代码对比全集
  pitfalls.md               # 避坑 + 问题代码 vs 推荐代码
  meta.json                 # 辅助元数据（非主阅读）
  SKILL.md                  # 可选：组合可安装 Skill
  rules/*.mdc.draft         # 可选
```

| 文件 | 一次开发 | 二次开发 | 代码对比 |
|------|----------|----------|----------|
| `experience.md` | 分层 ADR + **当前实现代码** | 改动簇 + **upstream vs local 代码** | 必填 |
| `upstream-diff.md` | — | 文件清单 + **§代码对比全集** | 必填 |
| `pitfalls.md` | 避坑卡 + **问题/推荐代码** | 同左 | ≥3 条含代码块 |

代码块格式见 [prompts/code_diff.md](prompts/code_diff.md)：每处改动 **修改前** + **修改后** 两个 fenced block（或 unified `diff`）。

**坑分级**（pitfalls.md）：L0 硬教训 > L1 架构 > L2 约定漂移 > L3 集成迁移 > L4 可接受债务。L0 不可为省事破例。

---

## 3. 执行流程

复制 checklist：

```
- [ ] Step 0  项目类型（主 + 副）
- [ ] Step 1  开发代际（primary / secondary）
- [ ] Step 2a secondary：**clone 上游** → diff_upstream →（可选 git 补演进）
      Step 2b primary：路径 A/B/C
- [ ] Step 3  类型镜头
- [ ] Step 4  合成 experience + pitfalls
- [ ] Step 5  写 .distill/*.md
- [ ] Step 6  汇报，等确认
```

### Step 0 — 项目类型

| 类型 | 核心问题 | 经验侧重 |
|------|----------|----------|
| **training** | 数据、实验、复现、ckpt | 管线、增强与部署对齐、实验可追溯 |
| **inference** | 上线、契约、性能、批处理 | IO 契约、单脚本 vs 框架、导出/runtime |
| **engineering** | 系统边界、协作、扩展 | 网关、Agent、前后端、鉴权、观测 |

**混合项目**：设 `primary` + `secondary`（如 `internal_ocr` = engineering + inference），两镜头各出一节，不强行单标签。

镜头：[prompts/training_lens.md](prompts/training_lens.md) | [inference_lens.md](prompts/inference_lens.md) | [engineering_lens.md](prompts/engineering_lens.md)

### Step 1 — 开发代际

| 模式 | 判定信号 |
|------|----------|
| **secondary** | README 声明 fork、vendor/子模块、`git remote` 指上游、大量保留上游目录结构、仅局部改动 |
| **primary** | 自研架构、无清晰单一上游、或从多源拼凑但无对齐基线 |

`dev_mode: auto` 时 Agent 推断并确认。secondary **必须**解析 `upstream.repo` + `upstream.ref`；**ref 不能为空**（manifest 空则问用户或用默认分支并标注）。

### Step 2a — 二次开发（secondary）— **必须先 clone 上游**，再 diff

按 [prompts/secondary_upstream_diff.md](prompts/secondary_upstream_diff.md)。

**门禁（L0，不可跳过）**：判定为 `secondary` 后，**第一步必须**把官方上游 clone 到本地对比目录——**即使本地已有 `.git`、已 `git fetch upstream` 也不行只跑 git diff**。未 clone 不得写 `upstream-diff.md` / 不得写「修改前」代码块。

```bash
python code-mate-skill/tools/fetch_upstream.py \
  --repo <owner/name> \
  --ref <branch|tag|commit> \
  --out <project>/.distill/_upstream/<short-name>
```

| 步骤 | 必做 | 说明 |
|------|------|------|
| **1. clone 上游** | **是** | `fetch_upstream.py`；落点 `_upstream/<short-name>/`；stdout JSON 的 `commit` 写入 meta |
| **2. 树级 diff** | **是** | `diff_upstream.py` → `_file_inventory.json` → 新增/删除/修改三表 |
| **3. 文件 hunk** | **是** | `git diff --no-index _upstream/<short-name>/<file> <project>/<file>` |
| **4. 本地 git 补充** | 可选 | 有 `.git` 时：`git diff upstream/<ref>...HEAD` 补**已提交**差异；`git log -p` 补 init 后动机 |
| **5. 聚类 + 代码对比** | **是** | **修改前**只许来自 `_upstream/` 真实文件或 `git show upstream/<ref>:path` |

**为何本地有 git 仍要 clone**：`git diff` 看不见未跟踪新增（如 `*_local.py`）、本地删除的上游文件、与 `origin` 同 commit 但工作区大改等；**树级 diff 才是完整基线**。

**中途 `git init` / 无 merge-base**：clone + `diff_upstream.py` 仍必做；另加 `git log -p`（init 后）→ `baseline_method: hybrid`，`git_coverage: partial`。

**基线拿不到**（clone 失败 / 无网络）：`upstream.resolved: false`，不得伪造 before；降级 primary 并在 README 说明。

1. **锁定 ref**；记录 **commit**、`baseline_method`（`clone` \| `hybrid`；禁止仅 `git_local`）、`git_coverage`、`upstream.clone_path`
2. **文件级清单**：以 `diff_upstream.py` 为准；git `--name-status` 仅作交叉校验
3. **划边界**：排除权重、TensorRT 捆绑包等（见 reference）
4. **改动聚类 + 动机 + 代码对比**（before 必须来自 `_upstream/` 或 `git show`）
5. **未改区域**：上游保留 vs 本地新增

产出：`upstream-diff.md` + `experience.md` + `pitfalls.md`

### Step 2b — 一次开发（primary）— 有 git 读历史，无 git 看架构

按 [prompts/primary_layer_rationale.md](prompts/primary_layer_rationale.md)：

**Step 0 — 三选一**（见 reference §一次开发设计思路来源 / §中途 git init）：

| 条件 | 做法 |
|------|------|
| **全程 git** | **路径 A**：`git log` / `git show` |
| **无 `.git`** | **路径 B**：架构拆解 + 推断 ADR |
| **中途 `git init`** | **路径 C — hybrid**：**架构 + 根 commit 快照（init 前）** + **`git log -p`（init 后）** |

共用步骤：

1. **as-is 地图** → `architecture.md`（[prompts/architecture_snapshot.md](prompts/architecture_snapshot.md)）
2. **按层拆解**（engineering / training / inference 层清单见 reference）
3. **每层 ADR**：背景 / 决策 / 备选 / 后果 / 若重做；标注证据来源（`git:<hash>` 或 `architecture:推断`）
4. **每层附代码**：**修改后（当前实现）** 必填；路径 A 用 `git show` 作 **修改前**；路径 B 用备选示意作 before（须标注推断）

**工程类常见层**：

| 层 | 要问的 why |
|----|------------|
| 网关 | 为何独立、路由、多模型、鉴权 |
| Agent | 编排、工具、记忆、失败策略 |
| 后端 | 服务切分、同步异步、状态 |
| 前端 | 状态、API 契约、错误体验 |
| 数据/模型 | 与训练推理边界 |

产出：`experience.md`（设计 rationale 章）

### Step 3 — 类型镜头

在 Step 2 结果上套用对应 lens，补类型特有问题（见各 lens 文件检查单）。  
训练项目必看：数据版本、增强与部署一致、实验记录。  
推理项目必看：契约、批处理、双轨。  
工程项目必看：边界、扩展点、观测。

### Step 4 — pitfalls + 总则

[prompts/pitfall_analyzer.md](prompts/pitfall_analyzer.md) + [prompts/experience_synthesizer.md](prompts/experience_synthesizer.md)

- 从 experience / diff / 演进史提炼避坑卡；**≥3 张卡含问题/推荐代码对比**
- **总则 5–10 条**（动词开头，可进 rule）
- 至少 **5 张卡**；secondary 至少 **3 个改动簇**，每簇 **≥1 组** before/after 代码

### Step 5 — 写 Markdown 文档

**直接写入** `<project>/.distill/*.md`（**不要**加 `.draft` 后缀；仅用户明确说「先出草稿」时才用 `*.md.draft`）。

```
<project>/.distill/
  README.md
  experience.md
  upstream-diff.md      # secondary
  pitfalls.md
  architecture.md
  meta.json             # 辅助索引，非主阅读
```

结构见 OUTPUT-TEMPLATES。同步写 `README.md` 索引。`meta.json` 记录：

```json
{
  "project_type": { "primary": "inference", "secondary": "engineering" },
  "dev_mode": "secondary",
  "upstream": {
    "repo": "owner/name",
    "ref": "main",
    "commit": "abc123...",
    "clone_path": "<project>/.distill/_upstream/<short-name>",
    "baseline_method": "clone",
    "resolved": true
  }
}
```

### Step 6 — 汇报

1. 分类结论（类型 + 代际 + 上游是否锁定）
2. experience 3 条精华 + pitfalls L0/L1 各 1 例（带证据）
3. 文档路径列表

**未经用户明确要求：不 git commit。** 若需回滚，用户可自行备份 `.distill/`。

---

## 4. 蒸馏后使用

新项目开工：

1. 读 `pitfalls.md` → L0/L1 pre-flight
2. 读 `experience.md` → 同类任务的设计或改动参考
3. secondary 场景 → 先对 upstream-diff 看是否重复造轮子

---

## 5. 增量模式

`git diff` + 近期 commit → 只更新 touched 模块。  
secondary：新 diff 簇追加到 `upstream-diff.md`。  
primary：变更层补 ADR。  
pitfalls 顶部 `## Changelog` 追加。

---

## 6. 铁律

- **主产出必须是 Markdown**
- **secondary 必先 clone 上游**：`fetch_upstream.py` → `.distill/_upstream/<short-name>/`；**禁止**未 clone 就写 upstream 对比；本地有 `.git` 不能代替 clone
- **secondary 的 before 代码**：只许摘自 `_upstream/` 同路径文件或 `git show upstream/<ref>:path`；禁止 README/记忆冒充
- **secondary 树级 diff 必跑**：`diff_upstream.py` 产出三类清单；不能只有 `git diff --name-status`
- **secondary + 中途 init**：clone + 树级 diff **与** init 后 `git log -p` 两段都做 → `baseline_method: hybrid`
- **primary**：全程 git → 读历史；无 git → 架构；**中途 init → hybrid（架构 + init 后 git）**
- **有改动必贴代码**：secondary 写 upstream vs local；primary 写实现 + 取舍对比
- 不因架构差跳过；不得只写「建议重写」
- secondary 基线（clone）拿不到 → `resolved: false`，不得写「相对 upstream」的代码对比
- **secondary 对比须三类清单**：**新增 / 删除 / 修改** 分表列出，再写各文件完整 diff
- **experience / pitfalls 须引用源文件**：链接 + 行号；精华可短，不得漏指 upstream-diff 全集
- 不得只有 `path:line` 而无链接与代码/diff 块
- 混合类型须分节，不混成一团

---

## 7. 示例指令

```
我是新人，蒸馏 <项目路径>，讲清训练到部署主链路
蒸馏 <项目路径>：secondary + inference，对比上游 ONNX 相关改动
蒸馏 <项目路径>：primary + engineering，按层写 ADR
只补某项目的 upstream-diff
新项目 / 新任务开工前，读 pitfalls 做 pre-flight
```

---

## 8. 关联 Skill

- `ocr-inference` — 推理框架方法论
- `model-edge-deploy` — 部署与训练推理对齐

冲突时以项目契约与入口为准，差异写入 experience / pitfalls。

---

## 9. 迭代说明

当前为 **v1.3**（**secondary 强制先 clone 上游**再 diff；git 仅作补充。primary 仍双路径：有 git 读历史，无 git 架构拆解）。见 [reference.md](reference.md)。  
**待办与路线图**：[TODO.md](TODO.md)（新提示词、tools、校验脚本等）。
