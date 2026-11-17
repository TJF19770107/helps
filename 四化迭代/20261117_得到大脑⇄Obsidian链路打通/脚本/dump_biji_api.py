# -*- coding: utf-8 -*-
"""dump_biji_api.py —— 从得到大脑网页 JS 提取真实后端端点（绕会员墙用）"""
import sys, re, urllib.request, json

sys.stdout.reconfigure(encoding="utf-8")

URLS = [
    "https://imgcdn.umiwi.com/fe-static/prod/home/js/home.f6b291ae.mjs",
    "https://imgcdn.umiwi.com/fe-static/prod/home/js/chunk-vendors.fcec45e4.mjs",
]

PATTERNS = [
    r'h5:\{url:"([^"]{2,90})"',
    r'url:"(/[a-zA-Z0-9/_\-\{\}\.\$]{3,80})"',
    r'url:"(/[a-zA-Z0-9/_\-\{\}\.\$]{3,80})"',
    r'"(/[a-z][a-zA-Z0-9/_\-\{\}\.\$]{3,80})"',
]

allp = set()
for u in URLS:
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        t = urllib.request.urlopen(req, timeout=120).read().decode("utf-8", "ignore")
    except Exception as e:
        print(f"❌ {u}: {e}")
        continue
    print(f"✅ {u}  len={len(t)}")
    for pat in PATTERNS:
        allp.update(re.findall(pat, t))

# 过滤成像后端路径的（不含明显的静态资源/前端路由特征）
keep = []
for p in sorted(allp):
    if not p.startswith("/"):
        continue
    if any(x in p for x in [".js", ".css", ".png", ".svg", ".gif", ".jpg", ".webp", ".woff"]):
        continue
    if len(p) < 6:
        continue
    keep.append(p)

print(f"\n候选后端路径 {len(keep)} 条：")
for p in keep:
    print("  ", p)

out = r"E:\博主学习库\_tmp_shot\biji_api_paths.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(keep, f, ensure_ascii=False, indent=1)
print(f"\n已存: {out}")
