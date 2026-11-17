# -*- coding: utf-8 -*-
"""
cdp_token_harvest.py —— 通过 CDP 接管已打开的得到大脑页面，抓网页登录 token

用法：python cdp_token_harvest.py [秒数]
  · 连 http://127.0.0.1:9333 找现有标签页
  · 判定登录态（DOM 信号 + localStorage + cookie）
  · 若已登录 → 导出 token（Authorization 用的那串）到 state json
  · 若未登录 → 打印「请在 Chrome 窗口登录」，并轮询等待
"""
import sys, json, time, urllib.request

sys.stdout.reconfigure(encoding="utf-8")

PORT = 9333
OUT = r"E:\博主学习库\_tools\getnote_web_state.json"
WAIT = int(sys.argv[1]) if len(sys.argv) > 1 else 600

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ playwright 未装")
    sys.exit(2)


def cdp_targets():
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/list", timeout=8) as r:
            return json.loads(r.read().decode("utf-8", "ignore"))
    except Exception as e:
        return []


print(f"=== CDP 目标列表 (127.0.0.1:{PORT}) ===")
tg = cdp_targets()
for t in tg:
    print(f"  [{t.get('type')}] {t.get('title','')[:40]}  {t.get('url','')[:90]}")
if not tg:
    print("  ⚠️ 无目标 —— Chrome 可能没开远程调试或已被关闭")
    sys.exit(3)

with sync_playwright() as pw:
    browser = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    ctx = browser.contexts[0] if browser.contexts else browser.new_context()
    pages = [p for c in browser.contexts for p in c.pages]
    print(f"\n页面数: {len(pages)}")

    target = None
    for p in pages:
        if "biji.com" in p.url:
            target = p
            break
    if target is None:
        target = pages[0] if pages else ctx.new_page()
        if "biji" not in target.url:
            print(f"  打开 https://www.biji.com ...")
            target.goto("https://www.biji.com", wait_until="domcontentloaded", timeout=60000)
            time.sleep(4)
    print(f"目标页: {target.url}")

    def probe():
        """返回 (logged, info_dict)"""
        info = {}
        try:
            content = target.content()
            info["has_login_btn"] = (target.locator("text=注册/登录").count() +
                                     target.locator("text=登录").count())
            info["has_logout"] = any(k in content for k in ["退出登录", "个人中心", "我的主页"])
        except Exception as e:
            info["err"] = str(e)[:100]
        try:
            info["localStorage"] = target.evaluate(
                "() => Object.fromEntries(Object.entries(localStorage).map(([k,v])=>[k,String(v).slice(0,120)]))")
        except Exception as e:
            info["ls_err"] = str(e)[:80]
        try:
            info["sessionStorage"] = target.evaluate(
                "() => Object.fromEntries(Object.entries(sessionStorage).map(([k,v])=>[k,String(v).slice(0,120)]))")
        except Exception:
            pass
        try:
            cks = ctx.cookies()
            info["biji_cookies"] = [{"name": c["name"], "len": len(c["value"]),
                                     "domain": c["domain"]} for c in cks if "biji" in c.get("domain", "")]
        except Exception:
            pass
        # 判定
        logged = False
        ls = info.get("localStorage", {}) or {}
        tok = {k: v for k, v in ls.items() if re_search_token(k, v)}
        if tok:
            logged = True
        if info.get("has_logout") and not info.get("has_login_btn"):
            logged = True
        if info.get("biji_cookies") and not info.get("has_login_btn"):
            logged = True
        return logged, info, tok

    def re_search_token(k, v):
        import re
        if not isinstance(k, str):
            return False
        return bool(re.search(r"token|auth|jwt|session|user", k, re.I)) and len(str(v)) > 8

    logged, info, tok = probe()
    print(f"\n=== 初始状态 ===")
    print(f"  登录判定: {'✅ 已登录' if logged else '❌ 未登录'}")
    print(f"  登录按钮数: {info.get('has_logout')} / {info.get('has_login_btn')}")
    print(f"  localStorage keys: {list((info.get('localStorage') or {}).keys())}")
    print(f"  biji cookies: {info.get('biji_cookies')}")
    if tok:
        print(f"  ★ token 候选: { {k: str(v)[:60] for k, v in tok.items()} }")

    t0 = time.time()
    while not logged and time.time() - t0 < WAIT:
        time.sleep(6)
        try:
            logged, info, tok = probe()
        except Exception:
            continue
        left = int(WAIT - (time.time() - t0))
        if left % 60 < 7:
            print(f"  等待登录中... 剩余 {left}s  (登录按钮数={info.get('has_login_btn')})")

    if logged:
        print("\n✅ 判定为已登录 —— 导出 token")
        state = {
            "harvested_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "url": target.url,
            "localStorage": info.get("localStorage", {}),
            "cookies": ctx.cookies(),
        }
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=1)
        print(f"  已存: {OUT}")
        print(f"  localStorage: {json.dumps(info.get('localStorage', {}), ensure_ascii=False)[:600]}")
        try:
            target.screenshot(path=r"E:\博主学习库\_tmp_shot\biji_logged_in.png")
            print("  截图: biji_logged_in.png")
        except Exception:
            pass
    else:
        print(f"\n⚠️ {WAIT}s 内未检测到登录")
        try:
            target.screenshot(path=r"E:\博主学习库\_tmp_shot\biji_login_wait.png")
            print("  截图: biji_login_wait.png")
        except Exception:
            pass
