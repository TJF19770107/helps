"""
微信视频号 Cookie 自动提取工具
用法: python wechat_cookie_login.py
步骤:
  1. 自动打开 Edge 浏览器
  2. 导航到 channels.weixin.qq.com
  3. 用手机微信扫码登录
  4. 自动检测登录成功并提取 Cookie
  5. Cookie 写入 wx_cookie.txt
"""
from playwright.sync_api import sync_playwright
import time, re, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "wx_cookie.txt")

print("=" * 50)
print("WeChat Video Channel Cookie Extractor")
print("=" * 50)
print()

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=False)
    page = browser.new_page()
    page.goto("https://channels.weixin.qq.com/", wait_until="domcontentloaded", timeout=30000)
    
    print(">>> Browser opened at channels.weixin.qq.com")
    print(">>> Scan the QR code with WeChat NOW!")
    print(">>> Waiting for login (auto-detecting, max 2 min)...")
    print()
    
    cookies = []
    logged_in = False
    
    for i in range(60):
        time.sleep(2)
        current_cookies = page.context.cookies()
        cookie_names = [c['name'] for c in current_cookies]
        
        # Detection: if we have meaningful cookies (not just analytics)
        meaningful = [c for c in current_cookies if c['name'] not in 
                      ('sensorsdata', '_ga', 'Hm_lvt', 'Hm_lpvt', 'Hm_lpvt_sm')]
        
        page_url = page.url.lower()
        url_changed = any(kw in page_url for kw in ('/home', 'dashboard', 'finder', 'profile'))
        
        if meaningful or url_changed:
            cookies = current_cookies
            logged_in = True
            break
        
        if i % 5 == 0:
            elapsed = i * 2
            print(f"  [{elapsed}s] Still waiting... (cookies: {len(current_cookies)}, url: {page.url})")
            # Print cookie names for debugging
            if cookie_names:
                print(f"  Cookie names: {', '.join(cookie_names)}")
    
    if logged_in:
        cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
        print(f"\n>>> SUCCESS! {len(cookies)} cookies extracted")
        print(f">>> Writing to {OUTPUT_FILE}...")
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(cookie_str)
        
        print(f">>> Done! Cookie string length: {len(cookie_str)}")
    else:
        print(f"\n>>> TIMEOUT: Login not detected after 2 minutes.")
        print(">>> Please make sure you've scanned the QR code with WeChat.")
        print(">>> Partial cookies will be saved anyway.")
        
        all_cookies = page.context.cookies()
        if all_cookies:
            cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in all_cookies])
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                f.write(cookie_str)
            print(f">>> Saved {len(all_cookies)} partial cookies")
    
    browser.close()

print()
print("=" * 50)
print("Complete. Check wx_cookie.txt for the result.")
print("Then tell WorkBuddy: 'wx_cookie ready'")
print("=" * 50)
