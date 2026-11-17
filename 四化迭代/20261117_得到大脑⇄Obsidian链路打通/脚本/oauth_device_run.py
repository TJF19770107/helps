# -*- coding: utf-8 -*-
"""
oauth_device_run.py —— 得到大脑 OAuth Device Flow 完整执行器

用途：把「网页登录 token」自动化拿下来，从而打通 notes-api.biji.com 网页通道
      （收藏网页 + 打「产品灵感」标签），绕开 299/年 OpenAPI 会员墙。

流程（标准 OAuth 2.0 Device Authorization Grant）：
  1. POST {base}/open/api/v1/oauth/device/code  {"client_id": ...}
     → code / user_code / verification_uri / verification_uri_complete
  2. 汤哥在浏览器打开 verification_uri_complete，点「授权」
  3. POST {base}/open/api/v1/oauth/token  {"grant_type":"device_code","client_id":...,"code":...}
     → access_token
  4. 验证：拿 access_token 打 notes-api.biji.com/voicenotes/web/notes

用法：
  python oauth_device_run.py start   # 申请 device code，打印授权链接，然后轮询
  python oauth_device_run.py poll    # 只轮询
"""
import sys, json, time, urllib.request, urllib.error

sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://notes-api.biji.com"          # 用网页后端，不受 openapi 会员墙影响
STATE = r"E:\博主学习库\_tools\oauth_device_state.json"
OUT = r"E:\博主学习库\_tools\getnote_web_token.json"

cfg = json.load(open(r"C:\Users\Administrator\.getnote\config.json", encoding="utf-8"))
CID = cfg["client_id"]

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")


def call(method, url, payload=None):
    h = {"User-Agent": UA, "Accept": "application/json",
         "Content-Type": "application/json"}
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "ignore")
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:120]}"


def request_code():
    st, body = call("POST", f"{BASE}/open/api/v1/oauth/device/code", {"client_id": CID})
    if st != 200:
        raise SystemExit(f"❌ 申请 device code 失败 {st}: {body[:200]}")
    j = json.loads(body)
    if not j.get("success"):
        raise SystemExit(f"❌ {body[:200]}")
    return j["data"]


def poll_token(code, timeout=900):
    """轮询换取 token
    实测口径（2026-11-17）：
      pending 响应 = {"success":true,"data":{"msg":"authorization_pending"},"error":null}
      → pending 判定必须看 data.msg，不能只看 error（error 为 null）
      → 成功判定必须有 access_token 字段，msg 不算成功
    """
    url = f"{BASE}/open/api/v1/oauth/token"
    t0 = time.time()
    while time.time() - t0 < timeout:
        st, body = call("POST", url, {"grant_type": "device_code",
                                      "client_id": CID, "code": code})
        try:
            j = json.loads(body)
        except Exception:
            j = {"raw": body[:200]}
        data = j.get("data") or {}
        if isinstance(data, dict) and (data.get("access_token") or data.get("token")):
            return data
        err = (j.get("error") or {})
        reason = str(err.get("reason") or err.get("message") or
                     data.get("msg") or j.get("raw") or "")[:160]
        if "pending" in reason.lower() or "slow_down" in reason.lower():
            left = int(timeout - (time.time() - t0))
            if left % 60 < 7:
                print(f"  等待授权中... 剩余 {left}s")
            time.sleep(5)
            continue
        print(f"  轮询返回 {st}: {body[:220]}")
        time.sleep(5)
    return None


def verify(token):
    """用拿到的 token 打网页后端验证（只读 GET）"""
    url = "https://notes-api.biji.com/voicenotes/web/notes?page=1&page_size=3"
    h = {"User-Agent": UA, "Accept": "application/json",
         "Authorization": f"Bearer {token}"}
    req = urllib.request.Request(url, headers=h, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "ignore")
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:110]}"


mode = sys.argv[1] if len(sys.argv) > 1 else "start"

if mode == "start":
    d = request_code()
    print("=" * 72)
    print("  得到大脑 OAuth Device Flow —— 请汤哥点一次授权（无需验证码）")
    print("=" * 72)
    print(f"  用户码 user_code : {d.get('user_code')}")
    print(f"  验证地址         : {d.get('verification_uri')}")
    print(f"  一键地址(免输码) : {d.get('verification_uri_complete')}")
    print(f"  有效期           : {d.get('expires_in')} 秒")
    print()
    print("  👉 在浏览器打开上面的「一键地址」，登录后点「授权/同意」即可")
    print("  （本脚本会自动轮询拿 token，不用再回来看）")
    print("=" * 72)
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    tok = poll_token(d["code"])
    if not tok:
        print("\n⚠️ 超时未拿到 token")
        sys.exit(4)
    print(f"\n✅ 拿到 token！字段: {list(tok.keys())}")
    at = tok.get("access_token") or tok.get("token")
    print(f"  access_token: {str(at)[:24]}... (len={len(str(at))})")
    st, body = verify(at)
    print(f"\n  验证 → notes-api.biji.com/voicenotes/web/notes : {st}")
    print(f"  {body[:300]}")
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"access_token": at, "all": tok,
                   "verified_status": st, "verified_body": body[:2000],
                   "at": time.strftime("%Y-%m-%d %H:%M:%S")}, f, ensure_ascii=False, indent=1)
    print(f"\n  已存: {OUT}")
    if st == 200:
        print("  🎉 网页通道已通 —— 可以写入得到大脑了")
    else:
        print(f"  ⚠️ 验证未通过（{st}），需进一步排查 token 用法")

elif mode == "poll":
    d = json.load(open(STATE, encoding="utf-8"))
    print(f"继续轮询 code={d.get('code')[:12]}... user_code={d.get('user_code')}")
    tok = poll_token(d["code"], timeout=int(sys.argv[2]) if len(sys.argv) > 2 else 600)
    if tok:
        at = tok.get("access_token") or tok.get("token")
        st, body = verify(at)
        print(f"✅ token 拿到，验证 {st}: {body[:300]}")
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump({"access_token": at, "all": tok, "verified_status": st,
                       "verified_body": body[:2000]}, f, ensure_ascii=False, indent=1)
        print(f"已存: {OUT}")
    else:
        print("⚠️ 未拿到 token")
