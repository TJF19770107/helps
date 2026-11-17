# -*- coding: utf-8 -*-
"""
fix_skill_version.py —— 技能版本号四处对齐 + 章节重号修复（第37形态 假成功防线）

问题（实测）：
  1. 正文标题 `# 得到大脑Obsidian四化拆解 SKILL v1.1.0` 与 frontmatter version: v2.0.0 不一致
  2. 章节重号：两个 `## 九、`、两个 `## 八、`

铁律：二进制安全。先 read_bytes 看行尾 → split(b"\n") 操作 → open("wb") 写回。
锚点必须逐字符等于原文一个完整语义单元，且 assert count==1。
"""
import os, sys, hashlib

sys.stdout.reconfigure(encoding="utf-8")

SKILL = r"E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v3.0\得到大脑Obsidian四化拆解\SKILL.md"

# (锚点原文, 替换后, 期望出现次数)
FIXES = [
    ("# 得到大脑Obsidian四化拆解 SKILL v1.1.0",
     "# 得到大脑Obsidian四化拆解 SKILL v2.0.0", 1),
    ("## 九、v2.0.0 实测升级（2026-11-17 第三轮 · Obsidian 复活 + REST 通道打通）",
     "## 十、v2.0.0 实测升级（2026-11-17 第三轮 · Obsidian 复活 + REST 通道打通）", 1),
    ("## 八、技能回馈（本技能 v2.0.0 诞生记录）",
     "## 十一、技能回馈（本技能 v2.0.0 诞生记录）", 1),
]

raw = open(SKILL, "rb").read()
print(f"原文件 {len(raw)} B  sha256 {hashlib.sha256(raw).hexdigest()[:16]}")
crlf = b"\r\n" in raw
print(f"行尾风格: {'CRLF' if crlf else 'LF'}")

sep = b"\r\n" if crlf else b"\n"
lines = raw.split(sep)
print(f"行数 {len(lines)}")

for anchor, repl, expect in FIXES:
    ab = anchor.encode("utf-8")
    idxs = [i for i, l in enumerate(lines) if l == ab]
    print(f"\n锚点: {anchor[:50]}...")
    print(f"  精确命中行号: {[i+1 for i in idxs]}  (期望 {expect})")
    if len(idxs) != expect:
        print(f"  ❌ 命中数不符，中止（不写回）")
        sys.exit(1)
    print(f"  命中行原文: {lines[idxs[0]].decode('utf-8')}")
    lines[idxs[0]] = repl.encode("utf-8")

new = sep.join(lines)

# 引号配对自检（铁律：插入式补写类任务收尾必查）
bad = [(i + 1, l.decode("utf-8", "replace"))
       for i, l in enumerate(lines) if l.count(b'"') % 2 == 1]
if bad:
    print(f"\n❌ 引号未配对行: {bad[:5]}")
    sys.exit(1)
print("\n✅ 引号配对自检 PASS")

open(SKILL, "wb").write(new)
print(f"✅ 已写回 {os.path.getsize(SKILL)} B  sha256 {hashlib.sha256(new).hexdigest()[:16]}")

# 复核
t = new.decode("utf-8")
print("\n=== 复核 ===")
for l in t.split("\n"):
    if l.startswith("# ") or l.startswith("## ") or l.startswith("### "):
        print("  " + l[:72])
import re
m = re.search(r"^version:\s*(\S+)", t, re.M)
print(f"frontmatter version = {m.group(1)}")
