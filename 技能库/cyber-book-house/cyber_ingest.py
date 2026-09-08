#!/usr/bin/env python3
"""赛博书屋 v1.5 — 全平台内容抓取与Obsidian写入引擎

执行模型：
  本脚本不再自行调用 curl 抓取 JS 渲染页面，而是生成「抓取指令」。
  Agent（Marvis）读取指令后通过 web_fetch / browser 真实抓取，
  再将结果回填到数据字典，最终由 save_to_obsidian 完成写入。

用法：
  # 生成抓取指令（Agent 需执行的 web_fetch 调用）
  python cyber_ingest.py --instruct shipinhao https://weixin.qq.com/sph/xxx

  # 直接写入（已有抓取数据时）
  python cyber_ingest.py --write '{"source":"shipinhao","data":{...}}'
"""

import os
import re
import json
import hashlib
from datetime import datetime


# ===================== 配置 =====================

OBSIDIAN_DIR = r"E:\龙虾AI主控中心\Obsidian\wiki\赛博书屋"

PLATFORM_LABELS = {
    "bilibili": "B站视频",
    "shipinhao": "视频号",
    "gongzhonghao": "公众号",
    "youtube": "YouTube",
    "twitter": "X",
    "web": "网页",
    "pan": "网盘",
    "github": "GitHub",
    "local": "本地",
}


# ===================== 抓取指令生成（v1.5 核心） =====================

def generate_fetch_instruction(url: str, platform: str) -> dict:
    """生成结构化抓取指令，Agent 读取后调用 web_fetch / browser 执行真实抓取。

    Args:
        url: 目标页面 URL
        platform: 平台标识 (bilibili/shipinhao/gongzhonghao/youtube/twitter/web)

    Returns:
        dict: {
            "platform": 平台名,
            "url": 目标URL,
            "fetch_method": "web_fetch_playwright" | "web_fetch_default" | "browser",
            "extract_fields": ["field1", "field2", ...],
            "instruction_hint": 给 Agent 的抓取提示,
            "output_schema": 期望回填的数据字段定义
        }
    """
    instructions = {
        "shipinhao": {
            "fetch_method": "web_fetch_playwright",
            "extract_fields": [
                "title",           # 视频标题/描述文本
                "author",          # 发布者昵称
                "description",     # 完整描述/正文
                "publish_time",    # 发布日期（如 2026年8月3日）
                "tags",            # 话题标签（#xxx 格式）
                "raw_text",        # 页面原始文本
            ],
            "instruction_hint": (
                "视频号页面为 JS 动态渲染，需使用 web_fetch_playwright 或 browser 抓取。"
                "提取视频描述中 '#xxx' 格式的话题标签作为 tags 字段。"
                "发布者信息通常在页面底部或头像旁，格式为 昵称+数字ID。"
            ),
        },
        "bilibili": {
            "fetch_method": "browser",
            "extract_fields": [
                "title",
                "author",
                "description",
                "publish_time",
                "tags",
                "raw_text",
            ],
            "instruction_hint": (
                "B站页面需通过浏览器打开提取。"
                "标题在 <title> 标签中（需去掉 _哔哩哔哩_bilibili 后缀）。"
                "字幕/简介/评论区文本都归入 raw_text。"
            ),
        },
        "gongzhonghao": {
            "fetch_method": "web_fetch_playwright",
            "extract_fields": [
                "title",
                "author",
                "content",
                "publish_time",
                "tags",
                "raw_text",
            ],
            "instruction_hint": (
                "公众号文章可能需微信环境 UA 才能正常抓取。"
                "正文以 content 字段返回，去除导航/广告等噪音。"
            ),
        },
        "youtube": {
            "fetch_method": "browser",
            "extract_fields": [
                "title",
                "author",
                "description",
                "publish_time",
                "tags",
                "raw_text",
            ],
            "instruction_hint": (
                "YouTube 页面需浏览器打开提取。"
                "标题去掉 ' - YouTube' 后缀。"
                "描述在 #description 元素中，字幕需额外提取。"
            ),
        },
        "twitter": {
            "fetch_method": "web_fetch_default",
            "extract_fields": [
                "title",
                "author",
                "content",
                "publish_time",
                "raw_text",
            ],
            "instruction_hint": (
                "X/Twitter 推文可通过 web_fetch 直接抓取文本。"
                "推文正文作为 content 字段。"
            ),
        },
        "web": {
            "fetch_method": "web_fetch_default",
            "extract_fields": [
                "title",
                "content",
                "raw_text",
            ],
            "instruction_hint": (
                "通用网页抓取。标题从 <title> 提取，正文去除 HTML 标签后作为 content。"
            ),
        },
    }

    plat_info = instructions.get(platform, instructions["web"])

    return {
        "platform": platform,
        "url": url,
        "fetch_method": plat_info["fetch_method"],
        "extract_fields": plat_info["extract_fields"],
        "instruction_hint": plat_info["instruction_hint"],
        "output_schema": {
            "title": "string — 标题",
            "author": "string — 作者/发布者（可空）",
            "description": "string — 描述/正文",
            "content": "string — 文章正文（公众号/web用）",
            "publish_time": "string — 发布日期",
            "tags": "string — 标签（逗号分隔或 #tag 格式）",
            "raw_text": "string — 原始文本",
            "url": "string — 原始URL",
            "platform": "string — 平台标识",
        },
    }


def fetch_video_info(url: str, platform: str) -> dict:
    """【v1.5】生成抓取指令而非直接抓取。

    当前函数不再用 curl 自行抓取（JS 渲染页面 curl 无法处理）。
    改为返回抓取指令，由 Agent（Marvis）读取后调用 web_fetch 执行真实抓取，
    再将结果传回 cyber_book_house_ingest(prefetched_data=...)。

    Args:
        url: 视频页面URL
        platform: 平台标识

    Returns:
        dict: 包含 _fetch_instruction 字段的字典，Agent 需要执行该指令
    """
    instruction = generate_fetch_instruction(url, platform)

    return {
        "_needs_fetch": True,
        "_fetch_instruction": instruction,
        "_agent_action": (
            f"请调用 web_fetch（method={instruction['fetch_method']}）抓取 {url}，"
            f"提取字段: {instruction['extract_fields']}。"
            f"抓取完成后调用 cyber_book_house_ingest("
            f"source='{platform}', target='{url}', prefetched_data=<抓取结果>)"
        ),
        "url": url,
        "platform": platform,
        "title": "",
        "author": "",
        "description": "",
        "publish_time": "",
        "raw_text": "",
    }


def fetch_article(url: str, platform: str) -> dict:
    """【v1.5】生成文章抓取指令。

    与 fetch_video_info 同理，不再自行 curl，改为生成指令。

    Args:
        url: 文章URL
        platform: 平台标识

    Returns:
        dict: 包含 _fetch_instruction 的字典
    """
    instruction = generate_fetch_instruction(url, platform)

    return {
        "_needs_fetch": True,
        "_fetch_instruction": instruction,
        "_agent_action": (
            f"请调用 web_fetch（method={instruction['fetch_method']}）抓取 {url}，"
            f"提取字段: {instruction['extract_fields']}。"
            f"抓取完成后调用 cyber_book_house_ingest("
            f"source='{platform}', target='{url}', prefetched_data=<抓取结果>)"
        ),
        "url": url,
        "platform": platform,
        "title": "",
        "author": "",
        "content": "",
        "publish_time": "",
        "raw_text": "",
    }


# ===================== Obsidian 写入 =====================

OBSIDIAN_TEMPLATE = """---
来源: {source_label}
作者: {author}
发布日期: {publish_date}
原始链接: {url}
标签: {tags}
---

# {title}

## 核心内容
{description}

## 原始文本
{raw_text}

## 关联
[[赛博书屋]] [[仓颉Skill]] [[龙虾五步法V3.0]]
"""


def save_to_obsidian(data: dict, category: str = "") -> str:
    """将内容写入 Obsidian 标准 Markdown 笔记。

    Args:
        data: 包含 title/author/description/raw_text/url 等字段的字典
        category: 分类目录（如 '视频号'/'B站视频'），为空则写入根目录

    Returns:
        str: 输出文件路径
    """
    os.makedirs(OBSIDIAN_DIR, exist_ok=True)

    if category:
        target_dir = os.path.join(OBSIDIAN_DIR, category)
    else:
        target_dir = OBSIDIAN_DIR
    os.makedirs(target_dir, exist_ok=True)

    platform_label = PLATFORM_LABELS.get(data.get("platform", "web"), "网页")
    author = (data.get("author") or "").strip() or "未知"
    title = (data.get("title") or "").strip() or "未命名"
    date_str = data.get("publish_time") or datetime.now().strftime("%Y-%m-%d")
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")

    safe_title = re.sub(r'[\\/:*?"<>|]', '-', title)[:60]
    safe_author = re.sub(r'[\\/:*?"<>|]', '-', author)[:20]
    filename = f"{platform_label}-{safe_author}-{safe_title}-{date_str}.md"
    filepath = os.path.join(target_dir, filename)

    if os.path.exists(filepath):
        base, ext = os.path.splitext(filename)
        filepath = os.path.join(
            target_dir,
            f"{base}_{hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:6]}{ext}"
        )

    content = OBSIDIAN_TEMPLATE.format(
        source_label=platform_label,
        author=author,
        publish_date=date_str,
        url=data.get("url", ""),
        tags=data.get("tags", ""),
        title=title,
        description=data.get("description", data.get("content", "")),
        raw_text=(data.get("raw_text") or "")[:3000],
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath


# ===================== 统一入口（v1.5 支持预抓取数据） =====================

def cyber_book_house_ingest(
    source: str,
    target: str,
    output_dir: str = None,
    prefetched_data: dict = None,
) -> dict:
    """赛博书屋统一入口。

    Args:
        source: 来源标识 (bilibili/shipinhao/gongzhonghao/youtube/twitter/web/pan/github/local)
        target: 资源路径/URL
        output_dir: 自定义输出目录，默认 Obsidian wiki/赛博书屋/
        prefetched_data: 外部已抓取数据，传入后跳过 fetch 直接写入 Obsidian。
            格式应与 fetch_video_info/fetch_article 输出 schema 一致：
            {title, author, description/content, publish_time, tags, raw_text, url, platform}

    Returns:
        dict: {"status": "ok", "output_path": "...", "token_count": N}
           或 {"status": "needs_fetch", "instruction": {...}}
    """
    global OBSIDIAN_DIR
    if output_dir:
        OBSIDIAN_DIR = output_dir

    # 路径 A：已有预抓取数据，直接写入 Obsidian
    if prefetched_data is not None:
        data = dict(prefetched_data)  # shallow copy
        data.setdefault("platform", source)
        data.setdefault("url", target)

        category = ""
        if source in PLATFORM_LABELS:
            category = PLATFORM_LABELS[source]

        output_path = save_to_obsidian(data, category)
        token_count = len(re.sub(r'\s+', ' ', data.get("raw_text", "") or ""))

        return {
            "status": "ok",
            "output_path": output_path,
            "token_count": token_count,
            "ingest_mode": "prefetched",
        }

    # 路径 B：需要抓取 → 生成指令
    video_platforms = {"bilibili", "shipinhao", "youtube"}
    article_platforms = {"gongzhonghao", "web", "twitter"}

    if source in video_platforms:
        data = fetch_video_info(target, source)
    elif source in article_platforms:
        data = fetch_article(target, source)
    else:
        # pan / github / local 兜底 — 无需抓取，直接写
        data = {
            "title": os.path.basename(target),
            "author": "",
            "description": f"来源: {source}, 路径: {target}",
            "raw_text": "",
            "url": target,
            "platform": source,
            "publish_time": datetime.now().strftime("%Y-%m-%d"),
            "tags": "",
        }
        category = PLATFORM_LABELS.get(source, "其他")
        output_path = save_to_obsidian(data, category)
        return {
            "status": "ok",
            "output_path": output_path,
            "token_count": 0,
            "ingest_mode": "local",
        }

    # 需要抓取的平台 → 返回指令
    return {
        "status": "needs_fetch",
        "instruction": data.get("_fetch_instruction", {}),
        "agent_action": data.get("_agent_action", ""),
        "ingest_mode": "requires_agent_fetch",
    }


# ===================== CLI入口 =====================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("cyber_ingest.py — 赛博书屋 v1.5 全平台抓取引擎")
        print()
        print("模式:")
        print("  --instruct <platform> <url>    生成抓取指令（供 Agent 执行）")
        print("  --write '<json>'               已有数据直接写入 Obsidian")
        print("  <source> <target> [out_dir]   传统入口（需抓取时返回指令）")
        print()
        print("平台: bilibili | shipinhao | gongzhonghao | youtube | twitter | web | pan | github | local")
        print()
        print("示例:")
        print('  python cyber_ingest.py --instruct shipinhao https://weixin.qq.com/sph/xxx')
        print('  python cyber_ingest.py --write \'{"source":"shipinhao","data":{"title":"测试",...}}\'')
        print("  python cyber_ingest.py shipinhao https://weixin.qq.com/sph/xxx")
        sys.exit(0)

    if sys.argv[1] == "--instruct":
        if len(sys.argv) < 4:
            print("用法: python cyber_ingest.py --instruct <platform> <url>")
            sys.exit(1)
        platform = sys.argv[2]
        url = sys.argv[3]
        instruction = generate_fetch_instruction(url, platform)
        print(json.dumps(instruction, ensure_ascii=False, indent=2))

    elif sys.argv[1] == "--write":
        if len(sys.argv) < 3:
            print("用法: python cyber_ingest.py --write '<json>'")
            sys.exit(1)
        payload = json.loads(sys.argv[2])
        source = payload["source"]
        data = payload.get("data", {})
        result = cyber_book_house_ingest(source=source, target=data.get("url", ""), prefetched_data=data)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        if len(sys.argv) < 3:
            print("用法: python cyber_ingest.py <source> <target> [output_dir]")
            sys.exit(1)
        source = sys.argv[1]
        target = sys.argv[2]
        out_dir = sys.argv[3] if len(sys.argv) > 3 else None
        result = cyber_book_house_ingest(source, target, out_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
