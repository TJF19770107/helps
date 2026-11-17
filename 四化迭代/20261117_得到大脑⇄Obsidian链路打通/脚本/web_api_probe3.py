# -*- coding: utf-8 -*-
"""
web_api_probe3.py —— 摸清网页 token 的携带方式（只读 GET，不写数据）

已定位：
  · 端点 https://notes-api.biji.com/voicenotes/web/notes → 400 {"message":"ParseTokenFailed"}
    （= 路径正确，只是没有 token；不是会员墙！）
  · 网页 JS 里 Authorization 头形如 "Bearer " + <token>

关键问题：token 从哪来？
  · 网页登录后存 localStorage（JS 里 c.b3.refreshToken() / needsRefresh()）
  · 也可能是 cookie

本脚本：把 CLI 的 gk_live api_key 各种形态都塞进 Authorization 试一遍，
        确认「会员墙」到底是不是「token 形态不对」。
"""
import sys, json, urllib.request, urllib.error

sys.stdout.reconfigure(encoding="utf-8")

cfg = json.load(open(r"C:\Users\Administrator\.getnote\config.json", encoding="utf-8"))
KEY = cfg["api_key"]
CID = cfg["client_id"]

URL = "https://notes-api.biji.com/voicenotes/web/notes?page=1&page_size=1"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")

CANDIDATES = {
    "① Bearer gk_live_...": {"Authorization": "Bearer " + KEY},
    "② Raw gk_live_...": {"Authorization": KEY},
    "③ Bearer client_id": {"Authorization": "Bearer " + CID},
    "④ X-Token": {"X-Token": KEY},
    "⑤ Token 头": {"Token": KEY},
    "⑥ Cookie auth": {"Cookie": f"auth_token={KEY}"},
    "⑦ Cookie token": {"Cookie": f"token={KEY}"},
    "⑧ Bearer + CID + UA": {"Authorization": "Bearer " + KEY, "X-Client-ID": CID},
    "⑨ Bearer + Referer": {"Authorization": "Bearer " + KEY,
                            "Origin": "https://www.biji.com",
                            "Referer": "https://www.biji.com/"},
    "⑩ Bearer gk_live (api-key 头)": {"Authorization": "Bearer " + KEY, "api-key": KEY},
}


def get(hdrs):
    h = {"User-Agent": UA, "Accept": "application/json"}
    h.update(hdrs)
    req = urllib.request.Request(URL, headers=h, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, r.read().decode("utf-8", "ignore")[:260]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "ignore")[:260]
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:100]}"


print("=" * 72)
print("  得到大脑网页 token 携带方式探针")
print(f"  端点: {URL}")
print("=" * 72)
for name, h in CANDIDATES.items():
    st, body = get(h)
    print(f"  {name:30} -> {str(st):5} {body[:150]}")
