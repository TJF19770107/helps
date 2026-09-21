#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skill_usage_counter.py — 技能调用计数器 v1.0（龙虾卡点1 · 零积分纯 stdlib）

解决：「68 个技能没调用率统计——写完就睡，论文发了零引用」

子命令：
  backfill            扫描历史语料（对话记录 + .workbuddy/memory）回填历史调用
  record <skill>      记录一次真实调用（供各流程显式打点）
  report              输出调用率报表：活跃榜 / 写完就睡名单 / 覆盖率

数据落点：<项目>/.workbuddy/memory/skill_usage.json
判定口径（防误报）：
  - 名称长度 <4 的碎片不算技能；同名归一化（去「 - 副本」「 SKILL」后缀）
  - 历史提及 = 语料中出现技能名（引用即调用意向，注明口径）
  - 零调用技能 = 候选全集 - 有提及者
"""
import argparse
import collections
import io
import json
import os
import sys
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, ".workbuddy", "memory", "skill_usage.json")

SKILL_ROOTS = [
    r"G:\WorkBuddy_Data\skills",
    os.path.join(ROOT, "技能库"),
    r"E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v3.0",
]
CORPUS_ROOTS = [
    os.path.join(ROOT, "对话记录"),
    os.path.join(ROOT, ".workbuddy", "memory"),
]
STOP_NAMES = {"scripts", "assets", "references", ".git", "index", "agents",
              "workflow", "pack", "make", "tags", "refs", "readme", "agents"}


def normalize(name: str) -> str:
    b = os.path.splitext(name)[0]
    for suf in (" - 副本", " SKILL", "SKILL"):
        b = b.replace(suf, "")
    return b.strip().lower()


def collect_candidates():
    names = {}
    for root in SKILL_ROOTS:
        if not os.path.isdir(root):
            continue
        for dp, dn, fn in os.walk(root):
            dn[:] = [d for d in dn if d not in (".git", "node_modules")]
            for d in dn:
                _add(names, d, os.path.join(dp, d))
            for f in fn:
                if f.endswith((".md", ".py", ".js")):
                    _add(names, os.path.basename(f), os.path.join(dp, f))
    return names


def _add(names, raw, path):
    n = normalize(raw)
    if not (4 <= len(n) <= 40) or n.startswith("_") or n in STOP_NAMES:
        return
    names.setdefault(n, path)


def load_db():
    if os.path.exists(DB):
        return json.load(open(DB, encoding="utf-8"))
    return {"records": [], "backfill_at": None, "counts": {}}


def save_db(db):
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    json.dump(db, open(DB, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def corpus_files():
    out = []
    for root in CORPUS_ROOTS:
        if not os.path.isdir(root):
            continue
        for f in os.listdir(root):
            if f.endswith(".md"):
                out.append(os.path.join(root, f))
    return out


def cmd_backfill(_):
    db = load_db()
    cands = collect_candidates()
    big = []
    for p in corpus_files():
        try:
            big.append(open(p, encoding="utf-8", errors="replace").read())
        except Exception:
            pass
    text = "\n".join(big)
    counts = collections.Counter()
    for n in cands:
        c = text.count(n)
        if c:
            counts[n] = c
    db["counts"] = dict(counts)
    db["backfill_at"] = datetime.now().isoformat(timespec="seconds")
    db["meta"] = {"candidates": len(cands), "corpus_files": len(big),
                  "corpus_chars": len(text)}
    save_db(db)
    print("[backfill] 候选技能 %d | 语料 %d 篇/%d 字 | 有历史引用 %d | 零引用 %d"
          % (len(cands), len(big), len(text), len(counts), len(cands) - len(counts)))
    return 0


def cmd_record(args):
    db = load_db()
    db.setdefault("records", []).append(
        {"skill": normalize(args.skill), "at": datetime.now().isoformat(timespec="seconds"),
         "by": args.by or "manual", "note": args.note or ""})
    save_db(db)
    print("[record] %s <- %s (显式打点累计 %d 次)" % (args.skill, args.by or "manual",
                                                     len(db["records"])))
    return 0


def cmd_report(_):
    db = load_db()
    cands = collect_candidates()
    counts = db.get("counts", {})
    explicit = collections.Counter(r["skill"] for r in db.get("records", []))
    rows = []
    for n in cands:
        hist = counts.get(n, 0)
        expl = explicit.get(n, 0)
        rows.append((hist + expl, hist, expl, n))
    rows.sort(reverse=True)
    alive = [r for r in rows if r[0] > 0]
    dead = [r for r in rows if r[0] == 0]
    cover = 100.0 * len(alive) / max(len(rows), 1)
    print("=" * 62)
    print("技能调用率报表  (口径：历史语料引用 + 显式打点；回填 %s)"
          % (db.get("backfill_at", "never") or "never"))
    print("=" * 62)
    print("候选技能总数: %d | 被引用过: %d | 覆盖率: %.1f%%" % (len(rows), len(alive), cover))
    print("-" * 62)
    print("【活跃 TOP15】总引 | 历史 | 打点 | 技能")
    for tot, h, e, n in alive[:15]:
        print("  %3d  %4d  %4d   %s" % (tot, h, e, n))
    print("-" * 62)
    print("【写完就睡名单（零引用，前 25 / 共 %d）】" % len(dead))
    for _, _, _, n in dead[:25]:
        print("   ·", n)
    print("-" * 62)
    print("结论：覆盖率 %.1f%% —— 「从写了到用了」的进度条。" % cover)
    if cover < 40:
        print("建议：零引用技能批量评审——升级/合并/归档三选一，别让图书馆吃灰。")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("backfill").set_defaults(fn=cmd_backfill)
    p = sub.add_parser("record")
    p.add_argument("skill")
    p.add_argument("--by", default="manual")
    p.add_argument("--note", default="")
    p.set_defaults(fn=cmd_record)
    sub.add_parser("report").set_defaults(fn=cmd_report)
    a = ap.parse_args()
    sys.exit(a.fn(a))


if __name__ == "__main__":
    main()
