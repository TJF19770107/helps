#!/usr/bin/env python3
"""
AI接单交付流水线 - 品类路由脚本
根据订单任务卡自动路由到最佳生成路径
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime


# 品类→路径路由表
ROUTE_TABLE = {
    "实拍照片": {"primary": "ImageGen", "cost": 5, "fallback": None, "fallback_cost": 0},
    "AI绘画": {"primary": "ImageGen", "cost": 5, "fallback": "Pillow", "fallback_cost": 0},
    "短视频": {"primary": "VideoGen", "cost": 75, "fallback": "zero-cost-video-render", "fallback_cost": 0},
    "文案": {"primary": "本地模板", "cost": 0, "fallback": None, "fallback_cost": 0},
    "设计图": {"primary": "ImageGen+后处理", "cost": 5, "fallback": "Pillow+FFmpeg", "fallback_cost": 0},
    "印章": {"primary": "ImageGen+后处理", "cost": 5, "fallback": "Pillow+FFmpeg", "fallback_cost": 0},
    "海报": {"primary": "ImageGen+叠字", "cost": 5, "fallback": "Pillow纯本地", "fallback_cost": 0},
}


def route_order(category: str, count: int, budget_credits: int, auto_fallback: bool = True) -> dict:
    """路由订单到最佳生成路径"""
    route = ROUTE_TABLE.get(category)
    if not route:
        return {"error": f"未知品类: {category}", "known": list(ROUTE_TABLE.keys())}

    total_primary = route["cost"] * count
    use_primary = total_primary <= budget_credits

    if not use_primary and route["fallback"] and auto_fallback:
        return {
            "category": category,
            "count": count,
            "chosen_path": route["fallback"],
            "path_cost": route["fallback_cost"] * count,
            "total_credits": route["fallback_cost"] * count,
            "reason": f"预算{budget_credits}不足首选{total_primary}，降级到{route['fallback']}",
            "quality_note": "降级路径，质量可能降低"
        }

    if not use_primary and not route["fallback"]:
        return {
            "category": category,
            "count": count,
            "chosen_path": "BLOCKED",
            "path_cost": 0,
            "total_credits": 0,
            "reason": f"预算{budget_credits}不足首选{total_primary}，且无降级路径",
            "action": "需用户追加积分或调整需求"
        }

    return {
        "category": category,
        "count": count,
        "chosen_path": route["primary"],
        "path_cost": route["cost"],
        "total_credits": total_primary,
        "budget_credits": budget_credits,
        "reason": "预算充足，走首选路径",
        "quality_note": "首选路径，质量最佳"
    }


def main():
    parser = argparse.ArgumentParser(description="AI接单交付路由")
    parser.add_argument("--category", required=True, help="品类（实拍照片/AI绘画/短视频/文案/设计图/印章/海报）")
    parser.add_argument("--count", type=int, default=1, help="数量")
    parser.add_argument("--budget", type=int, default=50, help="积分预算上限")
    parser.add_argument("--quote", type=float, default=0, help="报价金额（用于计算执行成本上限）")
    parser.add_argument("--cost-ratio", type=float, default=0.3, help="执行成本占报价比例（默认0.3）")
    parser.add_argument("--auto-fallback", action="store_true", default=True, help="自动降级")
    args = parser.parse_args()

    # 如果有报价，按比例计算预算
    if args.quote > 0:
        # 1积分≈0.5元换算（可调整）
        budget_from_quote = int(args.quote * args.cost_ratio / 0.5)
        budget = min(args.budget, budget_from_quote)
    else:
        budget = args.budget

    result = route_order(args.category, args.count, budget, args.auto_fallback)
    result["timestamp"] = datetime.now().isoformat()
    result["budget_used"] = budget

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    main()
