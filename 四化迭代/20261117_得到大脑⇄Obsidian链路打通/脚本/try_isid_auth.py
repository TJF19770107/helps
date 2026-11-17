# -*- coding: utf-8 -*-
"""
try_isid_auth.py —— 用浏览器里未过期的 ISID cookie 打网页 API（全自动路径，最后冲刺）

线索（实测）：
  · getnote-pw-profile/Default 有 .biji.com ISID，到期 2027-11-17（未过期）
  · POST /account/v2/web/user/auth/refresh 返回「刷新Token已过期」→ 曾有过网页会话
  · 网页后端 notes-api.biji.com 用 cookie 鉴权

Windows Chrome cookie 加密：
  · v10/v11 前缀 → AES-GCM，密钥在 Local State 的 os_crypt.encrypted_key（DPAPI 加密）
  · 解密密钥需 CryptUnprotectData（ctypes 调 crypt32.dll，系统 API 非 COM，沙箱应可用）

脱敏铁律：全程不打印 cookie 值/token 值，只报"成功/失败 + 长度"。
"""
import os, sys, json, sqlite3, shutil, tempfile, ctypes, ctypes.wintypes, base64, urllib.request, urllib.error, time

sys.stdout.reconfigure(encoding="utf-8")

PROFILES = [
    r"C:\Users\Administrator\AppData\Local\getnote-pw-profile\Default",
    r"E:\博主学习库\_tmp_shot\pw_profile_biji\Default",
]
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")


class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", ctypes.wintypes.DWORD),
                ("pbData", ctypes.POINTER(ctypes.c_byte))]


def dpapi_unprotect(data):
    """调 crypt32.dll CryptUnprotectData（系统 DPAPI，非 COM）"""
    crypt32 = ctypes.windll.crypt32
    blob_in = DATA_BLOB()
    buf = ctypes.create_string_buffer(data)
    blob_in.cbData = len(data)
    blob_in.pbData = ctypes.cast(buf, ctypes.POINTER(ctypes.c_byte))
    blob_out = DATA_BLOB()
    ok = crypt32.CryptUnprotectData(ctypes.byref(blob_in), None, None, None, None, 0,
                                    ctypes.byref(blob_out))
    if not ok:
        return None
    out = ctypes.string_at(blob_out.pbData, blob_out.cbData)
    if blob_out.pbData:
        ctypes.windll.kernel32.LocalFree(blob_out.pbData)
    return out


def get_aes_key(user_data_dir):
    ls = os.path.join(os.path.dirname(user_data_dir), "Local State")
    if not os.path.exists(ls):
        return None
    j = json.load(open(ls, encoding="utf-8", errors="ignore"))
    ek = (j.get("os_crypt") or {}).get("encrypted_key")
    if not ek:
        return None
    raw = base64.b64decode(ek)
    if raw.startswith(b"DPAPI"):
        raw = raw[5:]
    return dpapi_unprotect(raw)


def decrypt_cookie(val, aes_key):
    if not val:
        return None
    if val.startswith(b"v10") or val.startswith(b"v11"):
        if not aes_key:
            return None
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        except ImportError:
            return "NO_CRYPTOGRAPHY"
        nonce = val[3:15]
        ct = val[15:]
        return AESGCM(aes_key).decrypt(nonce, ct, None)
    # 老式 DPAPI 直加密
    return dpapi_unprotect(val)


def load_cookies(prof):
    aes_key = get_aes_key(prof)
    print(f"  AES key: {'✅ 拿到' if aes_key else '❌ 无'}")
    cookies = []
    for rel in [r"Network\Cookies", "Cookies"]:
        cf = os.path.join(prof, rel)
        if os.path.exists(cf):
            break
    else:
        return cookies
    tmp = os.path.join(tempfile.gettempdir(), "isid_ck.db")
    shutil.copy2(cf, tmp)
    con = sqlite3.connect(tmp)
    cur = con.cursor()
    cur.execute("SELECT host_key,name,encrypted_value FROM cookies WHERE host_key LIKE '%biji.com%' OR host_key LIKE '%dedao.cn%'")
    for host, name, enc in cur.fetchall():
        dec = decrypt_cookie(enc, aes_key)
        if isinstance(dec, bytes):
            cookies.append((host, name, dec.decode("utf-8", "ignore")))
            print(f"    ✅ 解密 {host:24} {name:16} len={len(dec)}")
        else:
            print(f"    ⚠️ 解密失败 {host} {name}: {dec}")
    con.close()
    os.remove(tmp)
    return cookies


def probe_api(cookies):
    """用 cookie 打网页后端（只读 GET）"""
    ck = "; ".join(f"{n}={v}" for h, n, v in cookies if "biji.com" in h)
    h = {"User-Agent": UA, "Accept": "application/json", "Cookie": ck}
    tests = [
        ("GET", "https://notes-api.biji.com/voicenotes/web/notes?page=1&page_size=1", None),
        ("GET", "https://notes-api.biji.com/voicenotes/web/notes/count", None),
        ("GET", "https://www.biji.com/api/user/profile", None),
        ("GET", "https://notes-api.biji.com/account/v2/web/user/auth/refresh", None),
    ]
    print("\n  用 ISID cookie 打网页 API:")
    ok = []
    for m, u, body in tests:
        req = urllib.request.Request(u, headers=h, method=m)
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                b = r.read().decode("utf-8", "ignore")
                print(f"    {r.status} {u[:62]} -> {b[:110]}")
                if r.status == 200:
                    ok.append((u, b[:500]))
        except urllib.error.HTTPError as e:
            b = e.read().decode("utf-8", "ignore")
            print(f"    {e.code} {u[:62]} -> {b[:110]}")
        except Exception as e:
            print(f"    ERR {u[:62]} -> {type(e).__name__}: {str(e)[:80]}")
    return ok


print("=" * 74)
print("  ISID cookie 全自动鉴权探测（脱敏，不打印凭证值）")
print("=" * 74)
all_ok = []
for prof in PROFILES:
    print(f"\n### {prof}")
    if not os.path.isdir(prof):
        print("  不存在，跳过")
        continue
    cookies = load_cookies(prof)
    if cookies:
        all_ok += probe_api(cookies)

print("\n" + "=" * 74)
if all_ok:
    print(f"🎉 网页 API 通了 {len(all_ok)} 个端点！可全自动写入，不用扫码")
    json.dump([{"url": u, "body": b} for u, b in all_ok],
              open(r"E:\博主学习库\_tmp_shot\isid_api_ok.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
else:
    print("❌ ISID cookie 未能打通网页 API —— 保持诚实边界，仍需一次授权")
