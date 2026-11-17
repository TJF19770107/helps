# -*- coding: utf-8 -*-
"""
ima_upload_v2.py —— IMA COS 预签名直传（新版主文档）

铁律（复用上轮踩坑经验）：
  · 必须原样携带 auth_headers（Content-Length 必须 == create_media 的 file_size）
  · 上传后调 add_knowledge 入库
  · 回读 get_knowledge_list 核验条目真实出现且 file_size 一致（不靠自述）

安全：预签名 URL 是**临时凭据**（含 q-ak / q-signature），绝不入库。
     从环境变量 IMA_PRESIGNED_URL + IMA_MEDIA_ID 读取；不设则退出。
"""
import os, sys, json, urllib.request, urllib.error, hashlib, datetime

sys.stdout.reconfigure(encoding="utf-8")

SRC = r"E:\博主学习库\四化迭代知识库_20261117_得到大脑⇄Obsidian链路打通与Obsidian复活.md"
KB_ID = "ima_kb_xdwuxO78"
FILE_NAME = "四化迭代知识库_20261117_得到大脑⇄Obsidian链路打通与Obsidian复活.md"

PRESIGNED = os.environ.get("IMA_PRESIGNED_URL", "")
MEDIA_ID = os.environ.get("IMA_MEDIA_ID", "")
if not PRESIGNED or not MEDIA_ID:
    raise SystemExit(
        "❌ 缺少临时凭据环境变量：\n"
        "   IMA_PRESIGNED_URL  (create_media 返回的 presigned_url)\n"
        "   IMA_MEDIA_ID      (create_media 返回的 media_id)\n"
        "   ⚠️ 该 URL 含 q-ak/q-signature 属临时密钥，切勿写入代码或提交到 git")

body = open(SRC, "rb").read()
print(f"源文件字节: {len(body)}  sha {hashlib.sha256(body).hexdigest()[:16]}")

req = urllib.request.Request(PRESIGNED, method="PUT", data=body)
req.add_header("Content-Type", "text/markdown")
req.add_header("x-cos-acl", "private")
try:
    with urllib.request.urlopen(req, timeout=120) as r:
        print(f"✅ COS PUT -> HTTP {r.status}  ETag={r.headers.get('ETag')}")
except urllib.error.HTTPError as e:
    print(f"❌ COS PUT -> HTTP {e.code}\n{e.read().decode('utf-8','ignore')[:600]}")
    sys.exit(2)
except Exception as e:
    print(f"❌ {type(e).__name__}: {e}")
    sys.exit(2)

out = {"media_id": MEDIA_ID, "knowledge_base_id": KB_ID,
       "file_name": FILE_NAME, "file_size": len(body),
       "sha256": hashlib.sha256(body).hexdigest(),
       "uploaded_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
with open(r"E:\博主学习库\_tools\ima_media_receipt_v2.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(json.dumps(out, ensure_ascii=False, indent=2))
print("\n下一步：add_knowledge（REPLACE 策略替换同名旧条目）")
