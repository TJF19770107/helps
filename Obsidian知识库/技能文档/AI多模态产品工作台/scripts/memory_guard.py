#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
内存守卫 v1.0 —— 防 OOM 连锁崩溃
================================================
定级：第 40 形态（Commit 耗尽型崩溃）
案例：2026-09-29 18:51 MarvisAgent.exe 被 OOM 击杀（用户感知为"自动关机"）
      同批次 17:25/18:07 powershell.exe OOM FailFast、18:06 Robocopy.exe 栈溢出

根因：页面文件被锁死 8GB + CommitLimit 被钉死 40.7GB + 内核池膨胀 8.4GB
      → Commit 冲到 91.3% → 系统连锁击杀进程

核心原则：
  1. Commit 率（提交内存/提交上限）才是 OOM 的判据，不是"可用物理内存"
  2. 重任务启动前必须先 assert，低于阈值直接拒绝，别把自己压垮
  3. 禁止用 Get-WinEvent -MaxEvents 800 这类重查询（本身就是压垮内存的元凶）

用法：
  python memory_guard.py check      # 体检 + 建议（人类可读）
  python memory_guard.py assert     # 超阈值则 exit 1（供流水线前置守卫）
  python memory_guard.py top        # 列吃内存 TOP 进程
  python memory_guard.py selftest   # 自检（含边界用例）
"""
import sys
import ctypes
from ctypes import wintypes

MB = 1024 * 1024

# === 阈值（依 2026-09-29 实测标定）===
COMMIT_WARN = 80.0    # 提交率超过 80% 警告
COMMIT_BLOCK = 90.0   # 提交率超过 90% 拒绝启动重任务
PHYS_WARN_MB = 4096   # 物理可用低于 4GB 警告
KERNEL_POOL_WARN_MB = 4096  # 内核池超过 4GB 警告（正常 <3GB）


class PERF(ctypes.Structure):
    _fields_ = [
        ('cb', wintypes.DWORD),
        ('CommitTotal', ctypes.c_size_t),
        ('CommitLimit', ctypes.c_size_t),
        ('CommitPeak', ctypes.c_size_t),
        ('PhysicalTotal', ctypes.c_size_t),
        ('PhysicalAvailable', ctypes.c_size_t),
        ('SystemCache', ctypes.c_size_t),
        ('KernelTotal', ctypes.c_size_t),
        ('KernelPaged', ctypes.c_size_t),
        ('KernelNonpaged', ctypes.c_size_t),
        ('PageSize', ctypes.c_size_t),
        ('HandleCount', wintypes.DWORD),
        ('ProcessCount', wintypes.DWORD),
        ('ThreadCount', wintypes.DWORD),
    ]


def snapshot():
    """取一次内存快照（psapi 底层，不依赖 PerfMon —— 实测 Get-Counter 在本机全失败）"""
    p = PERF()
    p.cb = ctypes.sizeof(PERF)
    ok = ctypes.windll.psapi.GetPerformanceInfo(ctypes.byref(p), p.cb)
    if not ok:
        raise RuntimeError('GetPerformanceInfo 调用失败')
    return {
        'commit_mb': p.CommitTotal * p.PageSize // MB,
        'commit_limit_mb': p.CommitLimit * p.PageSize // MB,
        'commit_pct': round(p.CommitTotal / p.CommitLimit * 100, 1),
        'phys_total_mb': p.PhysicalTotal * p.PageSize // MB,
        'phys_avail_mb': p.PhysicalAvailable * p.PageSize // MB,
        'sys_cache_mb': p.SystemCache * p.PageSize // MB,
        'kernel_total_mb': p.KernelTotal * p.PageSize // MB,
        'kernel_paged_mb': p.KernelPaged * p.PageSize // MB,
        'kernel_nonpaged_mb': p.KernelNonpaged * p.PageSize // MB,
        'proc_count': p.ProcessCount,
        'handle_count': p.HandleCount,
        'thread_count': p.ThreadCount,
    }


def judge(s):
    """判定核心 —— 纯函数，便于 selftest 注入假数据。
    返回 (verdict, reasons)；verdict ∈ ok/warn/block"""
    reasons = []
    if s['commit_pct'] >= COMMIT_BLOCK:
        reasons.append(f"提交率 {s['commit_pct']}% >= {COMMIT_BLOCK}% (OOM 高危)")
    elif s['commit_pct'] >= COMMIT_WARN:
        reasons.append(f"提交率 {s['commit_pct']}% >= {COMMIT_WARN}% (偏高)")
    if s['phys_avail_mb'] < PHYS_WARN_MB:
        reasons.append(f"物理可用 {s['phys_avail_mb']}MB < {PHYS_WARN_MB}MB")
    if s['kernel_total_mb'] > KERNEL_POOL_WARN_MB:
        reasons.append(f"内核池 {s['kernel_total_mb']}MB > {KERNEL_POOL_WARN_MB}MB (疑驱动泄漏)")
    if s['commit_pct'] >= COMMIT_BLOCK:
        return 'block', reasons
    if reasons:
        return 'warn', reasons
    return 'ok', []


def top_processes(n=12):
    """轻量取 TOP 进程（用 tasklist，避免 WMI 重查询）"""
    import subprocess
    try:
        out = subprocess.run(['tasklist', '/fo', 'csv', '/nh'],
                             capture_output=True, text=True,
                             encoding='gbk', errors='replace').stdout
    except Exception:
        return []
    rows = []
    for ln in out.splitlines():
        p = [x.strip('"') for x in ln.split('","')]
        if len(p) >= 5:
            try:
                rows.append((int(p[4].replace(',', '').replace(' K', '').strip()), p[0], p[1]))
            except ValueError:
                continue
    rows.sort(reverse=True)
    return rows[:n]


def cmd_check():
    s = snapshot()
    v, reasons = judge(s)
    print('=== 内存守卫体检 ===')
    print(f"提交内存  : {s['commit_mb']:>7} MB / 上限 {s['commit_limit_mb']} MB  →  {s['commit_pct']}%")
    print(f"物理内存  : {s['phys_total_mb']:>7} MB / 可用 {s['phys_avail_mb']} MB")
    print(f"系统缓存  : {s['sys_cache_mb']:>7} MB")
    print(f"内核池    : {s['kernel_total_mb']:>7} MB (分页 {s['kernel_paged_mb']} + 非分页 {s['kernel_nonpaged_mb']})")
    print(f"进程/句柄/线程: {s['proc_count']} / {s['handle_count']} / {s['thread_count']}")
    print()
    tag = {'ok': '[OK]', 'warn': '[WARN]', 'block': '[BLOCK]'}[v]
    print(f"{tag} 判定：{v.upper()}")
    for r in reasons:
        print(f"   - {r}")
    if v != 'ok':
        print()
        print('Top 吃内存进程：')
        for mem, name, pid in top_processes(10):
            print(f"   {mem/1024/1024:7.3f} GB  {name} (PID {pid})")
        print()
        print('缓解建议：')
        print('   1) 关掉不用的 Electron/浏览器/IDE（本机 360/2345 系安全软件会泄漏内核池）')
        print('   2) 页面文件改“系统自动管理”（根治，需管理员+重启）')
        print('   3) 重任务拆小步跑，别一次压满（参考第39形态：源站100s网关超时）')
    return v


def cmd_assert():
    s = snapshot()
    v, reasons = judge(s)
    if v == 'block':
        print(f'[BLOCK] 内存守卫拒绝启动重任务（提交率 {s["commit_pct"]}%）', file=sys.stderr)
        for r in reasons:
            print(f'   - {r}', file=sys.stderr)
        return 1
    if v == 'warn':
        print(f'[WARN] 内存吃紧但放行（提交率 {s["commit_pct"]}%）')
        for r in reasons:
            print(f'   - {r}')
    return 0


def cmd_top():
    for mem, name, pid in top_processes(20):
        print(f'{mem/1024/1024:8.3f} GB  {name} (PID {pid})')


def cmd_selftest():
    """自检：注入假快照验证判定逻辑（含边界与防误报用例）"""
    base = {'commit_mb': 10000, 'commit_limit_mb': 40000, 'commit_pct': 25.0,
            'phys_total_mb': 32000, 'phys_avail_mb': 20000, 'sys_cache_mb': 5000,
            'kernel_total_mb': 2000, 'kernel_paged_mb': 1500, 'kernel_nonpaged_mb': 500,
            'proc_count': 200, 'handle_count': 100000, 'thread_count': 3000}
    cases = [
        ('健康环境', dict(base), 'ok'),
        ('提交率80%边界(应warn)', {**base, 'commit_pct': 80.0}, 'warn'),
        ('提交率91%(应block)', {**base, 'commit_pct': 91.0}, 'block'),
        ('物理可用3G(应warn)', {**base, 'phys_avail_mb': 3000}, 'warn'),
        ('内核池5G(应warn)', {**base, 'kernel_total_mb': 5000}, 'warn'),
        ('复刻09-29实况(应block)', {**base, 'commit_pct': 91.3, 'phys_avail_mb': 6742, 'kernel_total_mb': 8429}, 'block'),
        ('健康但缓存高(应ok，防误报)', {**base, 'sys_cache_mb': 15000}, 'ok'),
        ('进程数多但内存健康(应ok，防误报)', {**base, 'proc_count': 500}, 'ok'),
    ]
    passed = 0
    for name, snap, expect in cases:
        v, _ = judge(snap)
        ok = (v == expect)
        passed += ok
        print(f"  {'PASS' if ok else 'FAIL'}  {name}: 期望={expect} 实得={v}")
    print(f'\n自检结果: {passed}/{len(cases)}')
    return 0 if passed == len(cases) else 1


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    if cmd == 'check':
        sys.exit(1 if cmd_check() == 'block' else 0)
    elif cmd == 'assert':
        sys.exit(cmd_assert())
    elif cmd == 'top':
        cmd_top()
    elif cmd == 'selftest':
        sys.exit(cmd_selftest())
    else:
        print(__doc__)
        sys.exit(2)
