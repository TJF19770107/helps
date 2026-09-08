# OpenClaw Agent — Agent-Reach 适配配置

> 版本: 1.0.0 | 日期: 2026-06-14

---

## 一、Agent 定位

OpenClaw 是龙虾AI主控中心的跨平台全能Agent，已原生内置 Agent-Reach 支持。本文档说明在龙虾AI主控中心统一调度下的适配配置。

---

## 二、调用方式

### 2.1 OpenClaw 内置集成

OpenClaw 已通过 Skill 注册方式集成 Agent-Reach，无需额外配置：

```bash
# OpenClaw 中注册 Agent-Reach 为 Skill
npx skills add Panniantong/Agent-Reach@agent-reach

# 或直接作为 Skill 加载
openclaw skill load agent-reach
```

### 2.2 原生调用（OpenClaw 内部直接执行）

```
"帮我看看这个链接写了什么"
"这个 YouTube 视频的内容总结一下"
"GitHub 上搜索 LLM 框架"
"订阅这个 RSS 源"
```

### 2.3 通过 CC Switch 统一调度

当通过龙虾AI主控中心 CC Switch 调用时：

```json
{
  "agent": "openclaw",
  "route": "agent-reach-network",
  "action": "web_read",
  "params": {
    "url": "https://example.com",
    "format": "markdown"
  }
}
```

### 2.4 Shell 命令调用

```powershell
# OpenClaw 内直接执行
agent-reach web read --url "https://xxx.com"
agent-reach youtube subtitle --url "https://www.youtube.com/watch?v=xxx"
agent-reach github search --query "AI agent"
```

---

## 三、OpenClaw 特有配置

### 3.1 exec 权限开启

OpenClaw 首次安装 Agent-Reach 前需要开启 exec 权限：

```bash
openclaw config set tools.profile "coding"
# 然后重启 Gateway
openclaw gateway restart
```

### 3.2 Skill 配置

```yaml
# openclaw-skills.yaml
skills:
  agent-reach:
    source: "Panniantong/Agent-Reach@agent-reach"
    auto_update: true
    channels:
      - web_reading
      - youtube
      - github
      - rss
      - semantic_search
```

---

## 四、手机端 Mavis 远程调用配置

OpenClaw 本身支持远程 Gateway，可直接通过以下方式暴露：

```yaml
# OpenClaw Gateway 配置
gateway:
  host: "0.0.0.0"
  port: 18789
  auth:
    type: "token"
    token: "<生成的认证令牌>"

# Mavis 端配置
openclaw_endpoint: "http://<公网IP>:18789"
```

---

## 五、兜底方案：Playwright 切换

OpenClaw 也支持 Playwright 作为浏览器引擎的兜底：

```bash
# OpenClaw 切换浏览器引擎为 Playwright
openclaw config set browser.engine "playwright"
openclaw config set browser.endpoint "http://127.0.0.1:9222"
```

---

## 六、适配验证清单

- [ ] OpenClaw 内置 Agent-Reach 集成正常
- [ ] CC Switch 统一调度正常
- [ ] exec 权限配置正确
- [ ] 全部 8 个基础通道可用
- [ ] Mavis 远程调用正常
- [ ] Playwright 兜底切换正常
