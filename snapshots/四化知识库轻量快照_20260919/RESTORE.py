# -*- coding: utf-8 -*-
"""RESTORE.py v1.0 · 轻量快照回滚/重放/校验
用法(在快照目录执行):
  python RESTORE.py rollback   # 还原守卫脚本到加固前
  python RESTORE.py reapply    # 重新应用加固版
  python RESTORE.py verify     # 校验当前状态
"""
import os, hashlib, sys, shutil

ROOT = r"E:\龙虾AI主控中心\我的AI分身\企业微信群定制接单项目"
GUARD = os.path.join(ROOT, "scripts", "python_runtime_guard.py")
SELF_DIR = os.path.dirname(os.path.abspath(__file__))
FIXED = os.path.join(SELF_DIR, "scripts", "python_runtime_guard.py")

ADD1 = (
    "\n# 已知不稳定盘（外置 USB，频繁 I/O 重试/掉盘）—— 2026-09-19 实证：G: = Seagate Expansion (USB)\n"
    "# 任何落在这些盘上的解释器/venv 都应被降级，绝不推荐给关键常驻服务。\n"
    'FLAKY_ROOTS = {"G:"}\n'
)
ADD2 = (
    '    # 优先选不在不稳定盘上的解释器（关键常驻服务绝不能依赖外置 USB 盘）\n'
    '    safe = [r for r in good if Path(r["path"]).drive.upper() not in FLAKY_ROOTS]\n'
    '    rec = (safe[0] if safe else (good[0] if good else None))\n'
    '    rec = rec["path"] if rec else ""\n'
    '    flaky_rec = bool(good) and rec and Path(rec).drive.upper() in FLAKY_ROOTS\n'
)
ADD3 = ',\n                          "flaky_recommended": flaky_rec,'
ADD4 = (
    '    if flaky_rec:\n'
    '        print("=" * 70)\n'
    '        print("\\u26a0\\ufe0f 严重：当前唯一可用的解释器位于不稳定盘（外置 USB，实测频繁 I/O 重试/掉盘）！")\n'
    '        print("   关键常驻服务(MCP/守卫/分身)若用它启动，G 盘一抖就会集体崩溃 -> 必须重启。")\n'
    '        print("   处置：\\u2460 立即换 USB 线/直插主板口保证供电稳定；\\u2461 把 WorkBuddy_Data 与")\n'
    '        print("         g_venv_* 迁到健康内盘(C:或 NVMe)并改指向 C 盘副本；\\u2462 备份 G 盘数据。")\n'
)


def is_fixed(text):
    return "FLAKY_ROOTS" in text


def revert(text):
    t = text
    t = t.replace(ADD1, "\n")
    t = t.replace(ADD2, '    rec = good[0]["path"] if good else ""\n')
    t = t.replace(ADD3, ",\n")
    t = t.replace(ADD4, "")
    return t


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def rollback():
    with open(GUARD, "r", encoding="utf-8") as f:
        cur = f.read()
    if not is_fixed(cur):
        print("[rollback] 当前已是加固前状态，无需回滚。")
        return
    orig = revert(cur)
    with open(GUARD, "w", encoding="utf-8") as f:
        f.write(orig)
    print("[rollback] 已还原 python_runtime_guard.py 到加固前版本。")


def reapply():
    if not os.path.exists(FIXED):
        print("[reapply] 快照内固定版缺失，无法重放。")
        return
    shutil.copy2(FIXED, GUARD)
    print("[reapply] 已重放加固版 python_runtime_guard.py。")


def verify():
    print("[verify] 守卫脚本当前状态:")
    with open(GUARD, "r", encoding="utf-8") as f:
        cur = f.read()
    print("  加固版(FLAKY_ROOTS 存在):", is_fixed(cur))
    for name in ("README.md", "SKILL.md", "RESTORE.py", "MANIFEST.json",
                 "scripts/python_runtime_guard.py",
                 "reports/reboot_diag_20260919.txt",
                 "reports/reboot_diag2_20260919.txt"):
        p = os.path.join(SELF_DIR, name)
        print("  %s: %s" % (name, ("OK " + sha(p)[:12]) if os.path.exists(p) else "缺失"))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "verify"
    {"rollback": rollback, "reapply": reapply, "verify": verify}.get(cmd, verify)()
