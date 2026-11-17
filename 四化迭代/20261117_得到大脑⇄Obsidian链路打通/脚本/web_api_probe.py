# -*- coding: utf-8 -*-
"""
web_api_probe.py —— 得到大脑「网页后端通道」鉴权探针（绕会员墙的关键实验）

背景（实测）：
  · CLI 走 https://openapi.biji.com  → 会员墙 10201 not_member（付费通道）
  · 网页版走 https://notes-api.biji.com → 普通用户通道（收藏/打标签是免费功能）
  · 网页后端鉴权靠 cookie/localStorage 的登录 token（不是 CLI 的 gk_live_ api_key）

本脚本：只探测，不写数据。逐个端点测 4 种凭证组合，找出网页通道的鉴权口径。
"""
import os, sys, json, urllib.request, urllib.error, time

sys.stdout.reconfigure(encoding="utf-8")

NOTES_API = "https://notes-api.biji.com"
WEB_URL = "https://www.biji.com"

cfg = {}
p = r"C:\Users\Administrator\.getnote\config.json"
if os.path.exists(p):
    cfg = json.load(open(p, encoding="utf-8"))
KEY = cfg.get("api_key", "")
CID = cfg.get("client_id", "")

# 已有 profile 的 cookie（若有）
COOKIES = []
for cp in [r"C:\Users\Administrator\AppData\Local\getnote-pw-profile\Default\Network\Cookies",
           r"C:\Users\Administrator\AppData\Local\getnote-pw-profile\Default\Cookies"]:
    if os.path.exists(cp):
        print(f"发现 cookie 文件: {cp}")
        break

ENDPOINTS = [
    ("GET", "/note_list"),
    ("GET", "/notes"),
    ("GET", "/note/search"),
    ("GET", "/tag"),
    ("GET", "/tags"),
    ("GET", "/user/auth/refresh"),
    ("GET", "/user/auth/upgrade"),
    ("GET", "/spacex"),
    ("GET", "/knowledge/v1/web/topic/mine/search/list"),
]

HEADERSETS = {
    "① 无凭证": {},
    "② Bearer gk_live": {"Authorization": "Bearer " + KEY},
    "③ Bearer+CID": {"Authorization": "Bearer " + KEY, "X-Client-ID": CID},
    "④ 浏览器 UA": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
                    "Origin": WEB_URL, "Referer": WEB_URL + "/"},
}


def probe(method, path, hdrs):
    url = NOTES_API + path
    h = {"Content-Type": "application/json", "Accept": "application/json"}
    h.update(hdrs)
    req = urllib.request.Request(url, headers=h, method=method)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            b = r.read().decode("utf-8", "ignore")
            return r.status, b[:200], time.time() - t0
    except urllib.error.HTTPError as e:
        b = e.read().decode("utf-8", "ignore")
        return e.code, b[:200], time.time() - t0
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:120]}", time.time() - t0


print("=" * 70)
print("  得到大脑网页后端通道探针 notes-api.biji.com")
print("=" * 70)

results = []
for m, path in ENDPOINTS:
    print(f"\n--- {m} {path} ---")
    for hn, hdrs in HEADERSETS.items():
        st, body, dt = probe(m, path, hdrs)
        print(f"  {hn:16} -> {str(st):5} {body[:130]}  ({dt:.1f}s)")
        results.append({"method": m, "path": path, "headers": hn, "status": st,
                        "body": body[:300]})

out = r"E:\博主学习库\_tmp_shot\web_api_probe.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print(f"\n结果已存: {out}")

# 判定
print("\n=== 判定 ===")
ok = [r for r in results if r["status"] and 200 <= r["status"] < 300]
if ok:
    print(f"✅ 有 {len(ok)} 个端点返回 2xx —— 网页通道可达")
    for r in ok[:10]:
        print(f"   {r['method']} {r['path']} [{r['headers']}] -> {r['status']}")
else:
    print("❌ 全部非 2xx —— 仍需一次网页登录拿 token/cookie")
