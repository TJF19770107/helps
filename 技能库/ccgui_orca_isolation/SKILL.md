---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_8c99b6f38c4c11f197fe525400826444
    ReservedCode1: HGtAgGAdA5HF/2XVXJXcsslxlNWrGor1TOek2IizARkrjSOMPDqF34S9IpZLvKEM8/KfB/p22n4+cDlJ9E6CaPIvt7UkylXJnzzAPd9TjkJTw6ZlN9iokYdEykF/O3SahQW68gwi3/CUIYZuvxcQByxOdeEPStwVFo4zQsQ+J2w4fN5nLhkbddMNggo=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_8c99b6f38c4c11f197fe525400826444
    ReservedCode2: HGtAgGAdA5HF/2XVXJXcsslxlNWrGor1TOek2IizARkrjSOMPDqF34S9IpZLvKEM8/KfB/p22n4+cDlJ9E6CaPIvt7UkylXJnzzAPd9TjkJTw6ZlN9iokYdEykF/O3SahQW68gwi3/CUIYZuvxcQByxOdeEPStwVFo4zQsQ+J2w4fN5nLhkbddMNggo=
---



# CCGUI与ORCA多实例隔离部署规范 V1.0

技能名称：CCGUI-ORCA并行多实例隔离部署
适用范围：CCGUI settings.json 配置、引擎绑定、端口规划、隔离部署
执行口径：CCGUI为并行调度面板，与ORCA舰队物理隔离运行，仅配置层兼容互通，不共用进程与端口
版本号：v1.0
生效范围：CCGUI + ORCA（Codex/Claude/Hermes）双向隔离

---

## 一、隔离基座原则

### 1.1 硬性隔离边界

| 维度 | CCGUI | ORCA | 互通方式 |
|------|-------|------|----------|
| 进程 | 独立 cc-gui 进程 | 独立 codex/claude/hermes 进程 | 无直接进程通信 |
| 端口 | 3080(Web) / 4732(Remote Backend) | ORCA原有端口空间 | 端口号不重叠 |
| 配置 | `%APPDATA%\com.zhukunpenglinyutong.ccgui\settings.json` | `E:\龙虾AI主控中心\` 下各引擎配置 | 仅模型ID对齐 |
| 工作目录 | CCGUI自行管理 | `E:\龙虾AI主控中心\Orca\` 项目目录 | 互不读写 |
| 引擎二进制 | 共享 claude.cmd / codex.cmd / hermes.exe | 同一套二进制，独立进程实例 | 多实例安全启动 |

### 1.2 操作禁令

- **禁止** CCGUI配置变更时接触ORCA目录下任何文件
- **禁止** CCGUI重启时影响ORCA正在运行的进程
- **禁止** CCGUI新实例绑定ORCA已有端口
- **禁止** 用CCGUI读写/覆盖ORCA技能库、注册表

---

## 二、CCGUI settings.json 引擎绑定规范

### 2.1 引擎通道映射

CCGUI原生仅支持五种引擎：Codex / Claude / OpenCode / Kimi / Grok。
Hermes通过OpenCode通道承载，不新增独立引擎分类。

| CCGUI引擎键 | 实际承载 | 二进制路径 | 模型锁定 |
|-------------|----------|-----------|----------|
| `codexBin` | Codex CLI | `C:\Users\Administrator\AppData\Roaming\npm\codex.cmd` | `mimo-v2.5-pro` |
| `claudeBin` | Claude CLI | `I:\npm\claude.cmd` | `mimo-v2.5-pro` |
| `opencodeBin` | Hermes（OpenCode通道） | `C:\Users\Administrator\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe` | `mimo-v2.5-pro` |

### 2.2 关键配置字段

```json
{
  "claudeBin": "I:\\npm\\claude.cmd",
  "opencodeEnabled": true,
  "lastComposerModelId": "mimo-v2.5-pro",
  "lastComposerPrefsByEngine": {
    "codex": { "modelId": "mimo-v2.5-pro", "effort": "medium" },
    "claude": { "modelId": "mimo-v2.5-pro", "effort": "medium" },
    "opencode": { "modelId": "mimo-v2.5-pro", "effort": "medium" }
  }
}
```

---

## 三、端口规划

### 3.1 CCGUI端口

| 端口 | 键 | 说明 |
|------|-----|------|
| 3080 | `webServicePort` | Web管理面板 |
| 4732 | `remoteBackendHost` | 远程后端API |

### 3.2 ORCA端口（不变）

ORCA端口空间由其各自引擎配置管理，CCGUI不接触。

### 3.3 端口冲突检测命令

```powershell
# 检测目标端口是否已被占用
$ports = @(3080, 4732)
foreach ($p in $ports) {
    $line = netstat -ano 2>$null | Select-String ":$p " | Select-String "LISTENING"
    if ($line) { Write-Warning "端口 $p 已占用" } else { Write-Output "端口 $p 空闲" }
}
```

---

## 四、标准操作流程

### 4.1 前置备份

每次修改settings.json前，强制备份：

```powershell
$src = "$env:APPDATA\com.zhukunpenglinyutong.ccgui\settings.json"
$ts = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item $src "$env:APPDATA\com.zhukunpenglinyutong.ccgui\settings.json.backup_$ts" -Force
```

### 4.2 修改后验证三步法

1. **JSON语法校验**: `Get-Content $src -Raw | ConvertFrom-Json`
2. **字段逐项验证**: 检查 claudeBin / lastComposerPrefsByEngine / lastComposerModelId
3. **重启后端口验证**: 确认无端口重叠

### 4.3 回滚

```powershell
Copy-Item "备份路径" "$env:APPDATA\com.zhukunpenglinyutong.ccgui\settings.json" -Force
# 重启CCGUI即可
```

---

## 五、环境自检清单

每次启动CCGUI前执行：

- [ ] ORCA进程是否正常运行（参考对比基座）
- [ ] CCGUI目标端口3080/4732是否空闲
- [ ] claudeBin路径 `I:\npm\claude.cmd` 是否存在
- [ ] opencodeBin路径是否存在
- [ ] codexBin路径是否存在
- [ ] lastComposerPrefsByEngine 三引擎是否全绑定

---

## 六、历史变更

| 日期 | 版本 | 变更摘要 |
|------|------|----------|
| 2026-07-31 | v1.0 | 初始版本：三引擎MiMo V2.5 Pro绑定，端口隔离确认 |
*（内容由AI生成，仅供参考）*
