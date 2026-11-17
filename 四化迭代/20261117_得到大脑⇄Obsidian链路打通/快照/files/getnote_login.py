# -*- coding: utf-8 -*-
"""
getnote_login.py —— 得到大脑网页版登录（一次登录，长期免登）
用有头模式打开登录页，汤哥完成手机号验证码登录后，
登录态（cookie/localStorage）持久化在 profile 目录，后续自动化直接复用。

用法：
  python getnote_login.py          # 有头模式，等人登录
  python getnote_login.py --check  # 无头检查登录态
"""
import os, sys, time, json, argparse, glob

sys.stdout.reconfigure(encoding="utf-8")

URL_HOME = "https://www.biji.com"
PROFILE_DIR = r"C:\Users\Administrator\AppData\Local\getnote-pw-profile"
SHOTS = r"E:\博主学习库\_tmp_shot"


def find_chrome():
    for pat in [r"C:\Users\Administrator\AppData\Local\ms-playwright\chromium-*\chrome-win64\chrome.exe",
                r"C:\Users\Administrator\AppData\Local\ms-playwright\chromium-*\chrome-win\chrome.exe"]:
        g = glob.glob(pat)
        if g:
            return g[0]
    return None


def is_logged(page):
    """多重判定登录态（不靠单一文本）"""
    try:
        content = page.content()
    except Exception:
        return False, "取内容失败"
    signals = []
    # 1) 有「退出登录」
    for kw in ["退出登录", "退出账号", "我的主页", "个人中心"]:
        if kw in content:
            signals.append(f"含「{kw}」")
    # 2) localStorage 里有 token
    try:
        ls = page.evaluate("() => JSON.stringify(Object.keys(localStorage))")
        if ls and len(ls) > 4:
            signals.append(f"localStorage keys={ls[:120]}")
        ls2 = page.evaluate("""() => {
            const out = {};
            for (let i=0;i<localStorage.length;i++){
                const k = localStorage.key(i);
                if (/token|user|account|uid|session|auth/i.test(k))
                    out[k] = String(localStorage.getItem(k)).slice(0,40);
            }
            return JSON.stringify(out);
        }""")
        if ls2 and ls2 != "{}":
            signals.append(f"auth类LS={ls2[:200]}")
    except Exception:
        pass
    # 3) cookie 里有 session
    try:
        cks = page.context.cookies()
        hit = [c["name"] for c in cks if "biji" in c.get("domain", "") and
               any(k in c["name"].lower() for k in ["token", "session", "user", "sid", "auth"])]
        if hit:
            signals.append(f"cookie={hit}")
    except Exception:
        pass
    # 4) 是否显示登录按钮
    try:
        login_btn = page.locator("text=注册/登录").count() + page.locator("text=登录").count()
    except Exception:
        login_btn = 0
    if login_btn:
        signals.append(f"⚠️ 仍有登录按钮({login_btn})")
    logged = any(not s.startswith("⚠️") for s in signals) and login_btn == 0
    return logged, " | ".join(signals) if signals else "无任何登录信号"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只检查登录态")
    ap.add_argument("--wait", type=int, default=300, help="等待登录秒数")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ playwright 未装")
        return 2
    exe = find_chrome()
    if not exe:
        print("❌ 找不到 chromium")
        return 2
    os.makedirs(PROFILE_DIR, exist_ok=True)
    os.makedirs(SHOTS, exist_ok=True)

    headless = args.check
    print(f"浏览器: {exe}")
    print(f"profile: {PROFILE_DIR}")
    print(f"模式: {'有头（等汤哥登录）' if not headless else '无头（只检查）'}")

    with sync_playwright() as pw:
        ctx = pw.chromium.launch_persistent_context(
            PROFILE_DIR, executable_path=exe, headless=headless,
            args=["--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage",
                  "--start-maximized"],
            viewport={"width": 1440, "height": 900}, locale="zh-CN",
            ignore_default_args=["--enable-automation"])
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(URL_HOME, wait_until="domcontentloaded", timeout=60000)
        time.sleep(3)

        logged, sig = is_logged(page)
        print(f"\n初始状态: {'✅ 已登录' if logged else '❌ 未登录'}")
        print(f"  信号: {sig}")

        if not logged and not args.check:
            print("\n" + "=" * 60)
            print("  请在弹出的浏览器窗口里完成登录：")
            print("    1) 点右上角「注册/登录」")
            print("    2) 用汤哥手机号收验证码并登录")
            print("    3) 登录成功后回到这个窗口，脚本会自动检测")
            print("  （登录态会保存在 profile 目录，之后免登录）")
            print("=" * 60)

            t0 = time.time()
            while time.time() - t0 < args.wait:
                time.sleep(5)
                try:
                    logged, sig = is_logged(page)
                    if logged:
                        print(f"\n✅ 检测到登录成功！（{sig}）")
                        break
                except Exception:
                    pass
                left = int(args.wait - (time.time() - t0))
                if left % 30 < 6:
                    print(f"  等待中... 剩余 {left}s")
            else:
                print(f"\n⚠️ {args.wait}s 内未检测到登录")
                logged = False

        page.screenshot(path=os.path.join(SHOTS, "getnote_login_state.png"))
        print(f"\n截图: {os.path.join(SHOTS, 'getnote_login_state.png')}")
        print(f"最终: {'✅ 已登录' if logged else '❌ 未登录'}")
        if logged:
            print(f"  信号: {sig}")
            # 记录真实可达路由（供后续脚本用）
            try:
                routes = page.evaluate("""() => {
                    const a = [...document.querySelectorAll('a[href]')].map(x=>x.getAttribute('href'));
                    return [...new Set(a)].filter(h=>h && h.startsWith('/')).slice(0,40);
                }""")
                print(f"  站内路由: {routes}")
            except Exception:
                pass
        ctx.close()
    return 0 if logged else 3


if __name__ == "__main__":
    sys.exit(main())
