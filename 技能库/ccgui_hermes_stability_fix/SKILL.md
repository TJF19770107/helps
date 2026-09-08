---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_49d0a83d8cb811f19f65525400e6dd8f
    ReservedCode1: gB5+VmJeHzZAWX6IzNGDjDBrXr/bA5YseBN0z9IVNFpRqKaM9Fd5yYy0JYBmztCPLSW4p4z7a4t0emvKFAfUrfVgFCUIljFHsf231GjtLIm1R3iauFJ1srDKbOGnD0bAVQqNMiqtk0BsZSNbB1R8o1fHD0nEsUx9CIs+46O6BRVcSCwFqRD8t0tBPFY=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_49d0a83d8cb811f19f65525400e6dd8f
    ReservedCode2: gB5+VmJeHzZAWX6IzNGDjDBrXr/bA5YseBN0z9IVNFpRqKaM9Fd5yYy0JYBmztCPLSW4p4z7a4t0emvKFAfUrfVgFCUIljFHsf231GjtLIm1R3iauFJ1srDKbOGnD0bAVQqNMiqtk0BsZSNbB1R8o1fHD0nEsUx9CIs+46O6BRVcSCwFqRD8t0tBPFY=
---

# CCGUI Hermes 链路稳定性修复经验沉淀

> 时间：2026-07-31 16:15
> 任务来源：CCGUI 三引擎集群配置 - Hermes OpenCode 会话失败修复
> 适用范围：CCGUI + Hermes Agent + MiMo V2.5 模型链路

---

## 一、故障现象

| 引擎 | 模型 | 结果 | 根因 |
|------|------|------|------|
| Claude Code | mimo-v2.5-pro | ✅ 正常 | 无 |
| Codex CLI | mimo-v2.5-pro | ✅ 正常 | 无（GitHub 同步受限为独立问题） |
| OpenCode (Hermes) | mimo-v2.5-free | ❌ 会话失败 | MiMo V2.5 Free 通道 Hermes 输出中断 |
| OpenCode (Hermes) | mimo-v2.5-pro | ✅ 正常 | 修复后 |

错误信息：`hermes -z: no final response was produced; treating the run as failed.`

---

## 二、根因分析

**故障 A：MiMo Free 链路 Hermes 输出中断**
- Hermes Agent (`hermes -z`) 在 `-m mimo-v2.5-free` 参数下无法产生完整响应
- `mimo-v2.5-free` 模型通道在 Hermes 引擎中不可用，返回空最终响应
- CCGUI 的 `lastComposerPrefsByEngine.opencode.modelId` 配置为 `opencode/mimo-v2.5-free`，导致每次会话默认走 Free 通道

**故障 B：Codex GitHub 仓库同步受限**（独立问题，另行处理）
- `gh auth status` 未登录，Codex 无法访问 GitHub 仓库上下文

---

## 三、修复方案

### 3.1 核心修复（CCGUI settings.json）
```
lastComposerPrefsByEngine.opencode.modelId: "opencode/mimo-v2.5-free" → "mimo-v2.5-pro"
lastComposerPrefsByEngine.claude.modelId: → "mimo-v2.5-pro"（防止 CCGUI 回写清空）
lastComposerPrefsByEngine.codex.modelId: → "mimo-v2.5-pro"（防止 CCGUI 回写清空）
```

### 3.2 关键发现：CCGUI 回写行为
- CCGUI v0.7.x 在重启后可能**清除非当前活跃引擎的 modelId 条目**
- 需在每次修复后同时补齐三个引擎的 modelId，不能只改 opencode
- **建议：** CCGUI 重启后执行 modelId 一致性校验脚本

### 3.3 保护措施
- ORCA 后台 15 个 Agent 进程（claude×1, codex×10, codex-plus-plus×2, hermes×1, node×1）全程未受影响
- 回滚节点路径：`E:\龙虾AI主控中心\我的AI分身\技能库\ccgui_orca_isolation\rollback_nodes\`
- 备份文件：`settings_stable_20260731_1615.json`（SHA256: A18099CB...）

---

## 四、验证结果

| 验证项 | 方法 | 结果 |
|--------|------|------|
| Hermes CLI + mimo-v2.5-pro | `hermes -z "你是谁" -m mimo-v2.5-pro` | ✅ 我是 Hermes，一个 AI 助手。 |
| settings.json 三引擎 modelId | JSON 字段读取 | ✅ claude/codex/opencode 统一 mimo-v2.5-pro |
| CCGUI 窗口状态 | 截图快照 | ✅ 正常运行，无崩溃 |
| ORCA 进程保护 | Get-Process 检查 | ✅ 15 个进程全部存活 |
| 回滚节点 SHA256 校验 | Get-FileHash | ✅ PASS |

---

## 五、经验提炼

1. **Hermes 仅在 MiMo V2.5 Pro 通道可用**，Free 通道会导致 `no final response`。未来新增模型需先在 CLI 验证再配置到 CCGUI。
2. **CCGUI 会回写清除 lastComposerPrefsByEngine 中的非活跃引擎条目**，修复时必须三引擎同时补齐。
3. **包装脚本 opencode.ps1 正确工作**：参数 `--model opencode/mimo-v2.5-pro` → 剥离前缀 → `hermes -z prompt -m mimo-v2.5-pro`。
4. **回滚机制**：每次修改 settings.json 前必须备份至 rollback_nodes 目录，SHA256 校验确认一致性。
5. **ORCA 隔离**：settings.json 修改不影响 ORCA 后台运行的 Agent 舰队。

---

## 六、一键恢复技能（固化）

```powershell
# 一键恢复 CCGUI 三引擎到稳定状态
$path = "C:\Users\Administrator\AppData\Roaming\com.zhukunpenglinyutong.ccgui\settings.json"
$json = Get-Content $path -Raw | ConvertFrom-Json
$json.lastComposerPrefsByEngine = [PSCustomObject]@{
    claude = [PSCustomObject]@{ accessMode=$null; collaborationModeId=$null; effort=$null; modelId="mimo-v2.5-pro" }
    codex = [PSCustomObject]@{ accessMode=$null; collaborationModeId=$null; effort="medium"; modelId="mimo-v2.5-pro" }
    opencode = [PSCustomObject]@{ accessMode=$null; collaborationModeId=$null; effort=$null; modelId="mimo-v2.5-pro" }
}
$json | ConvertTo-Json -Depth 5 | Set-Content $path -Encoding UTF8
```

---

## 七、关联技能

- `lobster_task_standard_workflow_v2.9` - 龙虾五步法
- `ccgui_orca_isolation` - CCGUI 与 ORCA 隔离子技能
- `ccgui_hermes_stability_fix_20260731` - 本技能
*（内容由AI生成，仅供参考）*
