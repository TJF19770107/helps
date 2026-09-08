---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_9863e1638cc711f1a974525400e6dd8f
    ReservedCode1: WIf6RZIQVVqiIiwoW/V0y1tMbXC4GnL3tHTxgrd6oyrdri/ro0EBqyy1wAg9iPMjei/qXLKqy9+thVtnHhvf+KOmDo6+Y5F7k5sBEbxQambwchCYK/4tfIvd/HR4efla9Qzb45tApiDgpnVtm7zZSCNwgzyTAYyrsr83OHKpfTMOOHSCsNV3lX6YuUQ=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_9863e1638cc711f1a974525400e6dd8f
    ReservedCode2: WIf6RZIQVVqiIiwoW/V0y1tMbXC4GnL3tHTxgrd6oyrdri/ro0EBqyy1wAg9iPMjei/qXLKqy9+thVtnHhvf+KOmDo6+Y5F7k5sBEbxQambwchCYK/4tfIvd/HR4efla9Qzb45tApiDgpnVtm7zZSCNwgzyTAYyrsr83OHKpfTMOOHSCsNV3lX6YuUQ=
---

# CCGUI 三引擎一键恢复技能

## 时间：2026-07-31 16:59

## 适用场景
CCGUI 启动后引擎配置被回写、引擎切换失败、某引擎无法正常对话时使用。

## 故障根因（三合一）
| 编号 | 故障 | 根因 | 修复 |
|------|------|------|------|
| A | Hermes 会话失败 `no final response was produced` | opencode.modelId 被设为 `mimo-v2.5-free`，Hermes Free 通道不可用 | 锁定 modelId=mimo-v2.5-pro |
| B | opencode.cmd NUL 字节损坏 | 文件系统/NPM 安装导致二进制污染 | 用干净副本覆盖（86 bytes, 0 NUL） |
| C | CCGUI 启动后回写 settings.json | CCGUI 启动时检测 CLI 状态后重写配置，非活跃引擎被删除 | 恢复后设只读锁 |
| D | gh 未登录 → Codex GitHub 同步受限 | 未执行 `gh auth login` | 另行安排授权 |

## 恢复步骤

### 步骤 1：强制终止 CCGUI
```powershell
Get-Process -Name "cc-gui" -ErrorAction SilentlyContinue | Stop-Process -Force
```

### 步骤 2：恢复核心文件
```powershell
# 恢复 settings.json（三引擎锁定 Pro）
Copy-Item "E:\龙虾AI主控中心\我的AI分身\技能库\ccgui_orca_isolation\rollback_nodes\settings_stable_20260731_164257.json" `
          "$env:APPDATA\com.zhukunpenglinyutong.ccgui\settings.json" -Force

# 恢复 opencode.cmd（无 NUL 字节）
Copy-Item "E:\龙虾AI主控中心\我的AI分身\技能库\ccgui_orca_isolation\rollback_nodes\opencode_cmd_clean_20260731_164257.cmd" `
          "I:\npm\opencode.cmd" -Force

# 锁定只读（防止 CCGUI 回写）
Set-ItemProperty "$env:APPDATA\com.zhukunpenglinyutong.ccgui\settings.json" -Name IsReadOnly -Value $true
```

### 步骤 3：启动 CCGUI
```powershell
Start-Process "$env:LOCALAPPDATA\ccgui\cc-gui.exe"
```

### 步骤 4：验证三引擎
```powershell
# CLI 验证
claude -p "你是谁" --output-format text
opencode.cmd run --model opencode/mimo-v2.5-pro "你是谁"
# 预期：
# Claude: "我是 Claude"
# OpenCode/Hermes: "我是 Hermes Agent"
```

## 验证标准（对话测试）
在 CCGUI 对话框中分别向三引擎发送"你是谁"：

| 引擎 | 预期回复 | CLI 验证 | CCGUI 验证 |
|------|---------|---------|-----------|
| Claude Code | 我是 Claude | ✅ | 待 UI 验证 |
| Codex | 我是 Codex / Codex Agent | ⚠️ gh 待登录 | ✅ "Codex Agent" |
| OpenCode (Hermes) | 我是 Hermes Agent | ✅ | ✅ 截图已确认 |

## 注意事项
1. **不要修改 ORCA**：ORCA 的 21 个进程与 CCGUI 配置完全独立，恢复操作不影响 ORCA
2. **只读锁**：每次恢复后必须设只读，否则 CCGUI 下次启动会再次回写
3. **Time 快照**：恢复节点创建于 2026-07-31 16:42:57
4. **三引擎 modelId**：全部锁定 `mimo-v2.5-pro`，禁止 Free 通道
*（内容由AI生成，仅供参考）*
