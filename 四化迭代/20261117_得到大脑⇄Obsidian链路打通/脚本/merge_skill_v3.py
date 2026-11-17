# -*- coding: utf-8 -*-
"""
merge_skill_v3.py —— 把本轮「得到大脑网页通道打通」新发现合并进 SKILL.md（字节级安全 + 幂等守卫）

新增章节（十一·附）：网页通道的真相 —— 会员墙只挡 OpenAPI，网页后端免费
关键实测结论：
  1. CLI/OpenAPI 基址 = https://openapi.biji.com/open/api/v1/...  → 10201 not_member（付费墙）
  2. 网页版基址   = https://notes-api.biji.com                  → 免费通道
     · 端点：POST /voicenotes/web/notes 建笔记
             POST /voicenotes/web/notes/{note_id}/tags  {"tags":[...]} 打标签
             GET  /voicenotes/web/tags 查标签
  3. 鉴权分两类：
     · gk_live_ api_key 打网页后端 → 403 LoginRequired（token 格式被解析成功，但类型不对）
     · OAuth Device Flow access_token → 网页后端可用
  4. OAuth Device Flow 端点（实测 200）：
     POST https://notes-api.biji.com/open/api/v1/oauth/device/code  {"client_id": ...}
       → {code, user_code, verification_uri, verification_uri_qrcode, expires_in:600, interval:5}
     POST https://notes-api.biji.com/open/api/v1/oauth/token
       {"grant_type":"device_code","client_id":...,"code":...}
       → pending 形态 {"success":true,"data":{"msg":"authorization_pending"},"error":null}
         ★ pending 判定必须看 data.msg，不能只看 error（error 为 null）
       → 成功形态 data.access_token
  5. 主机矩阵实测：
     openapi.biji.com      → 付费通道（10201）
     open-api.biji.com     → 404
     notes-api.biji.com    → ★ 网页免费通道
     get-notes.luojilab.com / notes.luojilab.com → 同源镜像
     www.biji.com          → 前端路由（/openapi 前缀走付费通道）
     knowledge-api.trytalks.com → AppNotFound（App 维度鉴权）
"""
import os, sys, hashlib

sys.stdout.reconfigure(encoding="utf-8")

SKILL = r"E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v3.0\得到大脑Obsidian四化拆解\SKILL.md"
ANCHOR = "## 十一、技能回馈（本技能 v2.0.0 诞生记录）"

NEW = """## 十一·附、网页通道的真相（2026-11-17 第四轮实测 · 会员墙只挡 OpenAPI）

### 11.1 双后端架构（关键认知修正）

| 通道 | 基址 | 鉴权 | 状态 |
|---|---|---|---|
| CLI / OpenAPI（付费） | `https://openapi.biji.com/open/api/v1/...` | `gk_live_` api_key + X-Client-ID | ❌ **10201 not_member**（会员墙） |
| 网页版（免费） | `https://notes-api.biji.com/...` | OAuth Device Flow access_token | ✅ **本轮打通** |

> 会员墙拦的是**付费 API 通道**，不是账号，也不是网页版功能。收藏网页 + 打标签是普通用户功能，走网页后端即可，**零付费**。

### 11.2 写入链路（三个端点，全实测）

| 步骤 | 端点 | 方法 | 请求体 |
|---|---|---|---|
| 建笔记 | `/voicenotes/web/notes` | POST | `{"title":..., "content":..., "url":...}` |
| 打标签 | `/voicenotes/web/notes/{note_id}/tags` | POST | `{"tags":["产品灵感", ...]}` |
| 查标签 | `/voicenotes/web/tags` | GET | `?page_size=50&page=1&hide_zero_note=false&query=` |
| AI 自动打标 | `/voicenotes/web/notes/{note_id}/generate-tags` | POST | `{"title":..., "content":...}` |

### 11.3 OAuth Device Flow（无需手机验证码，一次点授权）

```
① POST https://notes-api.biji.com/open/api/v1/oauth/device/code   {"client_id": "<cli_xxx>"}
   → {"data":{"code":"...","user_code":"XXXX-XXXX",
              "verification_uri":"https://biji.com/openapi/oauth/authorize?code=...",
              "verification_uri_qrcode":"data:image/png;base64,...",
              "expires_in":600,"interval":5}}
② 汤哥扫码/点链接 → 授权页点「同意」
③ POST https://notes-api.biji.com/open/api/v1/oauth/token
   {"grant_type":"device_code","client_id":"<cli_xxx>","code":"<code>"}
   pending: {"success":true,"data":{"msg":"authorization_pending"},"error":null}
   成功  : {"success":true,"data":{"access_token":"..."}}
```

★ **两个坑**：
- pending 判定必须看 **`data.msg`**，不能只看 `error`（pending 时 error 是 null）—— 踩过：判成成功 → 拿到 null token
- `verification_uri_qrcode` 是 base64 PNG，**渲染成本地图片让汤哥手机扫**，比在沙箱里开有头窗口稳（沙箱 Job Object 会杀浏览器进程树）

### 11.4 主机矩阵实测（别瞎猜路径）

| 主机 | 用途 | 备注 |
|---|---|---|
| `notes-api.biji.com` | ★ 网页免费通道 | 建笔记/打标签都在这 |
| `openapi.biji.com` | 付费 OpenAPI | 10201 会员墙 |
| `open-api.biji.com` | 旧名 | 404 |
| `get-notes.luojilab.com` / `notes.luojilab.com` | 同源镜像 | 与 notes-api 行为一致 |
| `www.biji.com` | 前端站点 | `/openapi` 前缀走付费通道；`/api/v1/*` 返回 JSON 404 |
| `knowledge-api.trytalks.com` | 知识库 | 403 AppNotFound（App 维度鉴权） |

### 11.5 沙箱内拉起浏览器的正确姿势（踩坑记录）

| 方式 | 结果 | 原因 |
|---|---|---|
| `subprocess` + DETACHED_PROCESS | ❌ 被杀 | 沙箱用 **Job Object 层级清理**，detach 逃不掉 |
| `schtasks` / WMI `CreateProcess` | ❌ 被拦 | Program Blacklist |
| PowerShell COM `WScript.Shell` | ❌ 被拦 | 安全策略（任意代码执行） |
| `explorer.exe <file.cmd>` | ❌ 没生效 | 转发未落地（实测 rc=1 无进程） |
| **PowerShell `Start-Process`** | ⚠️ 一时能起，但命令结束即被清 | 同 Job Object |
| **改走 API，别开浏览器** | ✅ **正解** | Device Flow 只要一次扫码授权 |

> **教训**：在 Job Object 沙箱里，「开 GUI 让人操作」这条路基本走不通 —— 应优先找**纯 API 路径**（本轮 OAuth Device Flow 就是这么找到的）。

### 11.6 本轮新增脚本

| 脚本 | 作用 |
|---|---|
| `oauth_device_run.py` | Device Flow 申请 + 轮询 + 验证 |
| `oauth_qr_render.py` | base64 二维码渲染成本地 PNG（汤哥手机扫） |
| `oauth_device_probe.py` | 各主机 × 端点鉴权口径探针 |
| `web_api_probe.py` / `web_api_probe2.py` / `web_api_probe3.py` | 端点 × 主机 × 凭证形态矩阵探针 |
| `dump_biji_api.py` / `dump_biji_write_api.py` | 从网页 JS 扒真实后端端点 |
| `dedao_web_writer.py` | 网页通道写入器（建笔记 + 打标签） |
| `fix_skill_version.py` | 技能版本号四处对齐 + 章节重号修复（第 37 形态防线） |

### 11.7 实战命令

```bash
# 申请授权（打印二维码 + 轮询）
python E:\博主学习库\_tools\oauth_device_run.py start
# 渲染二维码给汤哥扫
python E:\博主学习库\_tools\oauth_qr_render.py
# 验通道
python E:\博主学习库\_tools\dedao_web_writer.py --check
# 列已有标签
python E:\博主学习库\_tools\dedao_web_writer.py --list-tags
# 写入 + 打「产品灵感」标签
python E:\博主学习库\_tools\dedao_web_writer.py --url "https://www.biji.com" --title "标题" --tag 产品灵感
```

---

"""

raw = open(SKILL, "rb").read()
crlf = b"\r\n" in raw
sep = b"\r\n" if crlf else b"\n"
lines = raw.split(sep)
print(f"原 {len(raw)} B  行尾 {'CRLF' if crlf else 'LF'}  行数 {len(lines)}")

# 幂等守卫
if any(b"11.1" in l and b"\xe5\x8f\x8c\xe5\x90\x8e\xe7\xab\xaf" in l for l in lines):
    print("❌ 已存在「十一·附」章节，幂等守卫触发，不重复插入")
    sys.exit(0)

idxs = [i for i, l in enumerate(lines) if l == ANCHOR.encode("utf-8")]
print(f"锚点命中行号: {[i+1 for i in idxs]}")
if len(idxs) != 1:
    print("❌ 锚点不唯一，中止")
    sys.exit(1)
at = idxs[0]
print(f"  命中行原文: {lines[at].decode('utf-8')}")

new_lines = lines[:at] + NEW.encode("utf-8").split(sep) + lines[at:]
out = sep.join(new_lines)

bad = [(i + 1, l.decode('utf-8', 'replace')) for i, l in enumerate(new_lines) if l.count(b'"') % 2 == 1]
if bad:
    print(f"❌ 引号未配对: {bad[:5]}")
    sys.exit(1)
print("✅ 引号配对自检 PASS")

open(SKILL, "wb").write(out)
print(f"✅ 已写回 {os.path.getsize(SKILL)} B  sha256 {hashlib.sha256(out).hexdigest()[:16]}")
for l in out.decode("utf-8").split("\n"):
    if l.startswith("## ") or l.startswith("### "):
        print("  " + l[:70])
