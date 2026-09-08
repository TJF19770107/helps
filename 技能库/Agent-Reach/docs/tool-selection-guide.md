# Agent-Reach vs Playwright 分工使用指引

> 版本: 1.0.0 | 日期: 2026-06-14

---

## 一、对比总览

| 维度 | Agent-Reach | Playwright |
|------|------------|------------|
| **定位** | 轻量级网络读取脚手架 | 重量级浏览器自动化引擎 |
| **资源消耗** | 极低（纯命令行，无浏览器） | 高（需启动完整 Chromium） |
| **安装难度** | 低（pip install 一条命令） | 中（需安装浏览器驱动） |
| **平台覆盖** | 14+ 平台（专有通道） | 任意网站（通用浏览器访问） |
| **JS 渲染能力** | 有限（通过 Jina Reader） | 完整（真实浏览器引擎） |
| **交互能力** | 只读（读取/搜索/提取） | 完整（点击/输入/滚动/截图） |
| **反爬绕过** | 基础（Jina Reader 中转） | 强（真实浏览器行为） |
| **适用场景** | 日常信息获取、内容提取、搜索 | 复杂交互、强反爬、表单填写 |
| **维护成本** | 低（社区维护 upstream tools） | 中（自维护脚本，适应网站变化） |
| **Cookie 管理** | 平台级配置，一次配置复用 | 需在脚本中手动管理 |
| **并发能力** | 支持多平台并发 | 单浏览器实例 |

---

## 二、选型决策树

```
用户请求
    │
    ├── 是日常信息获取（读网页/看视频/搜资料/读GitHub）？
    │       └── 是 → 使用 Agent-Reach ✅
    │
    ├── 需要登录后才能访问的内容？
    │       ├── 平台在 Agent-Reach 支持列表中？
    │       │       └── 是 → 配置 Cookie 后使用 Agent-Reach ✅
    │       └── 平台不在支持列表中？
    │               └── 使用 Playwright ❗
    │
    ├── 需要复杂交互（点击/滚动/拖拽/表单填写）？
    │       └── 是 → 使用 Playwright ❗
    │
    ├── 目标网站有强反爬（DataDome/Cloudflare JS Challenge）？
    │       └── 是 → 先试 Agent-Reach，失败则降级 Playwright ❗
    │
    ├── 需要截图/PDF 导出？
    │       └── 是 → 使用 Playwright ❗
    │
    └── 是批量数据采集（大规模爬取）？
            └── 是 → 不推荐（违反使用规范），如果必须则 Playwright + 严格限速 ❗
```

---

## 三、场景分工详细表

### 3.1 Agent-Reach 擅长的场景（日常主力）

| 场景 | 命令示例 | 为什么用 Agent-Reach |
|------|----------|---------------------|
| 阅读技术文档 | `web read --url <url>` | 轻量快速，Markdown 输出 |
| 视频内容总结 | `youtube subtitle --url <url>` | 专有通道，直接提取字幕 |
| GitHub 项目调研 | `github read --repo <repo>` | 专有通道，结构化输出 |
| 技术搜索 | `search semantic --query <q>` | 免费语义搜索 |
| RSS 订阅追踪 | `rss parse --url <url>` | 专有 RSS 解析 |
| 公众号文章 | `wechat search --query <q>` | 专有通道 |
| B站字幕 | `bilibili subtitle --url <url>` | 本地即可用 |

### 3.2 Playwright 擅长的场景（复杂专项）

| 场景 | 说明 | 为什么用 Playwright |
|------|------|---------------------|
| 强反爬网站 | DataDome/CAPTCHA | 真实浏览器，不易被检测 |
| 表单自动填写 | 注册/登录/提交 | 完整交互能力 |
| 页面截图 | 需要视觉验证 | 原生截图 API |
| PDF 导出 | 网页转 PDF | 内置打印到 PDF |
| SPA 单页应用 | 内容全部由 JS 渲染 | 完整 JS 引擎 |
| 多步骤工作流 | 登录→导航→操作→提取 | 脚本化流程控制 |
| 不可预见的网站 | Agent-Reach 不支持 | 通用浏览器万能 |

---

## 四、切换流程

### 4.1 自动切换（推荐）

```
Agent-Reach 请求
       ↓
正常返回？── 是 → 返回结果给 Agent
       │
       否（超时/403/429/Blocked）
       ↓
CC Switch 检测异常
       ↓
自动路由至 Playwright 节点
       ↓
Playwright 执行请求
       ↓
返回结果 + 记录切换日志
```

### 4.2 手动切换命令

```powershell
# 临时切换所有 Agent 到 Playwright（30 分钟）
cc-switch route set --node playwright --duration 30m

# 仅切换某个 Agent
cc-switch route set --agent hermes --node playwright

# 恢复
cc-switch route set --node agent-reach-network

# 查看当前路由状态
cc-switch route status
```

### 4.3 Playwright 调用模板

```python
# E:\龙虾AI主控中心\我的AI分身\技能库\Agent-Reach\templates\playwright-fallback.py

from playwright.sync_api import sync_playwright
import sys
import json

def read_url(url: str, wait_seconds: int = 3) -> dict:
    """
    Playwright 兜底读取方案
    当 Agent-Reach 无法读取时自动调用
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--disable-gpu', '--no-sandbox']
        )
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        
        try:
            page.goto(url, wait_until='networkidle', timeout=30000)
            page.wait_for_timeout(wait_seconds * 1000)
            
            content = page.content()
            title = page.title()
            text = page.inner_text('body')
            
            return {
                'success': True,
                'url': url,
                'title': title,
                'text': text[:5000],  # 限制长度
                'method': 'playwright_fallback'
            }
        except Exception as e:
            return {
                'success': False,
                'url': url,
                'error': str(e),
                'method': 'playwright_fallback'
            }
        finally:
            browser.close()

if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else 'https://example.com'
    result = read_url(url)
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

---

## 五、选型结论

| 维度 | 结论 |
|------|------|
| **日常主力** | Agent-Reach —— 覆盖 90% 日常网络读取需求 |
| **复杂专项** | Playwright —— 处理强反爬和复杂交互场景 |
| **切换策略** | Agent-Reach 异常时 CC Switch 自动切换 Playwright |
| **成本最优** | Agent-Reach 低资源消耗，Playwright 按需启动 |
| **维护原则** | Agent-Reach 跟随社区更新，Playwright 脚本自主维护 |

---

## 六、升级与维护

| 维护项 | 频率 | 操作 |
|--------|------|------|
| Agent-Reach 版本更新 | 每两周 | `pip install --upgrade agent-reach` |
| Playwright 浏览器更新 | 每月 | `playwright install --force chrome` |
| Cookie 轮换 | 每月 | 更新 config.yaml 中各平台 Cookie |
| 健康检查 | 每周 | `agent-reach doctor` |
| 日志审查 | 每周 | 检查拦截率、异常日志 |
