# 码伴 CodeMate — 参考

## 分类决策

### project_type 判定

| 类型 | 典型信号 | 非信号（勿误判） |
|------|----------|------------------|
| **training** | `train.py`、`loss`、dataset、dataloader、checkpoint、wandb/mlflow、configs/experiments | 仅有 export 脚本 |
| **inference** | `*_infer*`、serving、ONNX/TRT、batch、prompt、INFER 契约 | 仅有 README 提推理 |
| **engineering** | gateway、API router、前端、Agent orchestration、auth、多服务 repo | 单文件脚本 |

**混合**：主类型 = 用户目标最相关；副类型 = 须单独开节的第二镜头。

### dev_mode 判定

| secondary 强信号 | primary 强信号 |
|------------------|----------------|
| README「基于 xx fork」 | 自研目录命名与上游无关 |
| `vendor/`、`third_party/` 大块原样 | scaffold 从零生成 |
| git submodule 指上游 | 架构文档自述绿场 |
| 文件头 license 保留上游 | 多模块均为本团队命名 |

`auto`：Agent 列出证据 → 用户确认。

### upstream 基线路径

二次开发要先 **clone 官方上游到本地**，再和本地树对比；**不能**只靠本地 `git diff` 跳过 clone。

```
判定 secondary
  └─ Step 0（必做）fetch_upstream.py → .distill/_upstream/<short-name>/
       └─ Step 1（必做）diff_upstream.py → 三类清单
            └─ Step 2（必做）git diff --no-index _upstream/ vs local/
                 └─ Step 3（可选）本地 git fetch + log 补 init 后 / 交叉校验
```

| 阶段 | 必做 | 典型命令 | before / 改动来源 |
|------|------|----------|-------------------|
| **clone** | **是** | [fetch_upstream.py](../tools/fetch_upstream.py) | `_upstream/<path>` |
| **树级 diff** | **是** | [diff_upstream.py](../tools/diff_upstream.py) | `_file_inventory.json` |
| **文件 hunk** | **是** | `git diff --no-index _upstream/... local/...` | `_upstream/` 真实文件 |
| **git 补充** | 否 | `git fetch upstream` · `git log -p` | init 后动机；与 clone 交叉校验 |
| **hybrid** | clone+diff **必做** + git log | 中途 `git init` 时 | `baseline_method: hybrid` |

**判定「中途 init」**（在 clone 完成后追加 git 段）：

```bash
git rev-list --count HEAD
git rev-list --max-parents=0 HEAD
git merge-base upstream/<ref> HEAD    # 无输出 → 须 hybrid
```

**路径 C 分工**（两条都要做）：

| 时段 | 用什么 | 回答什么 |
|------|--------|----------|
| **init 前 + 整体相对上游** | clone + `diff_upstream.py` | 相对官方改了什么 |
| **init 后** | `git log -p` | 入库后又改了什么、为何改 |

**共同要求**：

1. manifest `upstream.repo` + `upstream.ref`（**ref 必填**）
2. **必须先** `fetch_upstream.py`；记录 `upstream.clone_path` + **commit hash**
3. `baseline_method` 为 `clone` 或 `hybrid`（**禁止**在无 `_upstream/` 时填 `git_local`）
4. `git_coverage`：`full`（全程 git 且与上游同源）| `partial`（hybrid）| `none`（无本地 git）
5. 基线 clone 拿不到 → `resolved: false`，不写伪造对比

**标准流程（所有 secondary 项目）**：

```bash
# 1. 必做：clone
python code-mate-skill/tools/fetch_upstream.py \
  --repo sunny2109/SAFMN --ref main --out SAFMN/.distill/_upstream/SAFMN

# 2. 必做：树级 diff
python code-mate-skill/tools/diff_upstream.py \
  --upstream SAFMN/.distill/_upstream/SAFMN \
  --local SAFMN \
  --out SAFMN/.distill/_file_inventory.json

# 3. 必做：单文件 hunk
git diff --no-index \
  SAFMN/.distill/_upstream/SAFMN/basicsr/archs/safmn_arch.py \
  SAFMN/basicsr/archs/safmn_arch.py
```

**git 补充（可选，本地有 .git 时）**：

```bash
git remote add upstream https://github.com/sunny2109/SAFMN.git   # 若无
git fetch upstream main --depth 1
git diff --name-status upstream/main...HEAD    # 交叉校验，非替代 clone diff
git log -p $(git rev-list --max-parents=0 HEAD)..HEAD   # hybrid：init 后
```

**clone 目录**（secondary 必落）：`<project>/.distill/_upstream/<short-name>/`（大体积可 `.gitignore`，但蒸馏前须存在）

**diff 范围建议**：

- 包含：业务目录、推理脚本、配置、adapter
- 排除：权重、`.git`、`node_modules`、lock 文件（除非刻意改依赖策略）

---

## 一次开发：设计思路来源

一次开发要问「每层为什么这样设计」。

```
有 .git 且自项目起点就有完整提交史？
  ├─ 是 → 路径 A：git_history
  ├─ 否（无 .git）→ 路径 B：architecture
  └─ 中途 git init / 首 commit 整树导入 → 路径 C：hybrid（架构 + git 各做一段）
```

| 路径 | 何时用 | 典型命令 | rationale / before 来源 |
|------|--------|----------|-------------------------|
| **A — git_history** | 从第一天就有 git | `git log -p -- path` · `git show <commit>:path` | 全周期提交史 |
| **B — architecture** | 无 `.git`；拷贝 | 目录树、入口、契约 | 推断 |
| **C — hybrid** | **`git init` 前已开发**，首 commit 快照当前树 | **B 拆 as-is / 首 commit** + **A 的 init 后 log** | init 前：架构 + `git show <root>:path`；init 后：git patch |

**路径 C 分工**（两条都要做）：

| 时段 | 用什么 | 回答什么 |
|------|--------|----------|
| **init 前（无提交史）** | `architecture.md` + 根 commit 文件快照 | 初始模块为何这样拆（标注推断） |
| **init 后** | `git log -p` | 入库后的重构、修 bug、设计调整 |

**路径 A 示例**：

```bash
git log --oneline --graph -20
git log -p --follow -- gateway/router.py
git show abc123:framework/infer_task.yaml
```

**路径 B**：完成 `architecture.md` 后按层写 ADR；备选用文字/伪代码，**不得伪造 commit**。

**路径 C 示例**：

```bash
ROOT=$(git rev-list --max-parents=0 HEAD)
git show --stat $ROOT | head
git show $ROOT:gateway/router.py          # init 时快照作「起点」
git log -p $ROOT..HEAD -- gateway/        # init 之后演进
```

记录 `meta.json` → `rationale_source`: `git_history` | `architecture` | `hybrid`；`git_coverage`: `full` | `partial` | `none`。

---

## 中途 git init（primary / secondary 共用）

很多项目是**先写代码、后 `git init`**，或 fork 后丢失与上游的 git 关联。此时 **git 只覆盖 init 之后**，init 之前必须用架构或上游 clone 补全。

| 代际 | init 前 / 全量基线 | init 后 |
|------|-------------------|---------|
| **primary** | 架构拆解 + 根 commit 快照 | `git log -p` |
| **secondary** | clone 上游 + 目录 diff | `git log -p`（细化近期动机） |

`experience.md` 建议分节：`## init 前 / 相对上游` 与 `## init 后（git 演进）`。  
**禁止**：只有 init 后几条 commit 却声称覆盖全项目设计史；或只做 clone diff 却忽略 init 后的 git 动机。

---

## 一次开发：分层清单

### engineering

| 层 | 扫描入口 | rationale 要点 |
|----|----------|----------------|
| 网关 | `gateway/`、路由配置、OpenAPI | 多模型、鉴权、限流、为何不全放业务服务 |
| Agent | agent 编排、tool、memory | 失败重试、人机协同、状态放哪 |
| 后端 | `api/`、`service/`、job 队列 | 同步/异步、幂等、错误模型 |
| 前端 | `web/`、`app/`、状态管理 | 与 API 契约、长任务 UI |
| 公共 | `common/`、中间件、观测 | 日志、trace、配置中心 |

### inference

| 层 | 要点 |
|----|------|
| 入口 | CLI/API、单张 vs batch |
| 预处理 | 图像、tokenize、与训练一致 |
| 模型封装 | wrapper、dtype、device |
| 后处理 | 解码、格式化、业务字段 |
| 部署 | export、runtime、图内图外 |

### training

| 层 | 要点 |
|----|------|
| 数据 | 版本、标注、增强 |
| 实验 | config、seed、记录 |
| 模型 | backbone、head、loss |
| 评估 | metric、val 集泄漏 |
| 交付 | ckpt → 推理契约衔接 |

---

## 二次开发：改动簇 taxonomy

| 簇 ID | 含义 | 动机常见问题 |
|-------|------|--------------|
| `preprocess` | 输入管线 | 数据域、EXIF、分辨率 |
| `model` | 结构/权重加载 | 内部模型源、量化 |
| `prompt` | VL 模板 | 任务特化 |
| `api` | 服务接口 | 公司内部规范 |
| `batch` | 吞吐 | 显存、并发 |
| `config` | 路径、环境 | 部署环境 |
| `deploy` | 导出、端侧 | 上线形态 |
| `integration` | 接内部框架 | wjh_ocr 等 |

每簇输出：**diff 摘要 → 动机 → 避坑 → 是否应上游贡献/应本地化固化**

---

## pitfalls 与 experience 关系

```
secondary: upstream diff → 代码 before/after → 动机 → experience.md → pitfalls
primary:   git 历史或架构拆解 → 分层 ADR + 实现代码 → experience.md → pitfalls
```

experience 偏「认知与取舍 + 可读代码」；pitfalls 偏「下次禁止/注意 + 改法代码」。

---

## 代码对比质量门槛

| 代际 | experience.md | upstream-diff.md | pitfalls.md |
|------|---------------|------------------|-------------|
| secondary | ≥3 簇 + **新增/删除/修改统计** | **三节清单** + 每文件 diff | ≥3 PIT |
| primary | ≥3 层含 after 代码 + 文件链接 | — | ≥2 PIT 含链接 + 代码 |

完整 diff 规则见 [prompts/code_diff.md](prompts/code_diff.md)。experience / pitfalls 可摘录，但须指回源文件与 upstream-diff。

---

## 迭代路线

| 版本 | 内容 |
|------|------|
| **v1.2（当前）** | primary / secondary 三路径 + **hybrid（中途 git init）** |
| v1.3 | `extract_diff.py` 自动 hunk → MD 片段 |
| v1.3 | `experience_writer.py` 统一落盘 |
| v2 | 定时增量、多项目 `README` 索引 |
