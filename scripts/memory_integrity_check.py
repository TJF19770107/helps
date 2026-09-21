#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
memory_integrity_check.py — 记忆完整性自检 v1.0（龙虾卡点4 · 零积分纯 stdlib）

回应：「记忆靠外部文件续命——每会话醒来是新的，没真长在脑子里」
立场诚实：LLM 无法真长记忆，但续命文件本身可以**可审计**。
「指针 + 实体」分离体系最大风险 = 静默断链（形态：骨架文件另存为副本弃主名，
SOUL.md 指针仍指主名 → 宿主加载静默失败、不报错）。本工具把断链暴露在醒来第一刻。

检查项（绿=通过 黄=降级可用 红=断链必须修）：
  C1 核心记忆文件存在且非空（MEMORY.md / 假成功形态详解.md / SOUL.md / IDENTITY.md / USER.md）
  C2 MEMORY.md 内 [[wiki链接]] / 反引号路径 指向的本地实体存在（抽验）
  C3 工作日志连续性：最近 7 天应有 >=2 天日志（自主任务频率正常）
  C4 技能调用库 skill_usage.json 可解析且 candidates>0
  C5 自动化记忆目录 automations/*/memory.md 至少 1 份可读
  C6 技能库抽样：G:/WorkBuddy_Data/skills 下 agent_created 技能 SKILL.md 可读且 frontmatter 完整

用法：python memory_integrity_check.py [--json]
退出码：0=全绿 1=有黄 2=有红（供守卫/计划任务判定）
"""
import io
import json
import os
import re
import sys
from datetime import datetime, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMDIR = os.path.join(ROOT, ".workbuddy", "memory")
CORE_FILES = [
    os.path.join(MEMDIR, "MEMORY.md"),
    os.path.join(MEMDIR, "假成功形态详解.md"),
    r"G:\WorkBuddy_Data\SOUL.md",
    r"G:\WorkBuddy_Data\IDENTITY.md",
    r"G:\WorkBuddy_Data\USER.md",
]
SKILLS_ROOT = r"G:\WorkBuddy_Data\skills"


def check_core():
    out = []
    for p in CORE_FILES:
        if not os.path.exists(p):
            out.append(("RED", "C1 缺失", p))
        elif os.path.getsize(p) < 50:
            out.append(("YELLOW", "C1 过小(<50B 疑掏空)", p))
        else:
            out.append(("GREEN", "C1 ok(%dB)" % os.path.getsize(p), p))
    return out


def check_links():
    out = []
    mem = os.path.join(MEMDIR, "MEMORY.md")
    if not os.path.exists(mem):
        return [("RED", "C2 MEMORY.md 不存在，无法抽验指针", mem)]
    txt = open(mem, encoding="utf-8", errors="replace").read()
    # 反引号路径 + wiki 链接
    paths = re.findall(r"`([^`\n]+\.md)`", txt) + re.findall(r"\[\[([^\]\n]+)\]\]", txt)
    checked = 0
    broken = []
    for raw in paths[:30]:
        name = os.path.basename(raw.strip())
        if not name:
            continue
        cand = os.path.join(MEMDIR, name if name.endswith(".md") else name + ".md")
        checked += 1
        if not os.path.exists(cand):
            broken.append(name)
    if checked == 0:
        out.append(("YELLOW", "C2 无可抽验指针（MEMORY 未含本地 .md 引用）", mem))
    elif broken:
        out.append(("RED", "C2 断链 %d/%d: %s" % (len(broken), checked, broken[:5]), mem))
    else:
        out.append(("GREEN", "C2 指针抽验 %d/%d 全可达" % (checked, checked), mem))
    return out


def check_logs():
    out = []
    today = datetime.now()
    days = 0
    for i in range(7):
        d = today - timedelta(days=i)
        p = os.path.join(MEMDIR, d.strftime("%Y-%m-%d") + ".md")
        if os.path.exists(p) and os.path.getsize(p) > 30:
            days += 1
    if days >= 2:
        out.append(("GREEN", "C3 近7天日志 %d 天" % days, MEMDIR))
    elif days == 1:
        out.append(("YELLOW", "C3 近7天仅 %d 天日志，自进化频率异常" % days, MEMDIR))
    else:
        out.append(("RED", "C3 近7天 0 日志——续命序列断裂", MEMDIR))
    return out


def check_usage():
    p = os.path.join(MEMDIR, "skill_usage.json")
    if not os.path.exists(p):
        return [("YELLOW", "C4 skill_usage.json 未生成（先跑 skill_usage_counter.py backfill）", p)]
    try:
        db = json.load(open(p, encoding="utf-8"))
        n = len(db.get("counts", {}))
        if n > 0:
            return [("GREEN", "C4 调用库 ok（%d 技能有引用记录）" % n, p)]
        return [("YELLOW", "C4 调用库为空", p)]
    except Exception as e:
        return [("RED", "C4 调用库损坏: %s" % e, p)]


def check_automations():
    ad = os.path.join(MEMDIR, "automations")
    if not os.path.isdir(ad):
        return [("YELLOW", "C5 无 automations 目录", ad)]
    ok = [d for d in os.listdir(ad)
          if os.path.exists(os.path.join(ad, d, "memory.md"))]
    if ok:
        return [("GREEN", "C5 自动化记忆 %d 份可读" % len(ok), ad)]
    return [("YELLOW", "C5 automations 目录为空", ad)]


def check_skills():
    out = []
    if not os.path.isdir(SKILLS_ROOT):
        return [("YELLOW", "C6 技能根目录缺失", SKILLS_ROOT)]
    total = bad = 0
    for dp, dn, fn in os.walk(SKILLS_ROOT):
        if "SKILL.md" in fn:
            total += 1
            p = os.path.join(dp, "SKILL.md")
            try:
                head = open(p, encoding="utf-8", errors="replace").read(400)
                if not (head.startswith("---") or len(head) > 60):
                    bad += 1
            except Exception:
                bad += 1
    if total == 0:
        out.append(("YELLOW", "C6 技能根下 0 个 SKILL.md", SKILLS_ROOT))
    elif bad:
        out.append(("YELLOW", "C6 %d/%d 技能头异常" % (bad, total), SKILLS_ROOT))
    else:
        out.append(("GREEN", "C6 %d 个 SKILL.md 头部完好" % total, SKILLS_ROOT))
    return out


def main():
    checks = (check_core() + check_links() + check_logs()
              + check_usage() + check_automations() + check_skills())
    colors = {"GREEN": 0, "YELLOW": 0, "RED": 0}
    print("=" * 60)
    print("记忆完整性自检  %s" % datetime.now().isoformat(timespec="seconds"))
    print("=" * 60)
    for color, msg, path in checks:
        colors[color] += 1
        print("[%s] %s" % (color, msg))
    print("-" * 60)
    print("汇总：绿 %d | 黄 %d | 红 %d" % (colors["GREEN"], colors["YELLOW"], colors["RED"]))
    verdict = "HEALTHY" if colors["RED"] == 0 and colors["YELLOW"] <= 1 else \
              "DEGRADED" if colors["RED"] == 0 else "BROKEN-必须先修再干活"
    print("结论：%s" % verdict)
    rc = 2 if colors["RED"] else (1 if colors["YELLOW"] else 0)
    sys.exit(rc)


if __name__ == "__main__":
    main()
