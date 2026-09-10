# 香港隧道假死 + GptBrowser插件假死 双修复方法论（2026-09-10 汤小龙蒸馏）

> 来源：2026-09-10 两次实战修复（ERR_TUNNEL_CONNECTION_FAILED + GptBrowser 插件集体变灰）。
> 全程零积分，龙���五步法 V3.6 执行。

## 一、香港代理链路假死（ERR_TUNNEL_CONNECTION_FAILED）

### 链路架构（记死）
```
Chrome(系统代理 127.0.0.1:7897)
  → http2socks_7897.py (自建 HTTP→SOCKS5 中转, E:\龙虾AI主控中心\MCP服务\)
    → SSH 隧道 SOCKS5 127.0.0.1:1081 (计划任务 Lobster_HKTunnel 常驻)
      bat: C:\Users\Administrator\hk_proxy_tunnel.bat (-D 1081 -L 3002, 断线5s自动重连)
        → 香港轻量 43.161.202.206 (root, 密钥 ~/.ssh/id_ed25519)
```
⚠️ 7897 不是 Clash，是自建中转器（python.exe 监听）。

### 报错分流表
| 现象 | 故障层 |
|---|---|
| ERR_PROXY_CONNECTION_FAILED | 代理端口挂了（7897/1081 没监听） |
| ERR_TUNNEL_CONNECTION_FAILED | CONNECT 通但数据不通 = 隘道假死（最高频） |
| 直连 1081 通、走 7897 超时 | 中转器 http2socks 僵死 → 重启它 |
| 直连 1081 也超时 | ssh 假死或服务器侧 → 修复三板斧 |

### 核心铁律
- **TCP ESTABLISHED ≠ 链路可用**：ping 通 + netstat ESTABLISHED 都可能假死。
- 用**数据面探针**实测：SOCKS5 atyp=3 域名解析请求（域名由香港侧解析，直接暴露服务器侧转发健康度），10s 超时 = 假死实锤。
- 修复三板斧：`taskkill /F /PID <ssh_pid>` → 常驻 bat 5 秒自动重连 → 数据面复测。10 秒恢复，零手动干预。

### 本案坑位
- wmic 输出 UTF-16 直接看是乱码 → 重定向文件按 UTF-16 读。
- `curl | head` 后 `$?` 是 head 的退出码不是 curl 的 → 测连通用 `-o /dev/null -w "%{http_code}"`。
- 7897 被 python 中转器占用 → 别误判成 Clash 去 GUI 里折腾。

## 二、GptBrowser（GPT Chrome）插件集体变灰失灵

### 浏览器档案
- 任务栏「GPT Chrome」= `D:\Program Files\GptChrome\GptBrowser.exe`（谷歌 128 内核）
- user-data-dir = `C:\Users\Administrator\AppData\Local\SPChrome\User Data`（三步定位法：crashpad-handler 进程的 --user-data-dir 参数）
- 扩展注册看 **Secure Preferences**（Preferences 里 extensions.settings 恒为空，别误判全部禁用）

### 判定与修复
1. 先查 Secure Preferences `extensions.settings`：所有扩展 state=1 = 配置层没坏，别走重装弯路
2. 查 debug.log 崩溃记录：`crash server did not respond, self-terminating` = 崩溃后僵尸进程堆积
3. **修复 = 备份 + 全杀 + 重启**：备份两个 Preferences → `taskkill /F /IM GptBrowser.exe`（本案杀了 31 个僵尸进程）→ 重启 → 扩展进程恢复挂载（验证 `--extension-process` 进程数 > 0）
4. 扩展图标灰 = service worker 死了，重启浏览器即复活；**手动编辑 Secure Preferences 有 HMAC 校验风险**（protection.macs），删扩展必须走浏览器 UI

### 遗留项
- Obsidian Web Clipper 双副本：商店版 cnjifjpddelmedmihgijeibhnjfabmlf v1.7.1 + 未打包版 hlibkjmiafgncimagnkildcfpfcfgcla（指向 E:\lobster_ai_temp_fleet 临时目录）。清理必须走 chrome://extensions UI 点移除（HMAC 保护，禁外部改文件）。

## 三、豆包接管浏览器 → 「Windows 找不到文件 '--remote-debugging-port=9223'」弹窗定性
- mcp-helper.exe（E:\龙虾AI主控中心\Doubao\app\）= 豆包浏览器接管伴生进程
- 豆包启动外部浏览器带 CDP 参数时路径解析失败 → 把参数当文件名 ShellExecute → 弹窗
- 修复：taskkill mcp-helper.exe，豆包按需重拉即复位
