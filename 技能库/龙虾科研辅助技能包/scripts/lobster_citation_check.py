#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ARS 引用校验（零积分）v1.0 — 龙虾AI主控中心适配层

三层校验：
  L1 结构层：正文引用簇 与 参考文献表 是否一一对应（缺引 / 漏列 / 重复条目）
  L2 格式层：APA 7 常见格式问题（年份括号、et al.、DOI 链接、期刊名斜体标记）
  L3 存在性层：--verify 时联网核对 DOI / 标题是否真实存在（CrossRef + OpenAlex）
               这是拦截「AI 幻觉编造文献」的关键一层

用法：
  python ars_citation_check.py draft.md
  python ars_citation_check.py draft.md --verify           # 联网核对存在性（慢但必须做）
  python ars_citation_check.py draft.md --upstream         # 追加调用上游三层 lint 脚本

上游脚本（可选）：
  E:\\龙虾AI主控中心\\我的AI分身\\企业微信群定制接单项目\\skills\\research-suite\\
  skills\\academic-research-suite\\ars\\scripts\\check_v3_7_3_three_layer_citation.py
"""
import argparse
import os
import re
import sys
import time
import urllib.parse
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

UA = "lobster-ars-citation-check/1.0 (mailto:%s)" % os.environ.get("ARS_MAILTO", "ars-local@example.com")
UPSTREAM = (r"E:\龙虾AI主控中心\我的AI分身\企业微信群定制接单项目\skills\research-suite"
            r"\skills\academic-research-suite\ars\scripts\check_v3_7_3_three_layer_citation.py")

# 正文引用簇：(Smith, 2020) / (Smith & Lee, 2020) / (Smith et al., 2021) / Smith (2020)
IN_TEXT = re.compile(r"\(([A-Z\u4e00-\u9fff][^()]{0,120}?,\s*(?:19|20)\d{2}[a-z]?)\)"
                     r"|([A-Z\u4e00-\u9fff][A-Za-z\u4e00-\u9fff\-’']+)\s*\((?:19|20)\d{2}[a-z]?\)")
REF_LINE = re.compile(r"^\s*(?:[-*]\s*)?\[?\d{0,3}\]?\.?\s*(?P<body>.+)$")


def split_body(text):
    """把参考文献段落切成条目（按行；行过长时按句末年份切）。"""
    items = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        m = REF_LINE.match(s)
        body = m.group("body") if m else s
        if len(body) > 6:
            items.append(body)
    return items


def extract_year(item):
    m = re.search(r"\((19|20)\d{2}[a-z]?\)|\b(?:19|20)\d{2}[a-z]?\b", item)
    return m.group(0).strip("()") if m else ""


def surname(item):
    """参考文献条目的第一作者姓氏（英文取首个大写开头词，中文取前 4 字内的姓氏段）。"""
    head = item.split(",")[0] if "," in item[:40] else item
    m = re.match(r"^[\s\[\d.\]]*([A-Z][A-Za-z\-’' ]{1,30})", head)
    if m:
        return m.group(1).strip().split(" ")[0]
    m2 = re.match(r"^[\s\[\d.\]]*([\u4e00-\u9fff]{1,4})", head)
    return m2.group(1) if m2 else ""


def verify_doi(title):
    """联网核对标题是否真实存在；返回 (状态, 命中标题/DOI)。"""
    q = urllib.parse.quote(title[:120])
    for url, pick in (
        ("https://api.crossref.org/works?query.bibliographic=%s&rows=1&select=title,DOI" % q, "crossref"),
        ("https://api.openalex.org/works?search=%s&per-page=1" % q, "openalex"),
    ):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=25) as r:
                d = __import__("json").loads(r.read().decode("utf-8"))
            if pick == "crossref":
                its = d.get("message", {}).get("items", [])
                if its:
                    return True, (its[0].get("title") or [""])[0], its[0].get("DOI", "")
            else:
                res = d.get("results", [])
                if res:
                    return True, res[0].get("title", ""), (res[0].get("doi") or "")
        except Exception:  # noqa: BLE001
            continue
    return False, "", ""


def main():
    ap = argparse.ArgumentParser(description="ARS 零积分引用校验")
    ap.add_argument("files", nargs="+", help="待校验的 Markdown 文件")
    ap.add_argument("--verify", action="store_true", help="联网核对参考文献是否真实存在（强烈建议）")
    ap.add_argument("--upstream", action="store_true", help="追加调用上游 ARS 三层 lint 脚本")
    a = ap.parse_args()

    total_problem = 0
    for path in a.files:
        if not os.path.exists(path):
            print("文件不存在: %s" % path)
            continue
        raw = open(path, encoding="utf-8", errors="ignore").read()

        # 切分正文 / 参考文献
        m = re.search(r"^\s{0,3}#{1,6}\s*(参考文献|References|參考文獻| bibliography)\b.*$",
                      raw, re.I | re.M)
        body = raw[:m.start()] if m else raw
        refsec = raw[m.end():] if m else ""
        refs = split_body(refsec)

        print("\n=== %s ===" % os.path.basename(path))
        print("参考文献条目: %d | 正文引用簇: %d 处" % (len(refs), len(IN_TEXT.findall(body))))

        # L1 结构层
        cited = set()
        for cl in IN_TEXT.findall(body):
            seg = cl[0] or cl[1] or ""
            for part in re.split(r";|&|and", seg):
                y = extract_year(part)
                s = surname(part)
                if y:
                    cited.add((s.lower(), y))
        ref_keys = []
        for r in refs:
            ref_keys.append((surname(r).lower(), extract_year(r)))

        missing = [k for k in cited if k[1] and not any(rk[1] == k[1] and (not k[0] or rk[0].startswith(k[0][:4])) for rk in ref_keys)]
        unused = [r for r, k in zip(refs, ref_keys) if k[1] and not any(c[1] == k[1] and (not c[0] or k[0].startswith(c[0][:4])) for c in cited)]

        print("\n[L1 结构层]")
        if not refs:
            print("  ⚠ 未识别到参考文献区（需有 '参考文献' / 'References' 标题）")
        if missing:
            total_problem += len(missing)
            print("  ✗ 正文引用了但参考文献表查无对应（%d）：" % len(missing))
            for k in missing[:15]:
                print("      - %s %s" % (k[0] or "(未识别作者)", k[1]))
        else:
            print("  ✓ 正文引用均有对应参考文献（粗粒度匹配）")
        if unused:
            print("  · 参考文献表中未见正文引用（%d，可能是背景文献，需人工判断）：" % len(unused))
            for u in unused[:10]:
                print("      - %s" % u[:90])

        # L2 格式层
        print("\n[L2 格式层]")
        fmt = 0
        for r in refs:
            if not re.search(r"\((?:19|20)\d{2}", r) and not re.search(r"\b(?:19|20)\d{2}\b", r):
                fmt += 1
                print("  ! 缺少年份: %s" % r[:80])
            if "http" in r and "doi.org" not in r and not r.rstrip().endswith("."):
                print("  ! 链接结尾缺句号: %s" % r[:80])
        if not fmt:
            print("  ✓ 年份格式基本正常（深度 APA7 校对请用 --upstream）")
        total_problem += fmt

        # L3 存在性
        if a.verify:
            print("\n[L3 存在性层] 联网核对（每条间隔 1s，避免限流）")
            bad = 0
            for r in refs[:40]:
                time.sleep(1.0)
                ok, title, doi = verify_doi(r)
                mark = "✓" if ok else "✗ 未命中"
                print("  %s %s" % (mark, r[:70]))
                if ok:
                    print("      命中: %s%s" % (title[:70], (" | DOI:" + doi) if doi else ""))
                else:
                    bad += 1
            print("  未命中 %d 条 —— 未命中不等于造假，但必须人工逐条打开原文确认" % bad)
            total_problem += bad
        else:
            print("\n[L3 存在性层] 已跳过（强烈建议加 --verify 拦截幻觉文献）")

    if a.upstream and os.path.exists(UPSTREAM):
        print("\n=== 上游 ARS 三层 lint 追加执行 ===")
        import subprocess
        py = r"G:\g_venv_ars\Scripts\python.exe"
        if not os.path.exists(py):
            py = sys.executable
        r = subprocess.run([py, UPSTREAM] + a.files, capture_output=True, text=True,
                           encoding="utf-8", errors="ignore")
        print((r.stdout or "") + (r.stderr or ""))
    elif a.upstream:
        print("\n未找到上游脚本: %s" % UPSTREAM)

    print("\n" + "=" * 60)
    print("粗检问题数合计: %d" % total_problem)
    print("⚠ 本脚本为粗粒度匹配，不能替代人工逐条核验；所有统计量与引文必须人工复核。")


if __name__ == "__main__":
    main()
