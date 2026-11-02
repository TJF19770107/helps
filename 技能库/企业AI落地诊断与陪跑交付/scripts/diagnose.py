# -*- coding: utf-8 -*-
"""企业 AI 落地三级门槛诊断 + 环节打分
用法：
  python diagnose.py                # 跑内置示例
  python diagnose.py -i case.json   # 读客户实际情况
case.json 结构见下方 SAMPLE
"""
import json, sys, argparse

SAMPLE = {
    "company": "某精密零件厂",
    "headcount": 42,
    "has_it": False,           # 是否有 IT 部门
    "it_staff": 1,             # IT 人数（0 = 无）
    "ai_accounts": 5,          # 员工自己开的 AI 账号数
    "ai_rules": False,         # 公司是否有 AI 使用规则
    "pilot_failed": 0,         # 过去被砍掉的 AI 项目数
    "champion": None,          # 旗手（None = 没定）
    "champion_scene": False,   # 旗手有说得清的场景
    "champion_data": False,    # 旗手拿得到真实数据
    "champion_time": False,    # 旗手每周有固定时间
    "steps": [                 # 候选环节：名称 / 月人工小时 / 重复度(1-5) / 出错成本(元)
        {"name": "客户询价→报价", "hours": 46, "repeat": 5, "err_cost": 8000},
        {"name": "来料质检记录",   "hours": 30, "repeat": 5, "err_cost": 15000},
        {"name": "月度对账",       "hours": 24, "repeat": 3, "err_cost": 2000},
        {"name": "员工考勤汇总",   "hours": 12, "repeat": 4, "err_cost": 300},
    ],
}

# 环节打分权重：人工小时 40% / 重复度 35% / 出错成本 25%
W = {"hours": 0.40, "repeat": 0.35, "err_cost": 0.25}


def norm(vals):
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return [1.0] * len(vals)
    return [(v - lo) / (hi - lo) for v in vals]


def score_steps(steps):
    hs = norm([s["hours"] for s in steps])
    rs = norm([s["repeat"] for s in steps])
    es = norm([s["err_cost"] for s in steps])
    out = []
    for s, a, b, c in zip(steps, hs, rs, es):
        v = a * W["hours"] + b * W["repeat"] + c * W["err_cost"]
        out.append(dict(s, score=round(v * 100, 1),
                        monthly_value=s["hours"] * 60))  # 粗估：按 60 元/小时
    return sorted(out, key=lambda x: -x["score"])


def gate(c):
    """返回 (卡在第几关, 结论列表)"""
    hits = []
    # 门槛①：不知道从哪开始（无旗手 / 无场景）
    g1 = not c.get("champion") or not (c.get("champion_scene") and c.get("champion_data"))
    # 门槛②：没人负责（影子 AI / 无规则）
    g2 = (not c.get("ai_rules")) and c.get("ai_accounts", 0) > 0
    # 门槛③：没等到出数就被砍
    g3 = c.get("pilot_failed", 0) >= 1

    if g1:
        hits.append(("①", "不知道从哪开始",
                     "目标太笼统。动作：画三条线 → 用下面打分选最痛那条 → 点旗手"))
    if g2:
        hits.append(("②", "没人负责（影子 AI 风险）",
                     f"已有 {c.get('ai_accounts')} 个自开账号、无使用规则。"
                     "动作：立刻补《AI 使用规则》+ 四签名登记表"))
    if g3:
        hits.append(("③", "没等到出数就被砍",
                     f"已有 {c.get('pilot_failed')} 个项目被砍。"
                     "动作：改成 30/90/365 节奏，第 30 天必须交出一个可验证数字"))
    if not hits:
        hits.append(("—", "三关已过", "可以直接进陪跑排期"))
    return hits


def champion_check(c):
    ok = all([c.get("champion"), c.get("champion_scene"),
              c.get("champion_data"), c.get("champion_time")])
    miss = []
    if not c.get("champion"):
        miss.append("没点旗手")
    if not c.get("champion_scene"):
        miss.append("旗手说不出具体场景")
    if not c.get("champion_data"):
        miss.append("旗手拿不到真实数据")
    if not c.get("champion_time"):
        miss.append("旗手没有每周固定时间")
    return ok, miss


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input")
    a = ap.parse_args()
    c = json.load(open(a.input, encoding="utf-8")) if a.input else SAMPLE

    print(f"=== 诊断对象：{c.get('company')}（{c.get('headcount')} 人）===\n")

    print("【一、三级门槛定位】")
    for no, name, act in gate(c):
        print(f"  卡在 {no} {name}")
        print(f"     → {act}")
    print()

    print("【二、旗手配置】")
    ok, miss = champion_check(c)
    if ok:
        print("  ✅ 旗手三件齐备，可以启动")
    else:
        print("  ❌ 旗手条件不全，先别启动：")
        for m in miss:
            print(f"     · {m}")
    print("  提示：旗手还需 明确的时间 / 能拍板的权限 / 每月一次向管理层汇报的固定会议")
    print()

    print("【三、环节打分（选最痛那条，不是最容易展示那条）】")
    print(f"  权重：人工小时 {W['hours']:.0%} / 重复度 {W['repeat']:.0%} / 出错成本 {W['err_cost']:.0%}")
    print(f"  {'环节':<16}{'月人工h':>8}{'重复':>6}{'出错成本':>10}{'得分':>8}")
    for s in score_steps(c["steps"]):
        print(f"  {s['name']:<16}{s['hours']:>8}{s['repeat']:>6}{s['err_cost']:>10}{s['score']:>8}")
    best = score_steps(c["steps"])[0]
    print(f"\n  ▶ 建议首选：{best['name']}（{best['hours']} h/月，月价值约 "
          f"{best['monthly_value']:,} 元）")
    print(f"  ▶ 90 天目标写法：把「{best['name']}」从 {best['hours']} 小时/月 "
          f"压到 {max(1, int(best['hours'] * 0.25))} 小时/月，数字可被财务验证")
    print()

    print("【四、下一步（顺序不能反）】")
    print("  1. 给旗手三样东西 → 2. 填四签名登记表 → 3. 排 90 天（6 周×每周一次）")
    print("  4. 第 30/60/90 天各做一次「重跑验收」（外人照文档独立跑）")


if __name__ == "__main__":
    main()
