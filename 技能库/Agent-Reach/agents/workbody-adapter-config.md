# Workbody Agent — Agent-Reach 适配配置

> 版本: 1.0.0 | 日期: 2026-06-14

---

## 一、Agent 定位

Workbody 是龙虾AI主控中心的文档处理Agent，负责文档生成、格式化、排版和知识管理。Agent-Reach 为其提供在线参考资料获取、知识库补充和实时信息检索能力。

---

## 二、调用方式

### 2.1 自然语言触发

```
"帮我在网上找一份关于项目管理的模板参考"
"搜索最新的 Markdown 转 PDF 的最佳实践"
"看看 Confluence 这个页面里的文档结构"
```

### 2.2 Shell 命令调用

```powershell
# 参考资料获取
agent-reach web read --url "https://www.projectmanagement.com/" --format markdown

# 技术文档参考
agent-reach web read --url "https://www.markdownguide.org/" --format markdown

# GitHub 文档参考
agent-reach github read --repo "satwikkansal/wtfpython" --path "README.md"

# 微信公号文章获取
agent-reach wechat search --query "项目管理最佳实践"
```

### 2.3 MCP 调用示例

```json
{
  "mcp": "agent-reach-network",
  "action": "web_read",
  "params": {
    "url": "https://example.com/template",
    "format": "markdown"
  }
}
```

---

## 三、典型场景映射

| 场景 | 命令 | 说明 |
|------|------|------|
| 模板参考 | `web read --url` | 在线文档模板 |
| 知识库补充 | `search semantic --query` | 最新资料 |
| 技术规范查阅 | `web read --url` | RFC/标准文档 |
| 公众号文章 | `wechat search --query` | 微信生态内容 |
| GitHub 文档 | `github read --repo` | 开源文档参考 |

---

## 四、手机端 Mavis 远程调用配置

```yaml
# Mavis remote.yaml (Workbody 节点)
agent: "workbody"
cc_switch_endpoint: "http://<内网IP>:18789"
max_content_length: 10000  # 文档Agent限制内容长度
auto_summarize: true        # 自动摘要长内容
```

---

## 五、兜底方案：Playwright 切换

```powershell
cc-switch route set --agent workbody --node playwright --duration 30m
```

---

## 六、适配验证清单

- [ ] 网页参考材料获取正常
- [ ] 技术文档查阅正常
- [ ] 微信公众号搜索正常
- [ ] GitHub 文档读取正常
- [ ] Mavis 远程调用正常
- [ ] Playwright 兜底切换正常
