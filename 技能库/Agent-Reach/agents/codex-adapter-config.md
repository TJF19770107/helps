# Codex Agent — Agent-Reach 适配配置

> 版本: 1.0.0 | 日期: 2026-06-14

---

## 一、Agent 定位

Codex 是龙虾AI主控中心的代码专项Agent，负责代码生成、代码审查和编程辅助。Agent-Reach 为其提供实时技术文档、开源代码参考和最新API文档读取能力。

---

## 二、调用方式

### 2.1 自然语言触发

```
"查一下 FastAPI 最新版本的 middleware 文档"
"看看这个 GitHub Issue 讨论的解决方案 https://github.com/tiangolo/fastapi/issues/xxx"
"搜索一下 Python 3.13 的 match-case 最佳实践"
```

### 2.2 Shell 命令调用

```powershell
# 读取技术文档
agent-reach web read --url "https://fastapi.tiangolo.com/advanced/middleware/" --format markdown

# GitHub 代码搜索
agent-reach github search --query "fastapi middleware example" --language python

# 读取公开 Gist
agent-reach web read --url "https://gist.github.com/xxx" --format markdown

# Stack Overflow 问答
agent-reach web read --url "https://stackoverflow.com/questions/xxx"
```

### 2.3 MCP 调用示例

```json
{
  "mcp": "agent-reach-network",
  "action": "github_read",
  "params": {
    "repo": "tiangolo/fastapi",
    "path": "docs/en/docs/advanced/middleware.md"
  }
}
```

---

## 三、典型场景映射

| 场景 | 命令 | 说明 |
|------|------|------|
| API 文档查询 | `web read --url` | 实时获取最新文档 |
| 开源代码参考 | `github read --repo` | 查阅开源仓库源码 |
| 代码问题搜索 | `search semantic` | 搜索 Stack Overflow 等 |
| Issue 讨论查阅 | `github issue --repo` | 跟踪开源项目问题 |
| 版本更新日志 | `web read --url` | 读取 CHANGELOG |
| 技术博客追踪 | `rss parse --url` | 订阅技术博客 |

---

## 四、手机端 Mavis 远程调用配置

同 Claude Code 适配配置 §四，Codex 专用参数：

```yaml
# Mavis remote.yaml (Codex 节点)
agent: "codex"
cc_switch_endpoint: "http://<内网IP>:18789"
routes:
  - pattern: ["查文档", "API", "搜索.*代码"]
    node: "agent-reach-network"
```

---

## 五、兜底方案：Playwright 切换

与 Claude Code 一致。Codex 额外配置：

```powershell
# Codex 专属 Playwright 启动参数（无头模式，节省资源）
cc-switch playwright start --headless --disable-gpu --disable-images
```

---

## 六、适配验证清单

- [ ] 技术文档实时读取正常
- [ ] GitHub 仓库/Issue 读取正常
- [ ] 代码搜索正常
- [ ] Mavis 远程调用正常
- [ ] Playwright 兜底切换正常
