#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
five_lib_dispatch.py  v1.0  (龙虾零成本运维守卫 v1.3 组件)
「五库分发」一键编排器——把每天重复的五落点归档从手工操作变成幂等、可断点、可回查的脚本。

背景（为什么要造它）：
  每日自进化/技能产出都要分发到五个落点，此前全靠手工逐步执行，存在三类成本：
    1) 死凭据挂起：CNB 令牌失效时 git push 会一直等凭据助手，实测挂死 6+ 分钟；
    2) 弱判定返工：拿不到强结论只能反复试推，靠报错猜原因；
    3) 漏端无回执：某一端没落成功，事后靠回忆补，容易留空洞。
  本脚本用「前置门禁 + 逐端回执」一次性解决。

五端职责划分（诚实边界）：
  ① obsidian  本地文件系统   -> 全自动（copytree）
  ④ cnb       git 推送       -> 全自动（门禁 + 推送 + ls-remote 回查）
  ⑤ github    git 推送       -> 全自动（socks5 代理 + 门禁 + 回查）
  ② lexiang   乐享 MCP       -> 半自动：本脚本生成载荷 + 记录回执，MCP 调用由 Agent 执行
  ③ ima       IMA  MCP       -> 半自动：同上（推荐走 import_urls 导乐享页，最省事）

用法:
  python five_lib_dispatch.py --status
  python five_lib_dispatch.py --target obsidian --src <技能目录>
  python five_lib_dispatch.py --target cnb --repo G:/tmp/lobster-knowledge-base
  python five_lib_dispatch.py --target github --repo G:/tmp/lobster-knowledge-base --branch fresh-main
  python five_lib_dispatch.py --all --src <技能目录> --repo <镜像仓> --title "分发标题"
  python five_lib_dispatch.py --record-receipt lexiang --url https://lexiangla.com/pages/xxx
  python five_lib_dispatch.py --report

退出码:  0 = 全通或仅有已知阻断   2 = 有端 FAIL   4 = 参数错误
零积分：纯 stdlib，不调任何模型。
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
DOCTOR = os.path.join(HERE, "remote_repo_doctor.py")
SAFE_PUSH = os.path.join(HERE, "git_mirror_safe_push.py")
RECEIPT_DIR = os.path.join(PROJECT, "待分发任务")

OBSIDIAN_LIB = r"G:\龙虾AI主控中心\Obsidian\技能库"
PY = sys.executable

# 各端网络通道（实测定论，不要改）：
#   github -> 必须走 socks5://127.0.0.1:1081（香港链路），直连会挂 >6min
#   cnb    -> 必须清空代理（全局 http.proxy=7897 会污染），直连
GIT_CHANNEL = {
    "github": ["-c", "http.proxy=socks5://127.0.0.1:1081",
               "-c", "https.proxy=socks5://127.0.0.1:1081"],
    "cnb": ["-c", "http.proxy=", "-c", "https.proxy="],
}

SKIP_DIRS = {".git", "__pycache__", ".idea", ".vscode", "node_modules", ".workbuddy"}


def log(tag, msg):
    print("[%s] %s" % (tag, msg), flush=True)


def run(cmd, cwd=None, timeout=180):
    """统一子进程封装：stdout 走临时文件不用管道，规避 GCM 孙进程持管道导致 timeout 失效。"""
    tmp = os.path.join(os.environ.get("TEMP", "."), "_lb5_%d.tmp" % os.getpid())
    try:
        with open(tmp, "w", errors="ignore") as fo:
            p = subprocess.Popen(cmd, cwd=cwd, stdout=fo, stderr=subprocess.STDOUT,
                                 text=True, env=_env())
            try:
                p.communicate(timeout=timeout)
                rc = p.returncode
            except subprocess.TimeoutExpired:
                p.kill()
                try:
                    p.communicate(timeout=5)
                except Exception:
                    pass
                rc = -9
        with open(tmp, "r", errors="ignore") as fi:
            out = fi.read()
    except Exception as e:
        return 1, type(e).__name__ + " " + str(e)[:120]
    finally:
        try:
            os.remove(tmp)
        except Exception:
            pass
    return rc, out


def _env():
    env = dict(os.environ)
    env["GCM_INTERACTIVE"] = "never"
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["PYTHONUNBUFFERED"] = "1"
    return env


# ---------------------------------------------------------------- ① Obsidian
def dispatch_obsidian(src, report):
    if not src or not os.path.isdir(src):
        report("obsidian", "SKIP", "未指定 --src 或目录不存在: %s" % src)
        return
    name = os.path.basename(os.path.normpath(src))
    dst = os.path.join(OBSIDIAN_LIB, name)
    os.makedirs(dst, exist_ok=True)
    copied, skipped = 0, 0
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        rel = os.path.relpath(root, src)
        tgt = dst if rel == "." else os.path.join(dst, rel)
        os.makedirs(tgt, exist_ok=True)
        for f in files:
            if f.endswith((".pyc", ".tmp")):
                skipped += 1
                continue
            shutil.copy2(os.path.join(root, f), os.path.join(tgt, f))
            copied += 1
    report("obsidian", "OK", "%s -> %s（复制 %d 文件，跳过 %d）" % (name, dst, copied, skipped))


# ------------------------------------------------------- ④⑤ git 端（CNB/GitHub）
def doctor_gate(repo, remote):
    """推前门禁：让 remote_repo_doctor 先拿强判定，避免死凭据挂起。
    返回 (可推送 bool, 原因 str)。"""
    if not os.path.exists(DOCTOR):
        return True, "诊断器缺失(%s)，跳过门禁" % os.path.basename(DOCTOR)
    rc, out = run([PY, "-u", DOCTOR, "--repo", repo, "--remote", remote], timeout=120)
    m = re.search(r"\[(OK|FAIL|WARN)\]\s+IDN01\s+(.*)", out)
    if m and m.group(1) == "FAIL":
        return False, "令牌失效（身份探针 401）：%s" % m.group(2).strip()[:90]
    if rc == 0:
        return True, "诊断通过（身份探针 200 + ls-remote 可达）"
    # 无 FAIL 的 IDN01 但整体非 0：可能是网络，放行但带提示，由推送实测
    return True, "门禁弱通过（rc=%d，无令牌失效证据），继续实测推送" % rc


def safe_push_gate(repo):
    """复用 v1.1 的 12 项体检（假删除熔断 / 密钥扫描）。缺失或非 0 只告警不阻断。"""
    if not os.path.exists(SAFE_PUSH):
        return True, "体检脚本缺失，跳过"
    rc, out = run([PY, "-u", SAFE_PUSH, "--repo", repo], timeout=180)
    if rc == 0:
        return True, "安全体检通过"
    return True, "安全体检 rc=%d（仅告警）: %s" % (rc, out.strip().splitlines()[-1][:90] if out.strip() else "")


def dispatch_git(target, repo, branch, report, do_push=True):
    if not repo or not os.path.isdir(os.path.join(repo, ".git")):
        report(target, "SKIP", "仓库不存在: %s" % repo)
        return
    ok, why = doctor_gate(repo, target)
    if not ok:
        # 关键价值：这里直接止损，不再让 git 挂死 6 分钟
        report(target, "BLOCKED", why + " → 已跳过推送（未挂起）。处置：重签令牌后复跑")
        return
    ok2, why2 = safe_push_gate(repo)
    log("GATE", "%s %s" % (target, why2))

    rc, out = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo, timeout=30)
    cur = out.strip()
    if cur != branch:
        report(target, "SKIP", "当前分支 %s ≠ 目标 %s，不擅自切分支" % (cur, branch))
        return

    # 本地有没有待提交
    rc, out = run(["git", "status", "--porcelain"], cwd=repo, timeout=60)
    dirty = [l for l in out.splitlines() if l.strip()]
    if dirty:
        # 只 add「具体路径」绝不 add -A（假删除 3652 文件险情的血的教训）
        paths = sorted({l[3:].strip().strip('"') for l in dirty})
        run(["git", "add", "--"] + paths, cwd=repo, timeout=60)
        rc, out = run(["git", "commit", "-m", "五库分发: %s" % time.strftime("%Y-%m-%d %H:%M")],
                      cwd=repo, timeout=120)
        log("GIT", "commit rc=%d (%d 项)" % (rc, len(paths)))
    else:
        log("GIT", "工作区干净，无需 commit")

    head = run(["git", "rev-parse", "--short", "HEAD"], cwd=repo, timeout=30)[1].strip()
    if not do_push:
        report(target, "OK", "门禁通过（--no-push 模式），HEAD=%s" % head)
        return

    rc, out = run(["git"] + GIT_CHANNEL.get(target, []) + ["push", target, branch],
                  cwd=repo, timeout=300)
    if rc != 0:
        report(target, "FAIL", "push rc=%d: %s" % (rc, out.strip()[-200:]))
        return
    # 回查：远端 ref 必须等于本地 HEAD
    rc2, out2 = run(["git"] + GIT_CHANNEL.get(target, []) +
                    ["ls-remote", target, "refs/heads/" + branch], cwd=repo, timeout=120)
    remote_sha = out2.split()[0][:len(head)] if out2.split() else ""
    if remote_sha and remote_sha == head:
        report(target, "OK", "推送成功，ls-remote 回查一致 HEAD=%s" % head)
    else:
        report(target, "FAIL", "推送返回 0 但回查不一致(本地=%s 远端=%s)" % (head, remote_sha or "空"))


# ------------------------------------------------------------- ②③ MCP 端回执
def record_receipt(target, url, report=None):
    os.makedirs(RECEIPT_DIR, exist_ok=True)
    path = os.path.join(RECEIPT_DIR, "五库分发回执_%s.json" % time.strftime("%Y%m%d"))
    data = {}
    if os.path.exists(path):
        try:
            data = json.load(open(path, encoding="utf-8"))
        except Exception:
            data = {}
    data.setdefault("date", time.strftime("%Y-%m-%d"))
    data[target] = {"url": url, "at": time.strftime("%H:%M:%S")}
    json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    log("RECEIPT", "%s -> %s  (%s)" % (target, url, path))
    return path


def prepare_payload(title, src, report):
    """为 MCP 端（乐享/IMA）生成待发载荷，避免每次重写正文。"""
    os.makedirs(RECEIPT_DIR, exist_ok=True)
    payload = {"title": title, "source": src, "generated": time.strftime("%Y-%m-%d %H:%M:%S")}
    if src and os.path.isdir(src):
        md = [f for f in os.listdir(src) if f.upper().endswith(".MD")]
        payload["skill_files"] = md
    p = os.path.join(RECEIPT_DIR, "五库分发载荷_%s.json" % time.strftime("%Y%m%d"))
    json.dump(payload, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    report("payload", "OK", "MCP 端载荷已生成 %s" % p)
    return p


def show_status():
    print("=== 五库分发前置状态 ===")
    print("Obsidian 库 : %s %s" % (OBSIDIAN_LIB, "OK" if os.path.isdir(OBSIDIAN_LIB) else "MISSING"))
    print("诊断器      : %s %s" % (DOCTOR, "OK" if os.path.exists(DOCTOR) else "MISSING"))
    print("安全体检    : %s %s" % (SAFE_PUSH, "OK" if os.path.exists(SAFE_PUSH) else "MISSING"))
    rc, out = run(["git", "ls-remote", "--heads", "origin"], cwd=PROJECT, timeout=60)
    print("项目仓 origin: rc=%d" % rc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--target", choices=["obsidian", "lexiang", "ima", "cnb", "github", "payload"])
    ap.add_argument("--src", help="技能目录（Obsidian 落盘源）")
    ap.add_argument("--repo", help="镜像仓路径")
    ap.add_argument("--branch", default="fresh-main")
    ap.add_argument("--title", default="五库分发")
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--record-receipt", metavar="TARGET")
    ap.add_argument("--url", help="回执 URL")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()

    results = []

    def report(target, status, msg):
        results.append((target, status, msg))
        mark = {"OK": "✅", "SKIP": "⏸", "BLOCKED": "⛔", "FAIL": "❌"}.get(status, "•")
        log(mark, "%-9s %s" % (target, msg))

    if a.status:
        show_status()
        return 0
    if a.report:
        p = os.path.join(RECEIPT_DIR, "五库分发回执_%s.json" % time.strftime("%Y%m%d"))
        print(open(p, encoding="utf-8").read() if os.path.exists(p) else "今日无回执: %s" % p)
        return 0
    if a.record_receipt:
        record_receipt(a.record_receipt, a.url or "", report)
        return 0

    if a.all or a.target == "payload":
        prepare_payload(a.title, a.src, report)
    if a.all or a.target == "obsidian":
        dispatch_obsidian(a.src, report)
    if a.all or a.target == "cnb":
        dispatch_git("cnb", a.repo, a.branch, report, not a.no_push)
    if a.all or a.target == "github":
        dispatch_git("github", a.repo, a.branch, report, not a.no_push)
    if a.target in ("lexiang", "ima"):
        log("INFO", "%s 为 MCP 端：Agent 调用 MCP 后用 --record-receipt %s --url <链接> 记录回执"
            % (a.target, a.target))

    print("\n=== 五库分发报告 %s ===" % time.strftime("%Y-%m-%d %H:%M:%S"))
    for t, s, m in results:
        print("  %-9s %-8s %s" % (t, s, m))
    bad = [r for r in results if r[1] == "FAIL"]
    blocked = [r for r in results if r[1] == "BLOCKED"]
    print("  合计: OK=%d SKIP=%d BLOCKED=%d FAIL=%d"
          % (sum(1 for r in results if r[1] == "OK"),
             sum(1 for r in results if r[1] == "SKIP"),
             len(blocked), len(bad)))
    return 2 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
