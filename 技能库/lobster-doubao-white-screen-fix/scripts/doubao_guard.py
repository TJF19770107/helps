#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""豆包白板守卫 v1.0（龙虾零成本运维守卫家族）
判活三件套（杜绝「进程活着但白板」假成功）：
 1. 进程在不在 —— ctypes EnumProcesses（不用 tasklist，沙箱内静默返回空）
 2. 窗口在不在 —— EnumWindows + IsWindowVisible + GetWindowText
 3. 像素是不是白板 —— PrintWindow/BitBlt 抓窗口位图，统计颜色多样性
    · 单一颜色占比 > 97% → WHITE_SCREEN（白板）
    · 否则 → OK
外加：User Data 位置体检（junction 到外置盘 = 结构性风险）

用法：
  python doubao_guard.py            # 体检 + 报告
  python doubao_guard.py --fix      # 检出白板自动修复（杀进程→隔离GPU缓存→重启）
  python doubao_guard.py --json     # 纯 JSON 输出（供计划任务/告警消费）
"""
import os
import sys
import json
import time
import ctypes
import argparse
import subprocess
from ctypes import wintypes
from pathlib import Path
from datetime import datetime

k32 = ctypes.windll.kernel32
psapi = ctypes.windll.psapi
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

PROCESS_QUERY_LIMITED_INFO = 0x1000
PROCESS_TERMINATE = 0x0001
FILE_ATTRIBUTE_REPARSE_POINT = 0x400

USER_DATA_PARENT = Path(os.environ.get('LOCALAPPDATA', r'C:\Users\Administrator\AppData\Local')) / 'Doubao'
DOUBAO_EXE = Path(r'E:\龙虾AI主控中心\Doubao\app\Doubao.exe')
DEFAULT_REPORT = Path(r'G:\WorkBuddy_Data\tmp\doubao_guard_report.json')

LAUNCH_FLAGS = ['--disable-gpu', '--disable-gpu-compositing', '--disable-dev-shm-usage',
                '--renderer-process-limit=2']
CACHE_DIRS = ['Default/GPUCache', 'GrShaderCache', 'ShaderCache', 'GraphiteDawnCache',
              'Default/Code Cache', 'Default/Service Worker/CacheStorage']


def log(m):
    print(f'[{datetime.now().strftime("%H:%M:%S")}] {m}', flush=True)


# ---------- 进程层 ----------
def enum_pids():
    arr = (wintypes.DWORD * 8192)()
    need = wintypes.DWORD()
    psapi.EnumProcesses(ctypes.byref(arr), ctypes.sizeof(arr), ctypes.byref(need))
    return list(arr[:need.value // ctypes.sizeof(wintypes.DWORD)])


def exe_of(pid):
    h = k32.OpenProcess(PROCESS_QUERY_LIMITED_INFO, False, pid)
    if not h:
        return None
    try:
        b = ctypes.create_unicode_buffer(4096)
        s = wintypes.DWORD(4096)
        return b.value if k32.QueryFullProcessImageNameW(h, 0, b, ctypes.byref(s)) else None
    except Exception:
        return None
    finally:
        k32.CloseHandle(h)


def doubao_procs():
    return [(p, e) for p in enum_pids() if (e := exe_of(p)) and 'doubao' in e.lower()]


def kill_doubao():
    killed = []
    for pid, _ in doubao_procs():
        h = k32.OpenProcess(PROCESS_TERMINATE, False, pid)
        if h:
            if k32.TerminateProcess(h, 1):
                killed.append(pid)
            k32.CloseHandle(h)
    w = 0.0
    while doubao_procs() and w < 30:
        time.sleep(0.5)
        w += 0.5
    return killed, w


# ---------- 窗口层 ----------
def doubao_windows():
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    found = []

    def cb(hwnd, lp):
        found.append(hwnd)
        return True

    user32.EnumWindows(WNDENUMPROC(cb), 0)
    out = []
    for hw in found:
        if not user32.IsWindowVisible(hw):
            continue
        n = user32.GetWindowTextLengthW(hw)
        if not n:
            continue
        b = ctypes.create_unicode_buffer(n + 1)
        user32.GetWindowTextW(hw, b, n + 1)
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hw, ctypes.byref(pid))
        e = exe_of(pid.value)
        if e and 'doubao' in e.lower():
            r = wintypes.RECT()
            user32.GetWindowRect(hw, ctypes.byref(r))
            out.append({'hwnd': hw, 'pid': pid.value, 'title': b.value,
                        'minimized': bool(user32.IsIconic(hw)),
                        'w': r.right - r.left, 'h': r.bottom - r.top})
    return out


# ---------- 像素层（白板判活核心） ----------
def capture_and_analyze(hwnd):
    """抓窗口位图并统计颜色分布；返回 (unique_colors, dominant_ratio, ok)"""
    r = wintypes.RECT()
    if not user32.GetWindowRect(hwnd, ctypes.byref(r)):
        return None
    w, h = r.right - r.left, r.bottom - r.top
    if w < 50 or h < 50:
        return {'error': f'窗口过小 {w}x{h}'}

    hdc_screen = user32.GetWindowDC(hwnd)
    if not hdc_screen:
        return {'error': 'GetWindowDC failed'}
    hdc_mem = gdi32.CreateCompatibleDC(hdc_screen)
    bmp = gdi32.CreateCompatibleBitmap(hdc_screen, w, h)
    gdi32.SelectObject(hdc_mem, bmp)

    # PW_RENDERFULLCONTENT = 2，能抓到 DX/合成后的内容
    ok = user32.PrintWindow(hwnd, hdc_mem, 2)

    class BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [('biSize', wintypes.DWORD), ('biWidth', ctypes.c_long), ('biHeight', ctypes.c_long),
                    ('biPlanes', wintypes.WORD), ('biBitCount', wintypes.WORD), ('biCompression', wintypes.DWORD),
                    ('biSizeImage', wintypes.DWORD), ('biXPelsPerMeter', ctypes.c_long),
                    ('biYPelsPerMeter', ctypes.c_long), ('biClrUsed', wintypes.DWORD),
                    ('biClrImportant', wintypes.DWORD)]

    bi = BITMAPINFOHEADER()
    bi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bi.biWidth = w
    bi.biHeight = -h          # top-down
    bi.biPlanes = 1
    bi.biBitCount = 32
    bi.biCompression = 0

    buf_size = w * h * 4
    buf = (ctypes.c_char * buf_size)()
    got = gdi32.GetDIBits(hdc_mem, bmp, 0, h, buf, ctypes.byref(bi), 0)

    result = {'printwindow_ok': bool(ok), 'width': w, 'height': h, 'dibits': got}
    if got:
        # 采样统计（全量扫 4 字节太慢，隔行采样）
        from collections import Counter
        cnt = Counter()
        step = 4 * 7   # 隔 7 像素采样一次
        sampled = 0
        off = 0
        for y in range(0, h, 3):
            base = y * w * 4
            for x in range(0, w, 7):
                i = base + x * 4
                if i + 2 < buf_size:
                    # c_char 数组取到的是长度 1 的 bytes，需转 int
                    r_, g_, b_ = buf[i + 2][0], buf[i + 1][0], buf[i][0]
                    cnt[(r_, g_, b_)] += 1
                    sampled += 1
        if sampled:
            top_color, top_n = cnt.most_common(1)[0]
            dominant = top_n / sampled
            result.update({'sampled_pixels': sampled, 'unique_colors': len(cnt),
                           'dominant_color': f'#{top_color[0]:02X}{top_color[1]:02X}{top_color[2]:02X}',
                           'dominant_ratio': round(dominant, 4)})
            # 白板判定：单一颜色占比 > 97% 且色彩数极少
            result['white_screen'] = bool(dominant > 0.97 and len(cnt) < 50)
            result['verdict'] = 'WHITE_SCREEN' if result['white_screen'] else 'RENDERED'

    gdi32.DeleteObject(bmp)
    gdi32.DeleteDC(hdc_mem)
    user32.ReleaseDC(hwnd, hdc_screen)
    return result


# ---------- 存储层体检 ----------
def final_path(p):
    CreateFileW = k32.CreateFileW
    CreateFileW.restype = wintypes.HANDLE
    CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                            wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
    h = CreateFileW(str(p), 0, 0x1 | 0x2 | 0x4, None, 3, 0x02000000, None)
    if h == ctypes.c_void_p(-1).value or h is None:
        return None
    try:
        b = ctypes.create_unicode_buffer(4096)
        if k32.GetFinalPathNameByHandleW(h, b, 4096, 0):
            return b.value.replace('\\\\?\\', '')
    finally:
        k32.CloseHandle(h)
    return None


def storage_health():
    fp = final_path(USER_DATA_PARENT)
    is_rp = False
    try:
        is_rp = bool(os.lstat(USER_DATA_PARENT).st_file_attributes & FILE_ATTRIBUTE_REPARSE_POINT)
    except Exception:
        pass
    off_local = bool(fp and fp.upper().startswith('G:'))
    return {'path': str(USER_DATA_PARENT), 'is_reparse': is_rp, 'final_path': fp,
            'on_g_drive': off_local,
            'verdict': 'RISK_外置盘' if off_local else 'OK_本地盘'}


def mem_status():
    class MS(ctypes.Structure):
        _fields_ = [('dwLength', ctypes.c_ulong), ('dwMemoryLoad', ctypes.c_ulong),
                    ('ullTotalPhys', ctypes.c_ulonglong), ('ullAvailPhys', ctypes.c_ulonglong),
                    ('ullTotalPageFile', ctypes.c_ulonglong), ('ullAvailPageFile', ctypes.c_ulonglong),
                    ('ullTotalVirtual', ctypes.c_ulonglong), ('ullAvailVirtual', ctypes.c_ulonglong),
                    ('ullAvailExtendedVirtual', ctypes.c_ulonglong)]
    ms = MS()
    ms.dwLength = ctypes.sizeof(MS)
    k32.GlobalMemoryStatusEx(ctypes.byref(ms))
    return {'percent': ms.dwMemoryLoad, 'available_gb': round(ms.ullAvailPhys / (1024 ** 3), 2)}


# ---------- 修复 ----------
def quarantine_caches():
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    ud = USER_DATA_PARENT / 'User Data'
    done = []
    for rel in CACHE_DIRS:
        src = ud / rel
        if not src.exists():
            continue
        dst = Path(str(src) + f'.quar_{stamp}')
        try:
            os.rename(str(src), dst)
            done.append({'rel': rel, 'to': str(dst)})
        except Exception as e:
            done.append({'rel': rel, 'error': str(e)})
    return done


def fix():
    log('执行修复：杀进程 → 隔离缓存 → 重启')
    killed, waited = kill_doubao()
    q = quarantine_caches()
    subprocess.Popen([str(DOUBAO_EXE)] + LAUNCH_FLAGS, shell=False, creationflags=0x00000010)
    time.sleep(35)
    return {'killed': killed, 'waited': waited, 'quarantined': q}


# ---------- 主流程 ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fix', action='store_true', help='检出异常时自动修复')
    ap.add_argument('--json', action='store_true', help='输出纯 JSON')
    ap.add_argument('--out', default=str(DEFAULT_REPORT))
    args = ap.parse_args()

    rep = {'timestamp': datetime.now().isoformat(), 'guard': 'doubao-guard', 'version': '1.0'}
    procs = doubao_procs()
    wins = doubao_windows()
    rep['process'] = {'count': len(procs), 'pids': [p for p, _ in procs][:20]}
    rep['memory'] = mem_status()
    rep['storage'] = storage_health()

    visible = [w for w in wins if not w['minimized']]
    rep['windows'] = {'total': len(wins), 'visible': len(visible), 'list': wins}

    pixel = None
    if visible:
        # 取面积最大的窗口
        target = max(visible, key=lambda x: x['w'] * x['h'])
        rep['pixel_target'] = target
        pixel = capture_and_analyze(target['hwnd'])
    else:
        pixel = {'error': '无可见窗口'}
    rep['pixel'] = pixel

    # 综合判定
    issues = []
    if not procs:
        issues.append('豆包进程未运行')
    if not visible:
        issues.append('豆包无可见窗口')
    if pixel and pixel.get('white_screen'):
        issues.append(f"窗口白板（主色 {pixel.get('dominant_color')} 占比 {pixel.get('dominant_ratio')}）")
    if rep['storage']['on_g_drive']:
        issues.append(f"User Data 在外置盘 {rep['storage']['final_path']}（结构性风险）")
    if rep['memory']['percent'] >= 90:
        issues.append(f"内存压力 {rep['memory']['percent']}%")

    if not issues:
        level = 'GREEN'
    elif any('白板' in i or '未运行' in i or '无可见' in i for i in issues):
        level = 'RED'
    else:
        level = 'YELLOW'
    rep['issues'] = issues
    rep['level'] = level

    if args.fix and level == 'RED':
        rep['fix'] = fix()
        # 修复后复核
        w2 = [w for w in doubao_windows() if not w['minimized']]
        if w2:
            t = max(w2, key=lambda x: x['w'] * x['h'])
            rep['pixel_after_fix'] = capture_and_analyze(t['hwnd'])
        rep['level_after_fix'] = 'GREEN' if w2 and not rep.get('pixel_after_fix', {}).get('white_screen') else 'RED'

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(rep, f, ensure_ascii=False, indent=2)

    if args.json:
        print(json.dumps(rep, ensure_ascii=False))
    else:
        icon = {'GREEN': '🟢', 'YELLOW': '🟡', 'RED': '🔴'}[level]
        print(f'{icon} 豆包健康等级: {level}')
        print(f'  进程数: {len(procs)}  可见窗口: {len(visible)}')
        if pixel and 'dominant_ratio' in pixel:
            print(f"  像素判活: {pixel.get("verdict")} 主色{pixel.get("dominant_color")} "
                  f"占比{pixel.get("dominant_ratio")} 色彩数{pixel.get("unique_colors")}")
        print(f"  User Data: {rep['storage']['final_path']} ({rep['storage']['verdict']})")
        print(f"  内存: {rep['memory']['percent']}% 可用 {rep['memory']['available_gb']}GB")
        for i in issues:
            print(f'  ⚠️ {i}')
        print(f'  报告: {args.out}')


if __name__ == '__main__':
    main()
