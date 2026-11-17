# -*- coding: utf-8 -*-
"""
getnote_session.py —— 得到大脑网页版会话（登录一次，长期复用）
用系统 Chrome（有头）打开登录页；汤哥登录后自动检测并把 cookie 落盘，
之后所有自动化脚本用 storage_state 复用，不再需要人。

关键事实（实测）：
  · GptBrowser 有定制改造，Playwright 无法注入（TargetClosedError）→ 必须用系统 Chrome
  · 系统 Chrome: C:\Program Files\Google\Chrome\Application\chrome.exe
  · 独立 profile: C:\Users\Administrator\AppData\Local\getnote-pw-profile
"""
import os, sys, time, json, argparse

sys.stdout.reconfigure(encoding="utf-8")

URL_HOME = "https://www.biji.com"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE_DIR = r"C:\Users\Administrator\AppData\Local\getnote-pw-profile"
STATE_FILE = r"E:\博主学习库\_tools\getnote_storage_state.json"
SHOTS = r"E:\博主学习库\_tmp_shot"


def has_login_btn(page):
    try:
        return (page.locator("text=注册/登录").count() +
                page.locator("text=登录").count())
    except Exception:
        return 99


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wait", type=int, default=900)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--save", default="", help="截图路径")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ playwright 未装")
        return 2
    if not os.path.exists(CHROME):
        print(f"❌ 找不到 Chrome: {CHROME}")
        return 2
    os.makedirs(PROFILE_DIR, exist_ok=True)
    os.makedirs(SHOTS, exist_ok=True)

    with sync_playwright() as pw:
        ctx = pw.chromium.launch_persistent_context(
            PROFILE_DIR, executable_path=CHROME, headless=args.check,
            args=["--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage"],
            viewport={"width": 1440, "height": 900}, locale="zh-CN")
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(URL_HOME, wait_until="domcontentloaded", timeout=60000)
        time.sleep(3)

        nb = has_login_btn(page)
        print(f"初始登录按钮数: {nb}")

        if not args.check and nb:
            print("\n" + "=" * 62)
            print("  得到大脑登录窗口已打开（系统 Chrome）")
            print("  请在这个 Chrome 窗口里：")
            print("    1) 点右上角「注册/登录」")
            print("    2) 汤哥手机号 + 验证码登录")
            print("    3) 登录后脚本自动保存登录态并退出")
            print(f"  最多等待 {args.wait}s")
            print("=" * 62)
            t0 = time.time()
            while time.time() - t0 < args.wait:
                time.sleep(4)
                if has_login_btn(page) == 0:
                    print("\n✅ 检测到登录成功！")
                    break
                left = int(args.wait - (time.time() - t0))
                if left % 60 < 5:
                    print(f"  等待中... 剩余 {left}s")
            else:
                print(f"\n⚠️ {args.wait}s 内未检测到登录")

        shot = args.save or os.path.join(SHOTS, "getnote_session.png")
        try:
            page.screenshot(path=shot)
            print(f"截图: {shot}")
        except Exception:
            pass

        # 保存登录态
        try:
            ctx.storage_state(path=STATE_FILE)
            print(f"✅ 登录态已保存: {STATE_FILE}")
        except Exception as e:
            print(f"⚠️ 登录态保存失败: {e}")

        cks = [c["name"] for c in ctx.cookies() if "biji" in c.get("domain", "")]
        print(f"biji cookie: {cks}")
        ctx.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
