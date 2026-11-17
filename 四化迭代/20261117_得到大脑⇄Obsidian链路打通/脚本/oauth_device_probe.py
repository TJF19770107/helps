# -*- coding: utf-8 -*-
"""
oauth_device_probe.py —— 得到大脑 OAuth Device Flow 探测（只申请设备码，不写数据）

发现（实测自 CLI 二进制）：
  · /oauth/device/code   → 申请 device_code
  · /oauth/token         → {"grant_type":"device_code","client_id":"%s","code":"%s"}
  · CLI 的 gk_live_ api_key 打到网页后端 = 403 LoginRequired（token 格式对、类型不对）

假设：OAuth Device Flow 发的 token 是「网页登录 token」，可直接打 notes-api.biji.com
本脚本：只申请 device_code 并打印验证 URL + user_code，不轮询（不产生副作用）
"""
import sys, json, urllib.request, urllib.error

sys.stdout.reconfigure(encoding="utf-8")

cfg = json.load(open(r"C:\Users\Administrator\.getnote\config.json", encoding="utf-8"))
CID = cfg["client_id"]

HOSTS = ["https://openapi.biji.com", "https://open-api.biji.com",
         "https://www.biji.com", "https://notes-api.biji.com"]

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")


def post(url, payload, hdrs=None):
    h = {"User-Agent": UA, "Content-Type": "application/json",
         "Accept": "application/json"}
    if hdrs:
        h.update(hdrs)
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=h, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "ignore")
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:110]}"


print("=" * 72)
print("  OAuth Device Flow 探测")
print("=" * 72)

for host in HOSTS:
    for path in ["/oauth/device/code", "/open/api/v1/oauth/device/code"]:
        url = host + path
        st, body = post(url, {"client_id": CID})
        tag = "JSON" if body.lstrip().startswith("{") else "HTML/其他"
        print(f"  {url:56} -> {str(st):5} {tag}  {body[:160]}")
    print()
