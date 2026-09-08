#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ARS 文献检索（零积分）v1.0 — 龙虾AI主控中心适配层

直连四个完全免费的学术 API，无需密钥、不调用任何大模型积分：
  arxiv    https://export.arxiv.org/api/query
  openalex https://api.openalex.org/works   （建议设 ARS_MAILTO 进 polite pool）
  crossref https://api.crossref.org/works
  s2       https://api.semanticscholar.org/graph/v1/paper/search （无密钥有限流）

用法：
  python ars_lit_search.py --source arxiv    --q "large language model" --limit 10
  python ars_lit_search.py --source crossref --q "meta-analysis" --limit 5 --out refs.json
  python ars_lit_search.py --source all      --q "..." --limit 5 --cache .cache

铁律：本脚本只做检索，不做归纳。返回的每条文献标题/作者/年份/DOI 必须人工核验，
禁止凭空补全任何字段（见 ../风险提示与合规红线.md）。
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

UA_MAILTO = os.environ.get("ARS_MAILTO", "ars-local@example.com")
UA = "lobster-ars-lit-search/1.0 (mailto:%s)" % UA_MAILTO
TIMEOUT = 25


def _get(url, as_json=True, retries=2):
    last = None
    for i in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                raw = r.read()
            return json.loads(raw.decode("utf-8")) if as_json else raw
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1.5 * (i + 1))
    raise RuntimeError("请求失败: %s | %s" % (url, last))


def _clean(s):
    if not s:
        return ""
    s = re.sub(r"\s+", " ", str(s)).strip()
    return s


def search_arxiv(q, limit):
    url = ("https://export.arxiv.org/api/query?search_query=all:%s&max_results=%d"
           % (urllib.parse.quote(q), limit))
    raw = _get(url, as_json=False)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(raw)
    out = []
    for e in root.findall("a:entry", ns):
        out.append({
            "source": "arXiv",
            "title": _clean(e.findtext("a:title", "", ns)),
            "authors": [_clean(a.findtext("a:name", "", ns)) for a in e.findall("a:author", ns)][:8],
            "year": (_clean(e.findtext("a:published", "", ns)) or "")[:4],
            "venue": "arXiv preprint",
            "doi": _clean(e.findtext("{http://arxiv.org/schemas/atom}doi", "", ns)),
            "url": _clean(e.findtext("a:id", "", ns)),
            "abstract": _clean(e.findtext("a:summary", "", ns))[:600],
        })
    return out


def search_crossref(q, limit):
    url = ("https://api.crossref.org/works?query=%s&rows=%d&select=title,author,issued,"
           "container-title,DOI,URL,abstract" % (urllib.parse.quote(q), limit))
    d = _get(url)
    out = []
    for it in d.get("message", {}).get("items", []):
        out.append({
            "source": "CrossRef",
            "title": _clean((it.get("title") or [""])[0]),
            "authors": [_clean("%s %s" % (a.get("given", ""), a.get("family", "")))
                        for a in (it.get("author") or [])][:8],
            "year": str(((it.get("issued") or {}).get("date-parts") or [[""]])[0][0]),
            "venue": _clean((it.get("container-title") or [""])[0]),
            "doi": it.get("DOI", ""),
            "url": it.get("URL", "https://doi.org/%s" % it.get("DOI", "")),
            "abstract": _clean(re.sub(r"<[^>]+>", "", it.get("abstract", "") or ""))[:600],
        })
    return out


def search_openalex(q, limit):
    url = ("https://api.openalex.org/works?search=%s&per-page=%d&mailto=%s"
           % (urllib.parse.quote(q), limit, urllib.parse.quote(UA_MAILTO)))
    d = _get(url)
    out = []
    for it in d.get("results", []):
        out.append({
            "source": "OpenAlex",
            "title": _clean(it.get("title")),
            "authors": [_clean(a.get("author", {}).get("display_name"))
                        for a in (it.get("authorships") or [])][:8],
            "year": str(it.get("publication_year", "")),
            "venue": _clean(((it.get("primary_location") or {}).get("source") or {}).get("display_name")),
            "doi": _clean(it.get("doi")),
            "url": _clean(it.get("doi") or it.get("id")),
            "abstract": _clean(it.get("abstract") or "")[:600],
        })
    return out


def search_s2(q, limit):
    url = ("https://api.semanticscholar.org/graph/v1/paper/search?query=%s&limit=%d"
           "&fields=title,year,venue,abstract,externalIds,authors,url"
           % (urllib.parse.quote(q), limit))
    d = _get(url)
    out = []
    for it in d.get("data", []) or []:
        ids = it.get("externalIds") or {}
        out.append({
            "source": "SemanticScholar",
            "title": _clean(it.get("title")),
            "authors": [_clean(a.get("name")) for a in (it.get("authors") or [])][:8],
            "year": str(it.get("year", "")),
            "venue": _clean(it.get("venue")),
            "doi": _clean(ids.get("DOI")),
            "url": _clean(it.get("url") or ("https://doi.org/%s" % ids.get("DOI", "") if ids.get("DOI") else "")),
            "abstract": _clean(it.get("abstract") or "")[:600],
        })
    return out


SOURCES = {"arxiv": search_arxiv, "crossref": search_crossref,
           "openalex": search_openalex, "s2": search_s2}


def main():
    ap = argparse.ArgumentParser(description="ARS 零积分文献检索")
    ap.add_argument("--source", default="all",
                    choices=["arxiv", "crossref", "openalex", "s2", "all"])
    ap.add_argument("--q", required=True, help="检索关键词（英文命中率更高）")
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--out", default="", help="结果另存为 JSON 文件路径")
    ap.add_argument("--cache", default="", help="缓存目录（可选）")
    ap.add_argument("--abstract", action="store_true", help="输出含摘要")
    a = ap.parse_args()

    names = list(SOURCES) if a.source == "all" else [a.source]
    all_rows, errors = [], []
    for n in names:
        try:
            rows = SOURCES[n](a.q, a.limit)
            all_rows.extend(rows)
            print("[%s] 命中 %d 条" % (n, len(rows)))
        except Exception as e:  # noqa: BLE001
            errors.append("%s: %s" % (n, e))
            print("[%s] 失败：%s" % (n, str(e)[:160]))

    # 按 DOI 去重
    seen, uniq = set(), []
    for r in all_rows:
        k = (r.get("doi") or r.get("title") or "").lower()
        if k and k in seen:
            continue
        seen.add(k)
        uniq.append(r)

    print("\n共 %d 条（已去重）\n" % len(uniq))
    print("%-4s %-6s %-18s %-60s %s" % ("#", "年份", "来源", "标题", "DOI/URL"))
    print("-" * 130)
    for i, r in enumerate(uniq, 1):
        t = r["title"][:58]
        print("%-4d %-6s %-18s %-60s %s" % (i, r["year"], r["source"], t, r.get("doi") or r.get("url", "")[:40]))
        if a.abstract and r.get("abstract"):
            print("     摘要: %s" % r["abstract"][:200])

    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(uniq, f, ensure_ascii=False, indent=2)
        print("\n已保存: %s" % os.path.abspath(a.out))

    if a.cache:
        os.makedirs(a.cache, exist_ok=True)
        safe = re.sub(r"[^\w\-]+", "_", a.q)[:60]
        p = os.path.join(a.cache, "lit_%s_%s.json" % (safe, time.strftime("%Y%m%d")))
        with open(p, "w", encoding="utf-8") as f:
            json.dump(uniq, f, ensure_ascii=False, indent=2)
        print("已缓存: %s" % p)

    if errors:
        print("\n⚠ 部分数据源失败（不影响已得结果）：\n  " + "\n  ".join(errors))
    print("\n⚠ 人工核验：标题/作者/年份/DOI 必须与原文逐条核对，禁止直接引用未核实条目。")


if __name__ == "__main__":
    main()
