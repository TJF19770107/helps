# -*- coding: utf-8 -*-
"""
inspect_isid_blob.py —— 解析 ISID cookie 解密后的真实结构（脱敏：只报结构不打印值）

线索：v1 报 ISID len=64（加密值长度），v2 AES-GCM 解密后 len=46 且 ASCII安全=False
      —— 说明解密结果是二进制 blob，真正 token 可能在其中某段（如 DPAPI 二次加密 / JSON 包裹）
"""
import os, sys, json, sqlite3, shutil, tempfile, ctypes, ctypes.wintypes, base64, re

sys.stdout.reconfigure(encoding="utf-8")

PROF = r"C:\Users\Administrator\AppData\Local\getnote-pw-profile\Default"


class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", ctypes.wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_byte))]


def dpapi(data):
    bin = DATA_BLOB(); buf = ctypes.create_string_buffer(data)
    bin.cbData = len(data); bin.pbData = ctypes.cast(buf, ctypes.POINTER(ctypes.c_byte))
    bout = DATA_BLOB()
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(bin), None, None, None, None, 0, ctypes.byref(bout)):
        return None
    out = ctypes.string_at(bout.pbData, bout.cbData)
    ctypes.windll.kernel32.LocalFree(bout.pbData)
    return out


j = json.load(open(os.path.join(os.path.dirname(PROF), "Local State"), encoding="utf-8"))
raw = base64.b64decode(j["os_crypt"]["encrypted_key"])
KEY = dpapi(raw[5:] if raw.startswith(b"DPAPI") else raw)
print(f"AES key len={len(KEY)}")

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

cf = os.path.join(PROF, r"Network\Cookies")
tmp = os.path.join(tempfile.gettempdir(), "isid_inspect.db")
shutil.copy2(cf, tmp)
con = sqlite3.connect(tmp)
cur = con.cursor()
cur.execute("SELECT host_key,name,encrypted_value FROM cookies WHERE name='ISID'")
for host, name, enc in cur.fetchall():
    print(f"\n=== {host} {name} ===")
    print(f"  加密值 len={len(enc)}  前缀={enc[:12]!r}")
    if enc[:3] in (b"v10", b"v11"):
        dec = AESGCM(KEY).decrypt(enc[3:15], enc[15:], None)
    else:
        dec = dpapi(enc)
    print(f"  解密后 len={len(dec)}")
    print(f"  hex 前32字节: {dec[:32].hex()}")
    # 结构分析：找可打印 ASCII 段
    segs = re.findall(rb"[ -~]{8,}", dec)
    print(f"  可打印段数={len(segs)}:")
    for s in segs[:12]:
        # 脱敏：只报长度+前2后2字符+是否像 base64/hex/jwt
        t = s.decode("ascii", "ignore")
        kind = "JWT" if t.startswith("eyJ") else ("HEX" if re.fullmatch(r"[0-9a-fA-F]+", t) else
               ("BASE64" if re.fullmatch(r"[A-Za-z0-9+/=]+", t) else "MIX"))
        print(f"    len={len(t):3} {kind:6} {t[:2]}...{t[-2:]}")
    # 尝试二次 DPAPI
    d2 = dpapi(dec)
    print(f"  二次DPAPI: {'✅ 成功 len='+str(len(d2)) if d2 else '❌ 失败'}")
    if d2:
        segs2 = re.findall(rb"[ -~]{8,}", d2)
        for s in segs2[:8]:
            t = s.decode("ascii", "ignore")
            print(f"    len={len(t):3} {t[:2]}...{t[-2:]}")
    break
con.close(); os.remove(tmp)
