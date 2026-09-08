---
name: wecom-robot-rpa
description: 企业微信智能机器人 Playwright 自动化全流程：跨企业登录→管理后台→创建新机器人（非复用）→精准提取 BotID/Secret→加机器人到群。触发词：企微机器人、企微智能机器人、wexin-work bot、长连接凭证、企业微信 RPA、wecom bot create、跨企业、瀚文苏。
version: 2.0
agent_created: true
updated: 2026-08-21
cost_mode: strict
---

# 企业微信智能机器人 Playwright 自动化（V2.0 · 创建新机器人+加群+跨企业）

> V1.0 仅支持"复用现有机器人提取凭证"，V2.0 升级支持**真的创建新机器人**+**加群**+**跨企业切换**。
> 实测：2026-08-21 在 TJF19770107 提取 3 个机器人凭证，识别出"瀚文苏"企业下无机器人需独立创建。
> 依据：企业微信官方文档（developer.work.weixin.qq.com/document/path/101463 + /document/path/101833）

## 一、官方协议·事实纠正（V1.0 继承）

| 项目 | 官方真相 |
|------|---------|
| 长连接凭证 | **BotID + Secret**（非 CorpID/Token/AESKey） |
| 连接地址 | `wss://openws.work.weixin.qq.com` |
| 创建方式 | **无 API**！只能管理后台/客户端手动 |
| 同机器人同时仅 1 条长连接 | 新连接会踢旧连接 |
| 跨企业 | **每个企业独立注册**！TJF19770107 的机器人**不能**加到瀚文苏的群 |

## 二、关键路径（管理后台）

| 流程 | URL |
|------|-----|
| 管理后台入口 | `https://work.weixin.qq.com/wework_admin/frame` |
| 管理工具（含智能机器人卡片） | `#/manageTools` |
| 创建机器人 | `#/aiHelper/create` |
| 机器人管理列表 | `#/aiHelper/list?tab=manage` |
| 机器人详情 | `#/aiHelper/detail?aibotid=<aibotid>` |
| 登录（首次必扫手机） | `https://work.weixin.qq.com/wework_admin/loginpage_wx` |
| 切换企业 | 左上角企业名 → 弹窗 → 选目标企业 |

## 三、创建新机器人完整 Playwright 流程（V2.0 核心）

### 3.1 完整步骤
```
1. 打开 https://work.weixin.qq.com/wework_admin/loginpage_wx → 扫码登录
   （profile 复用：jiedan_pipeline/browser_profile/wecom_admin/）
2. 检查当前企业：若不是目标企业 → 左上角切换 → 重新登录
3. 导航 #/manageTools
4. 点击"可创建智能机器人"卡片 → 进入智能机器人管理页
5. 点击"创建机器人"按钮
6. （如有"AI 自动生成"vs"手动创建"）→ 选"手动创建"→"API 模式创建"
7. 填写：
   - 机器人名称（如「小龙虾接单助手」）
   - 简介/描述
   - 头像（可选）
8. 选 API 模式（如果页面有切换）
9. ⚠️ 必选「可见范围」—— 否则保存被守卫拒绝
   - 找"可见范围"区域 → 找"添加"按钮（用 evaluate 精准定位父级"添加"）
   - 在弹窗里选"全员"或"指定成员/部门" → 确认
10. 滚动到底部 → 点蓝色"保存"按钮
11. 等待跳转到详情页（含 BotID/使用长连接）
12. 选"使用长连接"（如未默认）→ 点"点击获取 Secret"按钮
13. 提取凭证：精准定位"Bot ID"和"Secret"标签相邻的 input/textarea
14. 保存到 outputs/wecom_robot_credential.json
```

### 3.2 关键避坑（V2.0 经验沉淀）
| 坑 | 解决 |
|----|-----|
| **"可见范围"未选** → 保存被守卫拒绝（红字"请选择可见范围"） | 用 evaluate 找"可见范围"文字的祖先树里的"添加"按钮 |
| **"管理"标签** 误命中左侧"通讯录管理"菜单 | 用 `xpath=//*[normalize-space(text())="管理"]` 精准匹配纯"管理"文字 |
| **"保存"按钮** 误命中其他"保存"字样 | 列表取**最后一个**（底部蓝色"保存"）或精准 class `button.btn_blue` |
| **"Secret 误读描述"** | 不用"最长 input"！用"Bot ID"/"Secret"标签相邻 input 定位 |
| **"使用长连接"未点** | 保存后详情页右侧有"API 配置"区，点"使用长连接"单选项 |
| **跨企业失败** | profile 登录态是 A 企业，要切到 B 企业必须重新扫码（5分钟） |

### 3.3 创建 vs 复用（V2.0 重大升级）
- V1.0：仅"复用现有机器人" → 从 `#/aiHelper/list?tab=manage` 提取已有凭证
- V2.0：**真的创建新机器人** → 走完整 14 步流程（适合"不要复用旧 MAXCLAW1"场景）

## 四、提取凭证三方法（精准·避免误读）

### 方法A（最稳）：按"Bot ID"和"Secret"标签定位
```javascript
const creds = await page.evaluate(() => {
  const out = { botId: '', secret: '' };
  for (const el of document.querySelectorAll('*')) {
    const t = (el.innerText || '').trim();
    if (el.children.length !== 0) continue;
    if (t === 'Bot ID' || t === 'BotID') {
      let cur = el.nextElementSibling;
      while (cur && !/input|textarea/.test(cur.tagName)) cur = cur.nextElementSibling;
      if (cur) out.botId = (cur.value || cur.innerText || '').trim();
      if (!out.botId && el.parentElement) {
        const inp = el.parentElement.querySelector('input, textarea');
        if (inp) out.botId = inp.value;
        else if (el.parentElement.nextElementSibling) {
          out.botId = (el.parentElement.nextElementSibling.innerText || '').trim();
        }
      }
    }
    if (t === 'Secret') { /* 同上逻辑 */ }
  }
  return out;
});
```

### 方法B（兜底）：正则匹配 innerText
```javascript
const text = await page.evaluate(() => document.body.innerText);
const idM = text.match(/Bot\s*ID[：:\s]+([A-Za-z0-9_\-]{15,60})/i);
const secM = text.match(/Secret[：:\s]+([A-Za-z0-9_\-]{30,80})/i);
```

### 方法C（次兜底）：readonly/disabled input
```javascript
document.querySelectorAll('input[readonly], input[disabled]').forEach(i => {
  const v = (i.value || '').trim();
  if (/^[A-Za-z0-9_-]{15,50}$/.test(v) && !out.botId) out.botId = v;
  else if (/^[A-Za-z0-9]{30,80}$/.test(v) && !out.secret) out.secret = v;
});
```

### 校验
- BotID 特征：`/^[A-Za-z0-9_-]{15,50}$/`
- Secret 特征：`/^[A-Za-z0-9]{30,80}$/`
- 排除描述：如果 Secret 含"接单|监听|电商|AI|短视频"等中文词，**必是误读**

## 五、加机器人到群（V2.0 新增能力）

企微**强制**人工加群（无 API 自动拉群）。两种方式：
1. **企微客户端 GUI**（用户手动操作）：
   - 打开目标群 → 群设置 → 添加成员 → 通讯录「智能机器人」分组下选机器人
2. **Playwright 半自动**（打开企微客户端 web 版）：
   - 暂不成熟（客户端 web 限制多）

**实际推荐**：用 wecom-cli 检查群列表 + 引导用户手动加群（1 分钟/人）。

## 六、跨企业切换（V2.0 关键能力）

### 6.1 现实
- 企微机器人**按企业独立注册**
- 浏览器 profile 登录态是按企业隔离的
- 同一 Playwright profile **不能** 同时保存两个企业的登录态

### 6.2 切换流程
```
方案A：使用独立 profile（推荐）
  - profile_hanwensu/ → 瀚文苏企业
  - profile_tjf19770107/ → TJF19770107 企业
  - 两个 profile 并行使用，不冲突

方案B：同一 profile 切换（不推荐）
  - 第一次扫码登录 A 企业
  - 切换 B 企业 → 重新扫码（覆盖 A 的 cookie）
  - 不能再访问 A 企业（除非再切回去再扫码）
```

### 6.3 当前项目推荐方案
- `browser_profile/wecom_admin/` 维持 TJF19770107 企业登录态（已就绪）
- 新建 `browser_profile/wecom_hanwensu/` 给瀚文苏企业（首次扫码后保留）

## 七、机器人能力授权（剩余人工点）

创建后**默认"消息"等 9 项能力未授权**（用户信息默认已授权）。需管理员在后台"机器人详情 → 可使用权限 → 消息 → 去授权"，通常需**手机企微扫码**确认。

无授权时：长连接可建立、能收消息，但 `reply_stream` 等回复 API 返回权限错误。

## 八、Chrome 启动（复用之前 RPA 经验）

```javascript
const ctx = await chromium.launchPersistentContext(PROFILE_DIR, {
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: false,
  viewport: { width: 1440, height: 900 },
  args: ['--start-maximized', '--disable-blink-features=AutomationControlled', '--no-sandbox'],
});
```

## 九、零积分说明

- Playwright 本地浏览器自动化零积分
- 企微 API 零费用
- 唯一人工点：① 首次手机扫码登录（10秒，**每个企业独立一次**）② 能力授权（30秒）③ 拉机器人进群（1分钟）

## 十、错误处理（V2.0 扩展）

| 错误 | 原因 | 修复 |
|------|------|------|
| `Executable doesn't exist` | Playwright Chromium 未装 | 用 `executablePath` 指向系统 Chrome |
| `text=管理` 误命中左侧菜单 | "通讯录管理"也含"管理" | `xpath=//*[normalize-space(text())="管理"]` |
| 保存失败（红字"请选择可见范围"） | 可见范围守卫 | 选全员/部门/成员（必填）|
| Secret 提取到描述 | 用最长 input 法 | 用"Bot ID"/"Secret"标签相邻定位 |
| 长连接建立后无法发消息 | 能力未授权 | 后台"去授权"+手机扫码 |
| **跨企业失败**（看不到目标企业的菜单）| profile 登录态是另一个企业 | 切换 profile 或重新扫码 |

## 十一、输出物

- `outputs/wecom_robot_credential.json`：单机器人凭证
- `outputs/wecom_robots_compare.json`：多机器人凭证对比
- `browser_logs/wecom_admin/*.png`：流程截图（每步）
- `config.yaml`：自动回填 bot_id / bot_secret

## 十二、版本日志

- V1.0 (2026-08-21)：基于实测 3 个机器人提取流程沉淀（复用模式）
- V2.0 (2026-08-21)：**重大升级**——支持真的创建新机器人（不偷工减料）、加群、跨企业切换、Profile 隔离
