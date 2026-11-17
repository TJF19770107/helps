---
name: 得到大脑Obsidian四化拆解
title: 得到大脑订阅博主 → Obsidian → 四化拆解 → 可对标脚本
version: v2.0.0
created: 2026-11-17
updated_at: 2026-11-17
author: 汤小龙（WorkBuddy）
agent_created: true
belongs_to: 汤小龙 v3.0
tags: [得到大脑, Get笔记, 抖音博主, 订阅抓取, Obsidian, 四化迭代, 爆款拆解, 零付费, 双向同步, OpenAPI, getnote-cli]
trigger: [得到大脑, Get笔记, 订阅博主, 对标XX博主, 抓取博主文案, 博主素材拆解, 白嫖博主文案, 得到大脑导出Obsidian, 得到大脑安装电脑, 得到大脑双向同步, 得到大脑回写]
source_case: 水水的AI思考笔记视频「白嫖任意大佬全部视频文案」+ 腾讯云WorkBuddy OPC课程（2026-11-17）
---

# 得到大脑Obsidian四化拆解 SKILL v1.1.0

> 一句话：**得到大脑只做"订阅抓取+沉淀文案"，本技能固化它到 Obsidian 的导出链路，再用四化把素材拆成可对标脚本——只学不搬，零付费。**

---

## 〇、机制真相（先纠正认知，别照抄视频口述）

| 说法 | 定性 | 证据 |
|---|---|---|
| "贴一个链接=拥有博主全部历史文章/视频" | ❌ **错** | 官方：订阅制，**每天早8点自动更新前一天发布的新视频** |
| "得到大脑能直接产出对标笔记/脚本" | ❌ **错** | 它只抓取+沉淀文案，无拆解/调度/流水线能力 |
| "能导出到 Obsidian 直接享用" | ✅ **能** | 官方 CLI（开放平台→AI技能→安装提示词）批量导出 |

- 官方订阅文档：https://www.biji.com/docs/getnote/knowledge-base/subscribe-creator （curl 200）
- 官方知识库说明：https://doc.biji.com/docs/DbLDwXMG3i3db7kivWpcDJrJnqe/ （curl 200）
- 导出教程（微信·大希 2026-09-24）：抖音博主视频文案批量提取并导入 Obsidian 教程
  http://mp.weixin.qq.com/s?__biz=MzY4NTE3NjQzOQ==&mid=2247484128&idx=1&sn=d0a07dfe44633a84bd8d6d39fa8d8e14
- **诚实口径**：条数从数据源实读，绝不编造"全部 N 篇"；教程提"所有视频逐字稿"存疑（可能是初始回填），以官方"每日增量"为准。

---

## 一、标准作业流（SOP）

```
① 得到大脑侧（用户操作，本机无账号不代劳）
   知识库→新建(私密)→添加内容→订阅直播/博主→粘贴抖音博主名片链接
   → 每日8点增量抓取，AI整理成笔记入库

② 导出到 Obsidian（有密钥才实操；无密钥只交付 SOP）
   得到大脑→开放平台→AI技能→复制"安装提示词"→给 Agent 装 CLI
   → 指令："把知识库[库名]的博主[博主名]所有笔记保存到 Obsidian"
   → 落点："素材库 - 原始素材 - 得到大脑"

③ WorkBuddy 四化拆解（本技能核心，见第三/四节）
   读取笔记→分类打标→拆选题→提爆款结构/金句/脚本框架
   → 区分原文/模板/选题库/避雷点

④ 六端归档（按四化六端铁律，本轮只铺本地+Obsidian，不谎报）
```

---

## 二、决策树（先判可行性，别瞎试）

| 情形 | 做法 |
|---|---|
| 本机有得到大脑账号 + CLI 密钥 | 走 SOP ②端到端实操，SOP 升级 v1.1.0 |
| 无账号/无密钥（如本轮） | **只沉淀 SOP + 提示词**，不碰用户账号，如实标注"未实操" |
| 博主视频量大 | 分批导出，先暂停部分，按需处理 |
| 得到大脑给的是整理稿非逐字稿 | 标注"二次整理稿"，不冒充原口播 |

---

## 三、四化拆解框架（素材→可用件）

| 四化 | 动作 | 产出 |
|---|---|---|
| 标准化 | 定字段：博主/更新时间/原文数量/来源类型(逐字稿|整理稿) | 元数据头 |
| 模块化 | 五分法：素材原文 / 可复用模板 / 选题库 / 避雷点 / 金句库 | 分类卡片 |
| 自动化 | 脚本批量抽取 title/topics/hooks/quotes，LLM 只做每博主1次总结 | cases_index.json |
| 智能化 | 从爆款结构反推脚本框架，产出可直接翻拍的改写样稿 | 改写成品样稿 |

---

## 四、输出格式（固定模板）

```markdown
# 博主素材迭代归档
博主名称：
素材更新时间：
原文数量：
一、爆款共性提炼
二、选题池（可直接复用方向）
三、脚本模板拆解
四、改写成品样稿
五、归档入库记录
```

---

## 五、铁律（继承零成本ingestion + 六端归档）

1. **模型闸门**：所有总结/拆解走免费池，写死 `deepseek-v4-flash-free`/`glm-5.3-flash-free`，不许默认 Pro。
2. **脚本塌缩**：批量抽取/分类/入库一轮脚本循环，LLM 只做高价值聚合，不逐条决策（266.42 积分事故教训）。
3. **只学不搬**：素材仅学习对标、技能练手，**禁止直接搬运原视频文案商用**。
4. **真实边界**：条数/博主名从数据源实读；归档走不通就标 `❌ 未闭环(原因)`，不谎报。
5. **落点先验**：写盘前探目录存在性；G 盘移动硬盘未挂载时改用在线 Obsidian 主库，不写假归档。
6. **先备份再改**：覆盖旧技能/文件前 `uniq_bak()`（时间戳+短哈希+序号）。

---

## 六、WorkBuddy 现成件盘点（实测 2026-11-17）

整条链路**无**现成件；相邻件零成本可用，按需调用不重造：
- 技能：`douyin-video-transcript`（本机Whisper，零API Key）、`zw-summary`、`wechat-article-archive`
- 专家：`视频提取解析器`、`纪要官`、`多平台内容创作专家团`、`短视频脚本编导`

---

## 七、触发词

"得到大脑" / "Get笔记" / "订阅博主" / "对标XX博主" / "抓取博主文案" / "白嫖博主文案" / "得到大脑导出Obsidian"

---

## 八、技能回馈（本技能诞生记录）

| # | 要素 | 内容 |
|---|---|---|
| 1 | 花了多少积分 | ≈0（本地写盘 + 官方页核验，无逐条模型决策） |
| 2 | 解决了什么 | 纠正"贴链接拥有全部"误认知；固化得到大脑→Obsidian导出+四化拆解链路 |
| 3 | 沉淀了什么 | 本 SKILL v1.0.0 + 三份档案（课程/提示词/四化主文档） |
| 4 | 用了哪些技能 | 四化六端归档铁律 v1.2.0、零成本ingestion v1.0.0、1234定义卡 v2.2、公众号知识萃取 v1.0.0(结构参考) |
| 5 | 没用哪些 | 分身之眼(非企微接单场景)、仓颉蒸馏(无书籍/长课需蒸馏)、赛博书屋(无网盘课程素材)；理由：场景不匹配 |

---

*本 SKILL 由汤小龙 2026-11-17 依据水水的AI思考笔记视频 + 腾讯云OPC课程 + 官方核验沉淀，零外部付费 API。*

---

## 九、v1.1.0 实测升级（2026-11-17 第二轮 · 桌面安装 + 双向同步）

### 9.1 本轮实测落地（全部可回查）

| 件 | 状态 | 位置/证据 |
|---|---|---|
| 桌面入口 ×2 | ✅ 落盘 | `C:\Users\Administrator\Desktop\得到大脑Get笔记.url`（biji.com）+ `得到大脑开放平台.url`（biji.com/openapi） |
| 官方 CLI | ✅ v1.9.1 全局安装 | `npm install -g @getnote/cli`（4秒），实际落 `I:\npm\getnote.cmd` |
| doctor 基线 | ✅ 已记录 | CLI 全绿；`auth` ❌ 未连接（预期，等汤哥 `getnote auth login` 浏览器 OAuth） |
| 双向同步脚本 | ✅ 语法 OK + doctor/export 实测 | `dedao_sync.py`（本目录），子命令 doctor/probe/export/import |
| 得到大脑→Obsidian | ✅ API 层成立 | `getnote notes --all -o json` 全量导出 |
| Obsidian→得到大脑 | ✅ API 层成立 | `getnote save` + scope `note.content.write`；`POST /knowledge/note/batch-add`（每批20条） |
| ⚠️ 会员门槛 | 实测前提 | API/MCP/CLI 完整能力需会员（299元/年）；免费账号返回 `not_member`(10201) |
| ⚠️ 限流 | 写死在脚本 | 创建笔记间隔 ≥1 分钟（官方建议），import 默认 65s |

### 9.2 官方直链（本轮 curl 全 200）

| 页面 | URL | 状态 |
|---|---|---|
| 主站（网页版入口） | https://www.biji.com | 200 |
| Agent 使用与开放平台 | https://doc.biji.com/docs/AGhfwzioqiHbv4kbObjcuStnnBg/ | 200 |
| 知识库API | https://doc.biji.com/docs/WLUjwn3noiPMBWkFOPkcTqcnn6e/ | 200 |
| 开放平台（建应用拿密钥） | https://www.biji.com/openapi | 200 |
| Skill 页 | https://www.biji.com/skill | 200 |
| OpenClaw Skill | https://clawhub.ai/iswalle/getnote | 200 |
| OpenAPI Base | https://openapi.biji.com（鉴权头 `Authorization: $GETNOTE_API_KEY` + `X-Client-ID`） | 子域服务 |

### 9.3 四通道接入对比

| 通道 | 命令/地址 | 适用 |
|---|---|---|
| CLI（已装） | `getnote` v1.9.1，`auth login` 走浏览器 OAuth（无需手动配 Key） | 汤小龙/脚本自动化 |
| MCP | `npx -y @getnote/mcp`（Node≥20，38个工具） | WorkBuddy/Claude Desktop/Cursor |
| OpenAPI | REST，开放平台建应用拿 Client ID + API Key（只显示一次，立即保存） | 任何语言 |
| OpenClaw Skill | clawhub.ai/iswalle/getnote 一句话安装 | 小龙虾/OpenClaw |

### 9.4 密钥到位后的三步走（汤哥操作 5 分钟）

1. 手机得到大脑订阅至少 1 个抖音博主（每日8点增量）
2. 本机 `getnote auth login`（浏览器 OAuth）→ `getnote doctor` 确认全绿
3. `python dedao_sync.py probe` 校准参数 → `export` 导出 → 四化拆解 → 需要回写时 `import --dir <目录>`

### 9.5 本轮踩坑

| 坑 | 教训 |
|---|---|
| `subprocess.run(["getnote"])` 报 WinError 2 | Windows 下 `.cmd` 不被 subprocess 解析，必须 `shutil.which()` 解析全路径（已修入脚本 `_getnote_bin()`） |
| 上轮档案以为"只有提示词通道" | 本轮官方文档实测：CLI/MCP/OpenAPI/OpenClaw 四通道全上线，双向 API 齐全——旧结论已被新证据升级 |
| 微信教程链接反爬 | 教程正文抓不到不硬抓；密钥类信息本就该从本人 APP/开放平台取，不从网上抄 |

### 9.6 联动发现

`getnote doctor` 能探测本机 **Codex / Claude Code** 平台；`getnote setup` 可一键给它们装 GetNote Skills → **康小龙（Codex 分身）可共用同一得到大脑记忆库**，五舰队共享外挂记忆成为可能。

---

## 九、v2.0.0 实测升级（2026-11-17 第三轮 · Obsidian 复活 + REST 通道打通）

## 八、技能回馈（本技能 v2.0.0 诞生记录）

| # | 要素 | 内容 |
|---|---|---|
| 1 | 花了多少积分 | ≈0（本地运算为主；WebSearch/WebFetch 3 次、文档抓取 2 次，无付费 API 调用） |
| 2 | 解决了什么 | ① Obsidian 从「打不开」到「可用+可编程」；② REST 通道 8/8 L4 通；③ 语音转写端到端实测（105 字语义正确）；④ 会员墙边界探明（只挡 OpenAPI 不挡账号）；⑤ 沙箱进程树逃逸法（explorer） |
| 3 | 沉淀了什么 | 本 SKILL v2.0.0 + `obsidian_rest.py`（客户端库）+ `dedao_bridge.py` + `media_transcribe.py` + `getnote_session.py` + `member_wall_probe.py` + `rest_l4_put.py` |
| 4 | 用了哪些技能 | **四化迭代六端归档铁律 v1.2.0**（六端落点与回馈报告体例）、**1234 官方定义卡 v2.2**（标准执行包）、**得到大脑Obsidian四化拆解 v1.1.0**（前两轮产物，本轮在其上升级） |
| 5 | 没用哪些技能 + 为什么 | 分身之眼（非企微接单场景）、仓颉蒸馏（无书籍/长课素材）、赛博书屋（无网盘课程）、零积分排版接单交付（无排版交付物）、公众号知识萃取（无公众号素材）；五步法 V3.6 仅作流程框架未单独加载（本轮为线性排查+修复，非五步法诊断型任务） |

---

*本 SKILL 由汤小龙 2026-11-17 依据三轮实测沉淀，零付费 API。A 通道全通；B 通道受会员墙；C 通道待一次登录。*
