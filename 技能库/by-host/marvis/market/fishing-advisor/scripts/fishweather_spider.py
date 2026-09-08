#!/usr/bin/env python3
"""fishweather.cn 爬虫模块 - 精确提取所有页面数据"""

import json
import sys
import re
import argparse
import hashlib
import time
from pathlib import Path

try:
    from pypinyin import pinyin, Style
except ImportError:
    pinyin = None
    Style = None

CACHE_DIR = Path.home() / ".fishing_advisor_cache"
CACHE_TTL = 1800


def city_to_pinyin(city_name: str) -> str:
    city_name = city_name.strip()
    special = {"重庆":"chongqing","厦门":"xiamen","长沙":"changsha","长春":"changchun","东莞":"dongguan"}
    if city_name in special:
        return special[city_name]
    if pinyin and Style:
        return "".join([p[0] for p in pinyin(city_name, style=Style.NORMAL)])
    return city_name.lower()


def get_cache_path(city):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR / f"fw_{hashlib.md5(city.encode()).hexdigest()}.json"


def load_cache(city):
    p = get_cache_path(city)
    if p.exists() and time.time() - p.stat().st_mtime < CACHE_TTL:
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return None


def save_cache(city, data):
    get_cache_path(city).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def scrape_fishweather(city_pinyin: str, city_name: str = "") -> dict:
    """精确爬取 fishweather.cn 全部数据"""
    from playwright.sync_api import sync_playwright

    url = f"https://fishweather.cn/city/{city_pinyin}"
    data = {
        "city": city_name or city_pinyin,
        "city_pinyin": city_pinyin,
        "url": url,
        "scrape_time": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            viewport={"width": 1280, "height": 900},
        )
        try:
            page.goto(url, timeout=30000, wait_until="networkidle")
            page.wait_for_timeout(4000)
            body = page.inner_text("body")

            data["weather"] = _parse_weather(body)
            data["fishing_index"] = _parse_fishing_index(body)
            data["weekly_index"] = _parse_weekly_index(body)
            data["today_advice"] = _parse_today_advice(body)
            data["pressure_trend"] = _parse_pressure_trend(body)
            data["moon"] = _parse_moon(body)
            data["best_time"] = _parse_best_time(body)
            data["gear_advice"] = _parse_gear(body)
            data["fish_species"] = _parse_fish_species(body)
            data["equipment"] = _parse_equipment(body)
            data["nearby_spots"] = _parse_nearby(body)
            data["hourly_48h"] = _parse_hourly_table(body)
            data["water"] = _parse_water_do(body)

        except Exception as e:
            data["error"] = str(e)
        finally:
            browser.close()
    return data


def _parse_weather(t: str) -> dict:
    """天气详细资料区"""
    r = {}
    # 气温
    m = re.search(r"气温\s*\n\s*(\d+)°", t)
    if m: r["temp"] = int(m.group(1))
    m = re.search(r"体感\s*(\d+)°", t)
    if m: r["feels_like"] = int(m.group(1))
    m = re.search(r"今日\s*(\d+)°\s*/\s*(\d+)°", t)
    if m: r["temp_max"] = int(m.group(1)); r["temp_min"] = int(m.group(2))

    # 湿度
    m = re.search(r"湿度.*?\n\s*(\d+)%", t)
    if m: r["humidity"] = int(m.group(1))
    m = re.search(r"露点\s*\n\s*(\d+)°", t)
    if m: r["dew_point"] = int(m.group(1))

    # 气压
    m = re.search(r"气压\s*\n\s*(\d+)\s*\n\s*hPa\s*\n\s*(\S+)", t)
    if m: r["pressure"] = int(m.group(1)); r["pressure_eval"] = m.group(2)

    # 风
    m = re.search(r"风\s*\n\s*(\d+)\s*\n\s*km/h\s*\n\s*([\u4e00-\u9fa5]+)\s*·\s*(\d+)°", t)
    if m: r["wind_speed"] = int(m.group(1)); r["wind_dir"] = m.group(2); r["wind_deg"] = int(m.group(3))
    m = re.search(r"阵风\s*(\d+)\s*km/h\s*·\s*(\d+级\s*\S*)", t)
    if m: r["gust"] = int(m.group(1)); r["wind_level"] = m.group(2).strip()

    # 云量
    m = re.search(r"云量\s*\n\s*(\d+)%\s*\n\s*(\S+)", t)
    if m: r["cloud_cover"] = int(m.group(1)); r["cloud_desc"] = m.group(2)

    # 降雨
    m = re.search(r"降雨量\s*\n\s*([\d.]+)\s*\n\s*mm/h\s*\n\s*(\S+)", t)
    if m: r["precip"] = float(m.group(1)); r["precip_desc"] = m.group(2)

    # 能见度
    m = re.search(r"能见度\s*\n\s*(\d+)\s*\n\s*km\s*\n\s*(\S+)", t)
    if m: r["visibility"] = int(m.group(1)); r["visibility_desc"] = m.group(2)

    # UV
    m = re.search(r"紫外线\s*\n\s*(\d+)\s*\n\s*(\S+)", t)
    if m: r["uv_index"] = int(m.group(1)); r["uv_desc"] = m.group(2)

    # AQI
    m = re.search(r"AQI\s*\n\s*(\d+)\s*\n\s*(\S+)", t)
    if m: r["aqi"] = int(m.group(1)); r["aqi_level"] = m.group(2)

    # 日出日落
    m = re.search(r"日出\s*\n\s*(\d+:\d+)", t)
    if m: r["sunrise"] = m.group(1)
    m = re.search(r"日落\s*\n\s*(\d+:\d+)", t)
    if m: r["sunset"] = m.group(1)

    # 天气描述 - 搜索"天气\n多云\n..." 格式
    m = re.search(r"\n天气\s*\n\s*(晴|多云|阴|小雨|中雨|大雨|雷阵雨|雪|雾|霾)\s*\n\s*(.+?)(?:\n\n|\n惠州|\n\S+本周)", t, re.DOTALL)
    if m: r["condition"] = m.group(1); r["condition_fishing"] = m.group(2).strip()
    elif not r.get("condition"):
        # 兜底：从实时天气区提取
        for kw in ["晴","多云","阴","小雨","中雨","大雨","雷阵雨","雪","雾","霾"]:
            if f"\n{kw}\n" in t:
                r["condition"] = kw
                break

    return r


def _parse_fishing_index(t: str) -> dict:
    """钓鱼指数（今日最高 + 实时）"""
    r = {}
    # 今日最高
    m = re.search(r"今日最高钓鱼指数\s*\n\s*(\d+)\s*\n\s*(\S+)", t)
    if m: r["today_peak"] = int(m.group(1)); r["today_peak_rating"] = m.group(2)

    # 本周今天指数（第一个）
    m = re.search(r"今天\s*\n\s*\S+\s*\n\s*(\d+)\s*\n\s*(\S+)", t)
    if m: r["current"] = int(m.group(1)); r["rating"] = m.group(2)

    # 气压下降描述
    m = re.search(r"(气压(?:下降|上升|稳定)\s*[^\n]*)", t)
    if m: r["pressure_advice"] = m.group(1).strip()

    return r


def _parse_weekly_index(t: str) -> list:
    """本周钓鱼指数（7天）"""
    result = []
    # 格式: "今天\n周日\n65\n良好\n30° / 20°\n周一\n63\n..."
    block = re.search(r"本周钓鱼指数.*?\n(今天.*?)(?:\n今日建议|\n24小时)", t, re.DOTALL)
    if not block:
        return result

    txt = block.group(1)
    # 匹配每天: 周X\n数字\n评级\n温度范围
    days = re.findall(r"(今天|周[一二三四五六日])\s*\n\s*(?:(周[一二三四五六日])\s*\n\s*)?(\d{2,3})\s*\n\s*(\S+)\s*\n\s*(\d+°\s*/\s*\d+°)", txt)
    for d in days:
        day_label = d[1] if d[1] else d[0]
        result.append({
            "day": day_label,
            "index": int(d[2]),
            "rating": d[3],
            "temp_range": d[4].replace(" ", ""),
        })
    return result


def _parse_today_advice(t: str) -> str:
    """今日建议完整文本"""
    m = re.search(r"今日建议[：:\s]*(当前水温.*?)(?:\n\n|\n24小时)", t, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"今日建议[：:\s]*(.+?)(?:\n\n)", t)
    if m:
        return m.group(1).strip()
    return ""


def _parse_pressure_trend(t: str) -> dict:
    """24小时气压趋势"""
    r = {}
    m = re.search(r"24小时气压趋势\s*\n\s*(\d+)\s*\n\s*hPa\s*\n\s*([-\d]+)", t)
    if m: r["current"] = int(m.group(1)); r["change_24h"] = int(m.group(2))
    m = re.search(r"(气压(?:下降|上升|稳定)\s*[-+]?\d*\s*hPa[^\n]*)", t)
    if m: r["description"] = m.group(1).strip()
    return r


def _parse_moon(t: str) -> dict:
    """月相数据 - 直接从页面提取"""
    r = {}
    m = re.search(r"月相\s*\n\s*(\S+)\s*\n\s*垂钓\s*(\S+)\s*\n\s*([\d.]+%)", t)
    if m: r["name"] = m.group(1); r["fishing_eval"] = m.group(2); r["illumination"] = m.group(3)

    m = re.search(r"月龄\s*\n\s*([\d.]+)\s*天", t)
    if m: r["age"] = float(m.group(1))

    m = re.search(r"距满月\s*\n\s*(\d+)\s*天", t)
    if m: r["days_to_full"] = int(m.group(1))

    m = re.search(r"月相趋势\s*\n\s*(\S+)", t)
    if m: r["trend"] = m.group(1)

    m = re.search(r"月相评分\s*\n\s*(\d+)", t)
    if m: r["score"] = int(m.group(1))

    m = re.search(r"(距满月还有.*?活跃度最高)", t)
    if m: r["description"] = m.group(1).strip()

    return r


def _parse_best_time(t: str) -> str:
    m = re.search(r"最佳时段\s*\n\s*(\d+:\d+-\d+:\d+)", t)
    return m.group(1) if m else ""


def _parse_gear(t: str) -> dict:
    r = {}
    m = re.search(r"推荐钓位\s*\n\s*(\S+)\s*\n\s*(.+?)(?:\n\n|\n饵料)", t, re.DOTALL)
    if m: r["position"] = m.group(1); r["position_detail"] = m.group(2).strip()

    m = re.search(r"饵料选择\s*\n\s*(.+?)\s*\n\s*(.+?)(?:\n\n|\n线组)", t, re.DOTALL)
    if m: r["bait"] = m.group(1).strip(); r["bait_detail"] = m.group(2).strip()

    m = re.search(r"线组参考\s*\n\s*(.+?)\s*\n\s*(.+?)(?:\n\n|\n今日推荐)", t, re.DOTALL)
    if m: r["line_group"] = m.group(1).strip(); r["line_detail"] = m.group(2).strip()

    return r


def _parse_fish_species(t: str) -> list:
    """活跃鱼种表格"""
    result = []
    block = re.search(r"活跃鱼种\s*\n.*?基于气压.*?\n(.*?)(?:\n活跃度依据|$)", t, re.DOTALL)
    if not block:
        return result
    txt = block.group(1)
    # 格式: "鱼种名活跃度\n水层\n饵料" (名字和活跃度粘在一起)
    # 先按活跃度关键词切分
    fish_names = ["鲫鱼", "鲤鱼", "草鱼", "鲮鱼", "罗非", "鳊鱼", "鳜鱼", "翘嘴",
                   "黑鱼", "黄颡鱼", "鲢鳙", "鲢鱼", "鳙鱼", "鲈鱼", "青鱼", "鲶鱼", "白条"]
    rows = re.findall(
        r"(" + "|".join(fish_names) + r")(非常活跃|活跃|一般|不活跃|停口)\s*\n\s*([^\n]+)\s*\n\s*([^\n]+)", txt
    )
    for row in rows:
        result.append({
            "name": row[0],
            "activity": row[1],
            "depth": row[2].strip(),
            "bait": row[3].strip(),
            "source": "fishweather",
        })
    return result


def _parse_equipment(t: str) -> dict:
    """出钓装备详细信息"""
    r = {}
    # 鱼竿
    m = re.search(r"鱼竿\s*\n\s*首选\s*\n\s*(.+?)\s*\n\s*(.+?)(?:\n\s*备选|\n\s*线组)", t, re.DOTALL)
    if m: r["rod_primary"] = m.group(1).strip(); r["rod_primary_detail"] = m.group(2).strip()
    m = re.search(r"鱼竿.*?备选\s*\n\s*(.+?)\s*\n\s*(.+?)(?:\n\s*线组)", t, re.DOTALL)
    if m: r["rod_secondary"] = m.group(1).strip(); r["rod_secondary_detail"] = m.group(2).strip()

    # 浮漂
    m = re.search(r"浮漂\s*\n\s*首选\s*\n\s*(.+?)\s*\n\s*(.+?)(?:\n|$)", t)
    if m: r["float"] = m.group(1).strip(); r["float_detail"] = m.group(2).strip()

    return r


def _parse_nearby(t: str) -> list:
    """附近热门钓点"""
    result = []
    block = re.search(r"惠州附近热门钓点\s*\n\s*查看全部\s*\n(.*?)(?:\n钓友分享|\n$)", t, re.DOTALL)
    if not block:
        block = re.search(r"附近热门钓点\s*\n.*?\n(.*?)(?:\n钓友分享|\n$)", t, re.DOTALL)
    if not block:
        return result

    txt = block.group(1)
    # 格式: "类型\n距离\n名称\n评分\n鱼种...\n今日X人\n最佳:时段"
    spots = re.findall(
        r"(野钓|台钓|船钓|矶钓|路亚)\s*\n\s*([\d.]+km)\s*\n\s*(.+?)\s*\n\s*([\d.]+)\s*\n\s*(.*?)\s*\n\s*今日\s*(\d+)\s*人\s*\n\s*最佳:\s*(.+?)(?:\n|$)",
        txt
    )
    for s in spots:
        result.append({
            "type": s[0], "distance": s[1], "name": s[2],
            "rating": float(s[3]), "fish": s[4].strip(),
            "anglers": int(s[5]), "best_time": s[6].strip(),
        })
    return result


def _parse_hourly_table(t: str) -> dict:
    """48h逐时数据表 - 解析为结构化数据"""
    result = {"hours": [], "wind_speed": [], "wind_dir": [], "gust": [],
              "weather": [], "temp": [], "precip": [], "cloud": [],
              "pressure": [], "visibility": []}
    try:
        # 时间行
        m = re.search(r"时间\t(.+?)(?:\n|$)", t)
        if m:
            result["hours"] = [h.strip() for h in m.group(1).split("\t") if h.strip()]

        # 温度行
        m = re.search(r"温度°C\t(.+?)(?:\n|$)", t)
        if m:
            result["temp"] = [int(x) for x in m.group(1).split("\t") if x.strip()]

        # 气压行
        m = re.search(r"气压hPa\t(.+?)(?:\n|$)", t)
        if m:
            result["pressure"] = [int(x) for x in m.group(1).split("\t") if x.strip()]

        # 云量行
        m = re.search(r"云量%\t(.+?)(?:\n|$)", t)
        if m:
            result["cloud"] = [int(x) for x in m.group(1).split("\t") if x.strip()]

        # 能见度行
        m = re.search(r"能见度km\t(.+?)(?:\n|$)", t)
        if m:
            result["visibility"] = [int(x) for x in m.group(1).split("\t") if x.strip()]

        # 天气行 (更复杂，需要处理)
        m = re.search(r"天气\t(.+?)(?:\n温度)", t, re.DOTALL)
        if m:
            items = [x.strip() for x in m.group(1).split("\t") if x.strip()]
            # 过滤出天气名称
            weathers = [w for w in items if w in ("晴","多云","阴","小雨","中雨","大雨","雷阵雨","雪","雾")]
            result["weather"] = weathers

    except Exception:
        pass
    return result


def _parse_water_do(t: str) -> dict:
    """从今日建议文本中提取水温和溶氧"""
    r = {"water_temp": None, "water_temp_eval": "", "do": None, "do_eval": ""}
    # "当前水温24.4°C，高于理想区间"
    m = re.search(r"水温([\d.]+)\s*°?\s*C?\s*[，,]\s*(.+?)(?:[，,]|$)", t)
    if m:
        r["water_temp"] = float(m.group(1))
        r["water_temp_eval"] = m.group(2).strip()
    # "溶氧水平5.6mg/L，中等偏低"
    m = re.search(r"溶氧[水平量]*([\d.]+)\s*mg/?[Ll]\s*[，,]\s*(.+?)(?:[，,]|$)", t)
    if m:
        r["do"] = float(m.group(1))
        r["do_eval"] = m.group(2).strip()
    return r


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", required=True)
    parser.add_argument("--no-cache", action="store_true")
    args = parser.parse_args()
    city = args.city.strip()
    if not args.no_cache:
        cached = load_cache(city)
        if cached:
            print(json.dumps(cached, ensure_ascii=False, indent=2))
            return
    city_py = city_to_pinyin(city)
    print(f"[INFO] 爬取 fishweather.cn/city/{city_py} ...", file=sys.stderr)
    data = scrape_fishweather(city_py, city)
    save_cache(city, data)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
