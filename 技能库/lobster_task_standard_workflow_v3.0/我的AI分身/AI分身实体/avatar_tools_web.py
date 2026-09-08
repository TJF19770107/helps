# -*- coding: utf-8 -*-
"""avatar_tools_web.py · Firecrawl / 内置抓取 网页工具
有 FIRECRAWL_API_KEY（fc- 开头）→ 走 Firecrawl 云端（清洗后 Markdown）。
无 key → 内置 urllib 抓取 + 去标签提取文本（零成本可用）。
用法：!web <网址>
"""
import os, re, html as _html, json, urllib.request

def _fallback(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=40) as r:
        raw = r.read().decode("utf-8", "replace")
    txt = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", raw)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = _html.unescape(re.sub(r"\s+", " ", txt)).strip()
    return txt

def web_fetch(url):
    url = (url or "").strip()
    if not url:
        return "用法: !web <网址>"
    if not url.startswith("http"):
        url = "https://" + url
    key = os.environ.get("FIRECRAWL_API_KEY", "").strip()
    if key and key.startswith("fc-"):
        try:
            body = json.dumps({"url": url, "formats": ["markdown"]}).encode("utf-8")
            req = urllib.request.Request("https://api.firecrawl.dev/v1/scrape", data=body,
                                         headers={"Authorization": "Bearer " + key,
                                                  "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as r:
                d = json.loads(r.read().decode("utf-8"))
            md = (d.get("data", {}).get("markdown") or d.get("markdown") or json.dumps(d))
            return "Firecrawl: " + md[:3000]
        except Exception as e:
            return "Firecrawl失败(%s)，改用内置抓取: %s" % (type(e).__name__, _fallback(url)[:2000])
    return "内置抓取: " + _fallback(url)[:3000]


def register():
    import avatar
    avatar.TOOLS["web"] = (web_fetch, "联网抓网页：web <网址>（Firecrawl清洗，无key用内置抓取）")

if __name__ == "__main__":
    import sys
    print(web_fetch(sys.argv[1] if len(sys.argv) > 1 else ""))