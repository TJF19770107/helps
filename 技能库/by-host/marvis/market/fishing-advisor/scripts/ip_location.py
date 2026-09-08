#!/usr/bin/env python3
"""IP定位模块 - 通过公网IP获取用户所在城市"""

import json
import urllib.request
import sys


def get_location_by_ip():
    """通过多个免费IP定位API获取城市信息"""
    apis = [
        {
            "url": "https://ipapi.co/json/",
            "parser": lambda d: {
                "city": d.get("city", ""),
                "province": d.get("region", ""),
                "country": d.get("country_name", ""),
                "lat": d.get("latitude"),
                "lon": d.get("longitude"),
                "ip": d.get("ip", ""),
            },
        },
        {
            "url": "https://ip-api.com/json/?lang=zh-CN",
            "parser": lambda d: {
                "city": d.get("city", ""),
                "province": d.get("regionName", ""),
                "country": d.get("country", ""),
                "lat": d.get("lat"),
                "lon": d.get("lon"),
                "ip": d.get("query", ""),
            },
        },
        {
            "url": "https://myip.ipip.net/json",
            "parser": lambda d: {
                "city": d.get("data", {}).get("location", ["", "", "", ""])[2] if isinstance(d.get("data", {}).get("location"), list) else "",
                "province": d.get("data", {}).get("location", ["", "", ""])[1] if isinstance(d.get("data", {}).get("location"), list) else "",
                "country": d.get("data", {}).get("location", [""])[0] if isinstance(d.get("data", {}).get("location"), list) else "",
                "lat": None,
                "lon": None,
                "ip": d.get("data", {}).get("ip", ""),
            },
        },
    ]

    for api in apis:
        try:
            req = urllib.request.Request(
                api["url"],
                headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                result = api["parser"](data)
                if result["city"]:
                    return result
        except Exception:
            continue

    return None


def main():
    result = get_location_by_ip()
    if result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"error": "无法通过IP定位城市，请手动指定 --city 参数"}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
