# -*- coding: utf-8 -*-
"""dump_biji_write_api.py —— 提取写笔记/标签的完整端点与请求体字段"""
import sys, re, urllib.request

sys.stdout.reconfigure(encoding="utf-8")

req = urllib.request.Request(
    "https://imgcdn.umiwi.com/fe-static/prod/home/js/home.f6b291ae.mjs",
    headers={"User-Agent": "Mozilla/5.0"})
s = urllib.request.urlopen(req, timeout=120).read().decode("utf-8", "ignore")

# 所有 /voicenotes/web/* 端点
eps = sorted(set(re.findall(r'url:"\.concat\([^)]*?"(/voicenotes/web/[a-zA-Z0-9/_\-]*)"', s)))
print(f"=== /voicenotes/web/* 端点 ({len(eps)}) ===")
for e in eps:
    print("  ", e)

# 所有 /v1/web/* 端点
eps2 = sorted(set(re.findall(r'url:"\.concat\([^)]*?"(/v1/web/[a-zA-Z0-9/_\-]*)"', s)))
print(f"\n=== /v1/web/* 端点 ({len(eps2)}) ===")
for e in eps2[:60]:
    print("  ", e)

print("\n=== createNote / 标签绑定 上下文 ===")
for kw in ["createNote:", "addTag", "bindTopic", "noteTopics", "topics/notes", "fetchTagO"]:
    m = re.search(re.escape(kw), s)
    if m:
        print(f"--- {kw} ---")
        print(repr(s[max(0, m.start() - 200):m.start() + 500]))
        print()
