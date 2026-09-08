from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests


def _skill_dir() -> Path:
    return Path(__file__).resolve().parent


def _project_root() -> Path:
    skill_dir = _skill_dir()
    if skill_dir.parent.name == "skills" and skill_dir.parent.parent.name in (".trae", ".hermes"):
        return skill_dir.parent.parent.parent
    return skill_dir.parent


def _core_dir() -> Path:
    return _project_root() / "核心程序"


def _data_dir() -> Path:
    return _core_dir() / "data"


def _default_config_path() -> Path:
    return _data_dir() / "collector_five_in_one_sources.json"


def _default_state_path() -> Path:
    return _data_dir() / "collector_five_in_one_state.json"


def _archive_root() -> Path:
    return _data_dir() / "archive" / "collector_five_in_one"


def _load_json(path: Path) -> Any:
    try:
        if not path.is_file():
            return None
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _atomic_write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(str(tmp), str(path))


def _load_json_env(env_name: str) -> Optional[dict]:
    try:
        raw = (os.environ.get(env_name, "") or "").strip()
        if not raw:
            return None
        obj = json.loads(raw)
        return obj if isinstance(obj, dict) else None
    except Exception:
        return None


def _sha256_text(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8", errors="ignore")).hexdigest()


def _slug(s: str, max_len: int = 60) -> str:
    t = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff_-]+", "_", (s or "").strip())
    t = t.strip("_")
    return (t[:max_len] if t else "item")


def _today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def _hermes_base_url() -> str:
    return (os.environ.get("HERMES_BASE_URL", "") or "http://127.0.0.1:8080").strip()


def _hermes_headers() -> Dict[str, str]:
    headers: Dict[str, str] = {"Content-Type": "application/json"}
    token = (os.environ.get("HERMES_API_TOKEN", "") or "").strip()
    header_name = (os.environ.get("HERMES_API_TOKEN_HEADER", "X-API-Token") or "X-API-Token").strip()
    if token:
        if header_name.lower() == "authorization":
            headers["Authorization"] = f"Bearer {token}"
        else:
            headers[header_name] = token
    return headers


def _push_file_to_hermes_kb(path: Path, title: str, push_to_doubao: bool) -> Tuple[bool, str]:
    try:
        r = requests.post(
            f"{_hermes_base_url().rstrip('/')}/hermes/learn/file",
            headers=_hermes_headers(),
            json={"path": str(path), "title": title, "push_to_doubao": bool(push_to_doubao)},
            timeout=20,
        )
        ok = bool(200 <= r.status_code < 300)
        return ok, (r.text or "")[:500]
    except Exception as e:
        return False, str(e)


def _load_fetch_text_func():
    core_dir = _core_dir()
    if str(core_dir) not in sys.path:
        sys.path.insert(0, str(core_dir))
    try:
        from hermes_sources import fetch_text_from_url  # type: ignore

        return fetch_text_from_url, ""
    except Exception as e:
        return None, str(e)


def _cookies_to_cookie_header(cookies: dict) -> str:
    parts = []
    for k, v in (cookies or {}).items():
        if not isinstance(k, str) or not isinstance(v, str):
            continue
        if not k:
            continue
        parts.append(f"{k}={v}")
    return "; ".join(parts)


def _merge_headers_and_cookies(headers: Optional[dict], cookies: Optional[dict]) -> Dict[str, str]:
    h: Dict[str, str] = {}
    if isinstance(headers, dict):
        for k, v in headers.items():
            if isinstance(k, str) and isinstance(v, str) and k.strip():
                h[k.strip()] = v
    if isinstance(cookies, dict):
        has_cookie = any(k.lower() == "cookie" for k in h.keys())
        if not has_cookie:
            ck = _cookies_to_cookie_header(cookies)
            if ck:
                h["Cookie"] = ck
    return h


def _fetch_text_requests(url: str, cookies=None, headers=None) -> Tuple[str, Dict[str, Any]]:
    fn, err = _load_fetch_text_func()
    if not fn:
        raise RuntimeError(err or "fetch_text_from_url 不可用")
    text, meta = fn(url, cookies=cookies, headers=headers)
    return (text or ""), (meta or {})


def _ytdlp_extract(url: str) -> Optional[Dict[str, Any]]:
    try:
        import yt_dlp  # type: ignore

        ydl_opts = {"quiet": True, "skip_download": True, "extract_flat": False, "nocheckcertificate": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return info if isinstance(info, dict) else None
    except Exception:
        pass

    try:
        cmd = [sys.executable, "-m", "yt_dlp", "--skip-download", "-J", url]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            return None
        obj = json.loads(r.stdout or "{}")
        return obj if isinstance(obj, dict) else None
    except Exception:
        return None


def _text_from_ytdlp(info: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    title = str(info.get("title") or info.get("fulltitle") or "").strip()
    desc = str(info.get("description") or "").strip()
    uploader = str(info.get("uploader") or info.get("uploader_id") or "").strip()
    upload_date = str(info.get("upload_date") or "").strip()
    webpage_url = str(info.get("webpage_url") or info.get("original_url") or info.get("url") or "").strip()
    tags = info.get("tags") if isinstance(info.get("tags"), list) else []
    pieces = []
    if title:
        pieces.append(f"标题：{title}")
    if uploader:
        pieces.append(f"作者：{uploader}")
    if upload_date:
        pieces.append(f"日期：{upload_date}")
    if webpage_url:
        pieces.append(f"链接：{webpage_url}")
    if tags:
        pieces.append("标签：" + ", ".join([str(x) for x in tags[:30]]))
    if desc:
        pieces.append("")
        pieces.append("正文：")
        pieces.append(desc)
    text = "\n".join([p for p in pieces if p is not None]).strip()
    meta = {
        "title": title,
        "uploader": uploader,
        "upload_date": upload_date,
        "webpage_url": webpage_url,
        "extractor": info.get("extractor"),
        "id": info.get("id"),
        "duration": info.get("duration"),
    }
    return text, meta


def _playwright_available() -> bool:
    return importlib.util.find_spec("playwright") is not None


def _browser_fetch_text(
    url: str,
    engine: str,
    channel: Optional[str],
    user_data_dir: Optional[str],
    headers: Optional[dict],
    cookies: Optional[dict],
    headless: bool,
) -> Tuple[str, Dict[str, Any]]:
    if not _playwright_available():
        raise RuntimeError("playwright 未安装，无法使用 browser 方法")
    from playwright.sync_api import sync_playwright  # type: ignore

    engine = (engine or "chromium").strip().lower()
    if engine not in ("chromium", "firefox", "webkit"):
        engine = "chromium"
    channel = (channel or "").strip() or None
    user_data_dir = (user_data_dir or "").strip() or None

    merged_headers = _merge_headers_and_cookies(headers=headers, cookies=cookies)
    ua = merged_headers.get("User-Agent") or merged_headers.get("user-agent")
    viewport = {"width": 1280, "height": 800}

    with sync_playwright() as p:
        browser_type = getattr(p, engine)
        if user_data_dir:
            ctx = browser_type.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=bool(headless),
                viewport=viewport,
                channel=channel if (engine == "chromium" and channel) else None,
            )
        else:
            browser = browser_type.launch(headless=bool(headless), channel=channel if (engine == "chromium" and channel) else None)
            ctx = browser.new_context(viewport=viewport, user_agent=ua, extra_http_headers=merged_headers or None)
        page = ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        try:
            page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            pass
        title = ""
        try:
            title = (page.title() or "").strip()
        except Exception:
            title = ""
        text = ""
        try:
            text = (page.inner_text("body") or "").strip()
        except Exception:
            try:
                text = (page.content() or "").strip()
            except Exception:
                text = ""
        try:
            ctx.close()
        except Exception:
            pass
    return text, {"title": title, "engine": engine, "channel": channel or "", "final_url": url, "content_type": "text/html"}


def _load_wechat_crawler_func():
    root = _project_root()
    skill_path = root / ".hermes" / "skills" / "wechat_crawler_v1.1" / "skill_entry.py"
    if not skill_path.is_file():
        return None, f"技能文件不存在: {skill_path}"
    try:
        spec = importlib.util.spec_from_file_location("wechat_crawler_skill_entry", str(skill_path))
        if not spec or not spec.loader:
            return None, "技能加载失败: spec 初始化异常"
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        fn = getattr(module, "skill_wechat_crawler_json", None)
        if not callable(fn):
            fn = getattr(module, "skill_wechat_crawler", None)
        if not callable(fn):
            return None, "技能入口不存在: skill_wechat_crawler(_json)"
        return fn, ""
    except Exception as e:
        return None, str(e)


def _write_markdown(kind: str, title: str, url: str, body: str, meta: Dict[str, Any]) -> Path:
    out_dir = _archive_root() / _slug(kind, 40)
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    name = f"{ts}_{_slug(title or url, 60)}.md"
    path = out_dir / name
    md = []
    md.append(f"# {title}".strip() if title else f"# {_slug(url, 80)}")
    md.append("")
    md.append(f"- 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md.append(f"- 类型：{kind}")
    md.append(f"- 来源：{url}")
    md.append("")
    if body:
        md.append(body.strip())
        md.append("")
    md.append("## 元信息")
    md.append("")
    md.append("```json")
    md.append(json.dumps(meta or {}, ensure_ascii=False, indent=2))
    md.append("```")
    path.write_text("\n".join(md), encoding="utf-8")
    return path


def run_skill(
    mode: str = "auto",
    rounds: int = 1,
    override_daily_cap: bool = False,
    notify: bool = False,
    config_path: Optional[str] = None,
) -> Dict[str, Any]:
    cfg_path = Path(config_path).resolve() if config_path else _default_config_path()
    state_path = _default_state_path()
    cfg = _load_json(cfg_path) or {}
    sources = cfg.get("sources") if isinstance(cfg.get("sources"), list) else []
    if not sources:
        return {"status": "skipped", "reason": "no_sources", "mode": str(mode or "auto"), "config_path": str(cfg_path)}

    state = _load_json(state_path) or {}
    seen_hashes = state.get("seen_hashes") if isinstance(state.get("seen_hashes"), list) else []
    seen_hashes = [str(x) for x in seen_hashes if isinstance(x, str)]
    url_hashes = state.get("url_hashes") if isinstance(state.get("url_hashes"), dict) else {}
    url_hashes = {str(k): str(v) for k, v in url_hashes.items() if isinstance(k, str) and isinstance(v, str)}

    today = _today()
    last_auto_date = str(state.get("last_auto_date") or "").strip()
    last_any_date = str(state.get("last_any_date") or "").strip()

    if mode == "auto" and last_auto_date == today:
        return {"status": "skipped", "reason": "already_ran_today", "mode": mode, "date": today}

    if mode == "manual" and (not override_daily_cap) and last_any_date == today:
        return {"status": "skipped", "reason": "daily_cap_reached", "mode": mode, "date": today}

    rounds = int(rounds or 1)
    rounds = max(1, min(rounds, 3))

    default_engine = (os.environ.get("HERMES_BROWSER_ENGINE", "") or "chromium").strip().lower() or "chromium"
    default_channel = (os.environ.get("HERMES_BROWSER_CHANNEL", "") or "").strip() or None
    default_user_data_dir = (os.environ.get("HERMES_BROWSER_USER_DATA_DIR", "") or "").strip() or None

    wechat_fn, wechat_err = _load_wechat_crawler_func()
    results: List[Dict[str, Any]] = []
    added_files: List[str] = []
    added_kb: List[Dict[str, Any]] = []

    for _ in range(rounds):
        for s in sources[:300]:
            if not isinstance(s, dict):
                continue
            st = str(s.get("type") or "").strip() or "web"
            title = str(s.get("title") or "").strip()
            url = str(s.get("url") or "").strip()
            mp_url = str(s.get("mp_url") or "").strip()
            method = str(s.get("method") or "auto").strip().lower()

            cookies = s.get("cookies") if isinstance(s.get("cookies"), dict) else None
            headers = s.get("headers") if isinstance(s.get("headers"), dict) else None
            cookies_env = str(s.get("cookies_env") or "").strip()
            headers_env = str(s.get("headers_env") or "").strip()
            if cookies_env:
                cookies = _load_json_env(cookies_env) or cookies
            if headers_env:
                headers = _load_json_env(headers_env) or headers

            if st in ("wechat", "wechat_mp", "公众号"):
                if not mp_url and url:
                    mp_url = url
                if (not mp_url) or ("mp.weixin.qq.com" not in mp_url):
                    results.append({"type": st, "status": "error", "msg": "mp_url 无效", "source": s})
                    continue
                if not wechat_fn:
                    results.append({"type": st, "status": "error", "msg": wechat_err or "wechat_crawler 不可用", "mp_url": mp_url})
                    continue
                try:
                    max_pages = s.get("max_pages")
                    resume = bool(s.get("resume", True))
                    out = wechat_fn(mp_url=mp_url, max_pages=max_pages, resume=resume)
                    results.append({"type": st, "status": "success", "mp_url": mp_url, "result": out})
                except Exception as e:
                    results.append({"type": st, "status": "error", "mp_url": mp_url, "msg": str(e)})
                time.sleep(0.6)
                continue

            if not url:
                results.append({"type": st, "status": "skipped", "reason": "empty_url", "source": s})
                continue

            browser_engine = str(s.get("browser_engine") or default_engine).strip().lower() or "chromium"
            browser_channel = str(s.get("browser_channel") or "").strip() or default_channel
            headless = bool(s.get("headless", True))

            text = ""
            meta: Dict[str, Any] = {"source": {"type": st, "url": url, "method": method}}

            try:
                if method in ("ytdlp", "yt-dlp", "video"):
                    info = _ytdlp_extract(url)
                    if info:
                        text, ym = _text_from_ytdlp(info)
                        meta["ytdlp"] = ym
                elif method == "browser":
                    text, bm = _browser_fetch_text(
                        url=url,
                        engine=browser_engine,
                        channel=browser_channel,
                        user_data_dir=default_user_data_dir,
                        headers=headers,
                        cookies=cookies,
                        headless=headless,
                    )
                    meta["browser"] = bm
                elif method == "html":
                    t, m = _fetch_text_requests(url, cookies=cookies, headers=headers)
                    text = t
                    meta["fetch"] = m
                else:
                    info = _ytdlp_extract(url)
                    if info:
                        text, ym = _text_from_ytdlp(info)
                        meta["ytdlp"] = ym
                    if not text:
                        t, m = _fetch_text_requests(url, cookies=cookies, headers=headers)
                        text = t
                        meta["fetch"] = m
                    if not text and _playwright_available():
                        text, bm = _browser_fetch_text(
                            url=url,
                            engine=browser_engine,
                            channel=browser_channel,
                            user_data_dir=default_user_data_dir,
                            headers=headers,
                            cookies=cookies,
                            headless=headless,
                        )
                        meta["browser"] = bm
            except Exception as e:
                results.append({"type": st, "status": "error", "url": url, "msg": str(e)})
                continue

            if not title:
                title = str(((meta.get("fetch") or {}).get("title") if isinstance(meta.get("fetch"), dict) else "") or "").strip()
                if not title:
                    title = str(((meta.get("browser") or {}).get("title") if isinstance(meta.get("browser"), dict) else "") or "").strip()
                if not title:
                    title = str(((meta.get("ytdlp") or {}).get("title") if isinstance(meta.get("ytdlp"), dict) else "") or "").strip()
                title = title or url

            if not text:
                results.append({"type": st, "status": "skipped", "reason": "empty_content", "url": url})
                continue

            text = text.strip()
            if len(text) > 25000:
                text = text[:25000]

            content_hash = _sha256_text(text)
            if content_hash in seen_hashes:
                results.append({"type": st, "status": "skipped", "reason": "dup_hash", "url": url})
                continue

            prev_hash = url_hashes.get(url)
            if prev_hash and prev_hash == content_hash:
                results.append({"type": st, "status": "skipped", "reason": "no_change", "url": url})
                continue

            meta["content_hash"] = content_hash
            out_path = _write_markdown(kind=st, title=title, url=url, body=text, meta=meta)
            added_files.append(str(out_path))

            ok, msg = _push_file_to_hermes_kb(out_path, title=title, push_to_doubao=bool(notify))
            added_kb.append({"path": str(out_path), "ok": ok, "msg": msg[:200]})

            url_hashes[url] = content_hash
            seen_hashes.append(content_hash)
            if len(seen_hashes) > 5000:
                seen_hashes = seen_hashes[-4500:]

            results.append({"type": st, "status": "success", "url": url, "path": str(out_path), "kb_ok": ok})
            time.sleep(0.6)

    state["seen_hashes"] = seen_hashes
    state["url_hashes"] = url_hashes
    state["last_any_date"] = today
    if mode == "auto":
        state["last_auto_date"] = today
    _atomic_write_json(state_path, state)

    return {
        "status": "success",
        "skill_version": "v2.0",
        "mode": mode,
        "date": today,
        "config_path": str(cfg_path),
        "state_path": str(state_path),
        "added_files": added_files,
        "kb_results": added_kb,
        "results": results,
        "cap": {"daily_auto": 1, "rounds_max": 3},
    }

