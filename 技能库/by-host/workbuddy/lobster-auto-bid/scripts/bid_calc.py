#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lobster-auto-bid · 接单自动报价计算器 v1.1（2026-08-22 校准）
零成本本地逻辑：纯算术，不联网、不调 API。

用法：
  python bid_calc.py --category 印章 --count 1
                     --urgency 1.0 --margin 0.6 --free_rev 2
输出 JSON：{cost, quote, margin_pct, package, urgent_quote, terms}
"""
import argparse
import json
import sys

# 品类默认基准（工时h, 时薪¥, 复杂度系数）
# v1.1 校准（2026-08-22）：用 2 个真订单反推（印章¥50/背景图¥50张），
# 从"人工时薪"改为"AI 全自动产能"——简单图 15 分钟出稿，毛利 60-70%。
BASE = {
    "印章":   (0.25, 50, 1.0),
    "logo":   (0.25, 50, 1.0),
    "海报":   (0.75, 60, 1.2),
    "背景图": (0.25, 50, 1.0),
    "ui":     (3.0, 80, 1.5),
    "网页":   (3.0, 80, 1.5),
    "短视频": (2.0, 70, 1.4),
    "文案":   (0.5, 50, 1.0),
}

URGENCY_LABEL = {1.5: "急单(≤1天)", 1.2: "加急(≤3天)", 1.0: "常规(>3天)"}


def calc(args):
    cat = args.category
    if cat in BASE:
        d_hours, d_rate, d_cx = BASE[cat]
    else:
        d_hours, d_rate, d_cx = (1.0, 60, 1.2)  # 未知品类默认

    hours = args.hours if args.hours is not None else d_hours * args.count
    rate = args.rate if args.rate is not None else d_rate
    cx = args.complexity if args.complexity is not None else d_cx
    urgency = args.urgency if args.urgency is not None else 1.0

    # 成本：人工 + 素材(人工的15%) + 平台预留(报价的10%，倒推)
    labor = hours * rate * cx
    material = labor * 0.15
    gross_cost = labor + material
    # 报价 = 成本 / (1 - 平台预留% - 利润率%)  -> 保证毛利与预留
    platform_reserve = 0.10
    margin = args.margin
    denom = 1.0 - platform_reserve - margin
    if denom <= 0:
        denom = 0.2
    quote = gross_cost / denom
    margin_pct = round((quote - gross_cost) / quote * 100, 1)

    # 套餐：单张裸价 × 数量 × 折扣(数量越多越低)
    discount = max(0.7, 1.0 - 0.05 * (args.count - 1))
    single = quote / args.count if args.count else quote
    package = round(single * args.count * discount, 2)

    urgent_quote = round(quote * urgency, 2)

    prepay = round(quote * 0.5, 2)
    terms = {
        "prepay_ratio": 0.5,
        "prepay_amount": prepay,
        "free_revisions": args.free_rev,
        "extra_rev_cost": round(single * 0.3, 2),
        "urgency_label": URGENCY_LABEL.get(urgency, "自定义"),
    }

    return {
        "category": cat,
        "count": args.count,
        "cost_breakdown": {
            "labor_hours": round(hours, 2),
            "labor_cost": round(labor, 2),
            "material_cost": round(material, 2),
            "gross_cost": round(gross_cost, 2),
        },
        "quote": round(quote, 2),
        "margin_pct": margin_pct,
        "package_price": package,
        "urgent_quote": urgent_quote,
        "terms": terms,
        "zero_cost": True,
    }


def main():
    p = argparse.ArgumentParser(description="接单自动报价计算器")
    p.add_argument("--category", required=True, help="品类: 印章/logo/海报/背景图/ui/网页/短视频/文案")
    p.add_argument("--count", type=int, default=1, help="数量")
    p.add_argument("--hours", type=float, default=None, help="总工时(h)，缺省按基准×数量")
    p.add_argument("--rate", type=float, default=None, help="时薪(¥)，缺省按基准")
    p.add_argument("--complexity", type=float, default=None, help="复杂度系数")
    p.add_argument("--urgency", type=float, default=1.0, help="交期系数: 1.5急/1.2加急/1.0常规")
    p.add_argument("--margin", type=float, default=0.6, help="目标利润率(默认0.6)")
    p.add_argument("--free_rev", type=int, default=2, help="含免费改稿次数")
    args = p.parse_args()
    print(json.dumps(calc(args), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
