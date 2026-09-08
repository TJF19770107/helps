# -*- coding: utf-8 -*-
"""
hy3_watchdog.py — HY3混元本地代理 看门狗
用途：由 Windows 计划任务调用（登录时 + 每5分钟）
行为：
  1. 探测 127.0.0.1:15731 是否存活
  2. 若已存活 → 直接退出（无操作）
  3. 若未存活 → 以 DETACHED 方式拉起 hy3_proxy.py（脱离父进程存活）
仅用标准库，无第三方依赖。
"""
import socket
import subprocess
import sys
import os
import time

PORT = 15731
PYTHON = r"C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe"
HERE = os.path.dirname(os.path.abspath(__file__))
PROXY = os.path.join(HERE, "hy3_proxy.py")
LOG_DIR = os.path.join(HERE, "logs")
DETACHED = 0x00000200 | 0x00000800  # CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS


def is_up():
    s = socket.socket()
    s.settimeout(2)
    try:
        s.connect(("127.0.0.1", PORT))
        return True
    except Exception:
        return False
    finally:
        try:
            s.close()
        except Exception:
            pass


def start():
    os.makedirs(LOG_DIR, exist_ok=True)
    log = open(os.path.join(LOG_DIR, "watchdog_launch.log"), "a", encoding="utf-8")
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    log.write(f"[{ts}] watchdog 尝试拉起 hy3_proxy.py\n")
    log.flush()
    subprocess.Popen(
        [PYTHON, PROXY],
        cwd=HERE,
        stdout=log,
        stderr=subprocess.STDOUT,
        creationflags=DETACHED,
        close_fds=True,
    )


if __name__ == "__main__":
    if is_up():
        print("OK :15731 代理已存活，无需操作")
        sys.exit(0)
    print("WARN :15731 未响应，watchdog 拉起代理...")
    start()
    time.sleep(3)
    if is_up():
        print("RESTART 成功 :15731 已恢复")
        sys.exit(0)
    else:
        print("RESTART 失败 :15731 仍无响应，请检查日志")
        sys.exit(1)
