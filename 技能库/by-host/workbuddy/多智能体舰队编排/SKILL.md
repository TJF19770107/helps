---
name: "多智能体舰队编排"
description: "基于 ORCA 的多智能体舰队编排架构与实战指南。覆盖 MiMO V2.5 Pro + Claude Code + Codex++ + Marvis + WorkBuddy 的编组方案、端口链路、Git Worktree 隔离、任务路由（量化/商单/小说/飞书）、统一聊天窗口（Chatbox）、技能共享架构、变现路线图。适用于龙虾AI主控中心的全域多Agent协作场景。"
version: "1.1"
date: "2026-07-14"
author: "WorkBuddy + 龙虾AI主控中心"
primary_path: "~/.workbuddy/skills/多智能体舰队编排/SKILL.md"
shared_path: "E:/龙虾AI主控中心/我的AI分身/技能库/多智能体舰队编排/SKILL.md (已镜像 ✅ 2026-07-14)"
---

# 多智能体舰队编排 — ORCA 舰队实战手册 v1.1

> **版本**：v1.1 | **生效日期**：2026-07-14 | **适用范围**：全域 / 永久
> **核心引擎**：MiMO V2.5 Pro（token-plan-cn.xiaomimimo.com/v1, 端口 18808）
> **编排框架**：ORCA（stablyai/orca）| **协议**：CC-Switch(15721) → AI Code Switch(4567) → MiMO(18808)

---

## 〇、技能存在哪？共享架构（用户核心疑问）

**结论**：技能的**权威源（canonical）应放在你 E 盘的共享技能库**，所有 AI 分身（Codex / Claude Code / Hermes / Marvis / WorkBuddy）从同一处读取，避免各存各的导致版本分裂。WorkBuddy 要能加载，需要在它自己的技能目录里有一份（junction 软链或镜像）。

| 位置 | 作用 | 状态 |
|------|------|------|
| `E:\龙虾AI主控中心\我的AI分身\技能库\` | **权威源·全员共享·git 版本化** | ✅ 已镜像（2026-07-14：mimo-bridge / ollama-bridge / 本技能） |
| `~\.workbuddy\skills\` | WorkBuddy 实际加载处 | ✅ 已写入（mimo-bridge / ollama-bridge / 本技能） |

**已于 2026-07-14 执行完成（你已授权 E 盘写入）**，命令留存作后续增量同步参考：
```bash
# 把 WorkBuddy 技能镜像到共享库（单向同步，以 E 盘为权威）
robocopy "C:\Users\Administrator\.workbuddy\skills\mimo-bridge" "E:\龙虾AI主控中心\我的AI分身\技能库\mimo-bridge" /E /COPYALL
robocopy "C:\Users\Administrator\.workbuddy\skills\ollama-bridge" "E:\龙虾AI主控中心\我的AI分身\技能库\ollama-bridge" /E /COPYALL
robocopy "C:\Users\Administrator\.workbuddy\skills\多智能体舰队编排" "E:\龙虾AI主控中心\我的AI分身\技能库\多智能体舰队编排" /E /COPYALL
```
> 中文名技能**不会冲突**（系统自带「多模态内容生成」即中文）。唯一要求：目录名全局唯一。

---

## 一、为什么用中文名？会冲突吗？

**不会冲突。** 证据：WorkBuddy 内置技能「多模态内容生成」就是中文名，Skill 系统支持 Unicode 目录名。调用时用 `Skill` tool 传 `skill: "多智能体舰队编排"` 即可。建议英文 slug 作备用标识，中文作显示名。

---

## 二、舰队总览：你的 AI 兵力清单

```
┌─────────────────────────────────────────────────────────────┐
│                    🚢 ORCA 舰队指挥中心                        │
│              (Fleet Manager / 并行编排层)                      │
└──────────┬──────────┬──────────┬──────────┬─────────────────┘
           │          │          │          │
     ┌─────▼────┐ ┌──▼───┐ ┌───▼──┐ ┌───▼────┐ ┌──▼──────┐
     │ MiMO V2.5││Claude││Codex ││Marvis  ││WorkBuddy│
     │ Pro 主引擎││ Code ││ ++   ││ 自动化  ││  Hy3    │
     │ (18808)  ││多模态 ││协议  ││调度    ││办公Agent│
     └─────▲────┘ └──────┘ └──▲───┘ └───▲────┘ └─────────┘
           │                │         │
     ┌─────┴────────────────┴─────────┴──────────────────┐
     │              CC-Switch (15721) 总网关               │
     │            AI Code Switch (4567) 协议转换            │
     └────────────────────┬──────────────────────────────┘
                          │
               ┌──────────▼──────────┐
               │   token-plan-cn      │
               │ xiaomimimo.com/v1   │
               │  (MiMO API 端点)     │
               └─────────────────────┘
```

### 各 Agent 角色定位

| Agent | 核心职责 | 强项 | 弱项 | 推荐任务类型 |
|-------|---------|------|------|-------------|
| **MiMO V2.5 Pro** | 主推理引擎 | 长程 Agent(1000+工具调用)、Token 效率高(省40-60%)、1M上下文 | 数学推理一般、纯文本无语音 | 量化策略编写、长代码生成 |
| **Claude Code** | 多模态编码 | 截图调试、UI稿→代码、图片分析 | Token 成本较高 | 前端、UI 还原、截图排错 |
| **Codex++** | 协议转换/IDE集成 | VSCode/Cursor 深度集成 | 依赖 CC-Switch 中转 | IDE 内编码、协议桥接 |
| **Hermes** | 大脑/指挥官 | 多模型编排、任务拆解路由 | 需配置 API | 舰队总调度、复杂规划 |
| **Marvis** | 任务自动化调度 | 定时任务、Token 统计、监控面板 | 当前半加载故障(待修复) | 批量调度、监控 |
| **WorkBuddy (Hy3)** | 办公/搜索 Agent + 对话入口 | BrowseComp 84.2≈GPT-5.5、搜索强 | 数学弱、纯文本 | 文档、研报、商单交付物、聊天指挥 |
| **DeerFlow** | 研究/工作流 | 已部署 .trae/skills/ | 待激活 | 知识库研究、流程自动化 |

---

## 三、端口与链路全景图

```
用户指令
  ▼
┌──────────────┐
│  ORCA 编排器  │ ← Fleet Manager（拆分/路由/聚合）
└──────┬───────┘
       │ 并行分发
       ▼
┌─────────────────────────────────────────────────┐
│         CC-Switch :15721 （总网关·不可改）        │
│         AI Code Switch :4567 （协议转换）         │
│  ANTHROPIC_BASE_URL → token-plan-cn.xiaomimimo   │
│                  /anthropic/v1                    │
└────────────────────┬────────────────────────────┘
                     ▼
        ┌────────────────────────┐
        │  MiMO V2.5 Pro API     │
        │  https://token-plan-   │
        │  cn.xiaomimimo.com/v1  │
        │  端口 18808（本地代理） │
        └────────────────────────┘
```

---

## 四、统一聊天窗口方案（用户核心疑问：Chatbox / ORCA 窗口）

### 4.1 你要的"一个窗口对应多个 Agent" → 用 **Chatbox AI**（桌面端，免费）

Chatbox 不是 WorkBuddy 内置，是一个**独立桌面应用**，支持多 Tab 各自连不同后端。这是把"Codex / Hermes / Claude Code / Ollama"都变成可贴截图的聊天窗口的最简解。

**在哪打开**：下载安装 Chatbox AI（官网 chatboxai.app）→ 打开 → 左上角「新对话」旁可「添加模型」，每个模型一个 Tab。

| Tab | 后端配置 | 用途 |
|-----|---------|------|
| Tab 1 · MiMO | API 类型=OpenAI兼容, Base=http://localhost:18808/v1 或 https://token-plan-cn.xiaomimimo.com/v1, Key=$MIMO_API_KEY, 模型=mimo-v2.5-pro | 主力推理/编码 |
| Tab 2 · Claude | API 类型=Anthropic, Base=https://token-plan-cn.xiaomimimo.com/anthropic/v1（走 MiMO 协议转换）, Key=同 MiMO | 多模态截图核查 |
| Tab 3 · Hermes | 按 Hermes 提供的 API 端点填 | 大脑/规划 |
| Tab 4 · Ollama | API 类型=OpenAI兼容, Base=http://localhost:11434/v1, 模型=qwen3.5:2b 或 gemma4:e4b | 免费本地热备 |

> 这样**所有 Agent 都是独立聊天窗口，可贴截图、可复制对话**，Codex 不必再困在 IDE 里。

### 4.2 ORCA 窗口能变成聊天窗口吗？

**ORCA 本身没有图形聊天窗口**——它是 CLI / 编排后台（Fleet Manager）。但它能"收编"上述聊天窗口：

```
Chatbox(4个Tab: MiMO/Claude/Hermes/Ollama)  ← 你日常操作的聊天界面
        │
        │  ORCA 通过 API 调用这些 Agent
        ▼
   ORCA CLI (fleet run <task>)  ← 并行分发、worktree 隔离、结果聚合
        │
        ▼
   MiMO / Claude / Codex / Marvis 实际执行
```

**所以正确心智模型**：Chatbox = 你的"聊天操作台"；ORCA = 背后的"并行调度员"。ORCA 不直接给你聊天框，但它调度的前端就是你的聊天窗口。

### 4.3 WorkBuddy 当 Codex 前端？

可以：配置 WorkBuddy 通过 CC-Switch 调 Codex → 我（WorkBuddy）就是 Codex 的聊天窗口，还能贴截图。**但注意这会消耗 Hy3 积分**，所以日常轻聊建议用 Chatbox 连 MiMO（走 Token Plan，不烧积分）。

### 4.4 已确定的前端策略（你 2026-07-14 拍板）

> **主前端 = WorkBuddy（我）** ｜ **后备前端 = Chatbox Tab1（连 MiMO）**

- **日常主用**：WorkBuddy 当 Codex / 通用聊天前端，花 Hy3 积分（系数仅 0.02x，成本极低、可接受）。优势：我能直接读你的仓库上下文、一键调 Agent、直接贴截图。
- **积分告急时**：自动切到 **Chatbox Tab1（连 MiMO，走 Token Plan）** 顶上，零积分消耗。Chatbox 已配好 4 个 Tab（详见 `Chatbox配置指南.md`）。
- **本质**：WorkBuddy = 高上下文便利入口；Chatbox+MiMO = 低成本长跑入口。两者互补，不冲突。

---

## 五、Git Worktree 分工方案（基于你的实际仓库结构）

项目根仓库：`E:\龙虾AI主控中心\`（git init）

| Worktree 分支 | Agent 绑定 | 对应路径 | 负责任务 |
|---------------|-----------|---------|---------|
| `fleet/mimo-main` | MiMO V2.5 Pro | `Codex量化策略20260615/币安/我的黑马策略/` | 黑马策略量化回测（已 git 化✅） |
| `fleet/claude-ui` | Claude Code | 前端/UI 相关 | 多模态截图/界面开发 |
| `fleet/codex-bridge` | Codex++ | `CC-Switch/` + `aicodeswitch_v5/` | 协议转换维护 |
| `fleet/marvis-auto` | Marvis | `Marvis/` | 自动任务调度 |
| `fleet/novel-writer` | 任意 Agent | `track_b_novel_publish/` | 小说创作 |
| `fleet/deerflow-research` | DeerFlow | `.trae/skills/DeerFlow/` | 研究自动化 |
| `fleet/workbuddy-office` | WorkBuddy(Hy3) | 办公文档区 | 研报/文档/商单交付物 |

---

## 六、五步执行法（融合龙虾五步法）

### Step 1: 备份（P0 强制）
```bash
cp -r "E:/龙虾AI主控中心" "G:/备份/龙虾AI_$(date +%Y%m%d_%H%M%S)/"
```

### Step 2: 环境诊断
```bash
tasklist | grep -iE "codex|orca|marvs|aicodeswitch"
netstat -ano | grep -E "15721|4567|18808|57321"
curl -s https://token-plan-cn.xiaomimimo.com/v1/models -H "Authorization: Bearer $MIMO_API_KEY" | head -c 200
cd "E:/龙虾AI主控中心" && git status --short && git branch -a
```

### Step 3: 方案落地
- **3A 跑通量化**：进黑马策略工作树 → MiMO 读现有代码 → 补依赖 → 单策略回测闭环 → 报告入 `Doc/`
- **3B ORCA 初始化**：`orca fleet init` → 注册 Agent → 建 worktree → 测试并行
- **3C 企业商单**：定义交付模板 → 连飞书 → 建「需求→分发→交付→验收」流水线

### Step 4: 结果验证
- [ ] 回测报告生成（收益曲线/最大回撤/夏普）
- [ ] ORCA ≥3 Agent 并行正常
- [ ] 飞书 = connected
- [ ] 每次操作 = 1备份 + 1日志

### Step 5: 迭代沉淀 → 更新本技能 + memory

---

## 七、变现预测模型

### 前置卡点（当前）
- ⚠️ MiMO Token Plan 今晚 8 点后续费
- ⚠️ E 盘 100% 满载风险（需先迁 G 盘）
- ⚠️ Marvis 半加载故障（待修复）
- ⚠️ 飞书 connector 断开（需重新授权）
- ⚠️ 多 Agent 端口不稳定（CC-Switch 中断是历史主因）
- ⚠️ gemma4:e4b 本机缺失（见第九节）

### 时间线预估

| 阶段 | 时间 | 关键里程碑 | 预期收入 |
|------|------|-----------|---------|
| **第 1 周** | 今~7/21 | ①续费 MiMO ②修端口 ③跑通黑马策略单回测 | ¥0（基建期） |
| **第 2 周** | 7/22~7/28 | ④ORCA 收编 2~3 Agent ⑤飞书连通 ⑥首份报告 | ¥0（验证期） |
| **第 1 月** | 8月 | ⑦首单企业商单 ⑧小说启动 | **¥3,000~8,000** |
| **第 2 月** | 9月 | ⑨舰队稳定 ⑩量化实盘小资金 ⑪商单复购 | **¥8,000~20,000** |
| **第 3 月** | 10月 | ⑫策略迭代 ⑬商单产品化 ⑭DeerFlow 激活 | **¥15,000~40,000** |

### 成本与利润率
- MiMO Token Plan：¥39~659/月 | ORCA：¥0（开源）| 云服务器可选 ¥50~300/月
- **利润率 70%~85%**（主要成本仅 MiMO Token）

---

## 八、积分与 Token 消耗参考

| 任务 | Token 消耗 | MiMO 成本 | CodeBuddy 积分 |
|------|-----------|-----------|----------------|
| 黑马策略单回测 | 50K~150K | ¥0.2~0.6 | 200~800 |
| ORCA 3 Agent 并行 | 200K~500K | ¥0.8~2.5 | — |

> **省钱关键**：重推理走 `mimo-bridge`（MiMO Token），别走 Hy3 积分。

---

## 九、已知坑与规避

| # | 坑 | 影响 | 规避 |
|---|-----|------|------|
| 1 | E盘满载 ENOSPC | 写入失败 | 迁 G 盘后再开跑 |
| 2 | CC-Switch 端口崩 | Agent 全断链 | 加保活/自动重启 |
| 3 | MiMO 到期不续 | 今晚8点后全停 | 设闹钟⏰/自动续费 |
| 4 | 飞书 connector 断 | 无法接企业单 | 优先修复授权 |
| 5 | Marvis 半加载 | 定时任务中断 | login.db重建+版本回退 |
| 6 | 中文技能名编码 | Git/工具乱码 | UTF-8 统一 |
| **7** | **gemma4:e4b 本机缺失（已确认 E/G 全盘无 GGUF）** | **本地免费热备暂不可用** | **计划部署到 G 盘（59G 可用）：设 `OLLAMA_MODELS=G:\Ollama\models` 后 `ollama pull gemma4:e4b`，不占 E 盘（详见 ollama-bridge）** |
| **8** | ~~E盘技能库写入被拦~~ | 已解决 | **2026-07-14 已授权并镜像三技能到 E 盘共享库 ✅** |

---

## 九·五、模式C闭环任务交换（v2.0 · 2026-07-16 升级，全自动+Git管控）

**核心思路**：WorkBuddy 作视觉大脑+编排，ORCA 三 Agent（Hermes/Codex/Claude Code）作执行臂。Agent 间不能直接互发消息，靠共享文件协作；协调中枢只能是 WorkBuddy。

**交换区 v2.0**：`E:\龙虾AI主控中心\我的AI分身\多智能体舰队编排\fleet_exchange\`
- ⚠️ **`多智能体舰队编排\` 已是独立 Git 项目**（2026-07-16 从「我的AI分身」monorepo detached）：分支 `main`/`develop`，Tag `v1.0.0-phase1`，父仓库已不再追踪
- Phase1→Phase2 演进蓝图见项目内 `docs/分阶段升级规划_对标Marvis18808.md`
- ⚠️ 旧路径 `E:\fleet_exchange\` 已 DEPRECATED（保留只读副本）
- 协议：`PROTOCOL.md` v2.0（含自动轮询规则、完整流转图）
- **脚本 v2.0（4个，消除人工中转）**：
  - 🆕 推送：`bash "<EX>/fleet_push.sh" "标题" "目标Agent" "优先级" "指令"` → WorkBuddy 一行命令写 incoming/
  - 取任务：`bash "<EX>/fleet_pull.sh"` 单次 / `bash "<EX>/fleet_pull.sh" auto 30 600` 自动轮询
  - 回写：`bash "<EX>/fleet_done.sh" "<WORKING_FILE>" "摘要"` → 写 results/ + 审计日志
  - 🆕 扫描：`bash "<EX>/marvis_scan.sh"` → 局域网自动发现 Marvis 端点
  - （其中 `EX="E:/龙虾AI主控中心/我的AI分身/多智能体舰队编排/fleet_exchange"`）
- 配套文档 v2.0（同在交换区）：README.md / PROTOCOL.md / 角色分工与自动调度规则.md / 视觉中枢降本测评.md / 模式C闭环测试说明书.md / 迁移实施报告.md / vision_config.json
- ✅ 全链路验证通过（push→pull→done→results + Git commit 15 files）

**视觉降本 v2.0 落地中**：
- Ollama 0.30.6（`E:\龙虾AI主控中心\Ollama_030\ollama.exe`，11434 在线）
- **模型存储已迁 G 盘**：User 级 `OLLAMA_MODELS=G:\Ollama\models` / `OLLAMA_HOME=G:\Ollama`（固化）；E 盘旧数据 3 天观察期后清理
- 已有 11 模型含 gemma4:e4b(文本/代码,无视觉) / qwen3.5:2b(✅vision)
- 🔄 正在拉取：minicpm-v + qwen2.5vl:7b
- **⚠️ 关键坑（必记）**：`ollama serve`/`ollama pull` **绝不能用 Bash 后台进程**启动——沙箱拦截对 G 盘写入（报 `Access is denied` 写 blobs partial）。必须走 **PowerShell 真实用户上下文**：`Start-Process ollama.exe -ArgumentList serve -WindowStyle Hidden`（继承 User 级 OLLAMA_MODELS 即可写 G 盘）。否则拉取必失败。
- 运维脚本 `fleet_exchange/ops/`：ollama_monitor.sh(监护) / ollama_env_check.ps1(开机自检) / ollama_recovery.ps1(三场景恢复) / disk_monitor.ps1(E<10GB弹窗) / github_backup.sh(独立远程)
- 每小时自动化巡检 Ollama 拉取（automation-1784136538241）
- vision_config.json 支持 Ollama(主力) / HY3(备援) / Marvis 一键切换
- marvis_scan.sh 已发现 Hermes(8642) + Ollama(11434) 端点

---

## 十、关联技能

| 技能名 | 路径 | 用途 |
|--------|------|------|
| **mimo-bridge** | `~/.workbuddy/skills/mimo-bridge/` | 直连 MiMO 省积分（本次新增✅） |
| **ollama-bridge** | `~/.workbuddy/skills/ollama-bridge/` | 本地免费热备 + gemma 状态（本次新增✅） |
| 龙虾标准五步法 v2.6 | `E:\...\lobster_task_standard_workflow_v2.6\SKILL.md` | 全域任务执行标准 |
| 龙虾全域官方模板 | `E:\...\龙虾全域官方模板-最终版.md` | 12大模板+280协议 |
| DeerFlow | `.trae/skills/DeerFlow/` | 研究自动化 |

---

*本技能由 WorkBuddy 根据龙虾AI主控中心实际环境生成，随舰队演进持续更新。*
*下次更新触发：ORCA 正式接入 / 首单商单成交 / 量化实盘验证 / E盘共享库镜像完成 ✅(2026-07-14)。*
