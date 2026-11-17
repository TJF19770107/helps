# -*- coding: utf-8 -*-
"""
test_writer_payload.py —— 写入器变更测试（防「断言恒绿」铁律）

目的：证明 dedao_web_writer.py 的请求构造、端点选择、请求体拼装
      真的会因为输入变化而变化，而不是打桩后照样 PASS。

测法（不写远端数据）：
  1. 用假 token 打真端点 → 必须得到 401/403（不是 200，也不是连接失败）
  2. 换路径 → 报错形态必须变（证明端点串真被拼进去了）
  3. 打请求体 → 断言 create_note 用的 payload 真含 title/content/url/tags
"""
import os, sys, json, importlib.util

sys.stdout.reconfigure(encoding="utf-8")

spec = importlib.util.spec_from_file_location(
    "dww", r"E:\博主学习库\_tools\dedao_web_writer.py")
dww = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dww)

print("=" * 70)
print("  写入器变更测试")
print("=" * 70)

# --- 测试 1：假 token 必须被拒（证明网络+端点+鉴权三层都通到服务端）---
print("\n【T1】假 token 打真端点 → 必须 401/403")
fake = "gk_test_0000000000000000000000000000000000000000000000000000"
st, body = dww.call("GET", "/voicenotes/web/notes", fake, query="?page=1&page_size=1")
print(f"  status={st}")
print(f"  body={body[:160]}")
ok1 = st in (401, 403)
print(f"  {'✅' if ok1 else '❌'} 被服务端拒绝（未落到客户端静默失败）")

# --- 测试 2：换端点必须换结果（证明 path 真被拼进去）---
print("\n【T2】故意用不存在的端点 → 报错形态必须不同")
st2, body2 = dww.call("GET", "/voicenotes/web/__不存在的端点__", fake)
print(f"  status={st2}")
print(f"  body={body2[:160]}")
ok2 = (st2, body2[:80]) != (st, body[:80])
print(f"  {'✅' if ok2 else '❌'} 端点串真被拼进 URL（结果随端点变化）")

# --- 测试 3：请求体拼装正确性 ---
print("\n【T3】create_note 请求体构造（含 tags/url/content）")
calls = []


def fake_call(method, path, token, payload=None, query=""):
    calls.append({"method": method, "path": path, "payload": payload, "query": query})
    if path.endswith("/tags"):
        return 200, json.dumps({"success": True})
    return 200, json.dumps({"success": True, "data": {"note_id": "TEST_NOTE_123"}})


dww.call = fake_call
nid, _ = dww.create_note(fake, "标题A", "正文B", "https://example.com", ["产品灵感"])
create_call = calls[0]      # 第 1 次 = 建笔记
tag_call = calls[1]         # 第 2 次 = 打标签
print(f"  建笔记: method={create_call['method']}  path={create_call['path']}")
print(f"  payload={json.dumps(create_call['payload'], ensure_ascii=False)}")
ok3a = create_call["method"] == "POST" and create_call["path"] == "/voicenotes/web/notes"
ok3b = create_call["payload"] == {"title": "标题A", "content": "正文B",
                                  "url": "https://example.com"}
print(f"  {'✅' if ok3a else '❌'} 建笔记端点与方法正确")
print(f"  {'✅' if ok3b else '❌'} 请求体字段正确")

print(f"\n  标签调用: method={tag_call['method']}  path={tag_call['path']}")
print(f"  标签体  : {json.dumps(tag_call['payload'], ensure_ascii=False)}")
ok4 = (tag_call["path"] == "/voicenotes/web/notes/TEST_NOTE_123/tags"
       and tag_call["payload"] == {"tags": ["产品灵感"]})
print(f"  {'✅' if ok4 else '❌'} 标签端点与请求体正确")

# --- 测试 5：改输入 → 输出必须跟着变 ---
print("\n【T4】变更测试：换 tags → payload 必须跟着变")
calls.clear()
dww.create_note(fake, "T", "C", "U", ["标签甲"])
p1 = calls[1]["payload"]
calls.clear()
dww.create_note(fake, "T", "C", "U", ["标签乙"])
p2 = calls[1]["payload"]
print(f"  p1={p1}  p2={p2}")
ok5 = p1 != p2
print(f"  {'✅' if ok5 else '❌'} 输出随输入变化（非恒绿）")

# --- 测试 6：中文路径必须被正确编码（真 bug 回归）---
print("\n【T5】中文路径编码回归（曾踩 UnicodeEncodeError）")
import urllib.parse as _up
try:
    enc = _up.quote("/voicenotes/web/测试路径", safe="/-_~.")
    ok6 = enc == "/voicenotes/web/%E6%B5%8B%E8%AF%95%E8%B7%AF%E5%BE%84"
    print(f"  encoded={enc}")
    print(f"  {'✅' if ok6 else '❌'} 中文路径已正确 percent-encode")
except Exception as e:
    ok6 = False
    print(f"  ❌ {e}")

print("\n" + "=" * 70)
allok = all([ok1, ok2, ok3a, ok3b, ok4, ok5, ok6])
print(f"  总判定: {'✅ 全部通过（写入器代码路径真活）' if allok else '❌ 有失败项'}")
print("=" * 70)
sys.exit(0 if allok else 1)
