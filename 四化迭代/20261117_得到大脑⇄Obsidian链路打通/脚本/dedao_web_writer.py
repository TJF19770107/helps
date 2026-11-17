# -*- coding: utf-8 -*-
"""
dedao_web_writer.py —— 得到大脑「网页通道」写入器（收藏网页 + 打标签）

架构（本轮实测打通的路径，绕开 299/年 OpenAPI 会员墙）：
  ① CLI/OpenAPI  → https://openapi.biji.com/open/api/v1/...  → 10201 not_member（付费通道，堵死）
  ② 网页后端     → https://notes-api.biji.com/voicenotes/web/... → 免费通道（普通用户功能）
     · 鉴权：OAuth Device Flow 换来的 access_token（Bearer）
     · 建笔记：POST /voicenotes/web/notes
     · 打标签：POST /voicenotes/web/notes/{note_id}/tags   {"tags": [...]}
     · 查标签：GET  /voicenotes/web/tags

用法：
  python dedao_web_writer.py --url "https://..." --title "..." --tag 产品灵感
  python dedao_web_writer.py --file 采集箱里的 md 文件（取其中的 url/title）
  python dedao_web_writer.py --check          # 只验 token 可用性
"""
import os, sys, json, time, argparse, urllib.request, urllib.error

sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://notes-api.biji.com"
TOKEN_FILE = r"E:\博主学习库\_tools\getnote_web_token.json"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")


def load_token():
    if not os.path.exists(TOKEN_FILE):
        raise SystemExit(f"❌ 没有 token 文件: {TOKEN_FILE}\n   先跑 oauth_device_run.py start")
    j = json.load(open(TOKEN_FILE, encoding="utf-8"))
    t = j.get("access_token")
    if not t:
        raise SystemExit(f"❌ token 为空（授权未完成）: {TOKEN_FILE}")
    return t


def call(method, path, token, payload=None, query=""):
    url = BASE + path + query
    h = {"User-Agent": UA, "Accept": "application/json",
         "Content-Type": "application/json", "Authorization": "Bearer " + token}
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "ignore")
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:150]}"


def check(token):
    st, body = call("GET", "/voicenotes/web/notes", token, query="?page=1&page_size=3")
    print(f"  GET /voicenotes/web/notes -> {st}")
    print(f"  {body[:400]}")
    return st == 200


def list_tags(token, query=""):
    st, body = call("GET", "/voicenotes/web/tags", token,
                    query=f"?page_size=50&page=1&hide_zero_note=false&hide_type=&query={query}")
    if st != 200:
        print(f"  ❌ 取标签失败 {st}: {body[:200]}")
        return []
    try:
        j = json.loads(body)
    except Exception:
        print(f"  ❌ 解析失败: {body[:200]}")
        return []
    data = j.get("data") or j
    items = data.get("items") or data.get("list") or data.get("tags") or []
    print(f"  标签数 {len(items)}")
    for it in items[:20]:
        print(f"    id={it.get('id')} name={it.get('name') or it.get('tag_name')}")
    return items


def create_note(token, title, content, url=None, tags=None, topics=None):
    """建笔记 + 打标签"""
    payload = {"title": title, "content": content}
    if url:
        payload["url"] = url
    if topics:
        payload["topic_ids"] = topics
    print(f"  → POST /voicenotes/web/notes  title={title!r}")
    st, body = call("POST", "/voicenotes/web/notes", token, payload)
    print(f"    {st} {body[:300]}")
    if st not in (200, 201):
        return None, body
    note_id = None
    try:
        j = json.loads(body)
        d = j.get("data") or j
        note_id = d.get("note_id") or d.get("id") or d.get("note", {}).get("note_id")
    except Exception:
        pass
    if not note_id:
        print("  ⚠️ 未解析到 note_id，需人工核对返回体")
    if note_id and tags:
        print(f"  → POST /voicenotes/web/notes/{note_id}/tags  {tags}")
        st2, body2 = call("POST", f"/voicenotes/web/notes/{note_id}/tags", token,
                          {"tags": tags})
        print(f"    {st2} {body2[:240]}")
    return note_id, body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="")
    ap.add_argument("--title", default="")
    ap.add_argument("--content", default="")
    ap.add_argument("--file", default="")
    ap.add_argument("--tag", action="append", default=[], help="可重复")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--list-tags", action="store_true")
    args = ap.parse_args()

    token = load_token()
    print(f"token: {token[:18]}... (len={len(token)})")

    if args.check:
        ok = check(token)
        print("\n  " + ("✅ 网页通道可用" if ok else "❌ 网页通道仍不通"))
        return 0 if ok else 2

    if args.list_tags:
        list_tags(token)
        return 0

    title, content, url = args.title, args.content, args.url
    if args.file:
        if not os.path.exists(args.file):
            raise SystemExit(f"❌ 文件不存在: {args.file}")
        txt = open(args.file, encoding="utf-8").read()
        title = title or os.path.basename(args.file).replace(".md", "")
        content = content or txt
        # 从 frontmatter 抽 url
        if not url and "url:" in txt[:400]:
            for line in txt[:400].splitlines():
                if line.strip().startswith("url:"):
                    url = line.split(":", 1)[1].strip().strip("\"'")
                    break
        if not title:
            for line in txt[:400].splitlines():
                if line.strip().startswith("title:"):
                    title = line.split(":", 1)[1].strip().strip("\"'")
                    break

    if not title:
        title = "得到大脑采集 " + time.strftime("%Y-%m-%d %H:%M")

    print(f"\n写入：title={title!r} url={url!r} tags={args.tag}")
    nid, body = create_note(token, title, content, url, args.tag or None)
    if nid:
        print(f"\n✅ 写入成功  note_id={nid}")
        return 0
    print("\n❌ 写入失败")
    return 2


if __name__ == "__main__":
    sys.exit(main())
