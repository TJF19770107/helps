#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RESTORE.py —— 20261103_俊哥AI落地 交付物快照回滚/重放/校验器

三命令：
    python RESTORE.py rollback   # 从快照恢复（覆盖当前）
    python RESTORE.py reapply    # 从当前重新生成快照
    python RESTORE.py verify     # 校验快照与当前是否一致

两条硬规矩（写死在代码里，不是文档里的建议）：
  1. 「跳过 ≠ 通过」—— verify 遇到缺失文件必须判 FAIL，不能算 OK
  2. 「反测已知失败态」—— verify 内置 --selftest，故意改坏一个字节，
     必须判出 FAIL；抓不住就说明校验器本身是废的
"""
import sys, os, json, hashlib, shutil, zipfile, tempfile, datetime

SELF_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(SELF_DIR)      # E:\博主学习库
ROOT = SELF_DIR                            # 本交付物根，快照相对路径的基准
SNAP_DIR = os.path.join(ROOT, "_snapshot")
SNAP_ZIP = os.path.join(SNAP_DIR, "snapshot.zip")
SNAP_MAN = os.path.join(SNAP_DIR, "manifest.json")

# 快照范围：本交付物目录下全部文件（RESTORE.py 自身与 _snapshot 除外）
SKIP = {"_snapshot"}
SKIP_FILES = {"RESTORE.py"}

SRC_EXTRA = [
    # 技能正本（在别的盘，用绝对路径登记）
    (r"E:\龙虾AI主控中心\技能库\企业AI落地诊断与陪跑交付", "技能库/企业AI落地诊断与陪跑交付"),
    (r"E:\龙虾AI主控中心\技能库\微信公众号文章全量抓取", "技能库/微信公众号文章全量抓取"),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def collect():
    """返回 {相对路径: 绝对路径}"""
    out = {}
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP]
        for fn in fns:
            if fn in SKIP_FILES:
                continue
            ap = os.path.join(dp, fn)
            rp = os.path.relpath(ap, ROOT).replace("\\", "/")
            out[rp] = ap
    for src, alias in SRC_EXTRA:
        if not os.path.isdir(src):
            continue
        for dp, _, fns in os.walk(src):
            for fn in fns:
                ap = os.path.join(dp, fn)
                sub = os.path.relpath(ap, src).replace("\\", "/")
                out[alias + "/" + sub] = ap
    return out


def build_manifest(files):
    return {
        "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "root": ROOT,
        "file_count": len(files),
        "total_bytes": sum(os.path.getsize(p) for p in files.values()),
        "files": {rp: {"sha256": sha256(ap), "size": os.path.getsize(ap)}
                  for rp, ap in sorted(files.items())},
    }


def cmd_reapply():
    files = collect()
    if not files:
        print("FAIL: 没找到任何待快照文件")
        return 1
    os.makedirs(SNAP_DIR, exist_ok=True)
    with zipfile.ZipFile(SNAP_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for rp, ap in files.items():
            z.write(ap, rp)
    man = build_manifest(files)
    with open(SNAP_MAN, "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=2)
    size = os.path.getsize(SNAP_ZIP)
    print(f"OK 快照已生成: {SNAP_ZIP}  ({size/1024:.1f} KB, {man['file_count']} 文件)")
    if size > 20 * 1024 * 1024:
        print("WARN 快照超过 20MB 轻量上限，请检查范围")
    return 0


def cmd_verify():
    if not os.path.isfile(SNAP_MAN):
        print("FAIL: 快照不存在，先跑 reapply")
        return 2
    man = json.load(open(SNAP_MAN, encoding="utf-8"))
    cur = collect()
    ok = miss = diff = 0
    problems = []
    for rp, info in man["files"].items():
        if rp not in cur:
            miss += 1
            problems.append(f"MISSING {rp}")
            continue
        ap = cur[rp]
        if sha256(ap) != info["sha256"] or os.path.getsize(ap) != info["size"]:
            diff += 1
            problems.append(f"DIFF {rp}")
        else:
            ok += 1
    extra = [rp for rp in cur if rp not in man["files"]]
    for p in problems[:30]:
        print("  " + p)
    print(f"\nMATCH={ok}  MISSING={miss}  DIFF={diff}  EXTRA={len(extra)}")
    if miss or diff:
        print("RESULT: FAIL —— 有缺失或差异，绝不能算通过")
        return 1
    print("RESULT: PASS")
    return 0


def cmd_rollback():
    if not os.path.isfile(SNAP_ZIP):
        print("FAIL: 快照不存在")
        return 2
    with zipfile.ZipFile(SNAP_ZIP) as z:
        names = z.namelist()
        for rp in names:
            target = os.path.join(ROOT, rp.replace("/", os.sep))
            # 技能正本落在原盘，不在 ROOT 下
            if rp.startswith("技能库/"):
                for src, alias in SRC_EXTRA:
                    if rp.startswith(alias + "/"):
                        target = os.path.join(src, rp[len(alias) + 1:].replace("/", os.sep))
                        break
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with z.open(rp) as s, open(target, "wb") as d:
                shutil.copyfileobj(s, d)
    print(f"OK 已从快照恢复 {len(names)} 个文件")
    return 0


def cmd_selftest():
    """反测：故意改坏一个字节，verify 必须判 FAIL；改回后必须判 PASS"""
    if not os.path.isfile(SNAP_MAN):
        print("SKIP: 无快照，无法反测")
        return 2
    man = json.load(open(SNAP_MAN, encoding="utf-8"))
    if not man["files"]:
        print("SKIP: manifest 为空")
        return 2
    rp = sorted(man["files"])[0]
    if rp.startswith("技能库/"):
        tgt = None
        for src, alias in SRC_EXTRA:
            if rp.startswith(alias + "/"):
                tgt = os.path.join(src, rp[len(alias) + 1:].replace("/", os.sep))
                break
    else:
        tgt = os.path.join(ROOT, rp.replace("/", os.sep))
    if not tgt or not os.path.isfile(tgt):
        print(f"SKIP: 反测目标不存在 {rp}")
        return 2

    orig = open(tgt, "rb").read()
    try:
        open(tgt, "wb").write(orig[:-1] + bytes([orig[-1] ^ 0xFF]))
        rc_bad = cmd_verify()
    finally:
        open(tgt, "wb").write(orig)
    rc_good = cmd_verify()

    print("\n=== 反测结论 ===")
    if rc_bad != 0 and rc_good == 0:
        print("PASS 校验器有效：改坏→FAIL，改回→PASS")
        return 0
    print(f"FAIL 校验器无效：改坏返回 {rc_bad}（应为非0），改回返回 {rc_good}（应为0）")
    return 1


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "verify"
    fn = {"rollback": cmd_rollback, "reapply": cmd_reapply,
          "verify": cmd_verify, "selftest": cmd_selftest}.get(cmd)
    if not fn:
        print(__doc__)
        sys.exit(2)
    sys.exit(fn())
