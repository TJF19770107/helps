# -*- coding: utf-8 -*-
"""
星穹铁道兑换码爬虫（Marvis Skill 版）
数据源:
  1. B站Wiki: https://wiki.biligame.com/sr/兑换码 (长期码)
  2. 游民星空: gamersky.com (前瞻直播码)

输出: JSON 到 stdout，供 Skill 直接解析使用
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime, timedelta
from urllib.parse import quote
import os
import sys
import time

# Windows终端编码修复
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# 日志输出到stderr，不污染stdout的JSON
def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", file=sys.stderr)

# ===== 配置 =====
WIKI_URL = "https://wiki.biligame.com/sr/兑换码"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

# 前瞻码正则：8-16位大写字母+数字组合
PREVIEW_CODE_PATTERN = re.compile(r'\b[A-Z0-9]{8,16}\b')

# 常见非兑换码的大写字符串（需排除）
CODE_BLACKLIST = {
    'GAMERSKY', 'MIHOYO', 'HOYOVERSE', 'COGNOSPHERE', 'ANDROID', 'IPHONE',
    'WINDOWS', 'STARRAIL', 'YOUTUBE', 'TWITCH', 'BILIBILI', 'FACEBOOK',
    'TWITTER', 'DISCORD', 'INSTAGRAM', 'TIKTOK', 'REDDIT', 'PLAYSTATION',
    'NINTENDO', 'SWITCH', 'XBOX', 'STEAM', 'EPIC', 'APPSTORE', 'GOOGLEPLAY',
    'COPYRIGHT', 'RESERVED', 'ALLRIGHT', 'PRIVACY', 'POLICY', 'TERMS',
    'SERVICE', 'CONTACT', 'ABOUT', 'DOWNLOAD', 'REGISTER', 'LOGIN',
}

# 已知前瞻码文章URL配置文件
PREVIEW_URLS_FILE = os.path.join(SCRIPT_DIR, "preview_article_urls.txt")


###############################################################################
# Part 1: B站Wiki 长期码爬取
###############################################################################

def fetch_wiki_page():
    """获取Wiki页面内容"""
    log(f"正在获取Wiki页面: {WIKI_URL}")
    try:
        response = requests.get(WIKI_URL, headers=HEADERS, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        log(f"页面获取成功，长度: {len(response.text)} 字符")
        return response.text
    except requests.RequestException as e:
        log(f"获取Wiki页面失败: {e}")
        return None


def parse_wiki_codes(html_content):
    """
    解析B站Wiki兑换码 - 只爬取"可使用"区域的表格
    过滤掉国际服码和已失效码
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    codes = []

    # 找到"可使用"区域的h2标题
    usable_h2 = None
    for h2 in soup.find_all('h2'):
        h2_text = h2.get_text(strip=True)
        if '可使用' in h2_text:
            usable_h2 = h2
            break

    if not usable_h2:
        log("未找到'可使用'区域标题，回退到全页面解析")
        tables = soup.find_all('table', class_='wikitable')
    else:
        # 只收集"可使用"h2和下一个h2之间的wikitable
        tables = []
        sibling = usable_h2.find_next_sibling()
        while sibling:
            if sibling.name == 'h2':
                break
            if sibling.name == 'table' and 'wikitable' in sibling.get('class', []):
                tables.append(sibling)
            elif sibling.name != 'table':
                nested_tables = sibling.find_all('table', class_='wikitable') if hasattr(sibling, 'find_all') else []
                tables.extend(nested_tables)
            sibling = sibling.find_next_sibling()
        log(f"'可使用'区域找到 {len(tables)} 个wikitable表格")

    for table_idx, table in enumerate(tables):
        # 检查是否国际服区块
        prev = table.find_previous(['h3', 'h2'])
        if prev and prev.name == 'h3':
            section_text = prev.get_text(strip=True)
            if '国际' in section_text or 'global' in section_text.lower():
                log(f"表格 {table_idx} 属于国际服区块，跳过")
                continue

        section_type = "cn"
        if prev and prev.name == 'h3' and '国服' not in prev.get_text(strip=True):
            section_type = "unknown"

        rows = table.find_all('tr')

        # 获取表头
        headers_list = []
        header_row = table.find('tr')
        if header_row:
            for th in header_row.find_all(['th', 'td']):
                headers_list.append(th.get_text(strip=True).lower())

        # 确定列索引
        code_col = type_col = reward_col = status_col = -1
        for i, h in enumerate(headers_list):
            if '兑换码' in h or 'code' in h or '礼包码' in h:
                code_col = i
            elif '区服' in h or '类型' in h or '服务器' in h or '适用' in h:
                type_col = i
            elif '奖励' in h or '内容' in h:
                reward_col = i
            elif '状态' in h or '有效' in h:
                status_col = i

        # 解析数据行
        for row in rows[1:]:
            cells = row.find_all(['td', 'th'])
            if len(cells) <= max(code_col, 0):
                continue

            code_cell = cells[code_col] if 0 <= code_col < len(cells) else None
            if not code_cell:
                continue

            code = code_cell.get_text(strip=True)
            if not code or len(code) < 4:
                continue

            # 区服类型
            code_type = section_type
            if 0 <= type_col < len(cells):
                type_text = cells[type_col].get_text(strip=True).lower()
                if '国服' in type_text:
                    code_type = "cn_only"
                elif '国际' in type_text or 'global' in type_text or 'os' in type_text:
                    code_type = "global_only"
                elif '通用' in type_text or '全服' in type_text:
                    code_type = "universal"

            # 奖励
            reward = ""
            if 0 <= reward_col < len(cells):
                reward = cells[reward_col].get_text(strip=True)

            # 有效期
            is_expired = False
            if 0 <= status_col < len(cells):
                status_text = cells[status_col].get_text(strip=True).lower()
                if '失效' in status_text or '过期' in status_text or '无效' in status_text:
                    is_expired = True
            row_text = row.get_text().lower()
            if '已失效' in row_text or '已过期' in row_text:
                is_expired = True

            # 过滤
            if code_type == "global_only":
                continue
            if is_expired:
                continue

            codes.append({
                "code": code,
                "type": "long_term",
                "source": "bilibili_wiki",
                "reward": reward,
                "expire_at": None,
            })

    return codes


def crawl_wiki_codes():
    """爬取B站Wiki长期码"""
    log("=" * 40)
    log("开始爬取B站Wiki长期码")

    html = fetch_wiki_page()
    if not html:
        log("无法获取Wiki页面")
        return []

    codes = parse_wiki_codes(html)
    log(f"Wiki长期码: 解析到 {len(codes)} 个有效码")
    return codes


###############################################################################
# Part 2: 游民星空 前瞻码爬取
###############################################################################

def load_known_preview_urls():
    """加载已知的前瞻码文章URL列表"""
    urls = []
    if os.path.exists(PREVIEW_URLS_FILE):
        with open(PREVIEW_URLS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and line.startswith('http'):
                    urls.append(line)
    return urls


def save_discovered_url(url):
    """将新发现的文章URL追加到配置文件"""
    existing = load_known_preview_urls()
    if url not in existing:
        with open(PREVIEW_URLS_FILE, 'a', encoding='utf-8') as f:
            f.write(f"\n# 自动发现于 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"{url}\n")
        log(f"新URL已保存: {url}")


def search_gamersky_preview_article():
    """通过百度搜索找游民星空前瞻码文章"""
    log("正在通过百度搜索游民星空前瞻码文章...")

    search_query = "崩坏星穹铁道 前瞻 兑换码 site:gamersky.com"
    search_url = f"https://www.baidu.com/s?wd={quote(search_query)}&rn=10"

    try:
        resp = requests.get(search_url, headers={
            **HEADERS,
            "Referer": "https://www.baidu.com/",
        }, timeout=15)
        resp.raise_for_status()
        resp.encoding = 'utf-8'
    except requests.RequestException as e:
        log(f"百度搜索失败: {e}")
        return []

    soup = BeautifulSoup(resp.text, 'html.parser')

    # 提取百度跳转链接
    baidu_links = []
    for result_div in soup.find_all(['div', 'h3']):
        a_tag = result_div.find('a', href=True)
        if a_tag:
            href = a_tag.get('href', '')
            if href.startswith('http') and 'baidu.com' in href:
                baidu_links.append(href)

    # 收集mu属性中的真实URL
    article_urls = []
    for tag in soup.find_all(attrs={"mu": True}):
        mu = tag.get('mu', '')
        if 'gamersky.com' in mu and mu.endswith('.shtml'):
            if mu not in article_urls:
                article_urls.append(mu)

    # 跟踪百度跳转
    for link in baidu_links[:8]:
        try:
            head_resp = requests.head(link, headers=HEADERS, timeout=10, allow_redirects=True)
            real_url = head_resp.url
            if 'gamersky.com' in real_url and real_url.endswith('.shtml'):
                if real_url not in article_urls:
                    article_urls.append(real_url)
        except requests.RequestException:
            continue

    log(f"百度搜索找到 {len(article_urls)} 个文章URL")
    return article_urls


def search_gamersky_via_bing():
    """备用：Bing搜索"""
    log("尝试Bing搜索...")

    search_query = "崩坏星穹铁道 前瞻 兑换码 site:gamersky.com"
    search_url = f"https://www.bing.com/search?q={quote(search_query)}&count=10"

    try:
        resp = requests.get(search_url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        resp.encoding = 'utf-8'
    except requests.RequestException as e:
        log(f"Bing搜索失败: {e}")
        return []

    soup = BeautifulSoup(resp.text, 'html.parser')
    article_urls = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if 'gamersky.com' in href and href.endswith('.shtml'):
            if href not in article_urls:
                article_urls.append(href)

    log(f"Bing搜索找到 {len(article_urls)} 个文章URL")
    return article_urls


def search_gamersky_via_sogou():
    """备用：搜狗搜索"""
    log("尝试搜狗搜索...")

    search_query = "崩坏星穹铁道 前瞻 兑换码 site:gamersky.com"
    search_url = f"https://www.sogou.com/web?query={quote(search_query)}"

    try:
        resp = requests.get(search_url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        resp.encoding = 'utf-8'
    except requests.RequestException as e:
        log(f"搜狗搜索失败: {e}")
        return []

    article_urls = []
    soup = BeautifulSoup(resp.text, 'html.parser')

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if 'gamersky.com' in href and href.endswith('.shtml'):
            if href not in article_urls:
                article_urls.append(href)

    url_pattern = re.compile(r'https?://www\.gamersky\.com/\w+/\d+/\d+\.shtml')
    for match in url_pattern.findall(resp.text):
        if match not in article_urls:
            article_urls.append(match)

    log(f"搜狗搜索找到 {len(article_urls)} 个文章URL")
    return article_urls


def fetch_article_page(url):
    """获取文章页面"""
    log(f"正在获取文章: {url}")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        resp.encoding = 'utf-8'
        return resp.text
    except requests.RequestException as e:
        log(f"获取文章失败 {url}: {e}")
        return None


def extract_preview_codes_from_article(html_content, article_url=""):
    """从游民星空文章中提取国服前瞻兑换码"""
    soup = BeautifulSoup(html_content, 'html.parser')

    content_div = (
        soup.find('div', class_='Mid2L_con') or
        soup.find('div', class_='Mid_con') or
        soup.find('div', class_='detail_content') or
        soup.find('article')
    )

    if not content_div:
        content_div = soup

    full_text = content_div.get_text(separator='\n')

    if not any(kw in full_text for kw in ['前瞻', '特别节目', '兑换码', '直播']):
        return [], None, None

    # 提取发布日期
    publish_date = None
    url_date_match = re.search(r'/(\d{4})(\d{2})/', article_url)
    if url_date_match:
        try:
            publish_date = datetime(int(url_date_match.group(1)), int(url_date_match.group(2)), 1)
        except ValueError:
            pass

    date_meta = soup.find('meta', attrs={'property': 'article:published_time'})
    if date_meta and date_meta.get('content'):
        try:
            publish_date = datetime.fromisoformat(date_meta['content'].replace('Z', '+00:00').split('+')[0])
        except ValueError:
            pass

    date_in_text = re.search(r'(\d{4})[年\-/](\d{1,2})[月\-/](\d{1,2})', full_text)
    if date_in_text and not publish_date:
        try:
            publish_date = datetime(int(date_in_text.group(1)), int(date_in_text.group(2)), int(date_in_text.group(3)))
        except ValueError:
            pass

    # 提取失效时间
    expire_at = None
    expire_patterns = [
        r'(\d{4})年(\d{1,2})月(\d{1,2})日\s*(\d{1,2}):(\d{2}):?(\d{2})?\s*失效',
        r'失效.*?(\d{4})年(\d{1,2})月(\d{1,2})日\s*(\d{1,2}):(\d{2}):?(\d{2})?',
        r'(\d{4})年(\d{1,2})月(\d{1,2})日\s*(\d{1,2}):(\d{2}):?(\d{2})?\s*(?:前|之前|过期)',
    ]
    for pattern in expire_patterns:
        match = re.search(pattern, full_text)
        if match:
            groups = match.groups()
            try:
                y, m, d, h, mi = int(groups[0]), int(groups[1]), int(groups[2]), int(groups[3]), int(groups[4])
                s = int(groups[5]) if groups[5] else 59
                expire_at = datetime(y, m, d, h, mi, s).isoformat()
            except (ValueError, IndexError):
                pass
            break

    # 文章发布超3天默认前瞻码已过期
    if not expire_at and publish_date:
        days_old = (datetime.now() - publish_date).days
        if days_old > 3:
            expire_at = (publish_date + timedelta(days=1)).isoformat()
            log(f"文章发布于{publish_date.strftime('%Y-%m-%d')}({days_old}天前)，默认前瞻码已过期")

    # 提取版本号
    version = None
    ver_match = re.search(r'(\d+\.\d+)\s*(?:版本|前瞻|特别节目)', full_text)
    if ver_match:
        version = ver_match.group(1)

    # 区分国服/国际服，只取国服码
    lines = full_text.split('\n')
    cn_codes = []
    global_codes = []
    current_region = "unknown"

    for line in lines:
        line_stripped = line.strip()

        if re.search(r'国服', line_stripped) and '国际' not in line_stripped:
            current_region = "cn"
            continue
        elif re.search(r'国际服|global|海外', line_stripped, re.IGNORECASE):
            current_region = "global"
            continue

        found_codes = PREVIEW_CODE_PATTERN.findall(line_stripped)
        for code in found_codes:
            if code.upper() in CODE_BLACKLIST:
                continue
            if code.isdigit():
                continue
            if len(code) < 8:
                continue

            if current_region == "cn":
                cn_codes.append(code)
            elif current_region == "global":
                global_codes.append(code)
            else:
                cn_codes.append(code)

    # 备选：全文提取
    if not cn_codes and not global_codes:
        log("未检测到国服/国际服区块标记，使用全文提取模式")
        all_codes = PREVIEW_CODE_PATTERN.findall(full_text)
        for code in all_codes:
            if code.upper() not in CODE_BLACKLIST and not code.isdigit() and len(code) >= 8:
                cn_codes.append(code)

    cn_codes = list(dict.fromkeys(cn_codes))

    log(f"提取到国服码 {len(cn_codes)} 个: {cn_codes}")
    if global_codes:
        log(f"跳过国际服码 {len(global_codes)} 个")

    result_codes = []
    for code in cn_codes:
        result_codes.append({
            "code": code.upper(),
            "type": "preview",
            "source": "gamersky",
            "reward": "星琼×100" if version else "",
            "expire_at": expire_at,
        })

    return result_codes, expire_at, publish_date


def crawl_preview_codes():
    """爬取前瞻码"""
    log("=" * 40)
    log("开始爬取前瞻直播码（游民星空）")

    all_candidate_urls = []

    # 优先级1: 配置文件中的已知URL
    known_urls = load_known_preview_urls()
    if known_urls:
        log(f"从配置文件加载 {len(known_urls)} 个已知URL")
        all_candidate_urls.extend(known_urls)

    # 优先级2-4: 搜索引擎
    for search_fn in [search_gamersky_preview_article, search_gamersky_via_bing, search_gamersky_via_sogou]:
        try:
            urls = search_fn()
            for url in urls:
                if url not in all_candidate_urls:
                    all_candidate_urls.append(url)
        except Exception as e:
            log(f"搜索失败: {e}")

        if len(all_candidate_urls) >= 5:
            break

    if not all_candidate_urls:
        log("未找到任何前瞻码文章URL")
        return []

    log(f"共 {len(all_candidate_urls)} 个候选文章URL")

    all_preview_codes = []
    processed_urls = set()

    for url in all_candidate_urls[:8]:
        if url in processed_urls:
            continue
        processed_urls.add(url)

        html = fetch_article_page(url)
        if not html:
            continue

        codes, expire_at, publish_date = extract_preview_codes_from_article(html, url)
        if not codes:
            continue

        # 检查是否过期
        if expire_at:
            try:
                expire_time = datetime.fromisoformat(expire_at)
                if expire_time < datetime.now():
                    log(f"文章 {url} 的前瞻码已过期({expire_at})，跳过")
                    continue
            except ValueError:
                pass

        all_preview_codes.extend(codes)
        log(f"从 {url} 提取到 {len(codes)} 个有效前瞻码")

        save_discovered_url(url)
        time.sleep(1)

    # 去重
    seen = set()
    unique_codes = []
    for code_info in all_preview_codes:
        code = code_info['code'].upper()
        if code not in seen:
            seen.add(code)
            unique_codes.append(code_info)

    log(f"前瞻码: 共获取 {len(unique_codes)} 个有效码")
    return unique_codes


###############################################################################
# Part 3: 合并输出
###############################################################################

def deduplicate_codes(codes):
    """全局去重"""
    seen = set()
    unique_codes = []
    for code_info in codes:
        code = code_info['code'].upper()
        if code not in seen:
            seen.add(code)
            code_info['code'] = code
            unique_codes.append(code_info)
    return unique_codes


def main():
    log("=" * 50)
    log("星穹铁道兑换码爬虫（Marvis Skill 版）")
    log("=" * 50)

    all_codes = []

    # 1. B站Wiki长期码
    wiki_codes = crawl_wiki_codes()
    all_codes.extend(wiki_codes)

    # 2. 游民星空前瞻码
    preview_codes = crawl_preview_codes()
    all_codes.extend(preview_codes)

    # 3. 全局去重
    all_codes = deduplicate_codes(all_codes)

    # 4. 分类统计
    long_term_count = sum(1 for c in all_codes if c.get('type') == 'long_term')
    preview_count = sum(1 for c in all_codes if c.get('type') == 'preview')

    result = {
        "game_id": "starrail",
        "crawl_time": datetime.now().isoformat(),
        "total": len(all_codes),
        "long_term_count": long_term_count,
        "preview_count": preview_count,
        "codes": all_codes,
    }

    # 输出 JSON 到 stdout
    print(json.dumps(result, ensure_ascii=False, indent=2))

    log(f"完成: 共 {len(all_codes)} 个有效码（长期码 {long_term_count} + 前瞻码 {preview_count}）")


if __name__ == "__main__":
    main()
