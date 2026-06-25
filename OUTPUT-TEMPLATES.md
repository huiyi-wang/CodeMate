# 产出模板

路径根：`<project>/.distill/`。**默认直接写 `*.md`**（勿用 `experience.md.draft` 这类双后缀）。仅用户要求草稿时才加 `.draft`。**主交付均为 Markdown。**

---

## §0 README.md（索引，推荐）

```markdown
# <项目> — 项目经验文档索引

> 扫描：YYYY-MM-DD · 类型：… · 代际：…

| 文档 | 说明 |
|------|------|
| [experience.md](./experience.md) | ★ 主交付：经验 + 代码对比 |
| [upstream-diff.md](./upstream-diff.md) | 上游 diff 与代码全集（secondary） |
| [pitfalls.md](./pitfalls.md) | 避坑 + 问题/推荐代码 |
| [architecture.md](./architecture.md) | 架构快照 |

- 代码对比规范：修改前（upstream/旧） / 修改后（local/现）
- 上游：`repo@ref` 或 partial
```

---

## §1 meta.json（辅助，非主阅读）

```json
{
  "schema_version": 2,
  "id": "hunyuan_ocr",
  "path": "OCR/HunyuanOCR",
  "scanned_at": "ISO8601",
  "dev_mode": "secondary",
  "upstream": {
    "repo": "...",
    "ref": "...",
    "commit": "...",
    "clone_path": "<project>/.distill/_upstream/<short-name>",
    "baseline_method": "clone",
    "resolved": true
  },
  "counts": {
    "added": 12,
    "deleted": 0,
    "modified": 45,
    "unchanged": 7,
    "diff_clusters": 5,
    "code_comparisons": 8,
    "pitfalls_with_code": 4
  }
}
```

primary 时增加 `"rationale_source": "git_history"` 或 `"architecture"`。

---

## §2 代码对比块（通用，嵌入各 MD）

见 [prompts/code_diff.md](../prompts/code_diff.md)。固定结构：

```markdown
### 代码对比：`relative/path.py` `45-72`

> 基线：`Tencent-Hunyuan/HunyuanOCR@abc123` · 类型：修改

**修改前（upstream）**

```python
# 上游 / README 官方示例
llm = LLM(model=model_path, trust_remote_code=True)
output = llm.generate([inputs], sampling_params)[0]
result = clean_repeated_substrings(output.outputs[0].text)
```

**修改后（local）**

```python
# 本地：类封装 + 坐标反归一化
result = self.clean_repeated_substrings(output.outputs[0].text)
result = self.process_spotting_response(result, image_width, image_height)
```

**差异摘要**（可选）

```diff
- result = clean_repeated_substrings(...)
+ result = self.process_spotting_response(...)
```

**为什么改**：spotting 需像素坐标  
**避坑**：任务契约写明是否 denorm
```

**新增文件**：修改前写 `（上游无此文件）`。  
**仅配置变更**：对比默认值字符串/环境变量。

---

## §3 experience.md（主交付）

### secondary 模板

```markdown
# <项目> — 项目经验

> 类型：inference · 代际：二次开发 · 上游：repo@ref

## 经验总则

1. …

## 改动经验

### 簇 preprocess — 坐标反归一化

| 改了什么 | … |
| 为什么改 | … |
| 沉淀 | … |

（此处嵌入 §2 代码对比块）

### 簇 integration — …

（代码对比块）

## 未改区域与隐患

## 类型镜头补充
```

### primary 模板

```markdown
# <项目> — 项目经验

> 类型：engineering · 代际：一次开发

## 经验总则

## 分层设计 rationale

### 网关层

| 为什么这样 | … |
| 备选未选 | … |

**修改前（备选：路由内嵌业务服务）**

```python
# 示意：未采用方案
```

**修改后（当前实现）**

```python
# gateway/app.py 摘录
```

### framework 层 — …
```

---

## §4 upstream-diff.md（secondary — 三类清单 + 完整 diff）

**铁律**：

1. §基线须含 **clone 路径** + **commit**（来自 `fetch_upstream.py` stdout）
2. 先 **新增 / 删除 / 修改** 三表（来自 `_file_inventory.json`），再按文件写完整 diff
3. 未执行 clone → 不得创建本文件

```markdown
# <项目> — 上游对比与代码差异

## 基线

| 项 | 值 |
|----|-----|
| 仓库 | [owner/repo](https://github.com/owner/repo) |
| ref | `main` |
| **baseline_method** | `clone` 或 `hybrid` |
| **基线 commit** | `abc123...`（fetch_upstream.py 输出） |
| **clone 路径** | `<project>/.distill/_upstream/<short-name>` |
| 清单来源 | `_file_inventory.json` @ 扫描日期 |

## 改动文件清单

> 统计：新增 **N** · 删除 **N** · 修改 **N** · 未改 **N**  
> 来源：`_file_inventory.json` @ 扫描日期

### 新增文件（added）

| 文件 | 簇 | 摘要 |

### 删除文件（deleted）

| 文件 | 摘要 |

### 修改文件（modified）

| 文件 | 簇 | 摘要 |

## 代码对比全集

### 新增 · `wjh_inference/inference_safmn.py`
（文件链接 + 本地全文或分段）

### 删除 · `scripts/foo.py`
（上游摘录；本地未引入）

### 修改 · `basicsr/archs/safmn_arch.py`
（双端链接 + 完整 ```diff```）
```

`experience.md` 各簇须 **链接** 上表中的 `.py` 与对应 `###` 锚点。

---

## §5 architecture.md

```markdown
# <项目> — 架构快照

## 入口与契约

## 关键入口代码（当前）

```python
# path:start-end
...
```

## 模块关系（mermaid）

## 演进线索
```

---

## §6 pitfalls.md

```markdown
# <项目> — 避坑

## 开工前必读

## L0 硬教训

### [PIT-001] 硬编码路径

| 症状 | … |
| **避坑** | 环境变量 |

#### 代码对比

**问题代码（当前）**

```python
model_path="/home/kas/wangjinghui/AI-OCR/HunyuanOCR"
```

**推荐写法**

```python
model_path = os.environ.get("HUNYUAN_OCR_MODEL", "tencent/HunyuanOCR")
```

## Changelog
```

---

## §7 combined SKILL.md / rule

从 `experience.md` + `pitfalls.md` 压缩；**保留至少全部 L0 的代码对比**。
