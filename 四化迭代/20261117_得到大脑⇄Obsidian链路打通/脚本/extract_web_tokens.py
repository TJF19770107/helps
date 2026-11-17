# -*- coding: utf-8 -*-
"""
extract_web_tokens.py —— 从浏览器 Local Storage leveldb 提取得到大脑 refresh_token / access_token

线索（实测锁定）：
  · 网页 JS 用 c.b3.refreshToken() / needsRefresh()，token 存 localStorage
  · POST /account/v2/web/user/auth/refresh 明确报「RefreshToken为必填字段」→ 需 body 传 refresh_token
  · pw_profile_biji/Default/Local Storage/leveldb 有 %_https://www.biji.com 等 key

脱敏铁律：只报 key 名 + 值形态（JWT/hex/base64）+ 长度 + 首末 4 字符，**不打印完整值**。
提取到的 token 只写本地 json（不进 git、不进聊天）。
"""
import os, sys, re, json, glob

sys.stdout.reconfigure(encoding="utf-8")

PROFILES = [
    r"E:\博主学习库\_tmp_shot\pw_profile_biji\Default\Local Storage\leveldb",
    r"C:\Users\Administrator\AppData\Local\getnote-pw-profile\Default\Local Storage\leveldb",
]

# token 类 key 的特征
TOKEN_KEYS = re.compile(r"(token|refresh|access|auth|jwt|session|credential|biji|userInfo|profile)", re.I)
# 值形态
JWT = re.compile(r"eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+")


def shape(v):
    if len(v) > 20 and JWT.match(v):
        return "JWT"
    if re.fullmatch(r"[0-9a-fA-F]{16,}", v):
        return "HEX"
    if re.fullmatch(r"[A-Za-z0-9+/=_\-]{16,}", v):
        return "B64"
    if v.startswith("{"):
        return "JSON"
    return "TXT"


def describe(k, v):
    s = shape(v)
    preview = v[:3] + "..." + v[-3:] if len(v) > 8 else v
    print(f"    {k[:46]:46} {s:4} len={len(v):4} {preview}")


all_hits = []
for d in PROFILES:
    print(f"\n### {d}")
    if not os.path.isdir(d):
        print("  不存在")
        continue
    files = glob.glob(os.path.join(d, "*.log")) + glob.glob(os.path.join(d, "*.ldb"))
    print(f"  leveldb 文件 {len(files)} 个")
    for f in files:
        try:
            b = open(f, "rb").read()
        except Exception:
            continue
        # leveldb 里 key 常以 UTF-16LE 或 UTF-8 存；两种都扫
        text_u8 = b.decode("utf-8", "ignore")
        text_u16 = b.decode("utf-16-le", "ignore")
        for text, enc in [(text_u8, "u8"), (text_u16, "u16")]:
            # 找 "key" + 值 的相邻可打印串
            for m in re.finditer(r"[\x20-\x7e]{4,}", text):
                seg = m.group()
                if not TOKEN_KEYS.search(seg):
                    continue
                # 只报含 biji 相关或明确 token 词的段
                if any(x in seg.lower() for x in ["biji", "token", "refresh", "auth"]):
                    describe(seg[:60], seg)
                    all_hits.append({"file": os.path.basename(f), "enc": enc,
                                     "key": seg[:60], "len": len(seg), "shape": shape(seg)})

# 去重
seen = set()
uniq = []
for h in all_hits:
    k = (h["key"], h["shape"])
    if k not in seen:
        seen.add(k)
        uniq.append(h)
print(f"\n去重后 {len(uniq)} 条")
json.dump(uniq, open(r"E:\博主学习库\_tmp_shot\web_token_keys.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("索引: E:\\博主学习库\\_tmp_shot\\web_token_keys.json")

# 关键：找 JWT 形态的完整 token（可能跨 leveldb 记录）
print("\n=== 全局 JWT 扫描（值形态）===")
jwt_count = 0
for d in PROFILES:
    if not os.path.isdir(d):
        continue
    for f in glob.glob(os.path.join(d, "*")):
        try:
            b = open(f, "rb").read()
        except Exception:
            continue
        for text in [b.decode("utf-8", "ignore"), b.decode("utf-16-le", "ignore")]:
            for m in JWT.finditer(text):
                jwt_count += 1
                print(f"  JWT in {os.path.basename(f)} len={len(m.group())} {m.group()[:8]}...")
print(f"JWT 总数: {jwt_count}")
