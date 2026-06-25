# Training 镜头

`project_type` 含 training 时执行（主或副）。

## 检查单

- [ ] 数据版本与路径是否可复现
- [ ] 增强/归一化是否与目标推理一致
- [ ] 实验 config、seed、日志是否可追溯
- [ ] val 泄漏、标注噪声处理
- [ ] ckpt 选择与推理入口是否文档化
- [ ] 训练脚本与 deploy 导出是否双轨

## 产出

在 `experience.md` 增 **「Training 镜头」** 一节；相关项写入 pitfalls（L2/L3 为主）。

## 经验形态

- 数据坑、实验坑、交付衔接坑
- 每条绑证据
