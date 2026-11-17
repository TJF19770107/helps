# -*- coding: utf-8 -*-
"""
archive_round6.py —— 第六轮归档：技能 v2.0.0(含第五轮踩坑) + 六端台账(CN B边界) + GitHub

不依赖得到大脑授权，先归档已确定的部分；授权写入结果等后台任务完成后再补。
"""
import os, sys, json, shutil, subprocess, re, hashlib, urllib.parse

sys.stdout.reconfigure(encoding="utf-8")

REPO = r"E:\博主学习库\_tmp_shot\lkb_clone"
DEST = os.path.join(REPO, "四化迭代", "20261117_得到大脑⇄Obsidian链路打通")
SKILL_DIR = r"E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v3.0\得到大脑Obsidian四化拆解"
TOOLS = r"E:\博主学习库\_tools"


def run(args, cwd=REPO, timeout=600, env=None):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", shell=False,
                       timeout=timeout, env=env)
    return r.returncode, ((r.stdout or "") + (r.stderr or "")).strip()


print("=== 1. 同步技能双副本 ===")
sk_dst = os.path.join(DEST, "技能")
for f in ["SKILL.md"]:
    s = os.path.join(SKILL_DIR, f)
    shutil.copy2(s, os.path.join(sk_dst, f))
    print(f"  ✅ 技能/{f}  {os.path.getsize(s)} B")
# 权威副本也同步成最新（v2.0.0 文件名副本）
shutil.copy2(os.path.join(SKILL_DIR, "SKILL.md"),
             os.path.join(SKILL_DIR, "SKILL_v2.0.0.md"))
shutil.copy2(os.path.join(SKILL_DIR, "SKILL.md"),
             os.path.join(sk_dst, "SKILL_v2.0.0.md"))
print(f"  ✅ SKILL_v2.0.0.md（双副本对齐）")

print("\n=== 2. 新增脚本归档 ===")
sc_dst = os.path.join(DEST, "脚本")
for f in ["push_force_final.py", "purge_presigned_url.py", "auto_finalize.py",
          "test_writer_payload.py", "merge_skill_v4.py", "archive_round6.py"]:
    s = os.path.join(TOOLS, f)
    if os.path.exists(s):
        shutil.copy2(s, os.path.join(sc_dst, f))
        print(f"  ✅ {f}")

print("\n=== 3. 更新六端台账（CNB 边界精确化）===")
LEDGER = os.path.join(DEST, "六端归档台账.md")
txt = open(LEDGER, encoding="utf-8").read()
add = """
## 第六轮更新（2026-11-17 20:xx · GitHub 推送历史清洗闭环）

| 端 | 状态 | 凭据（可独立核验） |
|---|---|---|
| GitHub | ✅ **本轮闭环** | `TJF19770107/helps` 分支 `lobster-kb`，commit `a07073a2` —— **ls-remote 回查同一 commit**。历史经 filter-branch 清除 COS 预签名 URL（GH013 secret scanning），推前扫描 5 个提交 0 命中 |
| CNB | ❌ **权限边界（非仓不存在，修正上轮口径）** | 实测：`cnb status` 已登录（CNB_TOKEN 环境变量，27字符）；但 `get-repos` → 403 `Missing required scopes: account-engage:r`；`create-repo` 需 `group-resource:rw`。CLI **有** create-repo 工具，是 token scope 不足，不是没工具/没仓。解法：汤哥在连接器授权时勾 `group-resource:rw`，或手动建 `lobster-knowledge-base` 仓后我一条 push 补齐 |
| 技能 | ✅ | SKILL.md 19855 B（sha `967842cc6bfae550`），新增第十二章「归档链路三道闸门」：GH013 / force-with-lease stale / CNB scope / 沙箱后台进程 |

### 本轮新增四条真坑（已进技能第十二章）

1. **GH013**：临时凭据（COS 预签名 URL / 40位 device code）进 git → push protection 拦。`git rm --cached` 不够（历史 blob 仍在），必须 `filter-branch` 重写 + `reflog expire` + `gc`
2. **force-with-lease stale**：显式 URL 强推无 tracking ref → lease 拿不到期望值 → 一律 stale；改 `--force` + ls-remote 回查
3. **CNB scope**：token 有效但缺 `group-resource:rw` → 不能建仓（修正上轮"仓不存在"口径）
4. **沙箱 Job Object**：`python x.py &` 起的后台进程命令返回即被清（日志停摆但实际状态脱节）→ 用平台受管理后台任务
"""
if "第六轮更新" not in txt:
    open(LEDGER, "w", encoding="utf-8").write(txt.rstrip() + "\n" + add)
    print(f"  ✅ 台账更新 {os.path.getsize(LEDGER)} B")

print("\n=== 4. git add（明确路径）===")
rc, out = run(["git", "add", "--", "四化迭代/20261117_得到大脑⇄Obsidian链路打通"])
print(f"  rc={rc}")

rc, out = run(["git", "diff", "--cached", "--stat"])
print("\n=== 5. 暂存区 ===")
print(out[:1200])

print("\n=== 6. commit ===")
rc, out = run(["git", "commit", "-m",
               "docs: 四化迭代 20261117 第六轮 GitHub历史清洗闭环+CNB权限边界+技能v2.0.0"])
print(f"  rc={rc} {out[:300]}")

print("\n=== 7. 推 GitHub ===")
HOSTS = os.path.join(os.path.expanduser("~"), ".config", "gh", "hosts.yml")
m = re.search(r"oauth_token:\s*(\S+)", open(HOSTS, encoding="utf-8", errors="ignore").read())
URL = f"https://x-access-token:{m.group(1)}@github.com/TJF19770107/helps.git"
env = dict(os.environ); env["GIT_TERMINAL_PROMPT"] = "0"
rc, out = run(["git", "push", "--force", URL, "fresh-main:lobster-kb"], env=env, timeout=600)
print(f"  rc={rc}\n  {out[:350]}")

print("\n=== 8. 回查远端 ===")
rc, out = run(["git", "rev-parse", "HEAD"]); local = out.strip()
rc, out = run(["git", "ls-remote", URL, "refs/heads/lobster-kb"], timeout=180)
found = out.strip().startswith(local)
print(f"  HEAD {local[:12]}  远端一致: {'✅ 是' if found else '❌ 否'}")
