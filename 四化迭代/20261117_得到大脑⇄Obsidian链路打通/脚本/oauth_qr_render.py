# -*- coding: utf-8 -*-
"""
oauth_qr_render.py —— 把 Device Flow 的授权二维码渲染成 PNG（汤哥手机扫）

同时打印可点的授权 URL（电脑端也能点）。
"""
import sys, json, base64, os

sys.stdout.reconfigure(encoding="utf-8")

STATE = r"E:\博主学习库\_tools\oauth_device_state.json"
PNG = r"E:\博主学习库\_tmp_shot\biji_oauth_qr.png"

d = json.load(open(STATE, encoding="utf-8"))
qr = d.get("verification_uri_qrcode") or ""
url = d.get("verification_uri") or ""

if qr.startswith("data:image/png;base64,"):
    b64 = qr.split(",", 1)[1]
    with open(PNG, "wb") as f:
        f.write(base64.b64decode(b64))
    print(f"✅ 二维码已渲染: {PNG}  ({os.path.getsize(PNG)} B)")
else:
    print(f"⚠️ 无 base64 二维码，字段值: {str(qr)[:120]}")

print(f"\n用户码   : {d.get('user_code')}")
print(f"授权地址 : {url}")
print(f"有效期   : {d.get('expires_in')} 秒   (轮询间隔 {d.get('interval')} 秒)")
print(f"\n👉 手机扫码图，或电脑直接打开授权地址 → 点「授权」")
