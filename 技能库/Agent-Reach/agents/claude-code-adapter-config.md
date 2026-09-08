# Claude Code Agent — Agent-Reach 适配配置

> 版本: 1.0.0 | 日期: 2026-06-14

---

## 一、Agent 定位

Claude Code 是龙虾AI主控中心的主开发Agent，负责代码编写、项目分析和复杂任务编排。Agent-Reach 为其提供全域网络信息读取能力，支撑技术调研、文档查阅和开源项目分析。

---

## 二、调用方式

### 2.1 自然语言触发

直接对 Claude Code 说出需求，CC Switch 会自动路由至 agent-reach-network：

```
# 网页读取
"帮我看下 https://docs.python.org/3/whatsnew/3.12.html 有哪些新特性"

# GitHub 仓库分析
"分析一下 https://github.com/Panniantong/agent-reach 这个项目的架构"

# 技术搜索
"搜索一下2026年最流行的Python异步框架"

# 视频内容提取
"这个 B站教程讲了什么 https://www.bilibili.com/video/BV1xx411c7mD"
```

### 2.2 Shell 命令调用（直接模式）

当需要精确控制参数时，可直接在终端执行：

```powershell
# 网页读取（Markdown 格式）
agent-reach web read --url "https://xxx.com" --format markdown

# GitHub 搜索
agent-reach github search --query "LLM agent framework" --stars ">=1000"

# YouTube 字幕
agent-reach youtube subtitle --url "https://www.youtube.com/watch?v=xxx" --lang zh-CN

# B站字幕
agent-reach bilibili subtitle --url "https://www.bilibili.com/video/BVxxx"

# 全网语义搜索
agent-reach search semantic --query "Python async best practices 2026"

# RSS 解析
agent-reach rss parse --url "https://blog.python.org/feeds/posts/default" --limit 10
```

### 2.3 MCP 调用示例

```json
{
  "mcp": "agent-reach-network",
  "action": "web_read",
  "params": {
    "url": "https://example.com",
    "format": "markdown"
  }
}
```

---

## 三、典型场景映射

| 场景 | 触发方式 | 调用命令 |
|------|----------|----------|
| 技术文档查阅 | 自然语言 | `agent-reach web read --url` |
| GitHub 项目调研 | 自然语言 | `agent-reach github read --repo` |
| 开源组件搜索 | 自然语言 | `agent-reach github search --query` |
| API 文档获取 | 自然语言 | `agent-reach web read --url --format markdown` |
| 技术博客订阅 | Shell | `agent-reach rss parse --url` |
| 会议视频总结 | 自然语言 | `agent-reach youtube subtitle --url` |
| 技术趋势搜索 | 自然语言 | `agent-reach search semantic --query` |

---

## 四、手机端 Mavis 远程调用配置

### 4.1 架构

```
手机端 Mavis → 内网穿透/端口映射 → CC Switch → agent-reach-network
```

### 4.2 配置步骤

1. **确保 PC 端 CC Switch 监听内网端口**
   - 默认端口：18789
   - 确认防火墙放通该端口

2. **配置内网穿透**
   - 使用 frp / ngrok / ZeroTier 等工具
   - 将 PC 内网 IP 的 18789 端口映射到公网

3. **Mavis 端配置**
   ```yaml
   # Mavis remote.yaml
   cc_switch_endpoint: "http://<公网IP或域名>:<映射端口>"
   node_name: "agent-reach-network"
   auth_token: "<CC Switch 认证令牌>"
   ```

4. **验证连通性**
   ```
   手机端 Mavis 发送: "测试: 读取 https://httpbin.org/ip"
   预期返回: 服务器出口 IP
   ```

### 4.3 安全建议

- 使用 HTTPS + Token 认证
- 限制请求频率（每分钟 ≤ 10 次）
- 仅开放 agent-reach-network 节点权限

---

## 五、兜底方案：Playwright 切换

### 5.1 自动切换条件

- agent-reach 连续 3 次请求超时（30秒）
- 返回 HTTP 403 / 429
- 返回 "Blocked" / "Captcha"
- agent-reach doctor 显示关键通道红色

### 5.2 手动切换命令

```powershell
# 在 CC Switch 中临时切换路由
cc-switch route set --node playwright --duration 30m

# 恢复
cc-switch route set --node agent-reach-network
```

### 5.3 Playwright 调用示例

```python
# Python 调用 Playwright
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")
    content = page.content()
    browser.close()
```

---

## 六、适配验证清单

- [ ] 自然语言触发网页读取正常
- [ ] Shell 命令直接调用正常
- [ ] GitHub 公开仓库读取正常
- [ ] 视频字幕提取正常
- [ ] RSS 订阅解析正常
- [ ] 全网搜索正常
- [ ] Mavis 远程调用正常
- [ ] Playwright 兜底切换正常
- [ ] Cookie 配置后社交平台读取正常
