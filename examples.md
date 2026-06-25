# 码伴 CodeMate — 示例

> 读者默认：**刚接手的算法工程师**。指令里可加「我是新人」以触发更细的链路与术语解释。

## 新人接手 — 对话示例

```
@码伴 我是新人，接手 guopei/inference_code_huazhi，
帮我蒸馏并讲清五阶段推理顺序和 pitfalls 里必须先看的 L0
```

## secondary — 代码对比片段（experience.md 内）

### 簇 preprocess — infer 内增加坐标反归一化

**修改前（upstream / README vLLM 示例）**

```python
output = llm.generate([inputs], sampling_params)[0]
print(clean_repeated_substrings(output.outputs[0].text))
```

**修改后（local `HunyuanOCR_infer_v2.py`）**

```python
result = self.clean_repeated_substrings(output.outputs[0].text)
result = self.process_spotting_response(result, image_width, image_height)
return result
```

## secondary — 新增文件

**修改前**：`（上游无 tritonmodel/HunyuanOCR/1/model.py）`

**修改后**：Triton `initialize` 引用 `HunyuanOCR_infer_v2`

## primary — 设计取舍

**修改前（备选）**：推理路由写在 gateway 单文件  
**修改后（现网）**：`framework/` + `gateway/` 分目录

## 指令

```
蒸馏 HunyuanOCR（secondary）：先 fetch_upstream clone，再产出 experience.md 和 upstream-diff.md
```
