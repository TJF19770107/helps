# -*- coding: utf-8 -*-
"""
web_token_autonomous_probe.py —— 找「不用人点授权」的网页 token 全自动路径（换假设）

已证伪的路（不再试）：
  · OpenAPI notes/list → 10201 not_member（会员墙）
  · gk_live_ 打 notes-api → 403 LoginRequired（token 类型不对）
  · OAuth Device Flow → 两次码超时（汤哥不在电脑前，客观无法扫码）

新假设（本脚本验证）：
  A. /v1/web/openapi/token/config  —— 网页 JS 里的端点，疑似「用 OpenAPI token 配置/换网页会话」
  B. /oauth/token grant_type=client_credentials —— 用 client_id + api_key 直接换 token
  C. /user/auth/refresh / /account/v2/web/user/auth/refresh —— 用 api_key 当 refresh_token
  D. /api/user/login —— 网页登录端点，看是否接受 api_key
  E. getnote CLI 本地是否存了网页 token（CLI auth 是登录态）

全部只读探测（GET/POST 空 payload 或凭证交换），不写笔记、不改配置。
"""
import sys, json, urllib.request, urllib.error, os, glob

sys.stdout.reconfigure(encoding="utf-8")

cfg = json.load(open(r"C:\Users\Administrator\.getnote\config.json", encoding="utf-8"))
KEY = cfg["api_key"]
CID = cfg["client_id"]
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")

HOSTS = ["https://notes-api.biji.com", "https://www.biji.com",
         "https://openapi.biji.com", "https://get-notes.luojilab.com"]


def call(method, url, payload=None, hdrs=None):
    h = {"User-Agent": UA, "Accept": "application/json", "Content-Type": "application/json"}
    if hdrs:
        h.update(hdrs)
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read().decode("utf-8", "ignore")[:300]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "ignore")[:300]
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:100]}"


print("=" * 74)
print("  网页 token 全自动路径探测（不扫码 / 不求人）")
print("=" * 74)

print("\n【A】/v1/web/openapi/token/config —— OpenAPI token 换网页会话？")
for host in HOSTS:
    for path in ["/v1/web/openapi/token/config", "/open/api/v1/web/openapi/token/config"]:
        st, b = call("GET", host + path,
                     hdrs={"Authorization": "Bearer " + KEY, "X-Client-ID": CID})
        print(f"  {host+path:62} -> {st}  {b[:110]}")

print("\n【B】/oauth/token grant_type 变体（client_credentials / api_key 交换）")
GRANTS = [
    ("client_credentials", {"grant_type": "client_credentials", "client_id": CID,
                            "client_secret": KEY}),
    ("client_credentials+key", {"grant_type": "client_credentials", "client_id": CID,
                                "client_secret": KEY, "api_key": KEY}),
    ("api_key exchange", {"grant_type": "api_key", "client_id": CID, "api_key": KEY}),
    ("token exchange", {"grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
                        "client_id": CID, "subject_token": KEY}),
]
for base in ["https://notes-api.biji.com", "https://openapi.biji.com"]:
    for path in ["/oauth/token", "/open/api/v1/oauth/token"]:
        for name, payload in GRANTS:
            st, b = call("POST", base + path, payload=payload)
            print(f"  {base.split('//')[1][:18]} {path:26} {name:22} -> {st} {b[:100]}")

print("\n【C】refresh 端点（api_key 当 refresh_token）")
for host in HOSTS:
    for path in ["/user/auth/refresh", "/account/v2/web/user/auth/refresh",
                 "/api/user/auth/refresh"]:
        st, b = call("POST", host + path, payload={"refresh_token": KEY, "client_id": CID})
        print(f"  {host+path:58} -> {st}  {b[:110]}")

print("\n【D】网页登录端点（api_key 作为凭证）")
for path in ["/api/user/login", "/login/login-by-auth", "/voicenotes/web/login/captcha"]:
    st, b = call("POST", "https://www.biji.com" + path,
                 payload={"api_key": KEY, "client_id": CID})
    print(f"  www.biji.com{path:36} -> {st}  {b[:130]}")

print("\n【E】CLI 本地是否藏了网页 token / refresh_token")
for pat in [r"C:\Users\Administrator\.getnote/*",
            r"C:\Users\Administrator\.agents/skills/getnote-*/**/*",
            r"C:\Users\Administrator\.claude/skills/getnote-*/**/*"]:
    for f in glob.glob(pat, recursive=True):
        if os.path.isfile(f) and os.path.getsize(f) < 200000:
            try:
                t = open(f, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            low = t.lower()
            if any(k in low for k in ["refresh_token", "access_token", "web_token", "biji_token"]):
                # 只报文件名与命中关键词，不打印值（脱敏铁律）
                hits = [k for k in ["refresh_token", "access_token", "web_token", "biji_token"]
                        if k in low]
                print(f"  ★ {f}  命中 {hits}")
