#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
限免游戏查询脚本（Skill 专用）
查询 Steam + Epic 当前限免/即将限免游戏，输出纯文本结果到 stdout
"""

import sys
import io
import argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import requests
from datetime import datetime
import re


# ============================================================
# Steam 相关函数
# ============================================================

def search_steam_appid(game_name):
    """通过游戏名搜索 Steam AppID，多结果时优先精确匹配"""
    try:
        clean_name = game_name.replace(' (Steam) Giveaway', '').replace(' Giveaway', '').strip()
        url = "https://store.steampowered.com/api/storesearch"
        params = {'term': clean_name, 'cc': 'cn', 'l': 'schinese'}
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        items = data.get('items', [])
        if not items:
            return None

        # 优先精确匹配（忽略大小写）
        target = clean_name.lower()
        for item in items:
            if item.get('name', '').lower() == target:
                return item.get('id')

        # 无精确匹配，退回第一个结果
        return items[0].get('id')
    except Exception as e:
        print(f"  搜索 Steam AppID 失败: {e}", file=sys.stderr)
        return None


def get_steam_game_details(appid):
    """获取 Steam 游戏详情（是否永久免费、语言支持、价格）"""
    try:
        url = "https://store.steampowered.com/api/appdetails"
        params = {'appids': str(appid), 'cc': 'cn', 'l': 'schinese'}
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        app_data = data.get(str(appid), {})
        if not app_data.get('success'):
            return None
        game_data = app_data.get('data', {})
        languages = game_data.get('supported_languages', '')
        return {
            'is_free': game_data.get('is_free', False),
            'has_chinese': '简体中文' in languages or 'Simplified Chinese' in languages,
            'price_overview': game_data.get('price_overview'),
        }
    except Exception as e:
        print(f"  获取 Steam 游戏详情失败: {e}", file=sys.stderr)
        return None


def get_steam_promo_time(appid):
    """从 Steam 商店网页提取促销截止时间"""
    try:
        url = f"https://store.steampowered.com/app/{appid}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(url, headers=headers, timeout=15)
        html = resp.text

        end_time = None
        start_time = None

        # 方案1: data-countdown-date 时间戳
        countdown_match = re.search(r'data-countdown-date="(\d+)"', html)
        if countdown_match:
            timestamp = int(countdown_match.group(1))
            end_dt = datetime.fromtimestamp(timestamp)
            end_time = end_dt.strftime('%m月%d日 %H:%M')

        # 方案2: "Free to keep when you get it before ..." 文字
        if not end_time:
            promo_text_match = re.search(
                r'Free to keep when you get it before\s+(.*?)\.',
                html, re.IGNORECASE | re.DOTALL
            )
            if promo_text_match:
                time_str = promo_text_match.group(1).strip()
                end_time = parse_steam_promo_time(time_str)

        # 方案3: discount_end_rtime
        if not end_time:
            rtime_match = re.search(r'"discount_end_rtime"\s*:\s*(\d+)', html)
            if rtime_match:
                timestamp = int(rtime_match.group(1))
                if timestamp > 0:
                    end_dt = datetime.fromtimestamp(timestamp)
                    end_time = end_dt.strftime('%m月%d日 %H:%M')

        return {'start_time': start_time, 'end_time': end_time}
    except Exception as e:
        print(f"    获取促销时间失败: {e}", file=sys.stderr)
        return {'start_time': None, 'end_time': None}


def parse_steam_promo_time(time_str):
    """解析 Steam 促销时间字符串，如 'Apr 6 @ 10:00am'"""
    try:
        time_str = re.sub(r'\s+', ' ', time_str.strip())
        match = re.match(r'(\w+)\s+(\d+)\s*@\s*(\d+):(\d+)(am|pm)', time_str, re.IGNORECASE)
        if match:
            month_str, day, hour, minute, ampm = match.groups()
            months = {
                'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
                'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
            }
            month = months.get(month_str.lower())
            if not month:
                return None
            hour = int(hour)
            minute = int(minute)
            if ampm.lower() == 'pm' and hour != 12:
                hour += 12
            elif ampm.lower() == 'am' and hour == 12:
                hour = 0
            year = datetime.now().year
            result = datetime(year, month, int(day), hour, minute)
            if result < datetime.now():
                result = datetime(year + 1, month, int(day), hour, minute)
            return result.strftime('%m月%d日 %H:%M')
        return None
    except Exception:
        return None


def get_steam_free_games():
    """获取 Steam 限免游戏（通过 GamerPower API）
    
    说明：不直接调用 Steam 官方接口（store.steampowered.com），
    因为用户本地环境通常没有加速器/翻墙能力，Steam 域名在国内不稳定，
    会导致长时间超时影响体验。改用 GamerPower 作为主数据源（国内可直连），
    再通过 Steam storesearch + appdetails 补充中文支持和人民币价格信息。
    """
    return get_steam_free_games_via_gamerpower()


def get_steam_free_games_via_gamerpower():
    """通过 GamerPower API 获取 Steam 限免游戏
    
    GamerPower 国内可直连，作为 Steam 限免的主数据源。
    获取到游戏列表后，通过 Steam storesearch + appdetails 接口
    补充人民币价格和中文支持信息（这两个接口相对稳定，单次请求即可）。
    """
    url = "https://gamerpower.com/api/giveaways"
    params = {'platform': 'steam', 'type': 'game', 'sort-by': 'value'}

    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        if isinstance(data, dict) and 'status' in data:
            return []

        games = []
        for item in data:
            game_name = item.get('title', '')
            # 清理 GamerPower 标题后缀：去掉 " Giveaway" 和平台标注如 "(Steam, Xbox, Playstation)"
            game_name = re.sub(r'\s*Giveaway$', '', game_name)
            game_name = re.sub(r'\s*\([^)]*\)\s*$', '', game_name).strip()
            print(f"  处理 Steam 游戏: {game_name}", file=sys.stderr)

            # 通过 Steam API 补充详细信息（价格、中文支持）
            appid = search_steam_appid(game_name)
            has_chinese = None
            worth = item.get('worth', 'N/A')
            if appid:
                details = get_steam_game_details(appid)
                if details:
                    price_info = details.get('price_overview', {})
                    original_price = price_info.get('initial', 0)
                    if details.get('is_free') and original_price == 0:
                        print(f"    ⚠️ 跳过永久免费游戏: {game_name}", file=sys.stderr)
                        continue
                    has_chinese = details.get('has_chinese')
                    # 优先用人民币价格，失败则保留 GamerPower 的美元价格
                    if original_price > 0:
                        worth = f"¥{original_price / 100:.0f}"

            steam_url = f"https://store.steampowered.com/app/{appid}" if appid else item.get('gamerpower_url', '')

            games.append({
                'platform': 'Steam',
                'name': game_name,
                'worth': worth,
                'start_time': item.get('published_date', ''),
                'end_time': item.get('end_date', ''),
                'link': steam_url,
                'has_chinese': has_chinese,
            })

        return games

    except Exception as e:
        print(f"  获取 Steam 限免数据失败: {e}", file=sys.stderr)
        return []


# ============================================================
# Epic 相关函数
# ============================================================

def get_epic_language_support(product_slug):
    """获取 Epic 游戏的中文支持信息"""
    try:
        url = f"https://store.epicgames.com/zh-CN/p/{product_slug}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(url, headers=headers, timeout=10)
        return '简体中文' in resp.text
    except Exception as e:
        print(f"  获取 Epic 语言支持失败: {e}", file=sys.stderr)
        return None


def get_epic_free_games():
    """从 Epic Games Store API 获取限免游戏"""
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
    params = {'locale': 'zh-CN', 'country': 'CN', 'allowCountries': 'CN'}

    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        games = []
        elements = data.get('data', {}).get('Catalog', {}).get('searchStore', {}).get('elements', [])

        for elem in elements:
            title = elem.get('title', '')
            promotions = elem.get('promotions')
            if not promotions:
                continue

            current_offers = promotions.get('promotionalOffers', [])
            upcoming_offers = promotions.get('upcomingPromotionalOffers', [])

            is_free_now = False
            is_upcoming = False
            end_date = ''
            start_date = ''

            for offer_group in current_offers:
                for offer in offer_group.get('promotionalOffers', []):
                    discount = offer.get('discountSetting', {}).get('discountPercentage', 0)
                    if discount == 0:
                        is_free_now = True
                        end_date = offer.get('endDate', '')
                        start_date = offer.get('startDate', '')
                        break

            if not is_free_now:
                for offer_group in upcoming_offers:
                    for offer in offer_group.get('promotionalOffers', []):
                        discount = offer.get('discountSetting', {}).get('discountPercentage', 0)
                        if discount == 0:
                            is_upcoming = True
                            start_date = offer.get('startDate', '')
                            end_date = offer.get('endDate', '')
                            break

            if not is_free_now and not is_upcoming:
                continue

            def format_time(iso_str):
                if not iso_str:
                    return ''
                try:
                    dt = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
                    return dt.strftime('%Y-%m-%d %H:%M')
                except:
                    return iso_str

            # 获取原价
            price_info = elem.get('price', {}).get('totalPrice', {})
            original_price = price_info.get('originalPrice', 0)
            price_str = f"¥{original_price / 100:.0f}" if original_price else '免费'

            # 获取链接
            offer_mappings = elem.get('offerMappings', [])
            catalog_mappings = elem.get('catalogNs', {}).get('mappings', [])
            page_slug = ''
            for m in offer_mappings + catalog_mappings:
                if m and m.get('pageSlug'):
                    page_slug = m.get('pageSlug')
                    break
            if not page_slug:
                page_slug = elem.get('productSlug') or elem.get('urlSlug', '')

            link = f"https://store.epicgames.com/zh-CN/p/{page_slug}" if page_slug else ''

            # 获取中文支持
            print(f"  处理 Epic 游戏: {title}", file=sys.stderr)
            has_chinese = get_epic_language_support(page_slug) if page_slug else None

            games.append({
                'platform': 'Epic',
                'name': title,
                'status': '当前限免' if is_free_now else '即将限免',
                'original_price': price_str,
                'start_time': format_time(start_date),
                'end_time': format_time(end_date),
                'link': link,
                'has_chinese': has_chinese,
            })

        return games

    except Exception as e:
        print(f"获取 Epic 数据失败: {e}", file=sys.stderr)
        return []


# ============================================================
# 格式化输出
# ============================================================

def format_chinese_support(has_chinese):
    """格式化中文支持显示"""
    if has_chinese is True:
        return "✅ 支持"
    elif has_chinese is False:
        return "❌ 不支持"
    else:
        return "❓ 未知"


def format_output(steam_games, epic_games):
    """格式化输出纯文本结果"""
    lines = []
    lines.append("🎮 喜加一速报")
    lines.append(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")

    # Steam 限免
    lines.append("🔵 Steam 限免")
    lines.append("━━━━━━━━━━━━")
    if steam_games:
        for game in steam_games:
            lines.append(f"【{game['name']}】")
            lines.append(f"  原价: {game['worth']}")
            lines.append(f"  中文: {format_chinese_support(game['has_chinese'])}")
            if game.get('start_time'):
                lines.append(f"  开始: {game['start_time']}")
            if game.get('end_time'):
                lines.append(f"  截止: ⏰ {game['end_time']}")
            lines.append(f"  链接: {game['link']}")
            lines.append("")
    else:
        lines.append("暂无限免游戏")
        lines.append("")

    # Epic 当前限免
    epic_current = [g for g in epic_games if g['status'] == '当前限免']
    epic_upcoming = [g for g in epic_games if g['status'] == '即将限免']

    lines.append("🟣 Epic 当前限免")
    lines.append("━━━━━━━━━━━━")
    if epic_current:
        for game in epic_current:
            lines.append(f"【{game['name']}】")
            lines.append(f"  原价: {game['original_price']}")
            lines.append(f"  中文: {format_chinese_support(game['has_chinese'])}")
            if game.get('start_time'):
                lines.append(f"  开始: {game['start_time']}")
            if game.get('end_time'):
                lines.append(f"  截止: ⏰ {game['end_time']}")
            if game.get('link'):
                lines.append(f"  链接: {game['link']}")
            lines.append("")
    else:
        lines.append("暂无限免游戏")
        lines.append("")

    # Epic 即将限免
    if epic_upcoming:
        lines.append("📅 Epic 即将限免")
        lines.append("━━━━━━━━━━━━")
        for game in epic_upcoming:
            lines.append(f"【{game['name']}】")
            lines.append(f"  原价: {game['original_price']}")
            lines.append(f"  中文: {format_chinese_support(game['has_chinese'])}")
            if game.get('start_time'):
                lines.append(f"  开始: {game['start_time']}")
            if game.get('end_time'):
                lines.append(f"  截止: {game['end_time']}")
            if game.get('link'):
                lines.append(f"  链接: {game['link']}")
            lines.append("")

    return "\n".join(lines)


# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='查询 Steam/Epic 限免游戏')
    parser.add_argument('--steam-only', action='store_true', help='只查询 Steam 限免')
    parser.add_argument('--epic-only', action='store_true', help='只查询 Epic 限免')
    args = parser.parse_args()

    steam_games = []
    epic_games = []

    if not args.epic_only:
        print("【获取 Steam 数据】", file=sys.stderr)
        steam_games = get_steam_free_games()

    if not args.steam_only:
        print("【获取 Epic 数据】", file=sys.stderr)
        epic_games = get_epic_free_games()

    # 输出格式化结果到 stdout
    output = format_output(steam_games, epic_games)
    print(output)


if __name__ == '__main__':
    main()
