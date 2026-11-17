# -*- coding: utf-8 -*-
"""
launch_login_detached.py —— 用 Windows 独立进程组(非沙箱树)拉起有头登录浏览器
关键：subprocess 的 CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS 让子进程脱离调用方进程树
"""
import os, sys, subprocess, time

sys.stdout.reconfigure(encoding="utf-8")

PY = r"C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe"
SCRIPT = r"E:\博主学习库\_tools\getnote_login.py"
WAIT = sys.argv[1] if len(sys.argv) > 1 else "900"

DETACHED = 0x00000008 | 0x00000200  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
CREATE_NEW_CONSOLE = 0x00000010

env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"
env["HF_ENDPOINT"] = "https://hf-mirror.com"

print(f"拉起有头登录浏览器（等待 {WAIT}s）...")
p = subprocess.Popen(
    [PY, SCRIPT, "--wait", WAIT],
    creationflags=DETACHED,
    env=env,
    cwd=r"E:\博主学习库\_tools",
    close_fds=True,
)
print(f"PID={p.pid}  （独立进程组，已脱离沙箱树）")
time.sleep(12)
print("=== 12 秒后检查 ===")
r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq chrome.exe", "/FO", "CSV", "/NH"],
                   capture_output=True)
n = len([l for l in r.stdout.decode("gbk", "ignore").splitlines() if "chrome" in l.lower()])
print(f"chrome 进程数: {n}")
r2 = subprocess.run(["tasklist", "/FI", "IMAGENAME eq python.exe", "/FO", "CSV", "/NH"],
                    capture_output=True)
n2 = len([l for l in r2.stdout.decode("gbk", "ignore").splitlines() if "python" in l.lower()])
print(f"python 进程数: {n2}")
