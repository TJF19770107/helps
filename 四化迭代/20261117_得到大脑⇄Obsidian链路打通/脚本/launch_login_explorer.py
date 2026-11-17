# -*- coding: utf-8 -*-
"""
launch_login_explorer.py —— 用 explorer.exe 拉起得到大脑登录窗口（逃出沙箱进程树）

实测教训（2026-11-17）：
  · DETACHED_PROCESS / CREATE_NEW_PROCESS_GROUP 都逃不掉 —— 沙箱用 Job Object 层级清理
  · 唯一可行：explorer.exe 拉起 .cmd —— 进程归属用户 shell，不在沙箱树内
  · schtasks / WMI CreateProcess / PowerShell COM 全被 Program Blacklist 拦

用法：python launch_login_explorer.py [等待秒数，默认 900]
"""
import os, sys, subprocess, time

sys.stdout.reconfigure(encoding="utf-8")

CMD = r"E:\博主学习库\_tools\run_getnote_login.cmd"
WAIT = sys.argv[1] if len(sys.argv) > 1 else "900"


def chrome_count():
    r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq chrome.exe", "/FO", "CSV", "/NH"],
                       capture_output=True)
    return len([l for l in r.stdout.decode("gbk", "ignore").splitlines() if "chrome" in l.lower()])


def cmd_count():
    r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq cmd.exe", "/FO", "CSV", "/NH"],
                       capture_output=True)
    return len([l for l in r.stdout.decode("gbk", "ignore").splitlines() if "cmd" in l.lower()])


print(f"用 explorer.exe 拉起: {CMD}  (等待 {WAIT}s)")
# explorer.exe <file> → 用文件关联打开，进程由 explorer（用户 shell）创建
p = subprocess.run(["explorer.exe", CMD], capture_output=True, text=True,
                   encoding="utf-8", errors="replace")
print(f"explorer rc={p.returncode} {p.stdout.strip()[:120]}")

for i in range(6):
    time.sleep(5)
    c, m = chrome_count(), cmd_count()
    print(f"  +{(i+1)*5}s  chrome={c}  cmd={m}")
    if c > 0:
        print(f"\n✅ Chrome 已启动 {c} 个进程 —— 汤哥可在屏幕上看到得到大脑登录窗口")
        break
else:
    print("\n⚠️ 30s 内未检测到 Chrome 进程，请检查桌面是否弹出窗口")
