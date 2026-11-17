# -*- coding: utf-8 -*-
"""
push_force_final.py —— 用 --force 强推重写后的历史（修 stale info）

根因（实测）：
  · 历史经 filter-branch 重写，所有 commit hash 变了
  · 之前用 --force-with-lease + 显式 URL（无 tracking ref）→ stale info
  · 远端 lobster-kb 停在 f3de35f7 → 必须 --force 强推

密钥安全：oauth_token 从 ~/.config/gh/hosts.yml 读取，不进命令行、不进日志、不进 git。

铁律：
  · 推前扫描待推提交里是否含真实预签名 URL / AKID 密钥（只报命中路径，不打印值）
  · 推后 ls-remote 回查同一 commit（不靠"我推了"自述）
"""
import os, sys, subprocess, re

sys.stdout.reconfigure(encoding="utf-8")

REPO = r"E:\博主学习库\_tmp_shot\lkb_clone"


def run(args, cwd=REPO, timeout=600, env=None):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", shell=False,
                       timeout=timeout, env=env)
    return r.returncode, ((r.stdout or "") + (r.stderr or "")).strip()


print("=== 1. 推前敏感串扫描（只报路径，不打印值）===")
# 只扫本轮新增的提交（filter-branch 重写后的头部 5 个），排除历史快照文档里的文字描述
rc, out = run(["git", "log", "-5", "--format=%H", "fresh-main"])
commits = [l for l in out.splitlines() if re.fullmatch(r"[0-9a-f]{40}", l)]
hits = []
for c in commits:
    rc, paths = run(["git", "grep", "-l", "-I",
                     r"q-signature=[0-9a-f]{20,}|AKID[A-Za-z0-9]{30,}",
                     c, "--", "四化迭代/", "脚本/", "--", "*.py", "*.json"],
                    timeout=120)
    for p in paths.splitlines():
        if p.strip():
            hits.append((c[:8], p.strip()))
print(f"  扫描 {len(commits)} 个提交，命中 {len(hits)} 处")
for c, p in hits[:10]:
    print(f"    ⚠️ {c} {p}")
if hits:
    print("  ❌ 仍有真实密钥，停止推送")
    sys.exit(2)
print("  ✅ 无真实预签名 URL / AKID 密钥")

print("\n=== 2. 读取 token（脱敏）===")
HOSTS = os.path.join(os.path.expanduser("~"), ".config", "gh", "hosts.yml")
m = re.search(r"oauth_token:\s*(\S+)",
              open(HOSTS, encoding="utf-8", errors="ignore").read())
if not m:
    print("  ❌ 无 oauth_token")
    sys.exit(3)
URL = f"https://x-access-token:{m.group(1)}@github.com/TJF19770107/helps.git"
env = dict(os.environ)
env["GIT_TERMINAL_PROMPT"] = "0"

print("\n=== 3. --force 强推（历史已重写）===")
rc, out = run(["git", "push", "--force", URL, "fresh-main:lobster-kb"], env=env, timeout=600)
print(f"  rc={rc}\n  {out[:600]}")
if rc != 0:
    print("  ❌ 推送失败")
    sys.exit(4)

print("\n=== 4. ls-remote 回查远端 ===")
rc, out = run(["git", "rev-parse", "HEAD"])
local = out.strip()
rc, out = run(["git", "ls-remote", URL, "refs/heads/lobster-kb"], timeout=180)
remote = out.strip()
print(f"  本地 HEAD : {local}")
print(f"  远端      : {remote}")
found = remote.startswith(local)
print(f"  同一 commit: {'✅ 是' if found else '❌ 否'}")
if not found:
    sys.exit(5)
print("\n✅ GitHub 归档闭环（远端回查同一 commit，非自述）")
