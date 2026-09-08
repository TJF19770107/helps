#!/usr/bin/env python3
"""
钓鱼天气顾问 - 主入口
用法:
    python3 fishing_main.py --city "惠州"
    python3 fishing_main.py                # 自动IP定位
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

# 将 scripts 目录加入路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))


def ensure_dependencies():
    """检查并安装依赖"""
    missing = []
    try:
        import pypinyin
    except ImportError:
        missing.append("pypinyin")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        missing.append("playwright")

    if missing:
        print(f"[INFO] 正在安装缺失依赖: {', '.join(missing)}", file=sys.stderr)
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing, "-q"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if "playwright" in missing:
            print("[INFO] 正在安装 Playwright Chromium 浏览器...", file=sys.stderr)
            subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def get_city(args_city: str = None) -> str:
    """获取城市名：优先参数 > IP定位"""
    if args_city:
        return args_city.strip()

    print("[INFO] 未指定城市，正在通过IP定位...", file=sys.stderr)
    from ip_location import get_location_by_ip
    loc = get_location_by_ip()
    if loc and loc.get("city"):
        city = loc["city"]
        print(f"[INFO] IP定位城市: {city} ({loc.get('province', '')})", file=sys.stderr)
        return city
    else:
        print("[ERROR] IP定位失败，请使用 --city 参数指定城市", file=sys.stderr)
        sys.exit(1)


def format_text_report(data: dict, three_elements: list) -> str:
    """生成文字摘要报告"""
    lines = []
    city = data.get("city", "未知")
    fi = data.get("fishing_index", {})
    weather = data.get("weather", {})
    water = data.get("water", {})
    pt = data.get("pressure_trend", {})
    best_time = data.get("best_time", "")
    moon = data.get("moon", {})
    gear = data.get("gear_advice", {})
    fish_species = data.get("fish_species", [])
    weekly = data.get("weekly_index", [])
    today_advice = data.get("today_advice", "")

    lines.append(f"# 🎣 {city} 钓鱼天气报告")
    lines.append(f"📅 {time.strftime('%Y年%m月%d日 %H:%M')}")
    lines.append("")

    # 钓鱼指数
    current = fi.get("current") or "—"
    rating = fi.get("rating", "")
    lines.append(f"## 📊 今日钓鱼指数: {current}分 {rating}")
    if fi.get("today_peak"):
        lines.append(f"- 今日最高指数: {fi['today_peak']}分 {fi.get('today_peak_rating','')}")
    if best_time:
        lines.append(f"- ⚡ **黄金垂钓时段: {best_time}**")
    lines.append("")

    # 关键数据
    lines.append("## 🌡️ 关键数据")
    if weather.get("condition"):
        lines.append(f"- 天气: {weather['condition']}  气温: {weather.get('temp', '—')}°C (体感{weather.get('feels_like','')}°C)")
    if water.get("water_temp"):
        lines.append(f"- 水温: {water['water_temp']}°C {water.get('water_temp_eval', '')}")
    if water.get("do"):
        lines.append(f"- 溶氧: {water['do']}mg/L {water.get('do_eval', '')}")
    if weather.get("pressure"):
        lines.append(f"- 气压: {weather['pressure']}hPa {weather.get('pressure_eval','')} (24h变化: {pt.get('change_24h','')}hPa)")
    if moon.get("name"):
        lines.append(f"- 月相: {moon['name']} 评分{moon.get('score', '—')} 照明{moon.get('illumination','')}")
    lines.append("")

    # 今日建议
    if today_advice:
        lines.append(f"## 📝 今日建议")
        lines.append(today_advice)
        lines.append("")

    # 三要素趋势
    lines.append("## 📈 三要素变化趋势（每3小时）")
    lines.append("| 时间 | 水温(°C) | 溶氧(mg/L) | 气压(hPa) | 鱼口 |")
    lines.append("|------|---------|-----------|----------|------|")
    for r in three_elements:
        if r["hour"] % 3 == 0:
            lines.append(f"| {r['hour']:02d}:00 | {r['water_temp']} | {r['do']} | {r['pressure']} | {r['overall']} {r['stars']} |")
    lines.append("")

    # 本周钓鱼指数
    if weekly:
        lines.append("## 📅 本周钓鱼指数")
        for d in weekly:
            lines.append(f"- {d['day']}: {d['index']}分 {d['rating']} ({d.get('temp_range','')})")
        lines.append("")

    # 鱼种推荐
    if fish_species:
        lines.append("## 🐟 活跃鱼种")
        for i, f in enumerate(fish_species[:8]):
            medals = ["🥇", "🥈", "🥉"]
            m = medals[i] if i < 3 else f"  {i+1}."
            depth = f.get('depth', '')
            bait = f.get('bait', '')
            extra = f" | {depth} | {bait}" if depth else ""
            lines.append(f"{m} {f['name']} {f.get('activity', '')}{extra}")
        lines.append("")

    # 出钓建议
    if any(gear.values()):
        lines.append("## 🎣 出钓建议")
        if gear.get("position"):
            lines.append(f"- 推荐钓位: {gear['position']} — {gear.get('position_detail','')}")
        if gear.get("bait"):
            lines.append(f"- 饵料选择: {gear['bait']} — {gear.get('bait_detail','')}")
        if gear.get("line_group"):
            lines.append(f"- 线组参考: {gear['line_group']} — {gear.get('line_detail','')}")
        lines.append("")

    return "\n".join(lines)


def search_fish_species(city: str) -> list:
    """网络搜索当地鱼种推荐"""
    import urllib.request
    import urllib.parse
    import re
    month = time.strftime("%m").lstrip("0")

    fish_names_all = [
        "鲫鱼", "鲤鱼", "草鱼", "鲮鱼", "罗非鱼", "罗非", "鳊鱼", "鳜鱼",
        "翘嘴", "黑鱼", "黄颡鱼", "鲢鳙", "鲢鱼", "鳙鱼", "鲈鱼", "青鱼",
        "鲶鱼", "白条", "马口", "鳗鱼", "鮰鱼", "乌鱼", "花鲢", "白鲢",
        "土鲮", "麦鲮", "泰鲮", "大头鱼", "鲳鱼", "黑鲷", "石斑", "海鲈",
    ]

    queries = [
        f"{city} 钓鱼 鱼种 推荐 {month}月",
        f"{city} 钓什么鱼",
    ]

    search_apis = [
        # Bing
        lambda q: (
            f"https://www.bing.com/search?q={urllib.parse.quote(q)}&count=5",
            {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        ),
        # 搜狗
        lambda q: (
            f"https://www.sogou.com/web?query={urllib.parse.quote(q)}&num=5",
            {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        ),
        # 百度
        lambda q: (
            f"https://www.baidu.com/s?wd={urllib.parse.quote(q)}&rn=5",
            {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        ),
    ]

    all_html = ""
    for query in queries:
        for api_fn in search_apis:
            try:
                url, headers = api_fn(query)
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=8) as resp:
                    html = resp.read().decode("utf-8", errors="ignore")
                    if len(html) > 1000:
                        all_html += html
                        print(f"[INFO] 搜索成功: {query[:20]}...", file=sys.stderr)
                        break  # 一个搜索引擎成功即可
            except Exception as e:
                continue

    if not all_html:
        print(f"[WARN] 所有搜索引擎都失败，使用地域鱼种兜底", file=sys.stderr)
        return _get_regional_fish(city)

    found = []
    for name in fish_names_all:
        count = all_html.count(name)
        if count > 0:
            found.append({"name": name, "mentions": count})
    found.sort(key=lambda x: x["mentions"], reverse=True)

    result = []
    seen = set()
    for f in found:
        base = f["name"]
        # 归一化
        alias_map = {"土鲮": "鲮鱼", "麦鲮": "鲮鱼", "泰鲮": "鲮鱼",
                     "花鲢": "鲢鳙", "白鲢": "鲢鳙", "乌鱼": "黑鱼",
                     "大头鱼": "鳙鱼", "罗非": "罗非鱼"}
        base = alias_map.get(base, base)
        if base not in seen:
            seen.add(base)
            activity = "非常活跃" if f["mentions"] >= 5 else "活跃" if f["mentions"] >= 2 else "一般"
            result.append({"name": base, "activity": activity, "source": "search"})

    # 如果搜索结果太少，补充地域鱼种
    if len(result) < 3:
        regional = _get_regional_fish(city)
        for rf in regional:
            if rf["name"] not in seen:
                seen.add(rf["name"])
                result.append(rf)

    print(f"[INFO] 搜索到 {len(result)} 种鱼: {[f['name'] for f in result]}", file=sys.stderr)
    return result


def _get_regional_fish(city: str) -> list:
    """基于地域的兜底鱼种推荐"""
    # 华南地区（广东、广西、海南、福建南部）
    south_cities = ["惠州", "深圳", "广州", "东莞", "佛山", "珠海", "中山", "江门",
                    "肇庆", "清远", "韶关", "河源", "梅州", "潮州", "汕头", "揭阳",
                    "湛江", "茂名", "阳江", "云浮", "博罗", "南宁", "桂林", "柳州",
                    "海口", "三亚", "厦门", "福州", "泉州", "漳州"]
    # 长三角
    yangtze_cities = ["上海", "杭州", "苏州", "南京", "无锡", "常州", "宁波", "绍兴",
                      "嘉兴", "湖州", "合肥", "芜湖", "马鞍山", "南通", "扬州"]
    # 北方
    north_cities = ["北京", "天津", "石家庄", "济南", "青岛", "郑州", "太原", "沈阳",
                    "大连", "长春", "哈尔滨"]

    month = int(time.strftime("%m"))

    if any(c in city for c in south_cities) or "广东" in city or "广西" in city:
        base = [
            {"name": "鲮鱼", "activity": "非常活跃" if 4 <= month <= 10 else "活跃"},
            {"name": "罗非鱼", "activity": "非常活跃" if 5 <= month <= 10 else "一般"},
            {"name": "鲫鱼", "activity": "活跃"},
            {"name": "鲤鱼", "activity": "活跃"},
            {"name": "草鱼", "activity": "活跃" if 4 <= month <= 10 else "一般"},
            {"name": "鲢鳙", "activity": "活跃" if 5 <= month <= 9 else "一般"},
            {"name": "黄颡鱼", "activity": "活跃" if 5 <= month <= 10 else "一般"},
            {"name": "翘嘴", "activity": "活跃" if 5 <= month <= 10 else "一般"},
        ]
    elif any(c in city for c in yangtze_cities):
        base = [
            {"name": "鲫鱼", "activity": "非常活跃"},
            {"name": "鲤鱼", "activity": "活跃"},
            {"name": "草鱼", "activity": "活跃" if 4 <= month <= 10 else "一般"},
            {"name": "鳊鱼", "activity": "活跃" if 4 <= month <= 10 else "一般"},
            {"name": "翘嘴", "activity": "活跃" if 5 <= month <= 10 else "一般"},
            {"name": "黄颡鱼", "activity": "活跃" if 5 <= month <= 10 else "一般"},
        ]
    else:
        base = [
            {"name": "鲫鱼", "activity": "活跃"},
            {"name": "鲤鱼", "activity": "活跃"},
            {"name": "草鱼", "activity": "活跃" if 4 <= month <= 10 else "一般"},
            {"name": "鲢鳙", "activity": "活跃" if 5 <= month <= 9 else "一般"},
            {"name": "翘嘴", "activity": "活跃" if 5 <= month <= 10 else "一般"},
        ]

    for f in base:
        f["source"] = "regional"
    return base


def merge_fish_species(fishweather_fish: list, search_fish: list) -> list:
    """合并 fishweather 活跃鱼种 + 网络搜索鱼种"""
    merged = {}
    # fishweather 优先
    for f in fishweather_fish:
        name = f["name"]
        merged[name] = {
            "name": name,
            "activity": f.get("activity", ""),
            "source": "fishweather",
        }
    # 搜索结果补充
    for f in search_fish:
        name = f["name"]
        if name in merged:
            # 已有则提升活跃度
            if "活跃" in f.get("activity", "") and not merged[name]["activity"]:
                merged[name]["activity"] = f["activity"]
            merged[name]["source"] = "both"
        else:
            merged[name] = f

    # 排序：有活跃度描述的在前
    result = sorted(merged.values(), key=lambda x: (
        "非常活跃" in x.get("activity", ""),
        "活跃" in x.get("activity", ""),
        x.get("source") == "both",
        x.get("source") == "fishweather",
    ), reverse=True)
    return result


def compute_moon_phase():
    """根据当前日期计算月相信息"""
    import math
    from datetime import datetime
    now = datetime.now()

    # 简化月相计算（基于已知新月日期 2000-01-06 18:14 UTC）
    ref_new_moon = datetime(2000, 1, 6, 18, 14)
    days_since = (now - ref_new_moon).total_seconds() / 86400
    synodic_month = 29.53058867
    moon_age = days_since % synodic_month

    # 照明度
    illumination = round((1 - math.cos(2 * math.pi * moon_age / synodic_month)) / 2 * 100, 1)

    # 月相名称
    if moon_age < 1.85:
        name = "新月"
    elif moon_age < 7.38:
        name = "蛾眉月"
    elif moon_age < 9.23:
        name = "上弦月"
    elif moon_age < 14.77:
        name = "盈凸月"
    elif moon_age < 16.61:
        name = "满月"
    elif moon_age < 22.15:
        name = "亏凸月"
    elif moon_age < 24.0:
        name = "下弦月"
    else:
        name = "残月"

    days_to_full = round(abs(synodic_month / 2 - moon_age), 1)
    if moon_age > synodic_month / 2:
        days_to_full = round(synodic_month - moon_age + synodic_month / 2, 1)

    # 月相钓鱼评分（新月/满月前后最好）
    phase_angle = abs(moon_age - synodic_month / 2) / (synodic_month / 2)
    score = int(50 + 50 * (1 - abs(2 * phase_angle - 1)))
    # 新月和满月前后2天加分
    if moon_age < 2 or abs(moon_age - synodic_month/2) < 2 or moon_age > synodic_month - 2:
        score = min(100, score + 15)

    return {
        "name": name,
        "age": round(moon_age, 1),
        "illumination": f"{illumination}%",
        "score": score,
        "days_to_full": days_to_full,
    }


def main():
    parser = argparse.ArgumentParser(description="🎣 钓鱼天气顾问")
    parser.add_argument("--city", help="城市名（中文），不指定则自动IP定位")
    parser.add_argument("--no-cache", action="store_true", help="禁用缓存，强制重新爬取")
    parser.add_argument("--output-dir", default=None, help="HTML输出目录")
    parser.add_argument("--json-only", action="store_true", help="仅输出JSON数据")
    args = parser.parse_args()

    # 0. 检查依赖
    ensure_dependencies()

    # 1. 获取城市
    city = get_city(args.city)

    # 2. 爬取 fishweather 数据
    from fishweather_spider import scrape_fishweather, city_to_pinyin, load_cache, save_cache

    if not args.no_cache:
        cached = load_cache(city)
        if cached:
            print(f"[INFO] 使用缓存数据（30分钟内）", file=sys.stderr)
            data = cached
        else:
            city_py = city_to_pinyin(city)
            print(f"[INFO] 爬取 fishweather.cn/city/{city_py} ...", file=sys.stderr)
            data = scrape_fishweather(city_py, city)
            save_cache(city, data)
    else:
        city_py = city_to_pinyin(city)
        print(f"[INFO] 爬取 fishweather.cn/city/{city_py} ...", file=sys.stderr)
        data = scrape_fishweather(city_py, city)
        save_cache(city, data)

    if data.get("error"):
        print(f"[WARN] 爬取过程中有警告: {data['error']}", file=sys.stderr)

    # 2.5 网络搜索鱼种 + 合并
    search_fish = search_fish_species(city)
    fw_fish = data.get("fish_species", [])
    data["fish_species"] = merge_fish_species(fw_fish, search_fish)

    # 2.6 月相：优先使用爬取数据，缺失时用计算兜底
    moon = data.get("moon", {})
    if not moon.get("name") or not moon.get("score"):
        computed = compute_moon_phase()
        for k, v in computed.items():
            if not moon.get(k):
                moon[k] = v
        data["moon"] = moon

    # 3. 三要素分析
    from three_elements import analyze_three_elements
    te_results = analyze_three_elements(data)

    # 4. JSON模式
    if args.json_only:
        data["three_elements"] = te_results
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    # 5. 生成文字报告
    text_report = format_text_report(data, te_results)
    print(text_report)

    # 6. 生成HTML
    from generate_html import generate_html
    output_dir = args.output_dir or str(Path.home() / "fishing_advisor_output")
    html_path = generate_html(data, te_results, output_dir)
    print(f"\n---\n📄 HTML交互报告已生成: {html_path}")
    print("💡 请在浏览器中打开查看完整可视化报告")


if __name__ == "__main__":
    main()
