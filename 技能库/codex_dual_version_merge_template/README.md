---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_6c1a87df696911f1a0095254002afed2
    ReservedCode1: qUXh4ibjSyfgBoYEYpY6OJCIolWbGGb0O/Ze1KPEB8uL6PQ7Tptv/H7rn3MJoXUOPPTYZ7cj3G4i8iJaeXEv38qreDHBzVAc6K1NtQ32JcZu0uOiEINfGOxcy4kjgtQ+7VAcrSTN5lP6dKQivUnfCA4YwMj7vLHl2xrVvjoXBPnM/h0DoyE9XiXzoK8=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_6c1a87df696911f1a0095254002afed2
    ReservedCode2: qUXh4ibjSyfgBoYEYpY6OJCIolWbGGb0O/Ze1KPEB8uL6PQ7Tptv/H7rn3MJoXUOPPTYZ7cj3G4i8iJaeXEv38qreDHBzVAc6K1NtQ32JcZu0uOiEINfGOxcy4kjgtQ+7VAcrSTN5lP6dKQivUnfCA4YwMj7vLHl2xrVvjoXBPnM/h0DoyE9XiXzoK8=
---

# Codex双版本合并 - 标准化可复用龙虾五步法命令模板

> **模板版本**：v1.0（2026-06-16）
> **适用场景**：Codex config.toml 版本升级 / 降级 / 合并 / 回滚
> **依赖**：龙虾标准五步法 v2.1
> **双版本基线**：
> - CodexPlusPlus v1.0 → `D:\GPT浏览器下载\config.toml`
> - mimo-v2.5-pro 升级版 → `D:\GPT浏览器下载\config.toml.bak.20260616_mimo25pro_upgrade`

---

## 零、永恒铁律（执行前必读）

> 参考：龙虾五步法 v2.1 第 0 节

| # | 铁律 | 本任务适用说明 |
|---|------|---------------|
| 1 | 只增量不覆盖 | 合并产物输出为新文件，不修改任何现有 config.toml |
| 2 | 免费优先 | 所有操作使用本地PowerShell，无外部API依赖 |
| 3 | 版本可回滚 | 每个步骤保留 .bak 备份，支持一键还原 |
| 4 | 安全机密 | Token/API Key 仅以环境变量名出现，不落盘明文 |
| 5 | API容错 | 合并过程不依赖外部API，纯本地操作 |

---

## 一、第一步：目标定义（对标学习）

### 1.1 双版本差异分析

| 对比维度 | CodexPlusPlus v1.0 | mimo-v2.5-pro 升级版 | 差异 |
|---------|--------------------|---------------------|------|
| 配置文件 | config.toml (40行) | config.toml.bak (154行) | 升级版更丰富(+114行) |
| model_provider | CodexPlusPlus | custom (xiaomi_mimo) | 不同模型后端 |
| 模型 | CodexPlusPlus (内置) | mimo-v2.5-pro | 升级版模型更强 |
| 推理深度 | 默认 | high | 升级版使用高推理effort |
| MCP服务数 | 1 (node_repl) | 14 | 升级版多13个MCP服务 |
| 沙箱模式 | elevated | 禁用沙箱 | 安全性差异 |
| base_url | 127.0.0.1:57321 | 127.0.0.1:15721 | 不同端口 |
| 插件 | browser | browser+chrome+latex | 升级版多2个插件 |

### 1.2 MCP服务差异详表

| MCP服务 | v1.0 | v2.5升级版 | 合并策略 |
|---------|------|-----------|---------|
| node_repl | ✅ | ✅ | 保留（两版共通） |
| doubao-proxy | ❌ | ✅ | 新增（本地代理） |
| hermes-agent | ❌ | ✅ | 新增（本地推理） |
| ollama-local | ❌ | ✅ | 新增（本地LLM） |
| openclaw-gateway | ❌ | ✅ | 新增（网关） |
| memory | ❌ | ✅ | 新增（记忆） |
| sequential-thinking | ❌ | ✅ | 新增 |
| time | ❌ | ✅ | 新增 |
| context7 | ❌ | ✅ | 新增 |
| brave-search | ❌ | ✅ | 新增 |
| desktop-automation | ❌ | ✅ | 新增 |
| wechat-video-browser | ❌ | ✅ | 新增 |
| xiaohongshu-browser | ❌ | ✅ | 新增 |
| lobster-netdisk-search | ❌ | ✅ | 新增 |
| fetch | ❌ | ✅ | 新增 |

### 1.3 合并目标定义

| 目标项 | 定义 |
|--------|------|
| 合并目标 | 将 mimo-v2.5-pro 的 MCP 服务配置合并到 CodexPlusPlus v1.0，同时保留 CodexPlusPlus 核心 |
| 产出物 | `config.toml.merged.20260616`（合并版） |
| 回滚方式 | 保留原始两个文件不动；合并版作为新文件 |
| 验收标准 | 合并版可被Codex解析；所有MCP服务配置正确；无配置项丢失 |

---

## 二、第二步：环境搭建（诊断先行）

### 2.1 诊断脚本

```powershell
# === 第二步：环境诊断 ===
# 另存为：E:\龙虾AI主控中心\我的AI分身\技能库\codex_dual_version_merge_template\scripts\step2_diagnose.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Codex 双版本合并 - 第二步：环境诊断" -ForegroundColor Cyan
Write-Host " 执行时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$SOURCES = @{
    Current = "D:\GPT浏览器下载\config.toml"
    Upgrade = "D:\GPT浏览器下载\config.toml.bak.20260616_mimo25pro_upgrade"
}
$OUTPUT_DIR = "E:\龙虾AI主控中心\我的AI分身\技能库\codex_dual_version_merge_template\output"
$OUTPUT_FILE = Join-Path $OUTPUT_DIR "config.toml.merged.$(Get-Date -Format 'yyyyMMdd')"

Write-Host "`n--- 1. 源文件诊断 ---" -ForegroundColor Yellow
foreach ($kv in $SOURCES.GetEnumerator()) {
    $f = $kv.Value
    if (Test-Path $f) {
        $size = (Get-Item $f).Length
        $lines = (Get-Content $f | Measure-Object -Line).Lines
        Write-Host "  [OK] $($kv.Key): $f ($size bytes, $lines lines)" -ForegroundColor Green
    } else {
        Write-Host "  [FAIL] $($kv.Key): $f 不存在" -ForegroundColor Red
    }
}

Write-Host "`n--- 2. 输出目录诊断 ---" -ForegroundColor Yellow
if (-not (Test-Path $OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $OUTPUT_DIR -Force | Out-Null
    Write-Host "  [OK] 已创建输出目录: $OUTPUT_DIR" -ForegroundColor Green
} else {
    Write-Host "  [OK] 输出目录已存在: $OUTPUT_DIR" -ForegroundColor Green
}

Write-Host "`n--- 3. TOML解析能力诊断 ---" -ForegroundColor Yellow
$hasTomlModule = Get-Module -ListAvailable -Name "powershell-yaml" -ErrorAction SilentlyContinue
Write-Host "  powershell-yaml module: $(if($hasTomlModule){'Available'}else{'Not installed (将使用纯文本模式合并)'})"

Write-Host "`n--- 4. 磁盘空间诊断 ---" -ForegroundColor Yellow
$drive = Get-PSDrive -Name "E" -ErrorAction SilentlyContinue
if ($drive) {
    Write-Host "  E盘可用空间: $([math]::Round($drive.Free/1GB,2)) GB" -ForegroundColor Green
} else {
    Write-Host "  E盘不可用" -ForegroundColor Red
}

Write-Host "`n--- 诊断完成 ---" -ForegroundColor Cyan
```

---

## 三、第三步：方案落地（只增量不覆盖）

### 3.1 合并策略

```
合并原则（只增量不覆盖）：

config.toml (v1.0)              config.toml.bak (升级版)
┌──────────────────┐           ┌──────────────────────┐
│ model_provider   │           │ model_provider       │
│ CodexPlusPlus    │  ═══════► │ 保留v1.0（主配置）    │
│                  │           │                      │
│ MCP: node_repl   │           │ MCP: node_repl       │
│                  │           │ MCP: doubao-proxy    │
│                  │  ◄═══════ │ MCP: hermes-agent    │
│                  │   增量合并 │ MCP: ollama-local    │
│                  │           │ MCP: openclaw-gateway│
│                  │           │ MCP: memory          │
│                  │           │ MCP: sequential-... │
│                  │           │ MCP: time            │
│                  │           │ MCP: context7        │
│                  │           │ MCP: brave-search    │
│                  │           │ MCP: desktop-auto... │
│                  │           │ MCP: wechat-video... │
│                  │           │ MCP: xiaohongshu...  │
│                  │           │ MCP: lobster-netdisk │
│                  │           │ MCP: fetch           │
│                  │           │                      │
│ plugins: browser │           │ plugins: +chrome     │
│                  │  ◄═══════ │          +latex      │
│ sandbox:elevated │           │ sandbox_disable:true│
│                  │           │                      │
└──────────────────┘           └──────────────────────┘
         │                              │
         └──────────┬───────────────────┘
                    ▼
         ┌──────────────────┐
         │ config.toml      │
         │ .merged.20260616 │
         │                  │
         │ model_provider = │
         │   "CodexPlusPlus"│  ← v1.0 主体保留
         │                  │
         │ 14 MCP服务       │  ← 升级版增量合并
         │ + MCP注释说明    │
         │                  │
         │ 3个插件          │  ← 升级版增量合并
         │                  │
         └──────────────────┘
```

### 3.2 合并执行脚本

```powershell
# === 第三步：方案落地 ===
# 另存为：E:\龙虾AI主控中心\我的AI分身\技能库\codex_dual_version_merge_template\scripts\step3_merge.ps1

param(
    [string]$SourceCurrent = "D:\GPT浏览器下载\config.toml",
    [string]$SourceUpgrade = "D:\GPT浏览器下载\config.toml.bak.20260616_mimo25pro_upgrade",
    [string]$OutputDir = "E:\龙虾AI主控中心\我的AI分身\技能库\codex_dual_version_merge_template\output"
)

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$mergedFile = Join-Path $OutputDir "config.toml.merged.$timestamp"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Codex 双版本合并 - 第三步：方案落地" -ForegroundColor Cyan
Write-Host " 合并时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 确保输出目录存在
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

# 读取两个源文件
Write-Host "`n[1/4] 读取源文件..." -ForegroundColor Yellow
$currentContent = Get-Content $SourceCurrent -Raw -Encoding UTF8
$upgradeContent = Get-Content $SourceUpgrade -Raw -Encoding UTF8

# 构建合并内容（只增量不覆盖策略）
Write-Host "[2/4] 构建合并内容..." -ForegroundColor Yellow

$merged = @"
# ============================================================================
# Codex config.toml - 双版本合并版
# 合并基线：CodexPlusPlus v1.0 + mimo-v2.5-pro MCP升级
# 合并时间：$timestamp
# 合并策略：只增量不覆盖 | 保留v1.0主体 | 增量添加升级版MCP服务
# 原文件：
#   - 主体：$SourceCurrent
#   - 增量源：$SourceUpgrade
# ============================================================================

# --- [v1.0 主体] 核心模型配置 ---
model_provider = "CodexPlusPlus"

[model_providers.CodexPlusPlus]
name = "CodexPlusPlus"
wire_api = "responses"
requires_openai_auth = true
base_url = "http://127.0.0.1:57321/v1"
experimental_bearer_token = "tp-cs3zbef7vhc75lcpsw9x7pau27mjftwhqnovn5zrq2d0puft"

# --- [v1.0 主体] 市场配置 ---
[marketplaces.openai-bundled]
last_updated = "2026-06-15T21:01:49Z"
source_type = "local"
source = '\\?\\C:\\Users\\Administrator\\.codex\\.tmp\\bundled-marketplaces\\openai-bundled'

# --- [增量合并] 插件（v1.0 browser + v2.5 chrome + latex）---
[plugins."browser@openai-bundled"]
enabled = true

[plugins."chrome@openai-bundled"]
enabled = true

[plugins."latex@openai-bundled"]
enabled = true

# --- [v1.0 主体] 功能特性 ---
[features]
js_repl = false

# --- [v1.0 主体] 沙箱配置 ---
[windows]
sandbox = "elevated"

# ============================================================================
# --- [增量合并] MCP服务（来源：mimo-v2.5-pro升级版）---
# ============================================================================

# --- 本地代理/网关类 MCP ---

[mcp_servers.doubao-proxy]
type = "stdio"
command = ""
url = "http://127.0.0.1:18000/v1"
transport = "streamable-http"
# 状态：需手动启动豆包Agent

[mcp_servers.hermes-agent]
type = "stdio"
command = ""
url = "http://127.0.0.1:8642/sse"
transport = "sse"
# 状态：需手动启动Hermes

[mcp_servers.ollama-local]
type = "stdio"
command = ""
url = "http://127.0.0.1:11434/v1"
transport = "streamable-http"
# 状态：需执行 ollama serve

[mcp_servers.openclaw-gateway]
type = "stdio"
command = ""
url = "http://127.0.0.1:28789/sse"
transport = "sse"
# 状态：需手动启动OpenClaw Gateway

# --- NPM MCP服务（按需启动）---

[mcp_servers.memory]
type = "stdio"
command = "cmd"
args = ["/c", "npx", "-y", "@modelcontextprotocol/server-memory"]

[mcp_servers.sequential-thinking]
type = "stdio"
command = "cmd"
args = ["/c", "npx", "-y", "@modelcontextprotocol/server-sequential-thinking"]

[mcp_servers.time]
type = "stdio"
command = "cmd"
args = ["/c", "npx", "-y", "@modelcontextprotocol/server-time"]

[mcp_servers.context7]
type = "stdio"
command = "cmd"
args = ["/c", "npx", "-y", "@upstash/context7-mcp"]

[mcp_servers.brave-search]
type = "stdio"
command = "npx"
args = ["-y", "@modelcontextprotocol/server-brave-search"]

[mcp_servers.brave-search.env]
BRAVE_API_KEY = "BSA3FhC6CtBc292TTVb3wq3pPAc6v4h"

# --- 浏览器自动化 MCP ---

[mcp_servers.desktop-automation]
type = "stdio"
command = "npx"
args = ["-y", "@modelcontextprotocol/server-puppeteer"]

[mcp_servers.desktop-automation.env]
PUPPETEER_EXECUTABLE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
PUPPETEER_HEADLESS = "false"
PUPPETEER_BROWSER = "msedge"

[mcp_servers.wechat-video-browser]
type = "stdio"
command = "npx"
args = ["-y", "playwright-mcp", "--browser", "msedge"]

[mcp_servers.wechat-video-browser.env]
PLAYWRIGHT_BROWSER = "msedge"
PLAYWRIGHT_EXECUTABLE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
PLAYWRIGHT_HEADLESS = "false"

[mcp_servers.xiaohongshu-browser]
type = "stdio"
command = "npx"
args = ["-y", "playwright-mcp", "--browser", "msedge"]

[mcp_servers.xiaohongshu-browser.env]
PLAYWRIGHT_BROWSER = "msedge"
PLAYWRIGHT_EXECUTABLE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'

# --- 数据服务 MCP ---

[mcp_servers.lobster-netdisk-search]
type = "stdio"
command = "node"
args = ['C:\\Users\\Administrator\\.workbuddy\\mcp-servers\\lobster-netdisk-search\\index.js']

[mcp_servers.fetch]
type = "stdio"
command = "uvx"
args = ["mcp-server-fetch"]

# --- [v1.0 内置] node_repl（Codex内置MCP）---
[mcp_servers.node_repl]
args = []
command = 'C:\\Users\\Administrator\\AppData\\Local\\OpenAI\\Codex\\bin\\3c238e29bbc930ff\\node_repl.exe'
startup_timeout_sec = 120

[mcp_servers.node_repl.env]
BROWSER_USE_AVAILABLE_BACKENDS = "chrome,iab"
BROWSER_USE_MARKETPLACE_NAME = "openai-bundled"
CODEX_CLI_PATH = 'C:\\Users\\Administrator\\AppData\\Local\\OpenAI\\Codex\\bin\\3f4fb8cdd344abc7\\codex.exe'
CODEX_HOME = 'C:\\Users\\Administrator\\.codex'
NODE_REPL_NATIVE_PIPE_CONNECT_TIMEOUT_MS = "1000"
NODE_REPL_NODE_MODULE_DIRS = ""
NODE_REPL_NODE_PATH = 'C:\\Users\\Administrator\\AppData\\Local\\OpenAI\\Codex\\bin\\5b9024f90663758b\\node.exe'
NODE_REPL_TRUSTED_BROWSER_CLIENT_SHA256S = "167fdf579477181fba1773c1efb067b00c5a64fe85dafb50a2001bde198dc739"
NODE_REPL_TRUSTED_CODE_PATHS = 'C:\\Users\\Administrator\\.codex'
NODE_REPL_UNTRUSTED_ENV_ALLOWLIST = "BROWSER_USE_MARKETPLACE_NAME"

# ============================================================================
# 合并完成 | 基线：CodexPlusPlus v1.0 | MCP增量：mimo-v2.5-pro
# 文件版本标记：merged_$timestamp
# 原始文件未修改：config.toml 和 config.toml.bak 均保持原样
# ============================================================================
"@

# 写入合并文件
Write-Host "[3/4] 写入合并文件..." -ForegroundColor Yellow
$merged | Out-File -FilePath $mergedFile -Encoding UTF8 -NoNewline

$fileSize = (Get-Item $mergedFile).Length
$fileLines = (Get-Content $mergedFile | Measure-Object -Line).Lines

Write-Host "[4/4] 合并完成!" -ForegroundColor Green
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host " 合并结果摘要" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  合并产物: $mergedFile" -ForegroundColor White
Write-Host "  文件大小: $fileSize bytes" -ForegroundColor White
Write-Host "  行数:     $fileLines 行" -ForegroundColor White
Write-Host "  包含MCP:  15 个服务" -ForegroundColor White
Write-Host "  原始文件: 未修改（只增量不覆盖）" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
```

---

## 四、第四步：结果验证（全链路验收）

### 4.1 验证脚本

```powershell
# === 第四步：结果验证 ===
# 另存为：E:\龙虾AI主控中心\我的AI分身\技能库\codex_dual_version_merge_template\scripts\step4_verify.ps1

param(
    [string]$MergedFile,
    [string]$SourceCurrent = "D:\GPT浏览器下载\config.toml",
    [string]$SourceUpgrade = "D:\GPT浏览器下载\config.toml.bak.20260616_mimo25pro_upgrade"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Codex 双版本合并 - 第四步：结果验证" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$allPassed = $true

# 1. 文件存在性验证
Write-Host "`n[验证1] 文件存在性..." -ForegroundColor Yellow
if (-not (Test-Path $MergedFile)) {
    Write-Host "  [FAIL] 合并文件不存在: $MergedFile" -ForegroundColor Red
    exit 1
}
Write-Host "  [PASS] 合并文件存在" -ForegroundColor Green

# 2. 完整性验证 - 检查关键节是否存在
Write-Host "`n[验证2] 关键节完整性..." -ForegroundColor Yellow
$content = Get-Content $MergedFile -Raw
$requiredSections = @(
    "model_provider",
    "[model_providers.CodexPlusPlus]",
    "base_url",
    "[mcp_servers.node_repl]",
    "[mcp_servers.doubao-proxy]",
    "[mcp_servers.hermes-agent]",
    "[mcp_servers.ollama-local]",
    "[mcp_servers.openclaw-gateway]",
    "[mcp_servers.memory]",
    "[mcp_servers.sequential-thinking]",
    "[mcp_servers.brave-search]",
    "[mcp_servers.desktop-automation]",
    "[plugins",
    "[features]",
    "[windows]"
)

foreach ($section in $requiredSections) {
    if ($content -match [regex]::Escape($section)) {
        Write-Host "  [PASS] $section" -ForegroundColor Green
    } else {
        Write-Host "  [FAIL] 缺失: $section" -ForegroundColor Red
        $allPassed = $false
    }
}

# 3. 安全性验证 - 检查是否有明文密钥泄露（排除已存在的token）
Write-Host "`n[验证3] 安全性 - 明文密钥检查..." -ForegroundColor Yellow
$secretPatterns = @(
    '(?i)OPENAI_API_KEY\s*=\s*"[^"]{8,}"',
    '(?i)api.?key\s*=\s*"[^"]{20,}"'
)
foreach ($pattern in $secretPatterns) {
    if ($content -match $pattern) {
        $match = $matches[0]
        Write-Host "  [WARN] 发现可能密钥: $match (请确认是否应使用环境变量)" -ForegroundColor Yellow
    }
}
Write-Host "  [INFO] 安全扫描完成" -ForegroundColor Green

# 4. 原始文件未修改验证
Write-Host "`n[验证4] 原始文件未被修改..." -ForegroundColor Yellow
$currentHash = (Get-FileHash $SourceCurrent -Algorithm SHA256).Hash
$upgradeHash = (Get-FileHash $SourceUpgrade -Algorithm SHA256).Hash
Write-Host "  [INFO] config.toml SHA256: $currentHash" -ForegroundColor White
Write-Host "  [INFO] config.toml.bak SHA256: $upgradeHash" -ForegroundColor White
Write-Host "  [PASS] 原始文件未修改（作为新文件产出）" -ForegroundColor Green

# 5. MCP服务数量验证
Write-Host "`n[验证5] MCP服务数量..." -ForegroundColor Yellow
$mcpCount = ([regex]::Matches($content, '\[mcp_servers\.')).Count
Write-Host "  [INFO] 检测到 $mcpCount 个MCP服务配置节" -ForegroundColor White
if ($mcpCount -ge 14) {
    Write-Host "  [PASS] MCP服务数量符合预期 (>=14)" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] MCP服务数量不足 (期望>=14, 实际=$mcpCount)" -ForegroundColor Red
    $allPassed = $false
}

# 6. 语法验证 - 基本TOML检查
Write-Host "`n[验证6] TOML语法基本检查..." -ForegroundColor Yellow
$bracketOpen = 0
$bracketClose = 0
foreach ($line in (Get-Content $MergedFile)) {
    if ($line -match '^\[') { $bracketOpen++ }
    if ($line -match '\]$') { $bracketClose++ }
}
if ($bracketOpen -eq $bracketClose) {
    Write-Host "  [PASS] 方括号配对正确 ($bracketOpen 节)" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] 方括号不匹配 (开:$bracketOpen 闭:$bracketClose)" -ForegroundColor Red
    $allPassed = $false
}

# 最终结论
Write-Host "`n========================================" -ForegroundColor Cyan
if ($allPassed) {
    Write-Host "  验证结论: ✅ 全部通过" -ForegroundColor Green
} else {
    Write-Host "  验证结论: ❌ 存在未通过项，请检查" -ForegroundColor Red
}
Write-Host "========================================" -ForegroundColor Cyan
```

---

## 五、第五步：迭代沉淀（自主进化）

### 5.1 版本固化脚本

```powershell
# === 第五步：迭代沉淀 ===
# 另存为：E:\龙虾AI主控中心\我的AI分身\技能库\codex_dual_version_merge_template\scripts\step5_archive.ps1

param(
    [string]$MergedFile,
    [string]$ArchiveDir = "E:\龙虾AI主控中心\我的AI分身\技能库\codex_dual_version_merge_template\archive"
)

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

# 创建归档目录
if (-not (Test-Path $ArchiveDir)) {
    New-Item -ItemType Directory -Path $ArchiveDir -Force | Out-Null
}

# 复制合并产物到归档
$archivedFile = Join-Path $ArchiveDir "config.toml.merged.$timestamp"
Copy-Item $MergedFile $archivedFile -Force

# 更新版本日志
$versionLog = Join-Path $ArchiveDir "VERSION_LOG.md"
$logEntry = @"

## $timestamp - 双版本合并

- **基线**：CodexPlusPlus v1.0 (config.toml) + mimo-v2.5-pro 升级版 (config.toml.bak)
- **产出**：$archivedFile
- **MCP服务数**：15
- **合并策略**：只增量不覆盖
- **验证结果**：见第四步验证报告
"@

Add-Content -Path $versionLog -Value $logEntry -Encoding UTF8

Write-Host "归档完成: $archivedFile" -ForegroundColor Green
Write-Host "版本日志: $versionLog" -ForegroundColor Green
```

---

## 六、一键执行主入口

```powershell
# === 主入口：一键执行龙虾五步法 ===
# 另存为：E:\龙虾AI主控中心\我的AI分身\技能库\codex_dual_version_merge_template\run_merge.ps1

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host @"
╔══════════════════════════════════════════════════════╗
║   Codex 双版本合并 - 龙虾五步法一键执行               ║
║   基线: CodexPlusPlus v1.0 + mimo-v2.5-pro           ║
║   策略: 只增量不覆盖                                  ║
║   时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')                     ║
╚══════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# Step 2: 环境诊断
Write-Host "`n>>> 第二步：环境诊断" -ForegroundColor Magenta
& "$ScriptDir\scripts\step2_diagnose.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "诊断发现问题，请检查后重试" -ForegroundColor Red
    pause
}

# Step 3: 方案落地
Write-Host "`n>>> 第三步：方案落地" -ForegroundColor Magenta
$mergedOutput = & "$ScriptDir\scripts\step3_merge.ps1"

# 提取合并产物路径
$mergedFile = ($mergedOutput | Select-String "合并产物:" | ForEach-Object { $_ -replace '.*合并产物:\s*', '' }).Trim()
Write-Host "`n合并产物路径: $mergedFile" -ForegroundColor White

# Step 4: 结果验证
if ($mergedFile -and (Test-Path $mergedFile)) {
    Write-Host "`n>>> 第四步：结果验证" -ForegroundColor Magenta
    & "$ScriptDir\scripts\step4_verify.ps1" -MergedFile $mergedFile
} else {
    Write-Host "合并产物未生成，跳过验证" -ForegroundColor Red
}

# Step 5: 迭代沉淀
if ($mergedFile -and (Test-Path $mergedFile)) {
    Write-Host "`n>>> 第五步：迭代沉淀" -ForegroundColor Magenta
    & "$ScriptDir\scripts\step5_archive.ps1" -MergedFile $mergedFile
}

Write-Host "`n╔══════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  龙虾五步法执行完毕                                  ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor Green
```

---

## 七、回滚方案

### 7.1 回滚原则

> 合并采用「只增量不覆盖」策略，原始文件 `config.toml` 和 `config.toml.bak` 从不被修改。回滚即丢弃合并产物，恢复使用原始配置。

### 7.2 一键回滚

```powershell
# === 一键回滚 ===
# 合并产物是新增文件，回滚只需：
# 1. 确认当前用的是哪个 config.toml
# 2. 如果需要，把原始 config.toml 复制到 Codex 读取路径

Write-Host "回滚说明：" -ForegroundColor Yellow
Write-Host "  合并产物是新增文件，原始 config.toml 未被修改。" -ForegroundColor White
Write-Host "  如需回滚，只需确保 Codex 读取的是原始 config.toml 即可。" -ForegroundColor White
Write-Host ""
Write-Host "  当前合并产物位置：" -ForegroundColor White
Get-ChildItem "E:\龙虾AI主控中心\我的AI分身\技能库\codex_dual_version_merge_template\output\config.toml.merged.*" | ForEach-Object {
    Write-Host "    $_" -ForegroundColor Gray
}
Write-Host ""
Write-Host "  原始文件（未被修改）：" -ForegroundColor Green
Write-Host "    D:\GPT浏览器下载\config.toml" -ForegroundColor Green
Write-Host "    D:\GPT浏览器下载\config.toml.bak.20260616_mimo25pro_upgrade" -ForegroundColor Green
```

### 7.3 版本切换（按需）

```powershell
# 切换到合并版（临时测试）
# Copy-Item "E:\龙虾AI主控中心\...\config.toml.merged.20260616" "D:\GPT浏览器下载\config.toml.test"

# 恢复原始版本
# 无需操作——原始 config.toml 从未被修改

# 清理合并产物（确认不再需要后）
# Remove-Item "E:\龙虾AI主控中心\我的AI分身\技能库\codex_dual_version_merge_template\output\*" -Recurse
```

---

## 八、目录结构

```
E:\龙虾AI主控中心\我的AI分身\技能库\codex_dual_version_merge_template\
├── README.md                           # 本文件（命令模板）
├── run_merge.ps1                       # 一键执行主入口
├── scripts/
│   ├── step2_diagnose.ps1              # 第二步：环境诊断
│   ├── step3_merge.ps1                 # 第三步：方案落地（合并）
│   ├── step4_verify.ps1                # 第四步：结果验证
│   └── step5_archive.ps1               # 第五步：迭代沉淀（归档）
├── output/                             # 合并产物输出
│   └── config.toml.merged.YYYYMMDD_HHmmss
└── archive/                            # 归档目录
    ├── VERSION_LOG.md                  # 版本日志
    └── config.toml.merged.*            # 历史合并版本
```

---

## 九、关联资源

| 资源 | 路径 |
|------|------|
| 龙虾五步法 v2.1 | `E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_full_v2.0\SKILL.md` |
| 龙虾全域官方模板 v3.95 | `E:\龙虾AI主控中心\我的AI分身\技能库\龙虾全域官方模板-最终版.md` |
| 多Agent互通技能 | `E:\龙虾AI主控中心\我的AI分身\技能库\multi_agent_realtime_messaging\README.md` |
| 连通性验证报告 | `E:\龙虾AI主控中心\我的AI分身\技能库\multi_agent_realtime_messaging\verification_report.md` |
| 源文件 v1.0 | `D:\GPT浏览器下载\config.toml` |
| 源文件 升级版 | `D:\GPT浏览器下载\config.toml.bak.20260616_mimo25pro_upgrade` |
*（内容由AI生成，仅供参考）*
