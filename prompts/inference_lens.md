# Inference 镜头

`project_type` 含 inference 时执行。

## 检查单

- [ ] IO 契约：输入格式、输出 schema、prompt 模板
- [ ] 单张 vs batch 是否双轨
- [ ] 预处理与训练/官方 demo 一致
- [ ] 权重加载、device、dtype
- [ ] 硬编码路径、环境变量
- [ ] 错误处理与超时
- [ ] 导出/runtime 与 PyTorch 对齐（若有 deploy）
- [ ] secondary：相对 upstream infer 的改动簇是否覆盖 batch/API

## 产出

`experience.md` → **「Inference 镜头」**；pitfalls 优先 L0/L1（契约、双轨）。

## OCR/VL 附加

- EXIF、max_side、crop_mode
- temperature=0、max_tokens
- 与 wjh_ocr / INFER 契约差异
