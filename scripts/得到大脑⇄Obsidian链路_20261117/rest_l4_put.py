# -*- coding: utf-8 -*-
"""Obsidian REST 通道 · L4 完整验收（PUT 整文件写入路径）
写入方式说明：
  PATCH 是「局部指令」（targetType/target/operation），用于改写既有文件的某个节点
  PUT  是「整文件替换」，新建文件走 PUT 更直接 → 本验收用 PUT
"""
import json, urllib.request, urllib.error, urllib.parse, sys, os, time, hashlib, datetime

sys.stdout.reconfigure(encoding="utf-8")

ENVF = r"E:\博主学习库\_tools\obsidian_rest.env"
KEY = [l.split("=", 1)[1].strip() for l in open(ENVF, encoding="utf-8")
       if l.startswith("OBSIDIAN_API_KEY=")][0]
BASE = "http://127.0.0.1:27123"
VAULT_ABS = r"E:\龙虾AI主控中心\我的AI分身\Obsidian知识库"
REL = "02_产物归档/_REST通道探针_20261117.md"
ABS = os.path.join(VAULT_ABS, REL.replace("/", os.sep))

R = {}


def call(path, key=KEY, method="GET", body=None, ctype="application/json", headers=None):
    req = urllib.request.Request(BASE + path, method=method)
    if key:
        req.add_header("Authorization", f"Bearer {key}")
    if body is not None:
        req.add_header("Content-Type", ctype)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    data = body.encode("utf-8") if isinstance(body, str) else (
        json.dumps(body).encode("utf-8") if body is not None else None)
    try:
        with urllib.request.urlopen(req, data=data, timeout=20) as r:
            return r.status, r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "ignore")
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


print("=" * 64)
print("  Obsidian local-rest-api · L4 验收（PUT 整文件写入）")
print("=" * 64)

print("\n【1】根路由 + 列表")
st, raw = call("/")
print(f"  GET / -> {st}")
st, raw = call("/vault/")
d = json.loads(raw)
fs = d.get("files", d if isinstance(d, list) else [])
print(f"  GET /vault/ -> {st}  顶层 {len(fs)} 项")
for f in fs[:6]:
    print(f"     {f if isinstance(f, str) else f.get('path')}")
R["list"] = st == 200 and len(fs) > 0

print("\n【2】负向测试（鉴权真生效）")
s1, _ = call("/vault/", "WRONG_KEY_12345")
s2, _ = call("/vault/", None)
print(f"  错 key -> {s1} {'✅ 401' if s1 == 401 else '❌'}   无 key -> {s2} {'✅ 401' if s2 == 401 else '❌'}")
R["neg_auth"] = (s1 == 401 and s2 == 401)

print("\n【3】PUT 新建文件")
CONTENT = f"""---
tags: [产品灵感, 探针, REST通道验收]
created: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
source: local-rest-api L4
---

# REST 通道探针 {datetime.datetime.now().strftime('%H:%M:%S')}

本文件由 local-rest-api 通道写入，验证 Obsidian ↔ 外部程序双向读写。
链路：得到大脑 ⇄ Obsidian 主库。
"""
st, raw = call("/vault/" + urllib.parse.quote(REL), method="PUT",
               body=CONTENT, ctype="text/markdown")
print(f"  PUT -> {st}   {raw[:150] if st not in (200, 201) else '写入成功'}")
R["put"] = st in (200, 201, 204)  # 204=创建成功(无body), 200=更新成功

print("\n【4】磁盘真值核对（不信接口自述）")
time.sleep(1.5)
if os.path.exists(ABS):
    disk = open(ABS, "rb").read()
    txt = disk.decode("utf-8", "ignore")
    ok = "REST 通道探针" in txt
    print(f"  ✅ 落盘 {len(disk)} B  sha {hashlib.sha256(disk).hexdigest()[:16]}")
    print(f"     含标题: {ok}   含标签: {'产品灵感' in txt}")
    R["disk"] = ok and "产品灵感" in txt
else:
    print(f"  ❌ 磁盘无此文件: {ABS}")
    R["disk"] = False

print("\n【5】GET 读回")
st, raw = call("/vault/" + urllib.parse.quote(REL))
if st == 200:
    ok = "REST 通道探针" in raw
    print(f"  GET -> {st}  {len(raw)} 字符  含标题: {ok}")
    R["read"] = ok
else:
    print(f"  GET -> {st}  {raw[:150]}")
    R["read"] = False

print("\n【6】读主库真实产物目录")
st, raw = call("/vault/" + urllib.parse.quote("P07_博主学习库（D盘+E盘）/02_产物归档/"))
if st == 200:
    dd = json.loads(raw)
    lst = dd.get("files", []) if isinstance(dd, dict) else dd
    print(f"  GET -> {st}  条目 {len(lst)}")
    for f in lst[:6]:
        print(f"     {f if isinstance(f, str) else f.get('path')}")
    R["list_p07"] = st == 200
else:
    print(f"  GET -> {st}")
    R["list_p07"] = False

print("\n【7】PATCH 局部改写（验证指令代数可用）")
# 先取 document-map 拿到真实标题（target 必须逐字符等于可寻址键）
stm, rawm = call("/vault/" + urllib.parse.quote(REL),
                 headers={"Accept": "application/vnd.olrapi.document-map+json"})
target_path = None
if stm == 200:
    dm = json.loads(rawm)
    hs = dm.get("headings", {})
    if hs:
        h1 = list(hs.keys())[0]
        target_path = [h1]
        if hs[h1]:
            target_path.append(list(hs[h1].keys())[0])
    print(f"  document-map 可寻址标题: {target_path}")
st, raw = call("/vault/" + urllib.parse.quote(REL), method="PATCH",
               body={"targetType": "heading", "target": target_path or ["REST 通道探针"],
                     "operation": "append", "content": "\n\nPATCH 追加行验证成功。"})
print(f"  PATCH -> {st}   {raw[:150] if st not in (200,201,204) else '追加成功'}")
R["patch"] = st in (200, 201, 204)

print("\n【8】DELETE 清理")
st, raw = call("/vault/" + urllib.parse.quote(REL), method="DELETE")
time.sleep(1)
gone = not os.path.exists(ABS)
print(f"  DELETE -> {st}  磁盘已消失: {gone}")
R["delete"] = st in (200, 204) and gone

ok = sum(1 for v in R.values() if v)
print("\n" + "=" * 64)
print(f"  ★ L4 验收: {ok}/{len(R)} 通过")
for k, v in R.items():
    print(f"     {'✅' if v else '❌'} {k}")
print("=" * 64)
with open(r"E:\博主学习库\_tools\rest_l4_result.json", "w", encoding="utf-8") as f:
    json.dump({"results": R, "passed": ok, "total": len(R), "base": BASE}, f,
              ensure_ascii=False, indent=2)
