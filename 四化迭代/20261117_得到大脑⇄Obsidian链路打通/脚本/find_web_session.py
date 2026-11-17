# -*- coding: utf-8 -*-
"""
find_web_session.py —— 全盘找网页版 refresh_token / 会话凭证（只读，脱敏）

线索：POST /account/v2/web/user/auth/refresh 返回「刷新Token已过期」(c=20124)
      → 说明某处有真实 refresh_token，只是过期了。若能刷新/重签，就不用人扫码。

搜索范围（全部只读）：
  1. 浏览器 profile 的 Cookies SQLite（所有域名，不局限 biji.com）
     · getnote-pw-profile / pw_profile_biji / GptBrowser / Chrome / Edge
  2. Local Storage / Session Storage（leveldb）里的 token 类 key
  3. getnote CLI 配置目录、.agents/skills、历史临时文件

脱敏铁律：只打印 key 名 / 域名 / 值长度 / 时间，**绝不打印 token 值本身**。
"""
import os, sys, glob, sqlite3, shutil, tempfile, json, re, time

sys.stdout.reconfigure(encoding="utf-8")

PROFILES = [
    ("getnote-pw-profile/Default", r"C:\Users\Administrator\AppData\Local\getnote-pw-profile\Default"),
    ("pw_profile_biji/Default", r"E:\博主学习库\_tmp_shot\pw_profile_biji\Default"),
    ("GptBrowser/Default", r"D:\Program Files\GptChrome\User Data\Default"),
    ("Chrome/Default", r"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default"),
    ("Edge/Default", r"C:\Users\Administrator\AppData\Local\Microsoft\Edge\User Data\Default"),
]

KEYWORDS = ["token", "refresh", "auth", "session", "biji", "getnote", "luojilab", "jwt", "sid", "uid"]


def scan_cookies(name, prof):
    found = []
    for rel in [r"Network\Cookies", "Cookies"]:
        cf = os.path.join(prof, rel)
        if not os.path.exists(cf):
            continue
        tmp = os.path.join(tempfile.gettempdir(), "ck_" + re.sub(r"\W", "_", name) + ".db")
        try:
            shutil.copy2(cf, tmp)
            con = sqlite3.connect(tmp)
            cur = con.cursor()
            cur.execute("SELECT host_key,name,length(encrypted_value),expires_utc FROM cookies")
            rows = cur.fetchall()
            for host, cname, ln, exp in rows:
                blob = f"{host} {cname}".lower()
                if any(k in blob for k in KEYWORDS):
                    found.append((host, cname, ln, exp))
            con.close()
        except Exception as e:
            print(f"  [{name}] 读 cookie 失败: {type(e).__name__}: {str(e)[:80]}")
        finally:
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except Exception:
                    pass
        break
    return found


def scan_leveldb(name, prof):
    found = []
    for sub in [r"Local Storage\leveldb", r"Session Storage\leveldb"]:
        d = os.path.join(prof, sub)
        if not os.path.isdir(d):
            continue
        for f in glob.glob(os.path.join(d, "*.log")) + glob.glob(os.path.join(d, "*.ldb")):
            try:
                b = open(f, "rb").read()
            except Exception:
                continue
            # 从二进制里抽可打印 key 名（不打印值）
            for m in re.finditer(rb"[ -~]{5,60}", b):
                s = m.group().decode("ascii", "ignore")
                sl = s.lower()
                if any(k in sl for k in ["token", "refresh", "auth", "biji", "getnote", "luojilab"]):
                    found.append((os.path.basename(f), s[:60]))
    # 去重
    return list(dict.fromkeys(found))[:30]


print("=" * 74)
print("  网页会话凭证全盘搜索（只读 / 脱敏：不打印 token 值）")
print("=" * 74)

all_cookies = []
all_ls = []
for name, prof in PROFILES:
    print(f"\n### {name}  ({'存在' if os.path.isdir(prof) else '不存在'})")
    if not os.path.isdir(prof):
        continue
    cks = scan_cookies(name, prof)
    print(f"  Cookies 命中 {len(cks)} 条:")
    for host, cname, ln, exp in cks[:20]:
        all_cookies.append((name, host, cname, ln, exp))
        print(f"    {host:34} {cname:28} enc={ln}B exp={exp}")
    lss = scan_leveldb(name, prof)
    print(f"  LocalStorage/SessionStorage 命中 {len(lss)} 条:")
    for f, s in lss[:20]:
        all_ls.append((name, f, s))
        print(f"    [{f}] {s}")

print("\n=== 汇总 ===")
print(f"Cookie 命中 {len(all_cookies)} 条，LS 命中 {len(all_ls)} 条")

# 保存脱敏索引
out = {
    "cookies": [{"profile": n, "host": h, "name": c, "enc_len": ln, "expires_utc": e}
                for n, h, c, ln, e in all_cookies],
    "localstorage": [{"profile": n, "file": f, "key": s} for n, f, s in all_ls],
}
json.dump(out, open(r"E:\博主学习库\_tmp_shot\web_session_index.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("脱敏索引: E:\\博主学习库\\_tmp_shot\\web_session_index.json")
