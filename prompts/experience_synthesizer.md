# Experience 合成（Markdown 主交付）

## 任务

合成 **`experience.md`**（纯 Markdown，人类可读主文档），含总则 + 分节经验 + **内嵌代码对比**。

## 格式铁律

1. **只输出 Markdown** — 不将经验正文写入 json；`meta.json` 仅元数据
2. 每个改动簇 / 每个设计层：**表格（动机）+ 代码对比块（before/after）**
3. 代码块格式严格遵循 [code_diff.md](code_diff.md)

## 总则写法

- 动词开头；可独立理解
- 绑定证据：`（簇 xxx / PIT-xxx / `path:line`）`

## 结构

| dev_mode | experience 主章 |
|----------|-----------------|
| secondary | 改动经验（**新增/删除/修改概览** + 每簇：动机表 + `.py` 链接） |
| primary | 分层 rationale（每层：ADR + **实现代码**；取舍处 before/after） |

两路径都加：经验总则、类型镜头节。

## 与 upstream-diff 分工

- `upstream-diff.md` — **每个差异 `.py` 一节**：文件链接表 + **完整 unified diff（全部 hunk）**
- `experience.md` — 改动簇动机 + **必须引用** 涉及的 `.py` 链接与 `upstream-diff` 锚点；可贴精华片段，**不得替代全集**
- `pitfalls.md` — 避坑 + **`.py` 文件链接** + 问题/推荐代码

secondary 时 experience 开头须有：

```markdown
## 改动概览

| 类型 | 数量 | 详见 |
|------|------|------|
| 新增 | N | [upstream-diff §新增](./upstream-diff.md#新增文件added) |
| 删除 | N | [upstream-diff §删除](./upstream-diff.md#删除文件deleted) |
| 修改 | N | [upstream-diff §修改](./upstream-diff.md#修改文件modified) |
```

格式见 [code_diff.md](code_diff.md) §两层分工、§`.py` 文件引用。

## 质量门槛

- secondary：≥3 改动簇，每簇 ≥1 组 before/after
- primary：≥3 层 ADR + after 代码；≥1 组设计取舍对比
