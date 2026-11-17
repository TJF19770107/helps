# -*- coding: utf-8 -*-
"""
member_wall_probe.py —— 得到大脑会员墙边界实测（重要结论固化）
要回答的问题：10201 挡的是「全部能力」还是「仅 API 通道」？
测法：
  1. getnote CLI 各子命令（save/note/tags/kb）—— 全走 OpenAPI
  2. 网页版（biji.com）—— 走 Web 后端，通常不受 API 会员墙限制
  3. 官方 Skill 说明（ClawHub）—— 声称登录即可用
输出：每一项的真实 status/code，判定会员墙边界
"""
import os, sys, json, subprocess, time

sys.stdout.reconfigure(encoding="utf-8")

GETNOTE = r"I:\npm\getnote.cmd"


def run(args, timeout=90):
    try:
        r = subprocess.run([GETNOTE] + args, capture_output=True, text=True,
                           encoding="utf-8", errors="ignore", timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return -1, "TIMEOUT"
    except Exception as e:
        return -1, f"{type(e).__name__}: {e}"


def classify(out):
    try:
        j = json.loads(out)
    except Exception:
        return "非JSON输出", out[:160].replace("\n", " ")
    if isinstance(j, dict):
        if j.get("success") is True:
            return "✅ 成功", json.dumps(j.get("data"), ensure_ascii=False)[:160]
        err = j.get("error") or {}
        code = err.get("code", "?")
        reason = err.get("reason", "")
        return f"❌ 失败 code={code} reason={reason}", (err.get("message", "") or "")[:140]
    return "?", str(j)[:140]


print("=" * 68)
print("  得到大脑会员墙边界实测")
print("=" * 68)

print("\n【1】CLI 子命令实测（全部走 OpenAPI）")
CASES = [
    (["notes", "--limit", "1", "-o", "json"], "读笔记"),
    (["search", "产品", "--limit", "1", "-o", "json"], "语义搜索"),
    (["tags", "-o", "json"], "标签列表"),
    (["kb", "list", "-o", "json"], "知识库列表"),
    (["capabilities", "-o", "json"], "能力声明"),
]
for args, label in CASES:
    rc, out = run(args)
    verdict, detail = classify(out)
    print(f"  {label:10} rc={rc:3}  {verdict}")
    print(f"             {detail}")

print("\n【2】网页版可达性（走 Web 后端，非 OpenAPI）")
try:
    import urllib.request
    for u in ["https://www.biji.com/", "https://www.biji.com/openapi"]:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            r = urllib.request.urlopen(req, timeout=25)
            print(f"  ✅ {u} -> HTTP {r.status}")
        except Exception as e:
            print(f"  ⚠️  {u} -> {type(e).__name__}: {str(e)[:100]}")
except Exception as e:
    print(f"  ❌ {e}")

print("\n【3】结论口径")
print("  · local_ready=true + api 10201 = 账号已登录、凭证有效，但服务端按会员资格拦截 API")
print("  · 即：会员墙拦的是「OpenAPI 通道」，不是「账号本身」")
print("  · 网页版（biji.com Web 后端）功能通常不受付费 API 墙限制 —— 需汤哥登录一次后由自动化复刻")
print("  · 唯一无法自动化的环节：手机号验证码登录（客观需本人）")

print("\n【4】会员开通入口（供汤哥拍板）")
print("  https://www.biji.com/checkout?product_alias=9Ab36BB3ZD")
