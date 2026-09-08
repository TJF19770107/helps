---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_b7acadda735511f1aabe5254007bceed
    ReservedCode1: jb3EEUzkPlvrS1pMa1lWBnpPJWpZL4vRaLjTap0wDsaP5c+CmFSTx84/Rhf4ga0rWT5v2ucBP4N2bCkmRr98tj/oAZHYvSW42sULQfsGrZjFEpJjRfr4wn9Y6MAc3u/8KxUUJVmwnnDLH5URwaJELwtNM95fe7WWj9Xi4d0nV9hbtw+eOORwicp2i+Y=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_b7acadda735511f1aabe5254007bceed
    ReservedCode2: jb3EEUzkPlvrS1pMa1lWBnpPJWpZL4vRaLjTap0wDsaP5c+CmFSTx84/Rhf4ga0rWT5v2ucBP4N2bCkmRr98tj/oAZHYvSW42sULQfsGrZjFEpJjRfr4wn9Y6MAc3u/8KxUUJVmwnnDLH5URwaJELwtNM95fe7WWj9Xi4d0nV9hbtw+eOORwicp2i+Y=
---

﻿---
name: "lobster_task_standard_workflow_v2.5_locked"
description: "龙虾五步法 V2.5 规则锁定版：目标定义→环境搭建→方案落地→结果验证→迭代沉淀。强制四铁律：精准备份/指令触发/全存E盘/禁止后台扫描。内置四大服务修复分支(Marvis/WorkBuddy/Codex/Claude Code)、四类精简备份规范、修复失败自动回滚、白名单管理子流程、MT5量化MCP对接运维子流程。"
version: "2.5"
merged_from: ["v2.0 原版(C/E盘)", "self-skill_R60 量化工作流", "Codex量化策略首轮执行经验", "豆包Agent R113稳态快照", "网络修复+代理重置实战", "WorkBuddy软件故障修复实战", "WorkBuddy自动化白名单+全自动修复实战", "MT5双AI量化MCP对接部署全流程实战(lobster_mt5_quant_mcp_deploy_v1.0)", "MT5双环境隔离+自然语言调用+Claude代理兼容全流程实战(lobster_mt5_dual_env_nl_v1.0)"]
date: "2026-06-29"
sync_mode: "bidirectional"
primary_path: "E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v2.5_locked\SKILL.md"
backup_path: "G:\龙虾AI主控中心\我的AI分身\技能库\backup\"
claude_path: "C:\Users\Administrator\.claude\skills\lobster_task_standard_workflow_v2.5_locked\SKILL.md"
ccswitch_path: "C:\Users\Administrator\.cc-switch\skills\lobster_task_standard_workflow_v2.5_locked\SKILL.md"
---

# 龙虾标准五步法 V2.5 规则锁定版

技能名称：龙虾标准五步法（规则锁定版·四大铁律·四大服务修复分支·MT5量化MCP对接运维子流程）
技能标识：lobster_task_standard_workflow_v2.3_locked
适用范围：全域任务（代码/配置/容器/流程/文档/排障/迭代/量化策略开发/网络修复/代理重置/软件故障修复/程序白名单管理/四大服务运维/MT5量化MCP对接运维/MT5双环境隔离+自然语言调用）
执行口径：严格按五步顺序执行，不许跳步；不删规则；不覆盖旧配置；只合并叠加
版本号：v2.5（规则锁定版，合并原版 v2.0 + 量化适配 + Codex首轮经验 + 豆包Agent稳态 + 网络修复实战 + WorkBuddy故障修复实战 + 自动化白名单全自动修复实战 + MT5双AI量化MCP对接部署实战 + MT5双环境隔离+自然语言调用+Claude代理兼容全流程实战）
更新时间：2026-06-29
生效范围：全域 / 永久 / Codex + Hermes + 豆包 + OpenClaw + WorkBuddy 统一

---

## 铁律总纲（最高优先级·所有规则凌驾于下）

### 铁律一：精准备份——只备份有用的，绝不乱备份

**备份范围（仅限四类，禁止扩大）**：

| 备份类别 | 具体内容 | 备份时机 |
|----------|----------|----------|
| ① 核心数据 | 对话历史、长上下文、用户配置、用户生成文件 | 仅修复前 |
| ② 环境配置 | 网络代理、环境变量、软件关键配置 | 仅修复前 |
| ③ 技能插件 | E:\龙虾AI主控中心\我的AI分身\技能库下的自定义技能、规则 | 仅修复前 |
| ④ 关键状态快照 | 服务进程/端口/上次正常运行日志 | 仅修复前 |

**备份时机铁则**：仅在下达「调用龙虾五步法修复XX」命令时，修复前执行一次备份。禁止自动定时备份。

**备份存储路径**：`G:\龙虾AI主控中心\我的AI分身\技能库\backup\{YYYYMMDD_HHmmss}_pre_{ServiceName}_repair`

**备份清理规则**：仅保留近 5 个正常节点备份，自动清理老旧冗余备份。

### 铁律一补充：快照触发体系（V2.5 扩展）

<!-- 冲突解决：若本扩展与 SKILL.md 正文冲突，以本扩展为准（仅限快照触发规则部分）。 -->

1. 快照分为三类：**手动确认快照、阈值自动快照、故障前置快照**，全部为轻量索引快照，统一存储至 G 盘，遵循 5 节点留存规则。
2. 手动快照：人工确认环境稳定后主动触发，优先级最高。
3. 阈值自动快照：五步法累计调用 10 次 或 服务连续运行 6 小时，满足其一自动静默生成，低频触发节约资源。
4. 故障前置快照：Marvis 定时轻量巡检，识别服务异常前兆时，自动抓取**上一轮最后正常状态**生成快照并执行回滚；服务彻底失联时，由 Marvis 独立完成操作，不依赖目标 Agent。
5. 常规调用龙虾五步法执行修复/运维时，默认不自动生成快照；如需同步备份，需在指令中明确注明「并生成快照」，按需触发以节省 Token、积分与磁盘资源。

### 铁律二：无命令不修复——绝不后台自动执行

**触发条件**：所有服务（Marvis/WorkBuddy/Codex/Claude Code）的巡检、备份、修复、重启操作，**仅在明确下达以下指令时执行**：
- `调用龙虾五步法修复XX` → 执行备份+修复+沉淀+迭代
- `调用龙虾五步法回滚` → 恢复到最近一次备份的正常状态

**禁止行为**：
- 禁止后台扫描服务状态
- 禁止自动修复
- 禁止无触发的资源占用
- 禁止定时巡检任务
- 禁止自动生成备份快照

**静默原则**：无对应指令时，全程静默，零资源占用。

### 铁律三：三盘分工存储——E盘主控/G盘备份/C盘缓存

**存储根目录**：`E:\龙虾AI主控中心\我的AI分身\技能库`（主技能） | `G:\龙虾AI主控中心\我的AI分身\技能库`（备份/镜像）

**分类存储规范**：

| 内容类型 | 存储路径 | 说明 |
|----------|----------|------|
| 技能定义文件 | `E:\龙虾AI...\技能库\{skill-name}\SKILL.md` | 每个技能独立目录，留存E盘 |
| 配置文件 | `E:\龙虾AI...\技能库\{skill-name}\` | 白名单JSON、脚本等，留存E盘 |
| 版本主文件 | `E:\龙虾AI...\技能库\lobster_task_standard_workflow_v2.3_locked\` | V2.3锁定版主副本，留存E盘 |
| 小型索引/日志 | `E:\龙虾AI...\技能库\` | 索引、运行日志，留存E盘 |
| 备份快照 | `G:\龙虾AI主控中心\我的AI分身\技能库\backup\` | 近5个节点，强制落地G盘 |
| 历史节点/大容量备份包 | `G:\龙虾AI主控中心\我的AI分身\技能库\backup\` | 强制落地G盘 |
| 技能镜像（CC-Switch） | `G:\龙虾AI主控中心\我的AI分身\技能库\mirror_ccswitch\` | 通过软链接挂载 |
| 技能镜像（Claude） | `G:\龙虾AI主控中心\我的AI分身\技能库\mirror_claude\` | 通过软链接挂载 |

**禁止行为**：
- 禁止将大容量备份/快照/镜像存入C盘或E盘
- 禁止将正式技能/备份/快照存入C盘
- C盘仅保留程序运行临时缓存、进程文件
- 禁止生成临时垃圾文件

### 铁律四：指令触发唯一入口

| 指令 | 执行动作 |
|------|----------|
| `调用龙虾五步法修复XX` | 备份→修复→沉淀→迭代 |
| `调用龙虾五步法回滚` | 恢复最近正常备份 |
| 其他任何输入 | 不触发巡检/修复/备份 |

---

## 0) 永恒铁律（全程硬门禁）

- 合并更新：只增量不覆盖；不删除、不顶替旧配置与旧规则；以"新增版本化文件/新增配置块/新增索引项"为首选交付形态。
- 免费优先：优先本地/离线/免费资源；禁止引入付费外网 API；新增依赖必须给出"零成本可替代方案"。
- 成本核算：每一步都要做成本现状盘点与性价比评估；淘汰冗余链路与浪费节点。
- 安全与机密：任何密钥/口令/Token/Cookie 仅允许以环境变量名出现；只允许检查是否 SET/是否生效；禁止明文落盘/日志回显。
- 稳定与风控：任何大写入/大下载/大镜像拉取必须先做空间门禁；优先不打断生产服务；不确定时如实输出证据与边界。
- 版本与回滚：所有变更必须可回滚；优先"新增新版本文件"实现回滚；避免不可逆改写。
- 三方一致：涉及 Hermes/Trae/豆包/Codex 链路时，必须执行三方握手与 GStack 标准工作流校验。
- 目录隔离：每个 Agent 的写入操作严格限定在自己的工作目录，外部存量仅只读参考。
- API 容错：任何外部 API 调用必须预设 fallback 降级路径；连续 3 次 5xx/超时自动切换为本地方案；禁止因外部 API 不可用导致任务阻塞。

---

## 1) 第一步：目标定义（对标学习）

目标：明确任务边界、标的、预期、风控红线，找到成熟方案对标。

### 通用流程
1. **定位同类基线**：明确本任务的同类项目/成熟方案对标清单
2. **免费成本核算**：优先使用本地免费资源
3. **性价比评估**：对比至少两条路线

### 量化策略专用流程
1. **交易标的**：明确品种、交易所、时间周期
2. **盈亏预期**：年化目标收益率、可接受最大回撤
3. **风控红线**：单笔最大亏损、总回撤上限、止损机制
4. **数据可用性**：确认本地数据源、时间范围、数据质量
5. **框架选型**：对比 vnpy/backtrader/自研方案

---

## 2) 第二步：环境搭建（诊断先行）

目标：全盘摸清现状，搭建隔离可复现的开发环境。

### 通用流程
1. **路径诊断**：关键目录是否存在、是否被误指向
2. **权限诊断**：读写边界是否符合隔离要求
3. **依赖诊断**：版本兼容性、冲突检测
4. **成本基线**：磁盘占用、冗余资源

### 软件服务故障诊断专用流程

适用场景：桌面应用/IDE/Agent 出现 502/ECONNRESET/socket断开/fetch failed 等网络层错误。

#### 诊断步骤
1. **症状采集**：读取应用日志最后 500 行中的 ERROR/warn 条目
2. **根因判别矩阵**：

| 日志关键词 | 根因方向 | 下一步 |
|-----------|---------|--------|
| `ECONNRESET` + `127.0.0.1:7897` | 代理残留 | 执行代理清理 |
| `fetch failed` + `skillhub` | 网络不通 | 检查直连 + DNS |
| `Client network socket disconnected` | TLS阻断 | 检查代理/防火墙 |
| `render-process-gone: killed` | 连续错误崩溃 | 先修网络再重启应用 |
| `connect ECONNREFUSED 127.0.0.1:50551` | MCP本地服务未启动 | 检查MCP进程 |

3. **代理残留检测**（最频发根因）：
   - 检查 ProxyEnable 和 ProxyServer 注册表项
   - 若 ProxyEnable=0 但 ProxyServer 仍有残留值 → ProxyServer残留（虽不生效但属脏数据）
   - 若 ProxyEnable=1 且端口无 LISTENING → 确认为代理残留

#### 修复流程
1. 终止代理进程
2. 清除系统代理注册表项（含 ProxyServer 残留）
3. 网络栈完整重置（winhttp + winsock + int ip + flushdns）
4. 直连验证：ping 确认通
5. 重启受影响应用，逐一验证功能恢复

### 程序自动化白名单管理子流程

适用场景：app-agent需要对Windows桌面应用（EXE）执行截图、进程启停、配置修改、接口校验等自动化操作，但应用不在白名单中被拦截。

#### 白名单权限模型

| 权限项 | 作用 | 无此权限时的表现 |
|--------|------|-----------------|
| screenshot | 截图应用窗口 | 截图返回空/拒绝 |
| process_control | 关闭/启动/重启进程 | 无法操作进程 |
| config_repair | 读写应用配置文件 | 配置修改被拦截 |
| interface_connectivity_check | 网络连通性诊断 | 网络检查失败 |
| full_automation | 全自动化超级权限 | - |

#### 配置文件
- 路径：`E:\龙虾AI主控中心\我的AI分身\技能库\automation-whitelist-manager\automation_whitelist.json`
- 操作：查/增/删/改 → 四步验证闭环（截图→进程启停→日志健康→子进程存活）

---

## 3) 第三步：方案落地（只增量不覆盖）

目标：按规范产出可运行的代码/配置/流程。

### 通用流程
1. **只增量不覆盖**：新增版本化文件
2. **穿透壁垒但不越界**：仅必要范围内调整
3. **成本守门**：新增依赖必须有免费替代

---

## 4) 第四步：结果验证（全链路验收）

目标：以真实运行结果为唯一标准验收。

### 通用流程
1. **全流程联调**：端到端跑通
2. **版本比对**：日志自检
3. **成本复核**：资源占用不恶化

---

## 5) 第五步：迭代沉淀（自主进化）

目标：版本固化、经验沉淀、构建自我迭代闭环。

### 通用流程
1. **复盘**：目标/步骤/结果/证据/风险/改进项
2. **版本化固化**：新增版本文件，不覆盖旧版本
3. **技能沉淀**：可复用流程/脚本提炼为独立技能，存入 `E:\龙虾AI主控中心\我的AI分身\技能库`
4. **V2.X 文件同步更新**：每次迭代后同步更新关联技能列表
5. **MEM 更新**：仅规则/经验，不含密钥
6. **SKILLS_INDEX.md 更新**：新增技能必须写入技能总索引

---

## 四大服务定向修复分支逻辑

> **触发铁则**：以下所有流程**仅在收到「调用龙虾五步法修复XX」指令时执行**。无指令时全程静默，禁止后台扫描/自动修复/资源占用。

### 分支A：修复 Marvis

```
1. 备份四类数据到 G:\龙虾AI主控中心\我的AI分身\技能库\backup\
2. 检查代理状态（ProxyEnable/ProxyServer）
3. 检查端口占用（5283/5284/5285/5286）
4. 检查 Marvis 主进程 + 子进程（10进程）
5. 如有异常按根因矩阵修复
6. 重新启动 Marvis
7. 验证全部端口可连接 + 全部子进程存活
8. 沉淀技能 + 更新索引
```

### 分支B：修复 WorkBuddy

```
1. 备份四类数据到 G:\龙虾AI主控中心\我的AI分身\技能库\backup\
2. 确认白名单状态（automation_whitelist.json）
3. 检查代理残留（ProxyServer 残留 127.0.0.1:7897）
4. 读取 WorkBuddy 日志尾部 500 行诊断
5. 按根因矩阵修复（代理清理/网络重置/MCP进程检查）
6. 优雅重启 WorkBuddy（先关闭再启动）
7. 验证 8 进程存活 + 截图确认界面正常 + 日志无 ECONNRESET
8. 沉淀技能 + 更新索引
```

### 分支C：修复 Codex

```
1. 备份四类数据到 G:\龙虾AI主控中心\我的AI分身\技能库\backup\
2. 检查 Codex 进程（codex.exe）是否运行
3. 加载 lobster_codex_dual_link_v1.0 双链路健康检测：
   端口诊断：15721(CC-Switch总网关)/4567(AI Code Switch)/57321(Codex++管理)
   链路穿透测试：POST :4567/codex/responses + POST :15721/v1/chat/completions
   MiMO直连验证：POST token-plan-cn.xiaomimimo.com
   故障定级 -> 主备链路一键切换/回滚
4. 检查 CC Switch 数据库完整性
5. 按诊断结果执行修复（三层递进：双链路切换 -> workbuddy-recovery-rollback 代理清理 -> direct-network-recovery-rollback 网络栈重置）
6. 验证 Codex 推理链路正常（双端口均可达 + 对话测试通过）
7. 沉淀技能 + 更新索引
```

### 分支D：修复 Claude Code

```
1. 备份四类数据到 G:\龙虾AI主控中心\我的AI分身\技能库\backup\
2. 检查 Claude Code 进程 + 端口
3. 检查 Ollama 本地模型服务（端口 11434）
4. 检查 CC Switch 中的 Claude 配置
5. 按诊断结果执行对应修复
6. 验证推理链路 + 模型可用
7. 沉淀技能 + 更新索引
```

---

## 修复失败自动回滚逻辑

### 触发条件
- 修复后服务无法启动
- 修复后端口不通
- 修复后进程数不达标
- 修复后核心功能异常

### 回滚流程
```
1. 确认最近一次正常备份快照路径
2. 终止目标服务所有进程
3. 从备份恢复四类数据：
   - 核心数据 → 还原到原始位置
   - 环境配置 → 还原注册表/配置文件
   - 技能插件 → 还原到 G:\龙虾AI主控中心\我的AI分身\技能库\backup\（从G盘备份恢复）
   - 状态快照 → 仅供参考，不还原运行态
4. 执行网络栈重置（winhttp + winsock + flushdns）
5. 启动目标服务
6. 验证恢复到修复前正常状态
7. 输出回滚报告：回滚原因 + 恢复结果
```

---

## 四类精简备份规范

### 备份目录结构
```
G:\龙虾AI主控中心\我的AI分身\技能库\backup\
├── 20260629_062400_pre_WorkBuddy_repair\
│   ├── 01_core_data\           # 对话历史/用户配置
│   ├── 02_env_config\          # 代理/环境变量/关键配置
│   ├── 03_skills\              # 自定义技能/规则快照
│   └── 04_state_snapshot\      # 进程列表/端口状态/正常运行日志
├── 20260628_120000_pre_Marvis_repair\
│   └── ...
└── README.md                    # 备份索引说明
```

### 备份清理规则
- 自动保留近 5 个正常节点备份
- 超过 5 个时，按时间顺序删除最旧的
- 异常备份（回滚后的）标记为 `_rollback` 保留 30 天

---

## 关联技能

- lobster_task_standard_workflow_v1.0（v1.0 基线，不删除）
- lobster_tripartite_handshake_v1.0（三方握手）
- gstack_standard_workflow_template_v1.0（GStack 标准工作流）
- self-skill_R60（龙虾AI分身元技能）
- doubao-agent-skill v1.0（豆包Agent核心能力技能，R113稳态快照提炼）
- direct-network-recovery-rollback v1.0（直连网络一键恢复+回滚，全域9大程序通用底层兜底方案）
- workbuddy-recovery-rollback v1.0（WorkBuddy网络故障诊断与修复）
- automation-whitelist-manager v1.0（程序自动化白名单管理，全权限授权与验证闭环）
- lobster_codex_dual_link_v1.0（Codex双链路架构——端口身份地图+主备链路隔离+一键切换+健康检测+自动故障切换，适配Codex 502/404/端口链路报错场景）
- lobster_mt5_quant_mcp_deploy_v1.0（MT5双AI量化MCP对接运维，环境诊断→组件部署→链路配置→服务巡检）
- lobster_mt5_dual_env_nl_v1.0（MT5双环境隔离+自然语言调用+Claude代理兼容全流程实战）

---

## V2.3 规则锁定版新增内容（2026-06-29）

| 新增项 | 说明 |
|--------|------|
| **四大铁律** | 精准备份/指令触发/全存E盘/禁止后台扫描，铁律总纲凌驾于所有章节 |
| **四大服务修复分支** | Marvis/WorkBuddy/Codex/Claude Code 分流程自动修复，仅指令触发 |
| **修复失败自动回滚** | 备份→修复→失败→回滚→还原 完整闭环 |
| **四类精简备份规范** | 备份仅四类（核心数据/环境配置/技能插件/状态快照），近5节点自动清理 |
| **白名单管理子流程** | app-agent自动化操作权限管理（截图/进程/配置/网络） |
| **MT5量化MCP对接运维子流程** | MT5双AI量化链路（方案A Claude Code / 方案B Codex）的环境诊断→组件部署→链路配置→服务巡检四大环节，详见 lobster_mt5_quant_mcp_deploy_v1.0 |
| **指令触发唯一入口** | 仅「调用龙虾五步法修复XX」或「回滚」触发，其他输入静默 |
| **E盘强制落地** | 全部备份/技能/配置/版本文件锁定E盘，C盘仅作执行缓存 |
| **MT5双环境隔离+自然语言调用** | sim/real双环境物理隔离+自然语言调用MT5标准化模板+Claude代理兼容替代方案，详见 lobster_mt5_dual_env_nl_v1.0 |

---

## 三向同步说明

- **S1（主副本）**：E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v2.5_locked\SKILL.md（留存E盘，不变）
- **S2（CC-Switch 镜像）**：通过软链接挂载至 `G:\龙虾AI主控中心\我的AI分身\技能库\mirror_ccswitch\`，对应源目录为 `C:\Users\Administrator\.cc-switch\skills\lobster_task_standard_workflow_v2.5_locked\`
- **S3（Claude 镜像）**：通过软链接挂载至 `G:\龙虾AI主控中心\我的AI分身\技能库\mirror_claude\`，对应源目录为 `C:\Users\Administrator\.claude\skills\lobster_task_standard_workflow_v2.5_locked\`
- **同步规则**：以 S1 为主副本，S2/S3 为只读镜像；G盘 mirror 目录通过软链接指向 C 盘实际物理位置
*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*
