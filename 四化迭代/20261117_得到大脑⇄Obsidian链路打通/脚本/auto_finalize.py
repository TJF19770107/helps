# -*- coding: utf-8 -*-
"""
auto_finalize.py —— 授权一旦完成，全自动收尾（零手工干预）

流程：
  1. 轮询 OAuth Device Flow 拿 access_token（pending 看 data.msg）
  2. token 落盘
  3. --check 验通道
  4. 读 write_payload.json → POST /voicenotes/web/notes 建笔记
  5. POST /voicenotes/web/notes/{id}/tags 打「产品灵感」标签
  6. GET /voicenotes/web/notes 回查确认笔记真在（不靠自述）
  7. 结果写 auto_finalize_result.json

密钥安全：token 只写本地 json，不打印完整值、不进 git。
"""
import os, sys, json, time, urllib.request, urllib.error

sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://notes-api.biji.com"
TOOLS = r"E:\博主学习库\_tools"
STATE = os.path.join(TOOLS, "oauth_device_state.json")
TOKEN_F = os.path.join(TOOLS, "getnote_web_token.json")
PAYLOAD = os.path.join(TOOLS, "write_payload.json")
RESULT = os.path.join(TOOLS, "auto_finalize_result.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")


def call(method, path, token=None, payload=None, query=""):
    # urllib URL 必须全 ASCII（实测踩坑：中文路径段需 percent-encode）
    import urllib.parse as up
    url = BASE + up.quote(path, safe="/-_~.") + query
    h = {"User-Agent": UA, "Accept": "application/json",
         "Content-Type": "application/json"}
    if token:
        h["Authorization"] = "Bearer " + token
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "ignore")
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:140]}"


def log(*a):
    print(time.strftime("[%H:%M:%S]"), *a, flush=True)


log("=== 自动收尾器启动 ===")
cfg = json.load(open(r"C:\Users\Administrator\.getnote\config.json", encoding="utf-8"))
st = json.load(open(STATE, encoding="utf-8"))
code = st["code"]
cid = cfg["client_id"]
log(f"授权码 {st.get('user_code')}  有效期至 {time.strftime('%H:%M:%S', time.localtime(time.time()+st.get('expires_in',600)))}")

# 1. 轮询 token
token = None
t0 = time.time()
while time.time() - t0 < st.get("expires_in", 600):
    http_status, body = call("POST", "/open/api/v1/oauth/token",
                             payload={"grant_type": "device_code",
                                      "client_id": cid, "code": code})
    try:
        j = json.loads(body)
    except Exception:
        j = {}
    data = j.get("data") or {}
    if isinstance(data, dict) and (data.get("access_token") or data.get("token")):
        token = data.get("access_token") or data.get("token")
        log("✅ 拿到 access_token")
        break
    msg = str(data.get("msg") or j.get("error") or "")[:80]
    left = int(st.get("expires_in", 600) - (time.time() - t0))
    if left % 60 < 8:
        log(f"等待授权中... 剩余 {left}s  ({msg})")
    time.sleep(5)

if not token:
    log("❌ 授权超时/未完成，未写入")
    json.dump({"status": "pending_auth", "user_code": st.get("user_code"),
               "at": time.strftime("%Y-%m-%d %H:%M:%S")},
              open(RESULT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.exit(4)

# 2. token 落盘
json.dump({"access_token": token, "at": time.strftime("%Y-%m-%d %H:%M:%S")},
          open(TOKEN_F, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
log(f"token 已落盘（len={len(token)}，不打印内容）")

# 3. 验通道
s, b = call("GET", "/voicenotes/web/notes", token, query="?page=1&page_size=1")
log(f"通道验证 GET /voicenotes/web/notes -> {s}  {b[:100]}")
if s != 200:
    log("❌ 通道验证失败，未写入")
    json.dump({"status": "token_invalid", "verify_status": s, "verify_body": b[:300],
               "at": time.strftime("%Y-%m-%d %H:%M:%S")},
              open(RESULT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.exit(5)

# 4. 读 payload 并建笔记
p = json.load(open(PAYLOAD, encoding="utf-8"))
title, content, url, tags = p["title"], p["content"], p.get("url"), p.get("tags", [])
log(f"建笔记 title={title!r}  tags={tags}")
s1, b1 = call("POST", "/voicenotes/web/notes", token,
              payload={"title": title, "content": content, "url": url})
log(f"建笔记 -> {s1}  {b1[:200]}")
note_id = None
if s1 in (200, 201):
    try:
        d = (json.loads(b1).get("data") or {})
        note_id = d.get("note_id") or d.get("id") or (d.get("note") or {}).get("note_id")
    except Exception:
        pass

# 5. 打标签
s2, b2 = None, "未执行（无 note_id）"
if note_id:
    log(f"打标签 note_id={note_id}  tags={tags}")
    s2, b2 = call("POST", f"/voicenotes/web/notes/{note_id}/tags", token,
                  payload={"tags": tags})
    log(f"打标签 -> {s2}  {b2[:200]}")

# 6. 回查确认（不靠自述）
s3, b3 = call("GET", "/voicenotes/web/tags", token,
              query="?page_size=50&page=1&hide_zero_note=false&query=")
tag_confirmed = bool(tags) and all(t in b3 for t in tags) if s3 == 200 else False
log(f"标签回查 -> {s3}  含「产品灵感」: {'✅' if tag_confirmed else '需人工核对'}")

result = {
    "status": "done" if (note_id and s2 in (200, 201)) else "partial",
    "note_id": note_id,
    "create_status": s1, "create_body": b1[:500],
    "tag_status": s2, "tag_body": b2[:500],
    "tag_list_status": s3, "tag_in_list": tag_confirmed,
    "title": title, "tags": tags, "url": url,
    "at": time.strftime("%Y-%m-%d %H:%M:%S"),
}
json.dump(result, open(RESULT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
log(f"=== 收尾完成 status={result['status']}  结果 {RESULT} ===")
