---
name: "browser-auto-universal"
description: "通用浏览器自动化技能V1.0：全窗口通用、跨会话不失效、无记忆断层。支持多种浏览器启动模式、SPA智能等待、检查点持久化、截图日志自动留存。解决Playwright自动化在复杂SPA场景下的导航失败、登录态丢失、跨窗口遮挡等痛点。"
version: "1.0.0"
date: "2026-07-20"
author: "WorkBuddy + 龙虾五步法 V2.7"
trigger_words: ["浏览器自动化", "自动操控浏览器", "browser automation", "playwright", "自动填表", "网页操作", "全自动上传", "控制台操作"]
---

# 通用浏览器自动化技能 V1.0

> **定位**：解决 WorkBuddy 在复杂 Web 应用（腾讯云控制台、CloudBase、ORCA 等 SPA 页面）中的浏览器自动化难题。
> **核心能力**：一次编写 → 多次复用 → 跨会话恢复 → 零记忆断层

---

## 一、问题清单（本技能要解决的痛）

| # | 痛点 | 本方案解法 |
|---|------|-----------|
| 1 | 无法连接已有浏览器（GPT浏览器/自定义Chromium无CDP） | 三种启动模式自适应 |
| 2 | 登录态反复丢失（taskkill/profile锁竞争） | 持久化上下文 + 热备Profile |
| 3 | SPA导航不稳定（URL变了DOM没变） | 双重检测：URL + DOM元素 |
| 4 | 新窗口被遮挡用户看不到 | 自动置顶 + 声音提示 |
| 5 | 每次重跑脚本从零开始 | JSON检查点序列化 + 断点续跑 |
| 6 | 出错后不知道页面长什么样 | 每步自动截图 + 日志 |
| 7 | 中文路径文件选择器失败 | 绕过方案：ZIP+CLI+模拟键盘 |

---

## 二、架构设计

```
┌─────────────────────────────────────────────┐
│              browser-auto-universal          │
│                                             │
│  ┌───────────┐  ┌───────────┐  ┌─────────┐ │
│  │ Browser   │  │  SPA      │  │ Check-  │ │
│  │ Launcher  │  │  Navigator│  │ point   │ │
│  │ (3 modes) │  │ (smart    │  │ Manager │ │
│  │           │  │  wait)    │  │ (JSON)  │ │
│  └─────┬─────┘  └─────┬─────┘  └────┬────┘ │
│        │               │             │       │
│  ┌─────▼───────────────▼─────────────▼─────┐ │
│  │           Core Orchestrator            │ │
│  │  (步骤编排 / 截图日志 / 错误恢复)        │ │
│  └─────────────────────────────────────────┘ │
│                                             │
│  ┌───────────┐  ┌───────────┐  ┌─────────┐ │
│  │ Screenshot│  │  File     │  │ Fallback│ │
│  │ Logger    │  │  Upload   │  │ Chain   │ │
│  │ (每步留存) │  │ (ZIP/路径)│  │ (手动接管)│ │
│  └───────────┘  └───────────┘  └─────────┘ │
└─────────────────────────────────────────────┘
```

---

## 三、三种浏览器启动模式

### Mode A: persistentContext（推荐用于需登录的网站）

```javascript
// 使用持久化浏览器配置目录，登录态跨会话保持
const context = await chromium.launchPersistentContext(USER_DATA_DIR, {
  headless: false,
  viewport: { width: 1280, height: 800 },
  args: ['--start-maximized']
});
```

**优点**：登录一次，永久有效（除非手动清除）
**缺点**：不能连接已有浏览器；需要独占profile目录

**适用场景**：腾讯云控制台、CloudBase、GitHub等需要登录的SPA

### Mode B: connectExisting（连接已有浏览器）

```javascript
// 连接已开启远程调试端口的浏览器
const browser = await chromium.connectOverCDP('http://localhost:9222');
```

**前提条件**：目标浏览器必须以 `--remote-debugging-port=9222` 启动
**适用场景**：标准Chrome/Edge（可配启动参数）；**不适用于GPT浏览器**

### Mode C: launchNew（全新匿名实例）

```javascript
const browser = await chromium.launch({ headless: false });
const context = await browser.newContext();
```

**适用场景**：无需登录的公开页面、一次性操作

### 模式选择决策树

```
需要登录？
├─ 是 → 目标浏览器支持CDP？
│       ├─ 是 → Mode B (connectExisting)
│       └─ 否 → Mode A (persistentContext) ← 最常用
└─ 否 → Mode C (launchNew)
```

---

## 四、SPA智能等待策略

### 问题
CloudBase/腾讯云控制台是Vue/React单页应用：
- URL变化 ≠ DOM更新完成
- `page.goto()` 返回不等于页面渲染完毕
- 动态加载的内容需要额外等待

### 解决方案：双重检测 + 递增超时

```javascript
/**
 * SPA智能等待：同时检测URL和关键DOM元素
 * @param {Page} page - Playwright Page对象
 * @param {Object} opts - 配置
 * @param {string} opts.urlContains - URL应包含的关键词
 * @param {string} opts.selector - 应出现的关键CSS选择器
 * @param {number} opts.timeout - 最大等待ms（默认30000）
 */
async function spaWait(page, { urlContains, selector, timeout = 30000 }) {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    const urlOk = urlContains ? page.url().includes(urlContains) : true;
    let domOk = false;
    if (selector) {
      try {
        const el = await page.$(selector);
        domOk = el !== null && await el.isVisible().catch(() => false);
      } catch(e) { domOk = false; }
    }
    if (urlOk && domOk) return true;
    await page.waitForTimeout(500); // 轮询间隔
  }
  return false; // 超时
}
```

### 常用SPA选择器映射表

| 目标页面 | URL关键词 | 关键选择器 | 备注 |
|---------|----------|-----------|------|
| CloudBase主页 | `tcb.cloud.tencent.com/dev` | `.env-container` 或 `.side-nav` | 左侧菜单栏 |
| CloudBase函数列表 | `/dev#/function` | `.fn-list-table` 或 `[class*=function]` | 函数表格 |
| 云函数创建页 | `/function/create` | `[class*=create]` 或 `form` | 创建表单 |
| 腾讯云登录 | `cloud.tencent.com/login` | `[class*=login]` | 登录框 |

---

## 五、检查点持久化机制

### 设计理念
将每个自动化步骤的状态保存到JSON文件。脚本中断后可以从上次的检查点继续，而不是从头开始。

### 数据结构

```json
{
  "session_id": "cloudbase-deploy-20260720-221000",
  "mode": "A_persistent",
  "browser_status": "running",
  "current_step": 3,
  "steps": [
    { "id": 1, "name": "launch_browser", "status": "completed", "ts": "2026-07-20T22:10:05" },
    { "id": 2, "name": "login_cloudbase", "status": "completed", "ts": "2026-07-20T22:11:30" },
    { "id": 3, "name": "navigate_to_create_fn", "status": "in_progress", "ts": "2026-07-20T22:12:00" },
    { "id": 4, "name": "fill_form_upload_code", "status": "pending", "ts": null }
  ],
  "context_data": {
    "function_name": "hy3-relay-proxy",
    "env_id": "tjf19770107-d0gcttvcmca9c4a3c"
  }
}
```

### API

```javascript
class CheckpointManager {
  constructor(checkpointFile) { /* ... */ }

  // 开始一个步骤
  async startStep(stepId, stepName) { /* ... */ }

  // 完成当前步骤
  async completeStep(stepId, data = {}) { /* ... */ }

  // 从检查点恢复：跳过已完成的步骤
  async resume() { /* 返回下一个待执行的 stepId */ }

  // 获取上次中断位置
  getLastPosition() { /* ... */ }
}
```

---

## 六、截图日志系统

### 规则
1. **每步必截**：每个自动化步骤执行前后各截一张图
2. **错误多截**：catch块中立即截图 + 全屏截图
3. **命名规范**：`{session}_{stepId:02d}_{action}.png`
4. **存储路径**：`./browser_logs/{session_id}/screenshots/`

### 实现

```javascript
async function screenshotStep(page, session, stepId, action) {
  const dir = `./browser_logs/${session}/screenshots`;
  const path = `${dir}/${session}_${String(stepId).padStart(2,'0')}_${action}.png`;
  await page.screenshot({ path, fullPage: true });
  console.log(`[SCREENSHOT] ${path}`);
  return path;
}
```

---

## 七、中文路径/文件上传绕过方案

### 背景
Windows文件选择对话框对深层嵌套中文路径支持不佳（本次实战验证）。

### 方案优先级

| 优先级 | 方案 | 适用场景 | 复杂度 |
|--------|------|---------|--------|
| ⭐⭐⭐⭐⭐ | **方案1: ElementHandle.setInputFiles()** | Playwright直接设置文件输入框的值，完全绕过OS对话框 | 低 |
| ⭐⭐⭐⭐ | **方案2: ZIP代码包上传** | 先用Python打包ZIP，再上传ZIP文件 | 中 |
| ⭐⭐⭐ | **方案3: CLI部署** | 用平台CLI工具（如tcb fn deploy）绕过Web UI | 中 |
| ⭐⭐ | **方案4: 模拟键盘输入路径** | 在文件对话框中用keyboard.type逐字输入路径 | 高且不稳定 |

### 方案1实现（推荐）

```javascript
// 找到文件 input 元素，直接用setInputFiles设置文件
const fileInput = page.locator('input[type="file"]');
await fileInput.setInputFiles('C:/absolute/path/to/file.zip');
// 完全不需要弹出OS文件选择对话框！
```

> **关键发现**：大多数Web应用的"上传"按钮背后都是一个 `<input type="file">` 元素，
> Playwright 的 `setInputFiles` 可以直接操控它，**完全绕过 Windows 文件选择对话框**。

---

## 八、标准使用模板

### 8.1 完整模板（复制即用）

```javascript
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// ========== 配置区 ==========
const CONFIG = {
  // 浏览器模式: A=persistentContext / B=connectCDP / C=launchNew
  mode: 'A',
  
  // 持久化目录（Mode A专用）
  userDataDir: './browser_profile/cloudbase',
  
  // 目标URL
  targetUrl: 'https://tcb.cloud.tencent.com/dev',
  
  // 检查点文件
  checkpointFile: './browser_logs/checkpoint.json',
  
  // 截图目录
  screenshotDir: './browser_logs/screenshots',
  
  // 会话ID
  sessionId: `auto-${new Date().toISOString().replace(/[:.]/g, '-')}`,
};

// ========== 初始化 ==========
function init() {
  [CONFIG.checkpointFile, CONFIG.screenshotDir].forEach(d => {
    if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true });
  });
}

// ========== 主流程 ==========
(async () => {
  init();
  
  let browser, context;
  
  // Step 1: 启动浏览器（根据模式）
  if (CONFIG.mode === 'A') {
    context = await chromium.launchPersistentContext(CONFIG.userDataDir, {
      headless: false,
      viewport: null, // 使用浏览器默认大小
      args: ['--start-maximized', '--disable-blink-features=AutomationControlled'],
    });
    // 持久化模式下 context === browser
    browser = context;
  } else if (CONFIG.mode === 'B') {
    browser = await chromium.connectOverCDP('http://localhost:9222');
    context = browser.contexts()[0];
  } else {
    browser = await chromium.launch({ headless: false });
    context = await browser.newContext();
  }
  
  const page = context.pages()[0] || await context.newPage();
  
  console.log('[STEP 1] Browser launched, mode=' + CONFIG.mode);
  await ss(page, '01_launched');
  
  // Step 2: 导航到目标页面
  await page.goto(CONFIG.targetUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
  console.log('[STEP 2] Navigated to:', page.url());
  await ss(page, '02_navigated');
  
  // Step 3: 等待登录（如需要）
  if (page.url().includes('login')) {
    console.log('[STEP 3] Login required - waiting for user...');
    // 等待URL变化离开login页（最长3分钟）
    await page.waitForURL('**/dev**', { timeout: 180000 });
    console.log('[STEP 3] Login complete!');
    await ss(page, '03_logged_in');
  }
  
  // Step 4+: 你的自定义操作...
  // 使用 spaWait() 等待SPA元素
  // 使用 setInputFiles() 上传文件（绕过OS对话框）
  // 每步调用 ss() 截图
  
  console.log('DONE!');
})().catch(err => {
  console.error('FATAL:', err.message);
}).finally(() => {
  // 不自动关闭浏览器，让用户查看结果
  console.log('Session ended. Browser stays open for inspection.');
});

// 辅助：截图
async function ss(page, name) {
  const p = path.join(CONFIG.screenshotDir, `${CONFIG.sessionId}_${name}.png`);
  await page.screenshot({ path: p, fullPage: true }).catch(() => {});
  console.log(`  📸 ${p}`);
}
```

---

## 九、实战案例：CloudBase云函数一键部署

基于本次经验沉淀的标准流程：

### 前置准备
1. 用Python打包ZIP：`hy3-relay-proxy-code.zip`
2. 确认执行超时设为30秒

### 自动化步骤

| 步骤 | 操作 | 技术要点 |
|------|------|---------|
| 1 | 启动浏览器(Mode A持久化) | 登录态保留 |
| 2 | 导航到CloudBase函数创建页 | spaWait检测左侧菜单 |
| 3 | 如需登录→等用户扫码 | waitForURL离login |
| 4 | 填写函数名/选运行时 | fill() + selectOption() |
| 5 | **上传代码包(setInputFiles)** | ⭐ 核心技巧：绕过OS文件选择器 |
| 6 | 改执行超时30秒 | click + fill |
| 7 | 点创建 | click + waitforResponse |
| 8 | 提取触发器URL | textContent() |
| 9 | 截图确认最终状态 | fullPage screenshot |

### 步骤5的关键代码

```javascript
// 找到隐藏的 <input type="file"> 并直接设置文件
// 这完全绕过了Windows文件选择对话框！
const fileInput = page.locator('input[type="file"][accept*="zip"], input[type="file"]');
if (await fileInput.count() > 0) {
  await fileInput.first().setInputFiles('E:/.../_deploy_package/hy3-relay-proxy-code.zip');
  console.log('✅ File uploaded via setInputFiles (bypassed OS dialog)');
} else {
  console.log('⚠️ No file input found, trying click upload button...');
  // 备选：点击上传按钮后处理新出现的input
  await page.click('text=上传');
  await page.waitForTimeout(1000);
  await page.locator('input[type="file"]').setInputFiles(zipPath);
}
```

---

## 十、CloudBase 小程序成长计划入口（⭐ 2026-07-20 实战沉淀）

### 正确入口路径（用户确认，必须从此入口进入！）

```
┌─────────────────────────────────────────────────────────────┐
│  微信公众平台                                              │
│    → 行业能力                                             │
│      → 小程序成长计划                                      │
│        → 「云开发资源及混元免费Token」卡片                  │
│          → 绿色按钮「去使用」                               │
│            → 自动跳转 tcb.cloud.tencent.com/dev             │
│              → 左侧菜单「云函数」→「云函数托管」            │
│                → 「新建」→ 选「通过代码包创建」tab          │
│                  → 函数类型: HTTP云函数 (非普通云函数!)     │
│                    → 函数名: hy3-relay-proxy               │
│                      → 运行环境: Node.js 20.19             │
│                        → 提交方式: 本地上传zip包           │
│                          → 上传代码包ZIP                   │
│                            → ⭐ 执行超时: 30秒 (默认3秒必挂)│
│                              → 点「创建」                │
│                                → 创建HTTP触发器           │
│                                  → 路径: /hy3-relay-proxy  │
│                                    → 提取公网地址 ✅       │
└─────────────────────────────────────────────────────────────┘
```

### ⚠️ 关键注意事项

| 项目 | 值 | 说明 |
|------|-----|------|
| **执行超时** | **必须30秒** | 默认3秒，AI调用必超时 |
| **函数类型** | **HTTP云函数** | 非普通云函数，否则无法通过HTTP访问 |
| **提交方式** | **本地上传zip包** | 不要用「本地上传文件夹」（中文路径会空） |
| **EnvID** | `tjf19770107-d0gcttvcmca9c4a3c` | 小程序成长计划环境 |

### 登录态管理经验

| 现象 | 根因 | 解决方案 |
|------|------|---------|
| 持久化context登录过期 | `taskkill` 清掉cookie / session超时(约2h) | 检测URL含`/login`→等用户扫码(5min) |
| 登录页误判为已登录 | 登录页本身含"腾讯云 CloudBase"文字 | **双重检测**: URL含`/login` + bodyText含"登录控制台" |
| bodyHTML只有~2KB | 在登录页非控制台 | 等HTML>10KB再继续操作 |
| GPT浏览器无法CDP连接 | 自定义Chromium无remote-debug端口 | 用Mode A持久化context启动新Chromium实例 |

---

## 十一、防踩坑清单

| # | 坑 | 解法 |
|---|-----|------|
| 1 | **f-string写进JS** | JS用模板字符串 `` `text ${var}` ``，不要用 Python f-string |
| 2 | **箭头函数return省略{}** | `( ) => expr` 不能带 `{}` 和 `return`，要用 `() => { return expr; }` |
| 3 | **taskkill清掉登录态** | 不要杀浏览器进程；用 browser.close() 优雅关闭 |
| 4 | **Chinese path in file picker** | 用 setInputFiles() 直接设置，不弹OS对话框 |
| 5 | **SPA DOM未就绪就用selector** | 用 spaWait() 双重检测，别只信 waitForSelector |
| 6 | **截图路径含中文报错** | 用ASCII路径存截图，或确保目录先存在 |
| 7 | **playwright装在workspace外找不到** | NODE_PATH指向正确node_modules目录 |
| 8 | **GPT浏览器不支持CDP连接** | 必须用 Mode A (persistentContext) 启动新实例 |

---

## 十二、快速参考卡

```bash
# 安装 Playwright（如果还没装）
cd ~/.workbuddy/binaries/node/workspace && npm install playwright

# 检查语法
node --check your_script.js

# 运行（带NODE_PATH）
NODE_PATH=~/.workbuddy/binaries/node/workspace/node_modules node your_script.js

# 截图目录
./browser_logs/{session_id}/screenshots/

# 检查点文件
./browser_logs/checkpoint.json

# 持久化浏览器配置（登录态保存在此）
./browser_profile/cloudbase/
```

---

*版本: 1.0.0 | 生效日期: 2026-07-20 | 来源: 2026-07-20 CloudBase实战排障沉淀*
