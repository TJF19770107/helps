# -*- coding: utf-8 -*-
"""RESTORE.py —— 一键回滚/重放/校验
用法：
  python RESTORE.py verify            # 校验当前态与快照一致
  python RESTORE.py rollback          # 回滚到快照态（移入隔离区，不删除）
  python RESTORE.py reapply           # 重放快照（把快照文件拷回原位）
  python RESTORE.py verify --expect broken   # 反测：期望不一致时必须 FAIL
"""
import os, sys, json, shutil, hashlib, datetime

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
MAN = os.path.join(HERE, "MANIFEST.json")
QUAR = os.path.join(HERE, "_rollback_quarantine")


def sha(p):
    if not os.path.isfile(p):
        return None
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def load():
    return json.loads(open(MAN, encoding="utf-8").read())


def cmd_verify(expect_match=True):
    m = load()
    ok = bad = miss = 0
    for it in m["files"]:
        cur = it["src"]
        if not os.path.exists(cur):
            print(f"  [MISS] {it['label']}  -> {cur}")
            miss += 1
            continue
        if it["sha256"] == "dir":
            print(f"  [DIR ] {it['label']}  (跳过哈希)")
            ok += 1
            continue
        h = sha(cur)
        if h == it["sha256"]:
            print(f"  [OK  ] {it['label']}")
            ok += 1
        else:
            print(f"  [DIFF] {it['label']}  当前={str(h)[:12]} 期望={it['sha256'][:12]}")
            bad += 1
    print(f"\n  查了 {len(m['files'])} 项：一致 {ok} / 不符 {bad} / 缺失 {miss}")
    match = (bad == 0 and miss == 0)
    if expect_match:
        print("  结论: " + ("PASS" if match else "FAIL"))
        return 0 if match else 1
    else:
        print("  结论(反测): " + ("PASS(发现不一致，校验器有效)" if not match else "FAIL(该报不一致却没报!)"))
        return 0 if not match else 1


def cmd_rollback():
    m = load()
    os.makedirs(QUAR, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    n = 0
    for it in m["files"]:
        cur = it["src"]
        if not os.path.exists(cur):
            continue
        dst = os.path.join(QUAR, f"{ts}_{it['label'].replace(chr(92), '_')}")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(cur, dst)   # 只移走，不删除
        print(f"  移入隔离区: {it['label']} -> {dst}")
        n += 1
    print(f"\n  已回滚 {n} 项，隔离区: {QUAR}")
    return cmd_verify()


def cmd_reapply():
    m = load()
    n = 0
    for it in m["files"]:
        s = it["snap"]
        d = it["src"]
        if not os.path.exists(s):
            print(f"  [skip] 快照缺失 {it['label']}")
            continue
        os.makedirs(os.path.dirname(d), exist_ok=True)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
        print(f"  已恢复: {it['label']}")
        n += 1
    print(f"\n  已重放 {n} 项")
    return cmd_verify()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "verify"
    exp = "broken" in sys.argv
    if cmd == "verify":
        sys.exit(cmd_verify(not exp))
    elif cmd == "rollback":
        sys.exit(cmd_rollback())
    elif cmd == "reapply":
        sys.exit(cmd_reapply())
    else:
        print(__doc__)
        sys.exit(1)
