# Step 0/1 — 分类 Prompt

## 任务

对 **{project}** 完成分类，写入蒸馏计划的「分类结论」块（随后写入 meta.json）。

## Step 0 — project_type

1. 扫 README、目录、入口文件、依赖
2. 判定 **primary**（必填）与 **secondary**（可选）
3. 列出 **3 条证据**（路径或文件名）
4. 若 manifest 已登记该项且与证据一致 → 采用；否则从代码推断并请用户确认

## Step 1 — dev_mode

1. 找 secondary 信号：fork 声明、vendor、submodule、remote、上游 license
2. 找 primary 信号：自研 scaffold、无单一 upstream、架构自述绿场
3. 判定 `primary` | `secondary`；`auto` 时必须输出置信度：高/中/低
4. secondary 时启动 **upstream 解析**（见 reference.md），输出 repo/ref 或 `resolved: false`
5. secondary 分类确认后，**第一步执行 clone 门禁**（见 [secondary_upstream_diff.md](secondary_upstream_diff.md) Step 0），再进入 diff

## 输出格式

```markdown
## 分类结论

| 项 | 值 | 证据 |
|----|-----|------|
| primary type | inference | `*_infer.py` |
| secondary type | — | |
| dev_mode | secondary | README fork 声明 |
| upstream | org/repo@ref | README 链接 |
| clone 门禁 | 待执行 fetch_upstream.py | secondary 必做 |
| 推荐路径 | Step 2a（先 clone） | |
| 待用户确认 | ref 是否锁定 | |
```

**禁止**：无证据猜测 upstream；不确定时标低置信度并提问。  
**禁止**：secondary 未 clone 上游就开始写 `upstream-diff.md`。
