#!/usr/bin/env python3
"""三要素变化分析模块 - 溶氧/水温/气压日内趋势（平滑曲线版）"""

import math
import time
from do_calculator import benson_krause_do_saturation


def analyze_three_elements(fishweather_data: dict) -> list:
    """基于 fishweather 48h逐时数据 + 实测值分析三要素"""
    results = []

    # 获取实测基准值
    water = fishweather_data.get("water", {})
    base_wt = water.get("water_temp")
    base_do = water.get("do")
    weather = fishweather_data.get("weather", {})
    base_temp = weather.get("temp") or 25

    # 获取48h逐时数据
    hourly = fishweather_data.get("hourly_48h", {})
    h_temps = hourly.get("temp", [])
    h_pressures = hourly.get("pressure", [])
    h_clouds = hourly.get("cloud", [])

    # 当前小时
    cur_hour = time.localtime().tm_hour

    for hour in range(24):
        # === 1. 气压：优先使用48h数据 ===
        if h_pressures and hour < len(h_pressures):
            pressure = float(h_pressures[hour])
        else:
            # 用平滑日变化模型
            base_p = weather.get("pressure") or 1013
            pressure = base_p + 1.5 * math.cos((hour - 10) * math.pi / 6)

        # === 2. 气温：优先使用48h数据 ===
        if h_temps and hour < len(h_temps):
            air_temp = float(h_temps[hour])
        else:
            air_temp = base_temp + 4.0 * math.sin((hour - 6) * math.pi / 12) - 2.0

        # === 3. 水温：基于实测值+平滑日变化 ===
        if base_wt:
            # 水温日变化幅度约 ±2°C，用正弦平滑过渡
            # 以14:00为基准（爬取时间大约在白天）
            wt_offset = 2.0 * math.sin((hour - 6) * math.pi / 12)
            wt_offset_at_ref = 2.0 * math.sin((14 - 6) * math.pi / 12)
            water_temp = base_wt + wt_offset - wt_offset_at_ref
        else:
            water_temp = air_temp - 3.0

        # === 4. 溶氧：平滑计算 ===
        cloud = h_clouds[hour] if h_clouds and hour < len(h_clouds) else 50
        do_sat = benson_krause_do_saturation(water_temp, pressure)

        # 平滑的饱和百分比曲线（避免骤变）
        # 基于时间的正弦变化：清晨最低(~50%)，午后最高(~75%)
        base_pct = 0.625  # 中间值
        amplitude = 0.125  # ±12.5%
        # 用正弦模拟：6点最低，14点最高
        time_factor = math.sin((hour - 6) * math.pi / 12) if 0 <= hour <= 24 else 0
        # 云量影响：云量越大，光合作用越弱
        cloud_factor = 1.0 - (cloud / 100.0) * 0.15
        do_pct = (base_pct + amplitude * time_factor) * cloud_factor

        do_value = do_sat * do_pct

        # 如果有实测值，在当前时间附近锚定到实测值，平滑过渡
        if base_do and abs(hour - cur_hour) <= 1:
            do_value = base_do
        elif base_do:
            # 距离当前时间越远，越依赖模型；越近，越接近实测值
            dist = min(abs(hour - cur_hour), 24 - abs(hour - cur_hour))
            # 6小时内做加权混合
            if dist <= 6:
                weight = 1.0 - dist / 6.0
                do_value = do_value * (1 - weight) + base_do * weight

        # === 5. 变化趋势 ===
        do_trend = ""
        temp_trend = ""
        press_trend = ""
        if len(results) >= 3:
            prev = results[-3]
            do_trend = _trend(do_value - prev["do"], 0.3, 0.8)
            temp_trend = _trend(water_temp - prev["water_temp"], 0.5, 1.5)
            press_trend = _trend(pressure - prev["pressure"], 0.5, 2.0)

        overall = _judge(do_value, water_temp, pressure, do_trend, press_trend)

        results.append({
            "hour": hour,
            "water_temp": round(water_temp, 1),
            "do": round(do_value, 2),
            "pressure": round(pressure, 1),
            "do_trend": do_trend,
            "temp_trend": temp_trend,
            "pressure_trend": press_trend,
            "overall": overall["label"],
            "stars": overall["stars"],
            "color": overall["color"],
        })

    return results


def _trend(diff, small, big):
    if diff > big: return "↑↑急升"
    elif diff > small: return "↑上升"
    elif diff > -small: return "→稳定"
    elif diff > -big: return "↓下降"
    else: return "↓↓急降"


def _judge(do_v, wt, pr, do_tr, pr_tr):
    s = 0
    if do_v >= 7: s += 3
    elif do_v >= 6: s += 2
    elif do_v >= 5: s += 1
    elif do_v < 4: s -= 2

    if 15 <= wt <= 25: s += 2
    elif 10 <= wt <= 30: s += 1
    else: s -= 1

    if pr >= 1015: s += 2
    elif pr >= 1005: s += 1
    else: s -= 1

    if "上升" in do_tr: s += 1
    if "下降" in do_tr: s -= 1
    if "上升" in pr_tr: s += 1
    if "急降" in pr_tr: s -= 1

    if s >= 6: return {"label": "黄金窗口", "stars": "★★★★★", "color": "#4ade80"}
    elif s >= 4: return {"label": "良好窗口", "stars": "★★★★", "color": "#a3e635"}
    elif s >= 2: return {"label": "普通", "stars": "★★★", "color": "#fbbf24"}
    elif s >= 0: return {"label": "较差", "stars": "★★", "color": "#fb923c"}
    else: return {"label": "极差", "stars": "★", "color": "#f87171"}
