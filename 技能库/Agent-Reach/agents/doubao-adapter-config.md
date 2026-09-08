# 豆包PC Agent — Agent-Reach 适配配置

> 版本: 1.0.0 | 日期: 2026-06-14

---

## 一、Agent 定位

豆包PC 是龙虾AI主控中心的办公助手Agent，负责日程管理、邮件处理、办公文档编辑等日常办公任务。Agent-Reach 为其提供实时资讯获取、行业动态追踪和办公参考资料收集能力。

---

## 二、调用方式

### 2.1 自然语言触发

```
"帮我搜索一下最近的行业新闻"
"看看这个竞品官网发布了什么新功能"
"读取这份公开的行业报告"
```

### 2.2 Shell 命令调用

```powershell
# 行业资讯搜索
agent-reach search semantic --query "2026年人工智能行业趋势报告"

# 竞品官网监控
agent-reach web read --url "https://competitor.com/whats-new" --format markdown

# 行业报告获取
agent-reach web read --url "https://example.com/industry-report-2026.pdf" --format markdown

# RSS 订阅行业媒体
agent-reach rss parse --url "https://36kr.com/feed" --limit 10

# 微博热搜（舆情监控）
agent-reach weibo hot --limit 20
```

### 2.3 MCP 调用示例

```json
{
  "mcp": "agent-reach-network",
  "action": "search_semantic",
  "params": {
    "query": "人工智能行业趋势报告 2026",
    "max_results": 10
  }
}
```

---

## 三、典型场景映射

| 场景 | 命令 | 说明 |
|------|------|------|
| 行业资讯 | `search semantic --query` | 实时行业动态 |
| 竞品分析 | `web read --url` | 竞品官网监控 |
| 报告获取 | `web read --url` | 公开行业报告 |
| 舆情监控 | `weibo hot --limit` | 微博热搜 |
| 行业媒体订阅 | `rss parse --url` | 36氪等媒体RSS |
| 财报数据 | `xueqiu stock --symbol` | 雪球行情数据 |

---

## 四、定时任务配置

豆包PC 可配置定时网络任务：

```yaml
# 豆包PC 定时网络任务
scheduled_tasks:
  - name: "每日行业资讯简报"
    cron: "0 8 * * *"
    action: "agent-reach search semantic --query 'AI行业今日新闻'"
    
  - name: "每周竞品监控"
    cron: "0 9 * * 1"
    action: "agent-reach web read --url 'https://competitor.com'"
    
  - name: "RSS 行业媒体扫描"
    cron: "0 */6 * * *"
    action: "agent-reach rss parse --url 'https://36kr.com/feed' --limit 20"
```

---

## 五、手机端 Mavis 远程调用配置

```yaml
# Mavis remote.yaml (豆包PC 节点)
agent: "doubao"
cc_switch_endpoint: "http://<内网IP>:18789"
scheduled_tasks_enabled: true
push_notifications: true  # 定时任务结果推送手机
```

---

## 六、兜底方案：Playwright 切换

```powershell
cc-switch route set --agent doubao --node playwright --duration 30m
```

---

## 七、适配验证清单

- [ ] 行业资讯搜索正常
- [ ] 竞品官网读取正常
- [ ] RSS 行业媒体解析正常
- [ ] 微博热搜获取正常
- [ ] 定时任务执行正常
- [ ] Mavis 远程调用正常
- [ ] Playwright 兜底切换正常
