# Hermes Agent — Agent-Reach 适配配置

> 版本: 1.0.0 | 日期: 2026-06-14

---

## 一、Agent 定位

Hermes 是龙虾AI主控中心的主搜索Agent，负责信息检索、知识整理和情报分析。Agent-Reach 是其核心工具，提供全域网络搜索和实时信息获取能力。

---

## 二、调用方式

### 2.1 自然语言触发

Hermes 是搜索主力，以下触发模式自动路由至 agent-reach-network：

```
# 全景搜索
"搜索2026年AI Agent领域的最新进展和发展趋势"
"帮我全面调研一下 LLM 推理加速的最新方案"

# 对比搜索
"对比一下 OpenAI、Anthropic 和 Google 2026年的模型发布策略"

# 情报整理
"收集最近一周关于AI安全监管的新闻和讨论"
"整理 GitHub 上 star 超过 10k 的 AI Agent 框架"

# 多源交叉验证
"关于XX事件，Twitter和微博上的讨论有什么不同"
```

### 2.2 高级搜索命令

```powershell
# 全网语义搜索（主力）
agent-reach search semantic --query "AI Agent multi-modal 2026 breakthrough"

# 多平台并行搜索
agent-reach search semantic --query "quantum computing progress 2026" --sources github,arxiv,reddit

# GitHub 搜索（精确过滤）
agent-reach github search --query "LLM agent" --stars ">=10000" --language python --sort stars

# 时间范围搜索
agent-reach search semantic --query "GPT-5 announcement" --time-range 7d

# 技术博客订阅搜索
agent-reach rss parse --url "https://feeds.feedburner.com/blogspot/gJZg" --limit 20
```

### 2.3 MCP 调用示例

```json
{
  "mcp": "agent-reach-network",
  "action": "search_semantic",
  "params": {
    "query": "AI Agent framework comparison 2026",
    "max_results": 20,
    "sources": ["github", "arxiv", "web"]
  }
}
```

---

## 三、搜索策略配置

### 3.1 搜索深度分级

| 级别 | 说明 | 搜索范围 | 结果数量 |
|------|------|----------|----------|
| 快速 | 日常查询 | 1-2 平台 | 5-10 |
| 标准 | 一般调研 | 全平台语义搜索 | 10-20 |
| 深度 | 全面调研 | 多轮迭代搜索 | 20-50 |
| 全景 | 系统性研究 | 全平台 + RSS + 时间轴 | 50+ |

### 3.2 平台权重配置

```yaml
# Hermes 搜索权重
search_weights:
  github: 0.25       # 技术类优先 GitHub
  arxiv: 0.20        # 学术论文
  web: 0.20          # 通用网页
  reddit: 0.10       # 社区讨论
  twitter: 0.10      # 实时动态
  zhihu: 0.05        # 中文技术社区
  weibo: 0.05        # 中文社交媒体
  xiaohongshu: 0.05  # 生活方式类
```

---

## 四、手机端 Mavis 远程调用配置

Hermes 作为搜索主力，Mavis 远程调用频率最高：

```yaml
# Mavis remote.yaml (Hermes 节点)
agent: "hermes"
cc_switch_endpoint: "http://<内网IP>:18789"
priority: "high"  # 搜索请求高优先级
rate_limit:
  max_per_minute: 20
  max_per_hour: 200
default_search_depth: "standard"  # 手机端默认标准深度
```

---

## 五、兜底方案：Playwright 切换

Hermes 在 Agent-Reach 搜索无结果或异常时自动切换：

```powershell
# 搜索兜底策略
# 1. agent-reach search semantic → 2. agent-reach web read → 3. Playwright
cc-switch route fallback --agent hermes --strategy "cascade"
```

---

## 六、适配验证清单

- [ ] 快速搜索正常
- [ ] 标准搜索正常
- [ ] 深度搜索正常
- [ ] GitHub 精确搜索正常
- [ ] RSS 订阅搜索正常
- [ ] 多平台并行搜索正常
- [ ] Mavis 远程搜索正常
- [ ] Playwright 兜底切换正常
