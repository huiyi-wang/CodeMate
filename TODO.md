# 码伴 CodeMate — 后续 TODO

> **新人算法工程师小助手**的能力 backlog：更多场景化提示词、一键工具、开工检查单。  
> 实现某项后：在本文件标 `[x]`，并同步更新 [SKILL.md](SKILL.md) §迭代说明。

---

## 怎么用本文档

| 角色 | 做法 |
|------|------|
| **Agent** | 蒸馏前扫一眼「高优先级」；缺工具时按 TODO 手写步骤，并在产出 README 注明「待工具化」 |
| **维护者** | 有新想法直接追加条目；完成则勾选并链到 PR/提交 |
| **对话指令** | `按 TODO.md 实现 distill_batch.py` 或 `为 ONNX 导出补一条 lens prompt` |

状态标记：`[ ]` 未做 · `[~]` 进行中 · `[x]` 已完成

---

## 一、Tools（`tools/`）

### 高优先级

- [ ] **`onboarding_preflight.md` — 新人首日检查单 prompt**  
  接手仓库第 1 天：环境、入口脚本、权重位置、必读 pitfalls L0、别碰的目录；输出一页 Markdown。

- [ ] **`distill_secondary.sh` / `distill_secondary.py` — 二次开发一键门禁**  
  顺序执行：`fetch_upstream.py` → `diff_upstream.py` → 打印三表 counts → 列出待 `git diff --no-index` 的 modified 文件。  
  ```bash
  python tools/distill_secondary.py --project team/SR/ExampleProject \
    --repo owner/ExampleProject --ref main \
    --include networks,models,utils
  ```

- [ ] **`validate_distill.py` — 产出校验**  
  检查 secondary 项目是否满足 v1.3 铁律：  
  - `_upstream/<name>/` 存在  
  - `_file_inventory.json` 与 `upstream-diff.md` counts 一致  
  - `meta.json` 含 `clone_path`、`commit`、`baseline_method` ∈ {clone, hybrid}  
  - `experience.md` 每簇是否链接 `upstream-diff`  
  - pitfalls ≥3 条含代码块  

- [ ] **`render_file_diff.py` — 批量生成 unified diff**  
  读 `_file_inventory.json` 的 `modified`，对每个文件输出 `git diff --no-index` 到 `upstream-diff.fragments/` 或 stdout，供 Agent 粘贴进 MD。

### 中优先级

- [ ] **`cluster_diff.py` — 改动自动聚类**  
  按路径前缀 / 关键词（`infer`、`onnx`、`train`、`local_`）把 added/modified 归入 preprocess / model / deploy / integration 等簇，输出 JSON 草稿供 `experience.md` 使用。

- [ ] **`extract_before_after.py` — 从 diff 抽代码块**  
  输入 unified diff，输出符合 [code_diff.md](prompts/code_diff.md) 的 before/after fenced blocks（附行号）。

- [ ] **`git_hybrid_log.py` — init 后演进摘要**  
  检测 `merge-base` 失败时，自动 `git log -p` 并按目录聚合，生成 `upstream-diff.md` §init 后 草稿。

- [ ] **`scan_monorepo.py` — 批量发现子项目**  
  扫目录树：README、`.git`、`remote`、`fork` 关键词 → 输出 `scan-manifest.yaml` 的 `projects` 草稿。

### 低优先级 / 探索

- [ ] **`diff_exclude_profiles.yaml`** — 按项目类型预置 exclude（权重、checkpoint、Testsets）  
- [ ] **`link_checker.py`** — 校验 `.distill/*.md` 内相对链接与锚点是否存在  

---

## 二、Prompts（`prompts/`）

### 镜头细化（按场景拆专用分析单）

- [ ] **`onnx_export_lens.md`** — 训练 module vs 部署 Infer、dtype、动态轴、opset、校验脚本  
- [ ] **`trt_edge_lens.md`** — TRT/端侧：uint8 图内归一化、tile、精度对齐  
- [ ] **`data_pipeline_lens.md`** — 数据版本、增强与线上一致性、合成数据标签泄漏  
- [ ] **`serving_contract_lens.md`** — Triton/gRPC/JSON 契约、批处理、超时与降级  
- [ ] **`multi_repo_lens.md`** — monorepo / 多 clone（如 MARCONet v1/v2/v3）血缘与「该改哪一版」  

### 分析链（Step 2 之后的可选深化）

- [ ] **`motivation_interview.md`** — 对每个改动簇追问：为什么不改上游、不回滚、不配置化；输出 ADR 表  
- [ ] **`regression_risk.md`** — 从 diff 标「必跑评测 / 必对指标」清单（待验证项集中列）  
- [ ] **`debt_classifier.md`** — 区分应固化 / 临时 debug / 应上游 PR / 应删除  
- [ ] **`incremental_distill.md`** — 增量模式操作单（`git diff` 触达模块 → 只更新对应 §）  
- [ ] **`cross_project_synth.md`** — 同一团队多项目（如 `team/*`）横向提炼共性问题  

### 产出压缩

- [ ] **`skill_compressor.md`** — 从 `experience.md` + `pitfalls.md` 生成可安装 `SKILL.md` / `.mdc` rule 草稿  
- [ ] **`preflight_card.md`** — 从 pitfalls L0/L1 生成「新项目开工 10 条检查」一页纸  

---

## 三、流程与自动化

- [ ] **Makefile / `justfile`** — `just distill PROJECT=... REPO=... REF=...`  
- [ ] **`scan-manifest.yaml` schedule** — `mode: cron` 时与 CI 结合的说明（仅文档，不绑死 CI）  
- [ ] **`.distill/.gitignore` 模板** — 忽略 `_upstream/` 大仓，保留 `_file_inventory.json`  
- [ ] **蒸馏报告模板** — Step 6 固定输出：分类表 + clone commit + 三表 counts + 3 条精华 + 文档路径  

---

## 四、质量与证据

- [ ] **`待验证` 统一区块** — OUTPUT-TEMPLATES 增加 `## 待验证` 节格式  
- [ ] **证据等级** — `git:<hash>` | `clone:_upstream/path` | `architecture:推断` 标签规范写入 reference  
- [ ] **示例库扩充** — [examples.md](examples.md) 增加：完整 secondary（含 clone 命令输出）、hybrid、primary ADR 各一例  

---

## 五、提议新条目的格式

```markdown
- [ ] **简短标题** — 一句话价值
  适用：primary | secondary | 两者
  产出：工具路径 或 prompts/xxx.md
  验收：怎样算做完（1–3 条）
```
