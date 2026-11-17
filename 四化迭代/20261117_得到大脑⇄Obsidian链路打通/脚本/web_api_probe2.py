# -*- coding: utf-8 -*-
"""
web_api_probe2.py —— 网页后端端点 × 主机 矩阵探针（只读 GET，不写数据）

目标：找到「收藏网页+打标签」的真实端点与鉴权口径，绕开 openapi 会员墙。
候选主机（从网页 JS 提取）：
  notes-api.biji.com      网页版主后端
  notes-api.biji.com/spacex
  get-notes.luojilab.com  笔记服务
  notes.luojilab.com
  knowledge-api.trytalks.com
  www.biji.com             站点（/openapi 前缀走付费通道）
候选端点：
  /voicenotes/web/notes       笔记列表/创建
  /voicenotes/web/notes/count
  /tags/                     标签
  /mine/notes                 我的笔记
  /v1/web/topic/mine/list     知识库
  /v1/web/search/history
"""
import sys, json, urllib.request, urllib.error, time

sys.stdout.reconfigure(encoding="utf-8")

HOSTS = [
    "https://notes-api.biji.com",
    "https://notes-api.biji.com/spacex",
    "https://get-notes.luojilab.com",
    "https://notes.luojilab.com",
    "https://knowledge-api.trytalks.com",
    "https://www.biji.com",
]

PATHS = [
    "/voicenotes/web/notes",
    "/voicenotes/web/notes/count",
    "/tags/",
    "/mine/notes",
    "/v1/web/topic/mine/list",
    "/user/info",
    "/space/info",
]

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")


def get(url, hdrs):
    h = {"User-Agent": UA, "Accept": "application/json, text/plain, */*",
         "Accept-Language": "zh-CN,zh;q=0.9"}
    h.update(hdrs)
    req = urllib.request.Request(url, headers=h, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read().decode("utf-8", "ignore")[:220]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "ignore")[:220]
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:90]}"


def is_html(b):
    b = b.lstrip()[:120].lower()
    return b.startswith("<!doctype") or b.startswith("<html")


print("=" * 76)
print("  得到大脑网页后端 端点×主机 矩阵探针")
print("=" * 76)

hits = []
for host in HOSTS:
    print(f"\n### {host}")
    for p in PATHS:
        url = host + p
        st, body = get(url, {})
        kind = "HTML" if is_html(body) else "JSON"
        print(f"  {p:36} -> {str(st):5} {kind}  {body[:110] if kind=='JSON' else ''}")
        if st and 200 <= st < 300 and kind == "JSON":
            hits.append({"url": url, "status": st, "body": body[:600]})

print("\n" + "=" * 76)
print(f"✅ 命中 JSON 2xx 的端点 {len(hits)} 个")
for h in hits:
    print(f"  {h['url']}  -> {h['status']}")
    print(f"      {h['body'][:180]}")

out = r"E:\博主学习库\_tmp_shot\web_api_probe2.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(hits, f, ensure_ascii=False, indent=1)
print(f"\n已存: {out}")
