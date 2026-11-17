# -*- coding: utf-8 -*-
"""oauth_probe_body.py —— 只看 token 轮询的真实返回体（不改文件）"""
import sys, json, urllib.request, urllib.error, time

sys.stdout.reconfigure(encoding="utf-8")

cfg = json.load(open(r"C:\Users\Administrator\.getnote\config.json", encoding="utf-8"))
CID = cfg["client_id"]
BASE = "https://notes-api.biji.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/140.0.0.0"


def call(method, url, payload=None):
    h = {"User-Agent": UA, "Accept": "application/json", "Content-Type": "application/json"}
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "ignore")
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:120]}"


st, body = call("POST", f"{BASE}/open/api/v1/oauth/device/code", {"client_id": CID})
print(f"device/code -> {st}")
d = json.loads(body)["data"]
print("  code       :", d["code"])
print("  user_code  :", d.get("user_code"))
print("  verify uri :", d.get("verification_uri"))
print("  complete   :", d.get("verification_uri_complete"))
print("  expires_in :", d.get("expires_in"))
print("  interval   :", d.get("interval"))
print("  全部字段   :", list(d.keys()))

print("\n--- 轮询第1次（未授权）---")
st2, b2 = call("POST", f"{BASE}/open/api/v1/oauth/token",
               {"grant_type": "device_code", "client_id": CID, "code": d["code"]})
print(f"  -> {st2}  {b2[:400]}")

with open(r"E:\博主学习库\_tools\oauth_device_state.json", "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
print("\nstate 已存")
