---
name: workbuddy-mcp-http-adapter
version: 1.1.0
type: skill
agent_created: true
updated: 2026-08-26
description: 构建/调试「WorkBuddy 本地 MCP-HTTP 适配服务」的可复用范式——把文件/Git/Playwright浏览器/知识蒸馏/四端同步等能力包装成仅绑定 127.0.0.1 的 MCP 服务，供豆包等工作客户端远程调用。覆盖纯标准库 MCP 双协议实现，以及两个致命坑：Chromium 版本错配导致的挂死、subprocess 管道被 Chromium 子进程继承引发的 communicate() 死锁。触发词：MCP-HTTP、MCP服务、豆包连接器、本地MCP、WorkBuddy适配、playwright挂死、subprocess死锁。
---

# WorkBuddy 本地 MCP-HTTP 适配服务

把 WorkBuddy 的本地能力（文件读写、Git、Playwright 浏览器、知识蒸馏、四端同步）暴露为标准 MCP-HTTP 服务，仅绑定 `127.0.0.1` 回环地址，供豆包工作等客户端远程调用。

## 何时用
- 需要把本机 AI 员工能力对外部客户端（豆包/Claude Desktop/任意 MCP 客户端）开放
- 要求：仅本机回环、密钥不落盘、路径沙箱隔离、零额外依赖安装

## 架构范式（纯标准库，零 pip）
- `ThreadingHTTPServer((127.0.0.1, port), Handler)`，HTTP/1.1
- **双协议并行**兼容豆包等未知客户端：
  - Streamable HTTP：`POST /mcp`（2025-03-26），响应头带 `Mcp-Session-Id`
  - Legacy SSE：`GET /sse` 下发 `session_id=`，`POST /messages?session_id=`
- 工具注册表 `TOOLS` 字典 + `handle_rpc()` 分发 `initialize/ping/tools/list/tools/call`
- `_guard()`：非回环源拒绝（403）+ 可选 Bearer 鉴权（401）
- `/health`：`{"status":"ok", tools:N, sandbox_root:...}`（保活脚本探活用）
- 公共层 `lobster_common.py`：路径沙箱 `resolve_in_sandbox()`、只读保护区、密钥脱敏 `redact()`（正则 + 环境变量值精确遮蔽）、`run_cmd()` 统一超时脱敏

## 五类工具集（典型 15 工具）
1. 文件 `fs_list/fs_read/fs_write(覆盖前自动备份)/fs_search/fs_info` —— 根目录锁定，越界/../穿越/写只读区全部拒绝
2. Git `git_status/commit/pull/push` —— 凭据临时注入远端 URL，用后还原，禁 `--force`
3. 浏览器 `browser_fetch/browser_screenshot/browser_probe` —— 见下方坑与修复
4. 蒸馏 `distill_markdown` —— 本地规则实现 RIA-TV++ 流水线，强制脱敏
5. 四端同步 `sync_four_ends/sync_status` —— Obsidian 直拷 / CNB 走 Git / IMA·乐享走 HTTP，凭据缺失入队不谎报

## 致命坑①：Playwright chromium 版本错配 → 抓取挂死
**现象**：`chromium.launch()` 不立即报错，而是卡 90s+（触发耗时下载/重试）。
**根因**：`playwright` npm 包要求的浏览器版本（如 1228）与 `ms-playwright` 缓存实际版本（如 1234）不一致；直接 `launch()` 找不到期望版本就尝试下载并挂起。
**修复**：不要依赖版本自动匹配。改用 `_find_chromium_exe()` 扫描 `os.environ['LOCALAPPDATA']/ms-playwright`，`rglob("chrome.exe")` / `chrome-headless-shell.exe`，把**真实存在的路径**作为 `executablePath` 传给 `chromium.launch({executablePath: <实际路径>})`，绕过版本号校验。优先完整 chromium（渲染更全），其次 headless shell。

```python
def _find_chromium_exe():
    cache = Path(os.environ.get("LOCALAPPDATA",""))/"ms-playwright"
    if not cache.exists(): return None
    found=[str(p) for pat in ("chrome.exe","chrome-headless-shell.exe")
           for p in cache.rglob(pat) if p.is_file()]
    for p in found:
        if "headless_shell" not in p and "chrome-headless-shell" not in p: return p
    return found[0] if found else None
```

## 致命坑②：subprocess 管道被 Chromium 子进程继承 → communicate() 死锁
**现象**：`subprocess.run([...,"node","playwright.js"], capture_output=True)` 永远等不到结束（直到 timeout），即使 Node 已打印结果。
**根因**：Chromium 会派生多个子进程并**继承父进程的 stdout/stderr 管道句柄**；`browser.close()` 未必让所有子进程退出 → 管道 EOF 永不到来 → `communicate()` 死锁。
**修复（双保险）**：
1. `run_cmd()` 支持把子进程输出**重定向到文件**（`stdout=open(path,'wb')` 而非 `capture_output=True`），Node 子进程不再持有管道。
2. Node 脚本把结果 JSON **直接写文件**（`fs.writeFileSync(process.env.LOBSTER_OUT_JSON, ...)`），Python 读文件取结果，不依赖 stdout 管道。标记行 `<<<LOBSTER_JSON>>>` 仅作日志兜底。
3. Node 的 `finally` 中**先写结果文件，再 `browser.close()`**，即使关闭挂起也不丢结果。

```python
# run_cmd 改造：接受 stdout_path/stderr_path
out_fh = open(stdout_path,"wb") if stdout_path else subprocess.PIPE
err_fh = open(stderr_path,"wb") if stderr_path else subprocess.PIPE
proc = subprocess.run(args, stdout=out_fh, stderr=err_fh, timeout=timeout, env=env)
# 读文件而非 proc.stdout
```

```js
// Node 侧：结果落盘优先
const fs=require('fs');
const outPath=process.env.LOBSTER_OUT_JSON;
// ... launch + goto ...
finally {
  if(outPath){ try{ fs.writeFileSync(outPath, JSON.stringify(result)); }catch(e){} }
  if(browser){ try{ await browser.close(); }catch(e){} }
}
```

## 启动与保活
- `start_mcp_http.ps1 -Detach -Port 8765`：后台常驻 + 保活守护（每 N 秒探活，异常指数退避重启）
- `stop_mcp_http.ps1`：按 pid 文件 + 端口释放
- `selftest_mcp.ps1 [-Full]`：模拟豆包完整握手 6 阶段自测（`-Full` 额外跑真实抓取+蒸馏）

## 沙箱/环境注意
- **PowerShell 工具可能拦截 `Start-Process powershell.exe`**（LOLBin 启发式）。本沙箱内 `-Detach` 嵌套拉起会被拒；改用 `-NoWatchdog` 直接以托管 Python 启动，服务作为独立子进程持续运行。脚本在用户本机正常 PowerShell 下 `-Detach` 保活正常。
- 优先用托管 Python：`C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe`
- 复用已装 Node Playwright：`NODE_BIN=C:\Users\Administrator\.workbuddy\binaries\node\versions\22.22.2\node.exe`，`NODE_PATH=G:\WorkBuddy_Data\binaries\node\workspace\node_modules`
- 零 pip 安装，契合磁盘危机；日志轮转（2MB×3）防占盘

## 红线
- 密钥/token 全走环境变量，`env.example.ps1` 不给明文
- 路径沙箱锁定根目录；只读保护区（如 `技能库`）禁止写入；非回环源拒绝
- 端口绑定前强制校验 host ∈ {127.0.0.1, localhost, ::1}，否则改回 127.0.0.1

---

## 跨技能联动矩阵

| 联动技能 | 关系 | 触发场景 |
|---------|------|---------|
| `ai-workstation-morning-check` | ← 前置预防 | 晨检探活 MCP `/health` 端点 → 无响应时提示启动 |
| `browser-auto-universal` | → 浏览器依赖 | MCP的 browser_fetch/screenshot 工具依赖 Playwright Chromium |
| `local-llm-integration-fix` | → MCP配置依赖 | MCP客户端（豆包/Claude Desktop）连接配置 |
| `marvis-repair` | ← 进程依赖 | MCP的蒸馏/同步工具依赖 Marvis 运行态 |
| `lexiang-knowledge-base` | → 知识库联动 | `sync_four_ends` 工具将蒸馏内容同步到乐享 |
| `cloudbase-hy3-relay` | → 云函数联动 | MCP的蒸馏工具可通过 HY3 代理调用云端能力 |

---

*V1.1 于 2026-08-26 由 auto-skill-generator 第48次执行迭代（补交叉引用矩阵）。待补充：`scripts/` 目录下的实际脚本文件（start_mcp_http.ps1 / stop_mcp_http.ps1 / selftest_mcp.ps1 / lobster_common.py）。*
