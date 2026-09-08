# -*- coding: utf-8 -*-
"""evolve_tangxiaolong.py · 汤小龙进化定时任务（每日自动迭代）
果位阶梯（天级）：硕士1天 → 博士1天 → 博士后1天 → 博导2-3天 → 院士7天 → 诺奖/菲尔兹1月
每次运行：更新进度、按天推进果位、写Obsidian迭代记录、登记技能扫描。
"""
import os, json, datetime, subprocess

ENT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(ENT)
OBS = r"G:\龙虾AI主控中心\Obsidian\wiki\我的AI分身"
PROG = os.path.join(ENT, "进化进度.json")

LADDER = [
    {"name": "硕士", "days": 1, "criterion": "单域独立闭环"},
    {"name": "博士", "days": 1, "criterion": "跨域贯通，方法可迁移"},
    {"name": "博士后", "days": 1, "criterion": "原创方法论/新技能"},
    {"name": "博导", "days": 3, "criterion": "带子Agent(ORCA舰队跑通)"},
    {"name": "院士", "days": 7, "criterion": "行业级影响力"},
    {"name": "诺奖/菲尔兹", "days": 30, "criterion": "定义新范式"},
]

def load_prog():
    if os.path.exists(PROG):
        try:
            with open(PROG, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"level": 0, "accum": 0, "start": datetime.date.today().isoformat(), "log": []}

def save_prog(p):
    with open(PROG, "w", encoding="utf-8") as f:
        json.dump(p, f, ensure_ascii=False, indent=2)

def main():
    p = load_prog()
    today = datetime.date.today().isoformat()
    # 若今天已跑过则不重复推进（幂等）
    if p.get("last_run") == today:
        print("今日已进化，跳过。当前果位:", LADDER[p["level"]]["name"])
        return
    p["accum"] = p.get("accum", 0) + 1
    p["last_run"] = today
    lv = min(p["level"], len(LADDER)-1)
    need = LADDER[lv]["days"]
    if p["accum"] >= need and p["level"] < len(LADDER)-1:
        p["level"] += 1
        p["accum"] = 0
        p["log"].append({"date": today, "to": LADDER[p["level"]]["name"]})
    cur = LADDER[p["level"]]
    save_prog(p)
    print("进化进度: 果位=%s 累计天数=%d 下一步=%s" % (cur["name"], p["accum"], LADDER[min(p["level"]+1,len(LADDER)-1)]["name"]))
    # 写 Obsidian 迭代记录
    os.makedirs(OBS, exist_ok=True)
    rec = """---
title: 迭代记录·汤小龙每日进化(自动)
tags: [四化迭代, 进化, 定时任务, 果位, 汤小龙]
distilled_at: %s
---
# 汤小龙每日进化（自动）%s
当前果位: **%s** | 累计天数: %s | 里程碑: %s
进化阶梯: 硕士→博士→博士后→博导→院士→诺奖/菲尔兹
""" % (today, today, cur["name"], p["accum"], cur["criterion"])
    path = os.path.join(OBS, "迭代记录_汤小龙每日进化_%s.md" % today.replace("-",""))
    with open(path, "w", encoding="utf-8") as f:
        f.write(rec)
    print("Obsidian 迭代已写:", path)
    # 回写 AGENTS.md 当前果位（灵魂自我更新）
    agents = os.path.join(ROOT, "AI分身实体", "AGENTS.md")
    if os.path.exists(agents):
        ac = open(agents, encoding="utf-8").read()
        import re
        new_ac = re.sub(r"当前：\S+。每日05:00", "当前：%s。每日05:00" % cur["name"], ac)
        if new_ac != ac:
            open(agents, "w", encoding="utf-8").write(new_ac)
            print("AGENTS.md 果位已回写: %s" % cur["name"])

if __name__ == "__main__":
    main()