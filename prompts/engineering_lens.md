# Engineering 镜头

`project_type` 含 engineering 时执行。

## 检查单

- [ ] 服务边界：网关 vs 业务 vs 推理 worker
- [ ] API 契约：OpenAPI、错误码、版本
- [ ] Agent：tool 注册、超时、人机回环
- [ ] 鉴权、多租户、配置来源
- [ ] 观测：日志、trace、指标
- [ ] 前端与 API 一致性
- [ ] 扩展点：新模型/新路由如何接入

## 产出

`experience.md` → **「Engineering 镜头」** 或与 primary 分层合并（避免重复）。

## 与 primary 关系

绿场 engineering 项目：分层 rationale 已覆盖大部分，本镜头补 **横切关注点**（安全、观测、扩展）。
