# Codex 代理 v6.2 全功能兼容修复记录

**日期**: 2026-08-01
**状态**: ✅ 已修复
**版本**: v6.2（图片分流网关）

## 核心问题

MiMo V2.5 Pro 原生不支持图片输入，Codex++ 粘贴截图报 `404 No endpoints found that support image input`。

## 解决方案：图片分流网关

### 架构
```
用户粘贴截图 → 代理检测图片 → 自动路由到 mimo-v2.5 → 返回图片描述
纯文本请求 → 代理透传 → mimo-v2.5-pro（代码能力强）
```

### MiMo 两版本分工
| 模型 | 能力 | 用途 |
|------|------|------|
| mimo-v2.5-pro | 纯文本/代码/Agent/工具调用 | 编程任务 |
| mimo-v2.5 | 全模态（文本+图片+视频+音频） | 图片任务 |

### 代理检测逻辑
1. 检查 `messages` 中是否有 `image_url` 类型
2. 检查是否有 `data:image/` base64 数据
3. 检查 `input` 数组中是否有图片元素
4. 检测到图片 → 自动切换模型为 `mimo-v2.5`

### 代码位置
- 图片检测方法：`ProxyHandler._detect_image()`
- Responses API 分流：`_proxy()` 方法第 299-305 行
- Chat Completions 分流：`_proxy()` 方法第 340-352 行

## 测试验证

| 测试项 | 请求类型 | 期望模型 | 实际模型 | 结果 |
|--------|----------|----------|----------|------|
| 纯文本 | Chat Completions | mimo-v2.5-pro | mimo-v2.5-pro | ✅ |
| 图片 | Chat Completions | mimo-v2.5 | mimo-v2.5 | ✅ |
| 纯文本 | Responses API | mimo-v2.5-pro | mimo-v2.5-pro | ✅ |
| 流式 | Responses API | mimo-v2.5-pro | mimo-v2.5-pro | ✅ |

### 图片测试详情
- 请求：1x1 红色 PNG base64
- 模型：mimo-v2.5（自动分流）
- 回复："这是一个长条形的纯亮黄色色块"
- image_tokens: 16

## 稳定性保障

1. **三层异常处理**：`handle_one_request()` + 响应路径 + 错误响应
2. **图片分流独立**：图片解析失败不影响主代理
3. **自动模型切换**：用户无感知，对话框照常粘贴截图

## 相关规则

- R-CODEX-15: MiMo 两版本分工明确
- R-CODEX-16: 图片分流网关（自动路由）
- R-CODEX-17: 图片分流不阉割功能
- R-CODEX-18: 分流网关稳定性保障

## 快照

路径：`E:\龙虾AI主控中心\MCP服务\snapshots\three_engine_snapshot_multimodal_20260801\`
大小：≤20MB
