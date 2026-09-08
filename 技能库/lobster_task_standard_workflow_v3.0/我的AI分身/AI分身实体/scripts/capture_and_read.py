#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
capture_and_read.py · 截图 + 读图 合并动作（一个命令：截屏→视觉模型→文字）
==================================================
用法：
  python capture_and_read.py [问题]
示例：
  python capture_and_read.py "读一下屏幕上有什么窗口"
产出：截图存 C:\\tmp\\screen_<ts>.png，并把 NVIDIA 视觉模型读出的文字打印出来。
零成本（NVIDIA 免费额度）。只新增本文件，不删不改任何东西。
"""
import os
import sys
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
VISION = os.path.join(HERE, "vision_read.py")
PY = r"C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe"
OUT_DIR = r"C:\tmp"


def capture(out_path):
    """PowerShell + System.Drawing 抓主屏，存 PNG。"""
    ps = (
        "Add-Type -AssemblyName System.Drawing; "
        "Add-Type -AssemblyName System.Windows.Forms; "
        "$b=[System.Windows.Forms.Screen]::PrimaryScreen.Bounds; "
        "$bmp=New-Object System.Drawing.Bitmap $b.Width,$b.Height; "
        "$g=[System.Drawing.Graphics]::FromImage($bmp); "
        "$g.CopyFromScreen($b.Location,[System.Drawing.Point]::Empty,$b.Size); "
        "$bmp.Save('" + out_path + "',[System.Drawing.Imaging.ImageFormat]::Png); "
        "$g.Dispose(); $bmp.Dispose()"
    )
    r = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                       capture_output=True, text=True, timeout=60)
    if r.returncode != 0 or not os.path.exists(out_path):
        raise RuntimeError("截图失败: " + (r.stderr or r.stdout or "").strip()[:300])
    return out_path


def main():
    question = sys.argv[1] if len(sys.argv) > 1 else "请用中文概述这张屏幕截图里能看到什么，包括窗口标题、界面元素。"
    os.makedirs(OUT_DIR, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    img = os.path.join(OUT_DIR, "screen_%s.png" % ts)
    capture(img)
    print("[截图] 已保存:", img)
    print("[读图] 调用视觉模型...")
    r = subprocess.run([PY, VISION, img, question], capture_output=True, text=True, timeout=120)
    print("---- 视觉解读 ----")
    print((r.stdout or r.stderr).strip())
    print("------------------")


if __name__ == "__main__":
    main()