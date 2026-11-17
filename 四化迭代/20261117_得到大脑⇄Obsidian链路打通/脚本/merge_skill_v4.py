# -*- coding: utf-8 -*-
"""
merge_skill_v4.py —— 追加第五轮踩坑（GitHub secret scanning / force lease / CNB scope / 沙箱后台）

字节级安全 + 幂等守卫 + 锚点逐字符完整 + 引号配对自检。
"""
import os, sys, hashlib

sys.stdout.reconfigure(encoding="utf-8")

SKILL = r"E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v3.0\得到大脑Obsidian四化拆解\SKILL.md"
ANCHOR = "## 十二、技能回馈（本技能 v2.0.0 诞生记录）"

NEW = """## 十三、第五轮踩坑：归档链路的三道闸门（2026-11-17 20:xx）

### 13.1 GitHub push protection（GH013）—— 临时凭据绝不能进 git

| 现象 | 真因 | 解法 |
|---|---|---|
| `remote: error: GH013 ... Push cannot contain secrets` | `ima_upload_v2.py` 硬编码 COS 预签名 URL（含 `q-ak=AKID...` + `q-signature=<40位hex>`）；`oauth_device_state.json` 有 40 位 device code | ①凭据改从环境变量读（`IMA_PRESIGNED_URL`/`IMA_MEDIA_ID`）；②一次性凭据文件进 `.gitignore`；③**已从索引删不够** —— 提交历史里还留着，必须 `git filter-branch --index-filter 'git rm --cached --ignore-unmatch <path>' --prune-empty` 重写历史 |

★ **关键**：push protection 扫的是**整个待推历史**，不是只有 HEAD。`git rm --cached` + 新提交**没用** —— 旧提交里的 blob 仍会被扫出来。必须重写历史。
- 收尾：`git reflog expire --expire=now --all && git gc --prune=now`，再 `git log --all -S "AKID" --oneline` 确认 0 命中
- 推前自检：`git grep -l -I 'q-signature=[0-9a-f]{20,}|AKID[A-Za-z0-9]{30,}' <commit> -- <路径>` —— **只报路径不打印值**（脱敏铁律）

### 13.2 `--force-with-lease` + 显式 URL → stale info

重写历史后强推报 `! [rejected] ... (stale info)`。真因：用 `git push <完整URL> local:remote` 时**没有对应的 tracking ref**，lease 拿不到"期望的远端值"→ 一律判 stale。
- 解法：重写历史后就用 `git push --force <URL> local:remote`（显式强推），推完 `git ls-remote <URL> refs/heads/<branch>` 回查同一 commit
- 备份先行：`git branch backup-before-purge-<oldhead[:8]>`（本轮做了 2 个备份分支）

### 13.3 CNB 建仓权限边界（诚实标注，不谎报）

`cnb repositories create-repo` 工具**存在**，但本环境的 `CNB_TOKEN`（27 字符受限 token）缺两个 scope：
- `get-repos` → 403 `Missing required scopes: account-engage:r`
- `create-repo` → 需 `group-resource:rw`
- 上一轮实测同一 token 能 `ls-remote orca-lobster` 业务仓 → **token 有效但权限不足**，非网络/非路径问题

→ 六端归档的 CNB 端如实写「❌ 未闭环：token scope 不含建仓权限，需汤哥在连接器授权时勾 `group-resource:rw` 或手动建仓」。**报 5.5 端真话，比报 6 端假话值钱。**

### 13.4 沙箱 Job Object 清后台进程

用 `python xxx.py &` 起的后台脚本，命令返回后**整棵子进程树被 Job Object 清掉** —— 表现：日志文件停在启动行、与实际状态脱节（本轮授权轮询误以为还在跑，实际进程已死）。
- 解法：用平台的**受管理后台任务**（Bash `run_in_background=true`）跑长轮询 —— 这类任务不受 Job Object 清理
- 判据：日志有持续心跳 + 任务状态 `running`；只看"进程数"不可靠（本轮 python 进程数一直是 7，实际目标进程早已被清）

### 13.5 本轮新增/更新的脚本

| 脚本 | 作用 |
|---|---|
| `push_force_final.py` | 推前敏感串扫描（只报路径）+ `--force` 强推 + ls-remote 回查 |
| `purge_presigned_url.py` | filter-branch 重写历史清密钥 + reflog/gc 清理 |
| `auto_finalize.py` | OAuth 授权后全自动建笔记+打标签+回查（受管理后台跑） |
| `test_writer_payload.py` | 6 项变更测试（含中文路径 UnicodeEncodeError 回归） |

---

"""

raw = open(SKILL, "rb").read()
crlf = b"\r\n" in raw
sep = b"\r\n" if crlf else b"\n"
lines = raw.split(sep)
print(f"原 {len(raw)} B  行尾 {'CRLF' if crlf else 'LF'}  行数 {len(lines)}")

if any(b"13.1" in l and b"push protection" in l.encode("utf-8", "ignore") for l in lines):
    print("❌ 已存在第十三章，幂等守卫触发，不重复插入")
    sys.exit(0)

idxs = [i for i, l in enumerate(lines) if l == ANCHOR.encode("utf-8")]
print(f"锚点命中: {[i+1 for i in idxs]}")
if len(idxs) != 1:
    print("❌ 锚点不唯一，中止")
    sys.exit(1)
at = idxs[0]
print(f"  原文: {lines[at].decode('utf-8')}")

lines = lines[:at] + NEW.encode("utf-8").split(sep) + lines[at:]
out = sep.join(lines)

bad = [(i + 1, l.decode("utf-8", "replace")) for i, l in enumerate(lines) if l.count(b'"') % 2 == 1]
if bad:
    print(f"❌ 引号未配对: {bad[:5]}")
    sys.exit(1)
print("✅ 引号配对自检 PASS")

open(SKILL, "wb").write(out)
print(f"✅ 已写回 {os.path.getsize(SKILL)} B  sha256 {hashlib.sha256(out).hexdigest()[:16]}")
for l in out.decode("utf-8").split("\n"):
    if l.startswith("## "):
        print("  " + l[:64])
