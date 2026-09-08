"""微信公众号历史文章全量爬虫（Hermes/Trae 技能版）。"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
import random
import re
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup


REQUIRED_PACKAGES = ["requests", "beautifulsoup4", "playwright"]
DEFAULT_HERMES_URL = os.environ.get("HERMES_BASE_URL", "http://127.0.0.1:8080").rstrip("/")
DEFAULT_TIMEOUT = int(os.environ.get("WECHAT_CRAWLER_TIMEOUT_S", "25"))


@dataclass
class Article:
    """保存单篇文章结构化信息。"""

    title: str
    publish_time: str
    link: str
    content: str
    source: str = "wechat_mp"
    keywords: Optional[List[str]] = None
    core_points: Optional[List[str]] = None


def ensure_dependencies(need_playwright: bool = True) -> None:
    """检查并自动安装技能依赖。"""

    missing = []
    for pkg in REQUIRED_PACKAGES:
        if pkg == "playwright" and not need_playwright:
            continue
        module_name = "bs4" if pkg == "beautifulsoup4" else pkg
        if importlib.util.find_spec(module_name) is None:
            missing.append(pkg)
    if missing:
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
    if need_playwright and importlib.util.find_spec("playwright") is not None:
        try:
            subprocess.run(
                [sys.executable, "-m", "playwright", "install", "chromium"],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            pass


def ensure_socket_available() -> None:
    """确保当前运行环境允许创建基础 socket（用于 Playwright/HTTP 请求）。"""

    try:
        import socket

        s = socket.socket()
        s.close()
    except Exception as e:
        raise RuntimeError(f"当前运行环境不可用 sockets，无法执行网络爬取: {e}")


def project_root_from_skill_dir(skill_dir: Path) -> Path:
    """从技能目录回溯项目根目录。"""

    if skill_dir.parent.name == "skills" and skill_dir.parent.parent.name in (".trae", ".hermes"):
        return skill_dir.parent.parent.parent
    return skill_dir.parent


def sanitize_filename(name: str) -> str:
    """将标题转换成安全文件名片段。"""

    cleaned = re.sub(r"[\\/:*?\"<>|\r\n]+", "_", name or "").strip(" ._")
    return cleaned[:80] or "untitled"


def brief_sleep(base: float = 1.0, jitter: float = 1.5) -> None:
    """随机抖动延时，降低触发风控概率。"""

    time.sleep(base + random.random() * jitter)


def retry_call(func, retries: int = 3, base_delay: float = 1.2):
    """执行可重试操作，带指数退避。"""

    last_exc = None
    for idx in range(retries):
        try:
            return func()
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if idx == retries - 1:
                raise
            time.sleep(base_delay * (2**idx) + random.random())
    if last_exc:
        raise last_exc


class WechatCrawler:
    """微信公众号历史消息全量抓取器。"""

    def __init__(self, mp_url: str, skill_dir: Optional[Path] = None):
        """初始化目录、状态文件和会话对象。"""

        self.mp_url = mp_url.strip()
        self.skill_dir = Path(skill_dir or Path(__file__).resolve().parent)
        self.project_root = project_root_from_skill_dir(self.skill_dir)
        self.output_dir = self.project_root / "hermes_skills" / "crawler_output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.kb_dir = self.skill_dir / "kb"
        self.kb_dir.mkdir(parents=True, exist_ok=True)
        self.state_path = self.output_dir / "wechat_crawler_state.json"
        self.index_path = self.output_dir / "index.csv"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            }
        )
        self._articles_seen = self._load_index_links()

    def _state_key(self) -> str:
        """生成当前公众号链接唯一键。"""

        return hashlib.sha256(self.mp_url.encode("utf-8")).hexdigest()

    def load_state(self) -> Dict:
        """读取断点状态。"""

        if not self.state_path.exists():
            return {}
        try:
            return json.loads(self.state_path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def save_state(self, state: Dict) -> None:
        """原子写入断点状态。"""

        temp_path = self.state_path.with_suffix(".tmp")
        temp_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        temp_path.replace(self.state_path)

    def _load_index_links(self) -> set:
        """读取 index.csv 里的已抓取链接集合用于去重。"""

        links = set()
        if not self.index_path.exists():
            return links
        try:
            with self.index_path.open("r", encoding="utf-8-sig", newline="") as f:
                for row in csv.DictReader(f):
                    link = (row.get("链接") or "").strip()
                    if link:
                        links.add(link)
        except Exception:
            return links
        return links

    def _extract_text(self, html: str) -> str:
        """从文章 HTML 抽取正文文本。"""

        soup = BeautifulSoup(html, "html.parser")
        node = soup.select_one("#js_content") or soup.select_one(".rich_media_content")
        text = node.get_text("\n", strip=True) if node else soup.get_text("\n", strip=True)
        return re.sub(r"\n{3,}", "\n\n", text).strip()

    def _extract_publish_time(self, html: str) -> str:
        """从文章 HTML 抽取发布时间。"""

        for pattern in (
            r"var\s+publish_time\s*=\s*\"(\d+)\"",
            r"n\.publish_time\s*=\s*\"(\d+)\"",
            r"ct\s*=\s*\"?(\d{10})\"?",
        ):
            match = re.search(pattern, html)
            if match:
                ts = int(match.group(1))
                return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _extract_article_title(self, html: str, fallback: str = "") -> str:
        """从文章 HTML 尽力提取标题。"""

        soup = BeautifulSoup(html, "html.parser")
        node = soup.select_one("#activity-name")
        if node:
            t = node.get_text(strip=True)
            if t:
                return t
        m = re.search(r"<meta[^>]+property=[\"']og:title[\"'][^>]+content=[\"']([^\"']+)[\"'][^>]*>", html, re.I)
        if m:
            return m.group(1).strip()
        m = re.search(r"<title[^>]*>([\s\S]*?)</title>", html, re.I)
        if m:
            return re.sub(r"\s+", " ", m.group(1)).strip()
        return (fallback or "").strip()

    def fetch_article(self, title: str, link: str, publish_time_hint: str) -> Article:
        """抓取单篇文章正文并补全结构化字段。"""

        def _request():
            resp = self.session.get(link, timeout=DEFAULT_TIMEOUT)
            resp.raise_for_status()
            return resp.text

        html = retry_call(_request, retries=3)
        content = self._extract_text(html)
        publish_time = self._extract_publish_time(html) or publish_time_hint
        title = self._extract_article_title(html, fallback=title.strip() or "未命名文章") or "未命名文章"
        keywords, points = summarize_article(content)
        return Article(
            title=title,
            publish_time=publish_time,
            link=link,
            content=content,
            keywords=keywords,
            core_points=points,
        )

    def _parse_profile_response(self, payload: Dict) -> Tuple[List[Dict], int, int]:
        """解析 profile_ext 的 JSON 数据并提取文章条目。"""

        data_blob = payload.get("general_msg_list")
        msg_list = []
        if isinstance(data_blob, str):
            try:
                msg_list = (json.loads(data_blob) or {}).get("list") or []
            except Exception:
                msg_list = []
        elif isinstance(data_blob, dict):
            msg_list = data_blob.get("list") or []

        items = []
        for msg in msg_list:
            ext = (msg or {}).get("app_msg_ext_info") or {}
            publish_ts = int(((msg or {}).get("comm_msg_info") or {}).get("datetime") or 0)
            publish_time = datetime.fromtimestamp(publish_ts).strftime("%Y-%m-%d %H:%M:%S") if publish_ts else ""
            candidates = [ext]
            multi = ext.get("multi_app_msg_item_list") or []
            if isinstance(multi, list):
                candidates.extend(multi)
            for row in candidates:
                title = (row or {}).get("title") or ""
                link = (row or {}).get("content_url") or ""
                if link.startswith("//"):
                    link = "https:" + link
                if title and "mp.weixin.qq.com" in link:
                    items.append({"title": title, "link": link, "publish_time": publish_time})
        can_continue = int(payload.get("can_msg_continue") or 0)
        next_offset = int(payload.get("next_offset") or 0)
        return items, can_continue, next_offset

    def _build_api_url(self, base_url: str, offset: int) -> str:
        """基于首包 URL 生成翻页请求 URL。"""

        parsed = urlparse(base_url)
        query = parse_qs(parsed.query, keep_blank_values=True)
        query["offset"] = [str(offset)]
        query["f"] = ["json"]
        query["count"] = [query.get("count", ["10"])[0]]
        query["action"] = [query.get("action", ["getmsg"])[0]]
        flat_query = urlencode({k: v[0] if isinstance(v, list) else v for k, v in query.items()})
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, flat_query, parsed.fragment))

    def fetch_all_metadata(self, max_pages: Optional[int] = None, resume: bool = True) -> List[Dict]:
        """通过 Playwright 抓取并翻页，返回文章元数据列表。"""

        ensure_dependencies(need_playwright=True)
        from playwright.sync_api import sync_playwright

        state = self.load_state()
        key = self._state_key()
        offset = int((state.get(key) or {}).get("offset") or 0) if resume else 0
        base_api_url = ""
        all_items: List[Dict] = []
        page_count = 0

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            captured_payloads: List[Tuple[str, Dict]] = []

            def on_response(resp):
                url = resp.url
                if "mp/profile_ext" in url and "action=getmsg" in url:
                    try:
                        captured_payloads.append((url, resp.json()))
                    except Exception:
                        pass

            page.on("response", on_response)
            page.goto(self.mp_url, wait_until="domcontentloaded", timeout=60000)
            for _ in range(20):
                page.mouse.wheel(0, 2000)
                brief_sleep(0.5, 0.8)
                if captured_payloads:
                    break

            if not captured_payloads:
                raise RuntimeError("未捕获到 profile_ext 接口响应，可能遇到页面风控或链接无效。")

            base_api_url, first_payload = captured_payloads[-1]
            first_items, can_continue, next_offset = self._parse_profile_response(first_payload)
            all_items.extend(first_items)

            cookies = context.cookies("https://mp.weixin.qq.com")
            for cookie in cookies:
                try:
                    self.session.cookies.set(cookie["name"], cookie["value"], domain=cookie.get("domain"), path=cookie.get("path"))
                except Exception:
                    continue

            current_offset = offset or next_offset
            while can_continue == 1:
                if max_pages is not None and page_count >= max_pages:
                    break
                page_count += 1
                api_url = self._build_api_url(base_api_url, current_offset)

                def _page_fetch():
                    resp = self.session.get(api_url, timeout=DEFAULT_TIMEOUT, headers={"Referer": self.mp_url})
                    resp.raise_for_status()
                    return resp.json()

                payload = retry_call(_page_fetch, retries=3)
                items, can_continue, next_offset = self._parse_profile_response(payload)
                all_items.extend(items)
                current_offset = next_offset
                state[key] = {"offset": current_offset, "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                self.save_state(state)
                brief_sleep(1.0, 2.5)

            browser.close()

        dedup = {}
        for row in all_items:
            if row["link"] not in dedup:
                dedup[row["link"]] = row
        return list(dedup.values())

    def run_single_article(self) -> Dict:
        """仅抓取单篇文章（mp.weixin.qq.com/s/...）并落盘入库。"""

        link = self.mp_url
        if link in self._articles_seen:
            report = {
                "status": "success",
                "mode": "single_article",
                "mp_url": self.mp_url,
                "fetched_total": 1,
                "new_saved": 0,
                "output_dir": str(self.output_dir),
                "index_csv": str(self.index_path),
                "trae_kb": str(self.kb_dir / "trae_skill_kb.jsonl"),
                "hermes_sync": {"ok": 0, "failed": [], "total": 0},
                "generated_files": [],
                "skipped_reason": "already_in_index",
            }
            (self.output_dir / "last_run_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            return report

        article = retry_call(lambda: self.fetch_article("", link, ""), retries=3)
        path = self.save_markdown(article)
        self.append_index([article])
        kb_path = self.save_trae_kb([article], [path])
        hermes_sync = self.push_to_hermes_kb([path])
        report = {
            "status": "success",
            "mode": "single_article",
            "mp_url": self.mp_url,
            "fetched_total": 1,
            "new_saved": 1,
            "output_dir": str(self.output_dir),
            "index_csv": str(self.index_path),
            "trae_kb": str(kb_path),
            "hermes_sync": hermes_sync,
            "generated_files": [str(path)],
        }
        (self.output_dir / "last_run_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        return report

    def save_markdown(self, article: Article) -> Path:
        """将单篇文章保存为 Markdown 文件。"""

        dt = normalize_datetime(article.publish_time)
        safe_title = sanitize_filename(article.title)
        name = f"{dt}_{safe_title}.md"
        path = self.output_dir / name
        md = [
            f"# {article.title}",
            "",
            f"- 发布时间: {article.publish_time}",
            f"- 链接: {article.link}",
            "",
            "## 正文",
            "",
            article.content or "（正文为空）",
            "",
            "## 摘要提取",
            "",
            "### 关键词",
            ", ".join(article.keywords or []),
            "",
            "### 核心观点",
            "\n".join(f"- {x}" for x in (article.core_points or [])),
            "",
        ]
        path.write_text("\n".join(md), encoding="utf-8")
        return path

    def append_index(self, rows: List[Article]) -> None:
        """增量写入索引 CSV。"""

        write_header = not self.index_path.exists()
        with self.index_path.open("a", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["标题", "时间", "链接"])
            if write_header:
                writer.writeheader()
            for art in rows:
                if art.link in self._articles_seen:
                    continue
                writer.writerow({"标题": art.title, "时间": art.publish_time, "链接": art.link})
                self._articles_seen.add(art.link)

    def save_trae_kb(self, rows: List[Article], file_paths: List[Path]) -> Path:
        """将结果结构化保存到 Trae 技能知识文件。"""

        kb_path = self.kb_dir / "trae_skill_kb.jsonl"
        with kb_path.open("a", encoding="utf-8") as f:
            for art, md_path in zip(rows, file_paths):
                obj = asdict(art)
                obj["markdown_path"] = str(md_path)
                obj["ingested_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(json.dumps(obj, ensure_ascii=False) + "\n")
        return kb_path

    def push_to_hermes_kb(self, file_paths: List[Path]) -> Dict:
        """将 Markdown 结果逐篇推送到 Hermes `/hermes/learn/file`。"""

        ok = 0
        failed = []
        for path in file_paths:
            payload = {"path": str(path), "title": path.stem, "push_to_doubao": False}

            def _send():
                resp = requests.post(f"{DEFAULT_HERMES_URL}/hermes/learn/file", json=payload, timeout=45)
                resp.raise_for_status()
                return resp.json()

            try:
                retry_call(_send, retries=3)
                ok += 1
            except Exception as exc:  # noqa: BLE001
                failed.append({"path": str(path), "error": str(exc)})
            brief_sleep(0.2, 0.5)
        return {"ok": ok, "failed": failed, "total": len(file_paths)}

    def run(self, max_pages: Optional[int] = None, resume: bool = True) -> Dict:
        """执行全流程：抓元数据、抓正文、落地文件、同步知识库。"""

        metadata_rows = self.fetch_all_metadata(max_pages=max_pages, resume=resume)
        new_articles: List[Article] = []
        md_paths: List[Path] = []

        for row in metadata_rows:
            link = row["link"]
            if link in self._articles_seen:
                continue
            article = retry_call(
                lambda: self.fetch_article(row["title"], link, row.get("publish_time", "")),
                retries=3,
            )
            path = self.save_markdown(article)
            new_articles.append(article)
            md_paths.append(path)
            brief_sleep(0.8, 1.8)

        self.append_index(new_articles)
        kb_path = self.save_trae_kb(new_articles, md_paths)
        hermes_sync = self.push_to_hermes_kb(md_paths) if md_paths else {"ok": 0, "failed": [], "total": 0}
        report = {
            "status": "success",
            "mp_url": self.mp_url,
            "fetched_total": len(metadata_rows),
            "new_saved": len(new_articles),
            "output_dir": str(self.output_dir),
            "index_csv": str(self.index_path),
            "trae_kb": str(kb_path),
            "hermes_sync": hermes_sync,
            "generated_files": [str(p) for p in md_paths],
        }
        (self.output_dir / "last_run_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        return report


def normalize_datetime(value: str) -> str:
    """将字符串时间转成 `YYYYMMDD_HHMMSS`。"""

    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value[:19], fmt).strftime("%Y%m%d_%H%M%S")
        except Exception:
            continue
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def summarize_article(content: str, max_keywords: int = 12, max_points: int = 5) -> Tuple[List[str], List[str]]:
    """使用规则法提取关键词与核心观点。"""

    text = re.sub(r"\s+", " ", content or "").strip()
    if not text:
        return [], []

    token_pattern = re.compile(r"[A-Za-z][A-Za-z0-9_\-]{2,}|[\u4e00-\u9fff]{2,6}")
    tokens = [t.lower() for t in token_pattern.findall(text)]
    stopwords = {"我们", "你们", "他们", "这个", "那个", "以及", "如果", "但是", "就是", "已经", "可以", "进行", "一个"}
    freq: Dict[str, int] = {}
    for t in tokens:
        if t in stopwords:
            continue
        freq[t] = freq.get(t, 0) + 1
    keywords = [k for k, _ in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:max_keywords]]

    sentences = re.split(r"[。！？\n]", text)
    sentences = [s.strip() for s in sentences if len(s.strip()) >= 18]
    sentences.sort(key=len, reverse=True)
    core_points = sentences[:max_points]
    return keywords, core_points


def render_markdown_report(result: Dict) -> str:
    """将执行结果格式化成 Hermes 可直接展示的 Markdown。"""

    lines = [
        "# wechat_crawler_v1.1 执行结果",
        "",
        f"- 状态: {result.get('status')}",
        f"- 公众号入口: {result.get('mp_url')}",
        f"- 发现文章数: {result.get('fetched_total')}",
        f"- 新增落盘数: {result.get('new_saved')}",
        f"- 输出目录: {result.get('output_dir')}",
        f"- 索引文件: {result.get('index_csv')}",
        "",
        "## Hermes 知识库同步",
        "",
        f"- 成功: {(result.get('hermes_sync') or {}).get('ok', 0)}",
        f"- 总数: {(result.get('hermes_sync') or {}).get('total', 0)}",
    ]
    failed = (result.get("hermes_sync") or {}).get("failed") or []
    if failed:
        lines.extend(["", "## 同步失败", ""])
        for row in failed[:20]:
            lines.append(f"- {row.get('path')}: {row.get('error')}")
    return "\n".join(lines)


def run_skill(mp_url: str, max_pages: Optional[int] = None, resume: bool = True) -> Dict:
    """技能统一执行入口（供 `skill_entry.py` 调用）。"""

    ensure_socket_available()
    url_path = (urlparse(mp_url).path or "").strip()
    is_single_article = url_path.startswith("/s/")
    crawler = WechatCrawler(mp_url=mp_url)
    if is_single_article:
        ensure_dependencies(need_playwright=False)
        result = crawler.run_single_article()
    else:
        result = crawler.run(max_pages=max_pages, resume=resume)
    result["markdown"] = render_markdown_report(result)
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python main.py <mp_url>")
        raise SystemExit(1)
    mp_url_cli = sys.argv[1].strip()
    output = run_skill(mp_url_cli)
    print(json.dumps(output, ensure_ascii=False, indent=2))
