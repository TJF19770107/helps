# Agent-Reach 全场景功能测试计划

> 版本: 1.0.0 | 日期: 2026-06-14
> 测试负责人: [待填写]
> 测试环境: Windows 10, Python 3.10+, Agent-Reach latest

---

## 测试概述

| 项目 | 说明 |
|------|------|
| 测试范围 | Agent-Reach 全部功能通道 + CC Switch 路由 + 全Agent适配 + 兜底切换 |
| 测试用例数 | 9 个主要用例 |
| 测试方法 | 手工执行 + 结果记录 |
| 通过标准 | 预期结果与实际结果一致 |

---

## 测试用例

### TC-01: 普通网页读取测试

| 字段 | 内容 |
|------|------|
| **测试目标** | 验证 Agent-Reach 能否正确读取普通网页并输出 Markdown 格式内容 |
| **前置条件** | Agent-Reach 已安装，网络正常 |
| **执行步骤** | 1. 执行 `agent-reach web read --url "https://httpbin.org/get"` |
|  | 2. 检查返回的 JSON 内容是否正确 |
|  | 3. 执行 `agent-reach web read --url "https://example.com" --format markdown` |
|  | 4. 检查返回是否为干净的 Markdown 格式 |
| **预期结果** | 步骤 1 返回 httpbin 的正常 JSON；步骤 3 返回 example.com 的页面文本，无 HTML 标签 |
| **实际结果** | |
| **备注** | |

---

### TC-02: B站视频字幕提取测试

| 字段 | 内容 |
|------|------|
| **测试目标** | 验证 Agent-Reach 能否正确提取 B站视频字幕 |
| **前置条件** | Agent-Reach 已安装，网络正常，代理已配置（如需） |
| **执行步骤** | 1. 找一个有字幕的 B站公开视频 |
|  | 2. 执行 `agent-reach bilibili subtitle --url "https://www.bilibili.com/video/BVxxx"` |
|  | 3. 检查返回的字幕内容是否完整 |
| **预期结果** | 成功返回视频字幕文本，内容与视频实际字幕一致 |
| **实际结果** | |
| **备注** | 本地环境通常无需代理；服务器环境需配置代理 |

---

### TC-03: GitHub 仓库读取测试

| 字段 | 内容 |
|------|------|
| **测试目标** | 验证 Agent-Reach 能否正确读取公开 GitHub 仓库信息 |
| **前置条件** | Agent-Reach 已安装，网络正常 |
| **执行步骤** | 1. 执行 `agent-reach github read --repo "Panniantong/agent-reach"` |
|  | 2. 检查是否返回仓库描述、README 内容 |
|  | 3. 执行 `agent-reach github search --query "LLM agent" --stars ">=1000"` |
|  | 4. 检查搜索结果是否包含相关仓库 |
| **预期结果** | 步骤 1 返回仓库基本信息 + README；步骤 3 返回 star≥1000 的 LLM agent 相关仓库列表 |
| **实际结果** | |
| **备注** | 私有仓库需配置 GitHub Personal Access Token |

---

### TC-04: RSS 订阅解析测试

| 字段 | 内容 |
|------|------|
| **测试目标** | 验证 Agent-Reach 能否正确解析 RSS 订阅源 |
| **前置条件** | Agent-Reach 已安装，网络正常 |
| **执行步骤** | 1. 执行 `agent-reach rss parse --url "https://blog.python.org/feeds/posts/default" --limit 5` |
|  | 2. 检查返回是否包含文章标题、摘要、发布时间、链接 |
|  | 3. 测试中文 RSS 源：`agent-reach rss parse --url "https://www.36kr.com/feed" --limit 5` |
| **预期结果** | 步骤 1 返回 Python 官方博客最近 5 篇文章；步骤 3 返回 36氪最近 5 篇文章 |
| **实际结果** | |
| **备注** | 部分 RSS 源可能需要代理 |

---

### TC-05: 全网语义搜索测试

| 字段 | 内容 |
|------|------|
| **测试目标** | 验证 Agent-Reach 全网语义搜索功能是否正常 |
| **前置条件** | Agent-Reach 已安装，MCP 语义搜索通道可用 |
| **执行步骤** | 1. 执行 `agent-reach search semantic --query "Python async programming best practices 2026"` |
|  | 2. 检查返回结果是否与搜索主题相关 |
|  | 3. 测试中文搜索：`agent-reach search semantic --query "2026年人工智能发展趋势"` |
| **预期结果** | 返回与查询主题高度相关的搜索结果，包含标题、摘要和链接 |
| **实际结果** | |
| **备注** | 语义搜索使用 Exa MCP，免费无需 API Key |

---

### TC-06: 社交平台读取测试（需 Cookie）

| 字段 | 内容 |
|------|------|
| **测试目标** | 验证 Agent-Reach 在配置 Cookie 后能否读取社交平台内容 |
| **前置条件** | Twitter 专用小号 Cookie 已配置，代理已配置 |
| **执行步骤** | 1. 配置 Twitter Cookie：`agent-reach configure twitter-cookies "<json>"` |
|  | 2. 执行 `agent-reach twitter read --url "https://x.com/OpenAI/status/xxx"` |
|  | 3. 检查返回的推文内容是否正确 |
| **预期结果** | 步骤 2 返回推文内容、作者和时间信息 |
| **实际结果** | |
| **备注** | 此测试依赖用户手动配置 Cookie，Cookie 未配置时跳过 |

---

### TC-07: PC 端 Mavis 调用测试

| 字段 | 内容 |
|------|------|
| **测试目标** | 验证 PC 端 Mavis 通过 CC Switch 调用 Agent-Reach 是否正常 |
| **前置条件** | CC Switch 已配置 agent-reach-network 节点，Mavis 已连接 |
| **执行步骤** | 1. 在 Mavis 界面输入："读取 https://example.com" |
|  | 2. 观察 CC Switch 是否正确路由至 agent-reach-network |
|  | 3. 检查 Mavis 返回的网页内容是否正确 |
| **预期结果** | Mavis 成功返回 example.com 的网页内容，CC Switch 日志显示请求正确路由 |
| **实际结果** | |
| **备注** | 需要 Mavis 和 CC Switch 均已启动 |

---

### TC-08: 手机端 Mavis 远程调用测试

| 字段 | 内容 |
|------|------|
| **测试目标** | 验证手机端 Mavis 通过内网穿透远程调用 Agent-Reach 是否正常 |
| **前置条件** | PC 端 CC Switch 运行中，内网穿透已配置，手机端 Mavis 已配置远程端点 |
| **执行步骤** | 1. 确认内网穿透连通：手机端 Mavis 发送 "测试连通性" |
|  | 2. 发送网络请求："搜索最新的 AI Agent 新闻" |
|  | 3. 检查返回结果是否正确 |
|  | 4. 发送视频请求："总结这个视频 https://www.bilibili.com/video/BVxxx" |
| **预期结果** | 步骤 1 返回连通性确认；步骤 2 返回搜索结果；步骤 4 返回视频字幕/总结 |
| **实际结果** | |
| **备注** | 需提前配置 frp/ngrok/ZeroTier 等内网穿透工具 |

---

### TC-09: Playwright 兜底切换测试

| 字段 | 内容 |
|------|------|
| **测试目标** | 验证 Agent-Reach 异常时能否自动切换至 Playwright 兜底方案 |
| **前置条件** | Agent-Reach 已安装，Playwright 已安装，CC Switch 已配置兜底路由 |
| **执行步骤** | 1. 模拟 Agent-Reach 异常：停止 agent-reach 服务或配置错误的代理 |
|  | 2. 发送网页读取请求 |
|  | 3. 观察 CC Switch 是否检测到异常 |
|  | 4. 检查是否自动切换至 Playwright 执行 |
|  | 5. 检查返回结果是否正确 |
|  | 6. 恢复 Agent-Reach 服务 |
|  | 7. 再次发送请求，检查是否恢复至 Agent-Reach |
| **预期结果** | 步骤 2-4：CC Switch 检测到异常后自动切换至 Playwright，返回正确结果；步骤 6-7：服务恢复后自动切回 Agent-Reach |
| **实际结果** | |
| **备注** | 可通过修改 config.yaml 代理端口为错误值来模拟异常 |

---

## 测试环境信息

| 项目 | 值 |
|------|-----|
| 操作系统 | Windows 10 (Build 19045) |
| Python 版本 | [待填写] |
| Agent-Reach 版本 | [待填写] |
| 代理地址 | 127.0.0.1:6738 |
| CC Switch 端口 | 18789 |

---

## 测试结论

| 统计项 | 数量 |
|--------|------|
| 总用例数 | 9 |
| 通过 | [待填写] |
| 失败 | [待填写] |
| 跳过 | [待填写] |
| 通过率 | [待填写]% |

**测试结论**: [待填写]

**遗留问题**: [待填写]
