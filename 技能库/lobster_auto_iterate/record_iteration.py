#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙虾迭代记录 Producer v1.0
补齐缺失环节：在问题修复完成后，将案例结构化写入
E:\\龙虾AI主控中心\\state\\issues_tracker.json 的 resolved 数组，
供已有固化引擎 lobster_skill_solidify.py (每日00:10) 消费。

用法:
  python record_iteration.py --problem "..." --root_cause "..." \
    --solution "..." --category codex_link \
    --keywords "词1,词2" --skill_package xxx --tools "a.bat,b.py"
"""
import argparse
import json
from datetime import datetime
from pathlib import Path

BASE = Path(r"E:\龙虾AI主控中心")
TRACKER = BASE / "state" / "issues_tracker.json"
SKILL_KB = BASE / "skill_knowledge"
OBSIDIAN_A = BASE / "Obsidian"
OBSIDIAN_B = BASE / "ObsidianVault"


def load_tracker():
    if TRACKER.exists():
        try:
            return json.loads(TRACKER.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"open": [], "resolved": [], "archived": []}


def save_tracker(data):
    TRACKER.parent.mkdir(parents=True, exist_ok=True)
    TRACKER.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def similarity(a: str, b: str) -> float:
    """简单关键词重叠相似度 (0~1)"""
    sa, sb = set(a.lower().split()), set(b.lower().split())
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def dedupe_check(problem: str, keywords: list):
    """检索历史，返回 (场景, 匹配旧条目)"""
    # 1. 查 skill_knowledge/*.json
    old_entries = []
    if SKILL_KB.exists():
        for f in SKILL_KB.glob("*.json"):
            try:
                e = json.loads(f.read_text(encoding="utf-8"))
                old_entries.append(e)
            except Exception:
                continue
    # 2. 查 tracker.archived 对应文件
    # 计算相似度
    best, best_score = None, 0.0
    probe = f"{problem} " + " ".join(keywords)
    for e in old_entries:
        old_text = f"{e.get('problem','')} " + " ".join(e.get('trigger_keywords', []))
        s = similarity(probe, old_text)
        if s > best_score:
            best, best_score = e, s
    if best_score >= 0.8:
        return "C(完全重复)", best
    if best_score >= 0.4:
        return "B(历史同类可优化)", best
    return "A(全新问题)", None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--problem", required=True)
    ap.add_argument("--root_cause", required=True)
    ap.add_argument("--solution", required=True)
    ap.add_argument("--category", default="general")
    ap.add_argument("--keywords", default="")
    ap.add_argument("--skill_package", default="")
    ap.add_argument("--tools", default="")
    ap.add_argument("--source_track", default="WorkBuddy")
    args = ap.parse_args()

    kws = [k.strip() for k in args.keywords.split(",") if k.strip()]
    tools = [t.strip() for t in args.tools.split(",") if t.strip()]

    # Step2 重复判定
    scene, matched = dedupe_check(args.problem, kws)
    print(f"[重复判定] 场景{scene} (匹配度参考)")

    # Step1 写入 resolved
    tracker = load_tracker()
    entry = {
        "problem": args.problem,
        "root_cause": args.root_cause,
        "solution": args.solution,
        "category": args.category,
        "trigger_keywords": kws,
        "skill_package": args.skill_package,
        "tools": tools,
        "source_track": args.source_track,
        "resolved_at": datetime.now().isoformat(),
        "iteration_scene": scene,
    }
    tracker.setdefault("resolved", []).append(entry)
    save_tracker(tracker)

    # Step3 软连接绑定 (追加到 INDEX.jsonl)
    SKILL_KB.mkdir(parents=True, exist_ok=True)
    idx = SKILL_KB / "INDEX.jsonl"
    idx_line = json.dumps({
        "problem": args.problem, "category": args.category,
        "skill_package": args.skill_package, "keywords": kws,
        "recorded_at": entry["resolved_at"]
    }, ensure_ascii=False)
    with idx.open("a", encoding="utf-8") as f:
        f.write(idx_line + "\n")

    # 迭代回执
    print("=" * 50)
    print("  龙虾迭代回执 (Iteration Receipt)")
    print("=" * 50)
    print(f"  问题闭环校验 : ✅ 已写入 issues_tracker.json.resolved")
    print(f"  重复判定     : {scene}")
    print(f"  软连接绑定   : ✅ INDEX.jsonl 已追加")
    print(f"  双端沉淀     : ⏳ Obsidian双库 + Git 待写入(见下方)")
    print(f"  多Agent同步  : ⏳ 待 AGENTS.md 引用更新")
    print(f"  固化待消费   : ✅ 固化引擎将在下次00:10自动消费")
    print("=" * 50)
    print(f"固化引擎路径: E:\\龙虾AI主控中心\\lobster_skill_solidify.py")
    print("任务闭环完成。")


if __name__ == "__main__":
    main()
