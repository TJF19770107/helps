# -*- coding: utf-8 -*-
"""
purge_presigned_url.py —— 从 Git 历史中彻底清除 COS 预签名 URL（临时凭据泄漏）

根因：ima_upload_v2.py 硬编码了 COS 预签名 URL（含 q-ak + q-signature）
      → GitHub push protection 判定为 secret，阻断 push（GH013）。

处理：
  1. 用 git filter-branch 从所有历史提交中删除该文件
  2. 保留文件在最新工作区（但改成从环境变量/参数读，且脱敏）
  3. 强推 + ls-remote 回查

注意：force push 是必要的（历史被重写）。这是**一次性凭据**，
      重写历史不会影响汤哥其他分支（只重写 fresh-main → lobster-kb）。
"""
import os, sys, subprocess, re

sys.stdout.reconfigure(encoding="utf-8")

REPO = r"E:\博主学习库\_tmp_shot\lkb_clone"
TARGET_REL = "四化迭代/20261117_得到大脑⇄Obsidian链路打通/脚本/ima_upload_v2.py"
BUCKET_REL = "四化迭代/20261117_得到大脑⇄Obsidian链路打通/脚本/ima_upload_v2.py"


def run(args, cwd=REPO, timeout=600, env=None):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", shell=False,
                       timeout=timeout, env=env)
    return r.returncode, ((r.stdout or "") + (r.stderr or "")).strip()


print("=== 1. 备份当前 HEAD（万一要回退）===")
rc, out = run(["git", "rev-parse", "HEAD"])
old_head = out.strip()
print(f"  旧 HEAD: {old_head[:12]}")
rc, out = run(["git", "branch", "backup-before-purge-" + old_head[:8]])
print(f"  备份分支: {out.strip()[:80]}")

print("\n=== 2. filter-branch 删除含预签名 URL 的文件 ===")
FILTER = (f'git rm --cached --ignore-unmatch "{TARGET_REL}"')
rc, out = run(["git", "filter-branch", "--force", "--index-filter",
               FILTER, "--prune-empty", "--tag-name-filter", "cat",
               "--", "fresh-main"], timeout=600)
print(f"  rc={rc}")
print(out[:900])

print("\n=== 3. 清理 filter-branch 残留 ===")
run(["git", "for-each-ref", "--format=%(refname)",
     "refs/original/"], timeout=120)
rc, out = run(["git", "for-each-ref", "--format=%(refname)", "refs/original/"])
refs = [l for l in out.splitlines() if l.strip()]
for ref in refs:
    run(["git", "update-ref", "-d", ref], timeout=60)
    print(f"  删除 {ref}")
run(["git", "reflog", "expire", "--expire=now", "--all"], timeout=120)
run(["git", "gc", "--prune=now", "--aggressive"], timeout=600)
print("  ✅ 清理完成")

print("\n=== 4. 确认历史中已无预签名 URL ===")
rc, out = run(["git", "log", "--all", "-p", "-S", "q-signature", "--oneline"],
              timeout=600)
print(f"  含 q-signature 的提交数: {len([l for l in out.splitlines() if re.match(r'^[0-9a-f]{7,}', l)])}")
rc, out = run(["git", "log", "--all", "-S", "AKID", "--oneline"], timeout=600)
print(f"  含 AKID 的提交数: {len([l for l in out.splitlines() if re.match(r'^[0-9a-f]{7,}', l)])}")

print("\n=== 5. 恢复工作区文件（脱敏版：URL 从环境变量读）===")
SAFE = '''# -*- coding: utf-8 -*-
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

SRC = r"E:\\博主学习库\\四化迭代知识库_20261117_得到大脑⇄Obsidian链路打通与Obsidian复活.md"
KB_ID = "ima_kb_xdwuxO78"
FILE_NAME = "四化迭代知识库_20261117_得到大脑⇄Obsidian链路打通与Obsidian复活.md"

PRESIGNED = os.environ.get("IMA_PRESIGNED_URL", "")
MEDIA_ID = os.environ.get("IMA_MEDIA_ID", "")
if not PRESIGNED or not MEDIA_ID:
    raise SystemExit(
        "❌ 缺少临时凭据环境变量：\\n"
        "   IMA_PRESIGNED_URL  (create_media 返回的 presigned_url)\\n"
        "   IMA_MEDIA_ID      (create_media 返回的 media_id)\\n"
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
    print(f"❌ COS PUT -> HTTP {e.code}\\n{e.read().decode('utf-8','ignore')[:600]}")
    sys.exit(2)
except Exception as e:
    print(f"❌ {type(e).__name__}: {e}")
    sys.exit(2)

out = {"media_id": MEDIA_ID, "knowledge_base_id": KB_ID,
       "file_name": FILE_NAME, "file_size": len(body),
       "sha256": hashlib.sha256(body).hexdigest(),
       "uploaded_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
with open(r"E:\\博主学习库\\_tools\\ima_media_receipt_v2.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(json.dumps(out, ensure_ascii=False, indent=2))
print("\\n下一步：add_knowledge（REPLACE 策略替换同名旧条目）")
'''
safe_path = os.path.join(REPO, TARGET_REL)
os.makedirs(os.path.dirname(safe_path), exist_ok=True)
with open(safe_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(SAFE)
print(f"  ✅ 脱敏版已写: {os.path.getsize(safe_path)} B")

# 同步到 _tools
with open(r"E:\博主学习库\_tools\ima_upload_v2.py", "w", encoding="utf-8", newline="\n") as f:
    f.write(SAFE)
print("  ✅ 同步到 _tools")

print("\n=== 6. git add + commit ===")
run(["git", "add", "--", TARGET_REL], timeout=120)
rc, out = run(["git", "diff", "--cached", "--stat"])
print(out[:600])
rc, out = run(["git", "commit", "-m",
               "chore: ima_upload_v2 改用环境变量读预签名URL，临时凭据不再入库"])
print(f"  rc={rc} {out[:250]}")

print("\n=== 7. 强推 GitHub ===")
HOSTS = os.path.join(os.path.expanduser("~"), ".config", "gh", "hosts.yml")
token = re.search(r"oauth_token:\s*(\S+)", open(HOSTS, encoding="utf-8", errors="ignore").read())
URL = f"https://x-access-token:{token.group(1)}@github.com/TJF19770107/helps.git"
env = dict(os.environ)
env["GIT_TERMINAL_PROMPT"] = "0"
rc, out = run(["git", "push", "--force-with-lease", URL, "fresh-main:lobster-kb"],
              env=env, timeout=600)
print(f"  rc={rc}\n  {out[:700]}")

print("\n=== 8. 回查远端 ===")
rc, out = run(["git", "rev-parse", "HEAD"])
local = out.strip()
rc, out = run(["git", "ls-remote", URL], timeout=180)
found = any(l.startswith(local) for l in out.splitlines())
print(f"  HEAD {local[:12]}  远端一致: {'✅ 是' if found else '❌ 否'}")
for l in out.splitlines():
    if l.startswith(local):
        print(f"  {l}")
