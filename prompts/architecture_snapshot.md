# Architecture Snapshot（as-is 地图）

**primary / secondary 共用**第一步：描述当前事实，不写「应该」。

## 与 git 的关系

| 场景 | 做法 |
|------|------|
| **secondary（任意）** | **必先** `fetch_upstream.py` → `_upstream/`；`diff_upstream.py` 定 as-is 相对上游的差异边界 |
| **primary + 全程 git** | as-is 地图 + `git log -- <dir>` 标热点 |
| **primary + 无 git** | 地图即主证据 |
| **中途 git init（hybrid）** | secondary：clone diff + init 后 `git log`；primary：地图 + init 后 `git log` |

判定 hybrid：`git rev-list --count` 很少、首 commit 大量 import、或与 upstream 无 `merge-base`。

## 提取

- 入口、契约文件、环境变量
- 目录树（深度 3–4）
- 模块依赖方向（谁 import 谁）
- 平行实现（两套 infer、两套配置）
- **有 git**：`git log --oneline -5 -- <path>` 标热点；migration 类 commit
- migration 文档（若有）

## 输出

填入 `architecture.md`（OUTPUT-TEMPLATES §4）。

## 疑点清单

供 pitfall / experience 跟进：

```
- [ ] 双入口：...
- [ ] 契约缺失：...
- [ ] git 热点 / 无 git 无法追溯：...
```
