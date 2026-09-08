---
name: "fleet-devops-orchestrator"
description: "多智能体舰队DevOps统一编排层。一键舰队健康体检(6维度30秒扫描)、标准化DevOps生命周期(诊断→修复→部署→验证→监控)、5大常用运维Playbook(新Agent上线/服务迁移/紧急故障切换/配置批量推送/日志聚合诊断)。编排orca-agent-connection-fix+tat-adhoc-exec+mimo-bridge+ollama-bridge+多智能体舰队编排的协同工作流。触发词：舰队运维、fleet health、一键体检、舰队状态、服务部署、agent部署、fleet devops、舰队健康检查、批量重启、配置推送"
version: "1.0"
date: "2026-07-19"
author: "auto-skill-generator V2.2"
agent_created: true
tags: ["fleet", "devops", "orchestrator", "运维", "编排"]
primary_path: "~/.workbuddy/skills/fleet-devops-orchestrator/SKILL.md"
---

# Fleet DevOps Orchestrator — 舰队统一运维编排层 v1.0

> **定位**：编排层（非执行层）。不重复底层技能的具体命令，而是定义「何时用哪个技能、按什么顺序、检查什么结果」。
> **编排对象**：orca-agent-connection-fix + tat-adhoc-exec + mimo-bridge + ollama-bridge + 多智能体舰队编排
> **核心价值**：把碎片化的6个舰队技能，收敛为1套可执行的标准运维流程

---

## 一、何时激活本技能

| 触发场景 | 示例话术 |
|---------|---------|
| 舰队整体状态不明 | "舰队状态怎么样"、"检查一下所有agent"、"一键体检" |
| 需要批量运维操作 | "重启所有服务"、"推送配置到所有节点"、"批量更新" |
| 新Agent上线流程 | "加一个新agent"、"新agent怎么配" |
| 紧急故障响应 | "舰队挂了"、"agent全断"、"紧急恢复" |
| 跨技能协同操作 | "诊断并修复"、"从排查到部署一条龙" |

---

## 二、一键舰队健康体检（30秒6维度扫描）

> **设计原则**：从外到内、从上游到下游，任何一环断裂即定位根因。

### 扫描流程

```
维度1: 上游API健康
  └─ curl MiMO /v1/models → 200=✅ | 非200=❌(上游问题)
      └─ 失败 → 检查 MIMO_API_KEY 是否过期(tp-开头的Token Plan专属key)
      └─ 失败 → 切换 ollama-bridge 本地热备

维度2: 本地代理链路
  └─ netstat 15721(CC-Switch) + 4567(AI Code Switch) + 18808(MiMO本地)
      └─ 全部LISTENING=✅ | 缺失=❌(对应服务未启动)

维度3: ORCA应用状态
  └─ tasklist | grep Orca → 存在=✅ | 不存在=❌(ORCA未运行)
      └─ ORCA未运行 → 启动ORCA重建15721代理端口

维度4: Agent连接验证
  └─ Codex: codex exec "回复OK" --model mimo-v2.5-pro
  └─ Claude Code: 检查 ~/.claude/settings.json 协议格式
      └─ 502/ConnectionRefused → 激活 orca-agent-connection-fix 技能

维度5: 远程服务器状态
  └─ TAT执行: systemctl status fleet-* --no-pager
      └─ 失败 → 激活 tat-adhoc-exec 技能检查TAT连通性

维度6: 模型可用性
  └─ MiMO: curl /v1/models (主引擎)
  └─ Ollama: curl localhost:11434/v1/models (热备)
      └─ MiMO不可达 → ollama-bridge 自动降级
```

### 体检报告模板

```markdown
## 舰队健康体检报告 — YYYY-MM-DD HH:MM

| 维度 | 检查项 | 状态 | 详情 |
|------|--------|------|------|
| 1.上游API | MiMO /v1/models | ✅/❌ | HTTP 200, 0.3s |
| 2.代理链路 | 15721/4567/18808 | ✅/❌ | 3/3 LISTENING |
| 3.ORCA | Orca.exe | ✅/❌ | PID 12345 |
| 4.Agent | Codex/Claude | ✅/❌ | Codex OK, Claude 502 |
| 5.远程 | HK服务器服务 | ✅/❌ | 4/4 active |
| 6.模型 | MiMO+Ollama | ✅/❌ | MiMO主, Ollama备 |

### 问题清单
1. [P0] Claude Code 502 → 激活 orca-agent-connection-fix 方案B
2. [P1] Ollama gemma4:e4b 缺失 → 仅影响热备

### 建议操作
→ 按P0→P1顺序执行修复，每步验证后再进下一步
```

---

## 三、标准化DevOps生命周期

> **5阶段闭环**：诊断 → 修复 → 部署 → 验证 → 监控

### 阶段1: 诊断（Diagnose）

| 症状 | 激活技能 | 关键检查 |
|------|---------|---------|
| Agent连接失败(502/Refused) | `orca-agent-connection-fix` | 端口15721 + 上游MiMO + 配置文件路径 |
| 模型401/推理失败 | `mimo-bridge` 六.5节 | env_key + OPENAI_API_KEY值 + auth.json一致性 |
| 远程服务异常 | `tat-adhoc-exec` | TAT连通性 + systemctl status + journalctl日志 |
| 整体状态不明 | 本技能 §二 | 一键6维度体检 |

**诊断输出标准**：必须明确「根因 + 影响范围 + 修复方案编号」

### 阶段2: 修复（Fix）

| 修复类型 | 激活技能 | 关键操作 | 验证方法 |
|---------|---------|---------|---------|
| Agent直连MiMO | `orca-agent-connection-fix` 方案A | 改config.toml(两份!) + env_key | `codex exec "回复OK"` |
| 重启ORCA重建代理 | `orca-agent-connection-fix` 方案B | 关闭→重开ORCA | 端口15721重新LISTENING |
| 协议转换桥 | `orca-agent-connection-fix` 方案C | python bridge.py 15722 | Claude Code面板可连 |
| 模型切换 | `mimo-bridge`→`ollama-bridge` | 改base_url指向localhost:11434 | curl /v1/models返回模型列表 |

**修复铁律**：
1. **先备份再修改** — `cp config.toml config.toml.bak_YYYYMMDD`
2. **Codex改两份** — `~/.codex/config.toml` + `G:/Orca/.../config.toml`
3. **Claude Code注意协议** — Anthropic格式≠OpenAI格式，不能直连MiMO
4. **改完必须验证** — 不验证=没改

### 阶段3: 部署（Deploy）

> 通过 `tat-adhoc-exec` 推送到远程服务器

**标准部署流程**：
```
Step 1: 编写本地Shell脚本(.sh, LF换行, #!/bin/bash)
Step 2: 转LF换行 — python -c "import pathlib; ..."
Step 3: TAT执行 — python tat_exec.py script.sh --name deploy_xxx --timeout 300
Step 4: 解析输出 — base64解码TaskResult.Output
Step 5: 验证 — systemctl status / curl health / tail日志
```

**部署检查清单**：
- [ ] 脚本首行 `#!/bin/bash`
- [ ] 换行为LF（CRLF会导致TAT返回SUCCESS但脚本未执行）
- [ ] 脚本内不echo真实密钥
- [ ] timeout设置合理（部署300s, 重启120s, 日志60s）
- [ ] 部署后验证服务状态

### 阶段4: 验证（Verify）

| 验证类型 | 命令 | 预期结果 |
|---------|------|---------|
| 服务状态 | `systemctl status fleet-*` | 4个服务全active(running) |
| 端口监听 | `ss -tlnp | grep -E '878[789]'` | 8787/8788/8789 LISTENING |
| Agent响应 | `codex exec "回复OK"` | 返回OK |
| 日志检查 | `journalctl -u fleet-workbody --since "5min ago"` | 无ERROR |
| 远程连通 | `curl http://43.161.202.206:8787/health` | 200 OK |

### 阶段5: 监控（Monitor）

> 轻量持续监控，不部署常驻进程

| 监控项 | 频率 | 方法 | 告警阈值 |
|--------|------|------|---------|
| MiMO API可用性 | 每5min | curl /v1/models | 连续2次非200 |
| ORCA代理端口 | 每10min | netstat 15721 | 端口消失 |
| 远程服务存活 | 每15min | TAT systemctl status | 任一服务inactive |
| 日志错误率 | 每30min | TAT journalctl --since "30min ago" | ERROR > 5条 |

---

## 四、5大常用运维Playbook

### Playbook 1: 新Agent上线（15分钟）

```
前置: 确认新Agent使用的协议格式(OpenAI/Anthropic)

1. [配置] 根据协议选择方案:
   ├─ OpenAI格式 → orca-agent-connection-fix 方案A(直连MiMO)
   └─ Anthropic格式 → orca-agent-connection-fix 方案B(ORCA代理转换)

2. [验证本地] codex exec / Claude Code面板测试连接

3. [部署远程] tat-adhoc-exec 推送.service文件到/opt/fleet/
   └─ 脚本: cat > /etc/systemd/system/fleet-newagent.service
   └─ 脚本: systemctl daemon-reload && systemctl enable fleet-newagent

4. [启动验证] TAT执行 systemctl start fleet-newagent && systemctl status

5. [注册] 更新 多智能体舰队编排 技能的Agent清单

✅ 完成标准: 本地+远程均可响应, systemd状态active
```

### Playbook 2: 服务迁移（30分钟）

```
场景: 将服务从本地迁移到HK服务器(或反向)

1. [导出] 本地打包配置+脚本 — tar czf fleet-backup.tar.gz /opt/fleet/
2. [传输] TAT执行: base64解码写入(避免SCP依赖)
   └─ 或用tat_exec.py的--script参数直接推送内容
3. [部署] TAT执行: 解压 + systemd注册 + daemon-reload
4. [切换] 更新本地Agent配置指向新地址
5. [验证] 新旧地址双重验证, 确认无误后停旧服务
6. [回滚准备] 保留旧配置7天, 标记回滚命令

⚠️ 铁律: 迁移期间双跑, 验证通过再切流量
```

### Playbook 3: 紧急故障切换（5分钟）

```
触发: MiMO完全不可达(401/超时/服务宕机)

1. [诊断] 30秒确认:
   └─ curl MiMO /v1/models → 非200 → 确认上游故障
   └─ 检查 MIMO_API_KEY 是否过期(tp-key有效期)

2. [切换Ollama] 修改所有Agent的base_url:
   └─ 从 https://token-plan-cn.xiaomimimo.com/v1
   └─ 改为 http://localhost:11434/v1
   └─ 模型名改为 qwen3.5:2b 或其他已装模型

3. [远程切换] TAT执行批量修改:
   └─ sed -i 's|token-plan-cn.xiaomimimo.com|localhost:11434|g' /opt/fleet/*.env
   └─ systemctl restart fleet-*

4. [验证] 全链路测试: 本地Agent + 远程服务
5. [恢复] MiMO恢复后反向操作, 先验证再切回

⚠️ 注意: Ollama仅适合轻量任务, 重推理任务等待MiMO恢复
```

### Playbook 4: 配置批量推送（10分钟）

```
场景: 统一更新所有节点的API Key / 环境变量

1. [准备] 新建env文件(local), 确保LF换行
2. [推送] TAT执行:
   └─ cat > /opt/fleet/shared.env << 'EOF'
   └─ (写入新配置)
   └─ EOF
3. [重启] TAT执行: systemctl restart fleet-hermes fleet-claude fleet-codex fleet-workbody
4. [验证] TAT执行: systemctl status fleet-* | grep Active
5. [日志] TAT执行: journalctl -u fleet-* --since "2min ago" | grep -i error

⚠️ 安全: env文件不echo密钥, 不入版本控制, 推送后删除本地临时文件
```

### Playbook 5: 日志聚合诊断（10分钟）

```
场景: 舰队异常但不知哪个环节出问题

1. [远程日志] TAT执行:
   └─ journalctl -u fleet-hermes --since "30min ago" --no-pager
   └─ journalctl -u fleet-claude --since "30min ago" --no-pager
   └─ journalctl -u fleet-codex --since "30min ago" --no-pager
   └─ journalctl -u fleet-workbody --since "30min ago" --no-pager

2. [本地日志]
   └─ ORCA: G:/Orca/data/appdata/Orca/logs/
   └─ Codex: ~/.codex/logs/
   └─ Claude Code: ~/.claude/logs/

3. [聚合分析] 按时间线排序, 找到第一个ERROR
4. [根因定位] 对照 orca-agent-connection-fix 症状矩阵
5. [修复] 按诊断结果选择对应修复方案

输出: 时间线 + 根因 + 修复方案 + 验证结果
```

---

## 五、技能编排矩阵

> 本技能是编排层，具体执行依赖以下底层技能

| 底层技能 | 被编排场景 | 调用时机 |
|---------|-----------|---------|
| `orca-agent-connection-fix` | Agent连接故障诊断与修复 | 诊断阶段/修复阶段 |
| `tat-adhoc-exec` | 远程服务器命令执行 | 部署阶段/验证阶段/监控阶段 |
| `mimo-bridge` | MiMO API直连与401排障 | 诊断阶段/修复阶段 |
| `ollama-bridge` | 本地模型热备切换 | 紧急故障切换 |
| `多智能体舰队编排` | 舰队架构参考与Agent清单 | 新Agent上线注册 |
| `powershell-windows-encoding-fix` | Windows脚本编码修复 | 部署阶段(脚本编码) |

### 编排决策树

```
用户请求
  ├─ "舰队状态" → §二 一键体检
  ├─ "Agent连不上" → orca-agent-connection-fix(诊断→修复)
  ├─ "部署到服务器" → tat-adhoc-exec(部署→验证)
  ├─ "MiMO挂了" → mimo-bridge诊断 → ollama-bridge切换
  ├─ "新加Agent" → Playbook 1
  ├─ "紧急恢复" → Playbook 3
  ├─ "批量更新" → Playbook 4
  └─ "不知道哪坏了" → Playbook 5(日志聚合)
```

---

## 六、关键运维参数速查

### 端口与地址

| 服务 | 地址 | 用途 |
|------|------|------|
| MiMO API | `https://token-plan-cn.xiaomimimo.com/v1` | 主推理引擎 |
| MiMO本地 | `http://127.0.0.1:18808/v1` | CC-Switch中转后 |
| CC-Switch | `127.0.0.1:15721` | 总网关 |
| AI Code Switch | `127.0.0.1:4567` | 协议转换 |
| Ollama | `http://localhost:11434/v1` | 本地热备 |
| ORCA代理 | `127.0.0.1:15721` | 临时代理(重启重建) |
| 协议转换桥 | `127.0.0.1:15722` | Anthropic↔OpenAI |
| HK服务器 | `43.161.202.206` | 远程舰队节点 |

### 配置文件位置

| Agent | 配置路径 | 注意事项 |
|-------|---------|---------|
| Codex(独立) | `~/.codex/config.toml` | ⚠️ 还要改ORCA内嵌那份 |
| Codex(ORCA) | `G:/Orca/data/appdata/Orca/codex-runtime-home/home/config.toml` | 两份必须同步! |
| Claude Code | `~/.claude/settings.json` | Anthropic格式,非OpenAI |
| ORCA全局 | `G:/Orca/data/appdata/Orca/orca-data.json` | Agent注册表 |
| TAT凭证 | `C:\Users\Administrator\WorkBuddy\2026-07-18-14-16-19\secrets\tencent.env` | APPID+SecretId+SecretKey |

### 远程服务清单

| 服务名 | 作用 | systemd单元 |
|--------|------|------------|
| fleet-hermes | 大脑/指挥官 | fleet-hermes.service |
| fleet-claude | Claude Code远程实例 | fleet-claude.service |
| fleet-codex | Codex远程实例 | fleet-codex.service |
| fleet-workbody | WorkBuddy远程实例 | fleet-workbody.service |

---

## 七、防复发与最佳实践

### 配置管理铁律

1. **备份优先** — 任何配置修改前 `cp config.toml config.toml.bak_$(date +%Y%m%d)`
2. **Codex双份同步** — `~/.codex/config.toml` 和 `G:/Orca/.../config.toml` 必须一致
3. **Claude协议注意** — Anthropic格式不能直连OpenAI端点，需ORCA代理或协议桥
4. **改完必验证** — 5秒验证: `codex exec "回复OK"` 或 Claude Code面板测试
5. **ORCA重启后检查** — ORCA启动会覆盖runtime副本，重启后验证配置未被重置

### 远程部署铁律

1. **LF换行** — CRLF会导致TAT返回SUCCESS但脚本未执行（已踩坑2次）
2. **不echo密钥** — 脚本中避免 `echo $SECRET`，用env文件注入
3. **timeout合理** — 部署300s/重启120s/日志60s/状态检查30s
4. **验证闭环** — 部署→启动→状态→日志，四步缺一不可
5. **回滚准备** — 每次部署前备份旧配置，标记回滚命令

### 故障响应SOP

```
发现故障
  ├─ 30秒定位: 一键体检(§二) → 确定故障维度
  ├─ 分类响应:
  │   ├─ P0(舰队全断) → Playbook 3 紧急切换
  │   ├─ P1(单Agent断) → orca-agent-connection-fix 对应方案
  │   └─ P2(性能降级) → Playbook 5 日志诊断
  ├─ 修复验证: 本地+远程双重验证
  └─ 记录归档: 故障时间+根因+修复方案+耗时
```

---

## 八、更新记录

| 版本 | 日期 | 变更 |
|------|------|------|
| V1.0 | 2026-07-19 | 初版创建。编排6个底层技能，定义5阶段DevOps生命周期+5大Playbook+6维度体检+决策树 |

---

## 九、关联技能

| 技能 | 关系 | 版本 |
|------|------|------|
| `orca-agent-connection-fix` | 底层执行：Agent连接诊断修复 | V1.0 |
| `tat-adhoc-exec` | 底层执行：远程命令执行 | V1.0 |
| `mimo-bridge` | 底层执行：MiMO API直连 | V1.1 |
| `ollama-bridge` | 底层执行：本地模型热备 | V1.0 |
| `多智能体舰队编排` | 架构参考：舰队总览与Agent清单 | V1.1 |
| `多智能体舰队编排调度技能` | 调度参考：标准化调度体系 | V1.1 |
| `powershell-windows-encoding-fix` | 底层执行：Windows脚本编码修复 | V1.0 |
