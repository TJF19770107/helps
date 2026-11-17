# -*- coding: utf-8 -*-
"""
try_isid_auth_v2.py —— 精简 cookie 集重试（排除 WAF cookie 干扰）

v1 教训：带全部 cookie（含 acw_tc/aliyungf_tc WAF cookie）→ HTML 400（WAF 层拒绝）。
v2：只带 ISID（真正会话 cookie）；逐组测试；打印每个 cookie 的"字符安全性"（不打印值）。
"""
import os, sys, json, sqlite3, shutil, tempfile, ctypes, ctypes.wintypes, base64, urllib.request, urllib.error

sys.stdout.reconfigure(encoding="utf-8")

PROF = r"C:\Users\Administrator\AppData\Local\getnote-pw-profile\Default"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")


class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", ctypes.wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_byte))]


def dpapi(data):
    crypt32 = ctypes.windll.crypt32
    bin = DATA_BLOB(); buf = ctypes.create_string_buffer(data)
    bin.cbData = len(data); bin.pbData = ctypes.cast(buf, ctypes.POINTER(ctypes.c_byte))
    bout = DATA_BLOB()
    if not crypt32.CryptUnprotectData(ctypes.byref(bin), None, None, None, None, 0, ctypes.byref(bout)):
        return None
    out = ctypes.string_at(bout.pbData, bout.cbData)
    ctypes.windll.kernel32.LocalFree(bout.pbData)
    return out


def aes_key():
    j = json.load(open(os.path.join(os.path.dirname(PROF), "Local State"), encoding="utf-8"))
    raw = base64.b64decode(j["os_crypt"]["encrypted_key"])
    return dpapi(raw[5:] if raw.startswith(b"DPAPI") else raw)


from cryptography.hazmat.primitives.ciphers.aead import AESGCM
KEY = aes_key()

cf = os.path.join(PROF, r"Network\Cookies")
tmp = os.path.join(tempfile.gettempdir(), "isid_v2.db")
shutil.copy2(cf, tmp)
con = sqlite3.connect(tmp)
cur = con.cursor()
cur.execute("SELECT host_key,name,encrypted_value FROM cookies WHERE host_key LIKE '%biji.com%'")
CKS = {}
for host, name, enc in cur.fetchall():
    if enc[:3] in (b"v10", b"v11"):
        val = AESGCM(KEY).decrypt(enc[3:15], enc[15:], None).decode("utf-8", "ignore")
    else:
        val = (dpapi(enc) or b"").decode("utf-8", "ignore")
    CKS[name] = val
    safe = all(32 <= ord(c) < 127 for c in val)
    print(f"  {name:16} len={len(val):3}  ASCII安全={safe}  前缀={val[:6]}")
con.close(); os.remove(tmp)

ISID = CKS.get("ISID", "")
CSRF = CKS.get("csrfToken", "")

COMBOS = {
    "① 仅 ISID": f"ISID={ISID}",
    "② ISID+csrf": f"ISID={ISID}; csrfToken={CSRF}",
    "③ ISID+Origin头": f"ISID={ISID}",
    "④ 仅 csrf": f"csrfToken={CSRF}",
}

URLS = [
    "https://notes-api.biji.com/voicenotes/web/notes?page=1&page_size=1",
    "https://www.biji.com/api/user/profile",
]


def probe(label, cookie, extra=None):
    h = {"User-Agent": UA, "Accept": "application/json", "Cookie": cookie}
    if extra:
        h.update(extra)
    print(f"\n  【{label}】")
    for u in URLS:
        req = urllib.request.Request(u, headers=h, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                b = r.read().decode("utf-8", "ignore")
                print(f"    {r.status} {u[:58]} -> {b[:120]}")
                if r.status == 200 and b.lstrip().startswith("{"):
                    return True, b
        except urllib.error.HTTPError as e:
            b = e.read().decode("utf-8", "ignore")
            kind = "HTML" if b.lstrip().lower().startswith("<") else "JSON"
            print(f"    {e.code}({kind}) {u[:58]} -> {b[:100]}")
        except Exception as e:
            print(f"    ERR {type(e).__name__}: {str(e)[:80]}")
    return False, None


print("=" * 70)
print("  ISID 精简 cookie 集探测（脱敏）")
print("=" * 70)
for name, ck in COMBOS.items():
    extra = {"Origin": "https://www.biji.com", "Referer": "https://www.biji.com/"} if "Origin" in name else None
    ok, body = probe(name, ck, extra)
    if ok:
        print(f"\n🎉 通了！{name}")
        json.dump({"cookie_combo": name, "body": body[:1000]},
                  open(r"E:\博主学习库\_tmp_shot\isid_v2_ok.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        sys.exit(0)
print("\n❌ 所有组合均未通 —— 诚实边界：仍需一次 OAuth 授权")
