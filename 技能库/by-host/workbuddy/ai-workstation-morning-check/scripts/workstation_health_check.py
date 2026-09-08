#!/usr/bin/env python3
"""
AI Workstation Morning Health Check
一键盘扫描所有关键AI基础设施组件，输出红黄绿三级健康报告。

Usage:
    python workstation_health_check.py              # 快速模式
    python workstation_health_check.py --full       # 完整模式（含Ollama/Git）
    python workstation_health_check.py --json       # JSON输出
    python workstation_health_check.py --quiet       # 仅输出异常项

Author: auto-skill-generator V2.3 (2026-08-26)
"""

import ctypes
import ctypes.wintypes as wt
import json
import os
import shutil
import socket
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# ============================================================
# 配置
# ============================================================

DISK_THRESHOLDS = {
    "C": {"critical": 2, "warning": 5},    # GB
    "E": {"critical": 2, "warning": 10},
    "G": {"critical": 20, "warning": 100},
    "D": {"critical": 2, "warning": 5},
}

MARVIS_PROCESSES = {
    "marvis.exe": 1,
    "marvissvr.exe": 1,
    "marvisdlsvr.exe": 1,
    "marvishost.exe": 1,
    "marvisagent.exe": 1,
    "marvisknowledgebase.exe": 4,
}

PORT_CHECKS = [
    (15721, "CC-Switch总网关", True),
    (4567, "AI Code Switch代理", True),
    (57321, "Codex++本地控制", False),
    (15731, "HY3混元代理", False),
    (18808, "MiMo V2.5 Pro", True),
    (8765, "MCP-HTTP适配器", False),
]

PYTHON_PATH = r"C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe"
NODE_PATH = r"C:\Users\Administrator\.workbuddy\binaries\node\versions\22.22.2\node.exe"

# Chrome paths to check
CHROME_CANDIDATES = [
    r"D:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\ms-playwright"),
]

OLLAMA_MODELS_CMD = "ollama list"

# Colors
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# ============================================================
# 检查函数
# ============================================================

def check_disk_space():
    """检查C/E/G/D盘可用空间"""
    results = []
    for letter, thresholds in DISK_THRESHOLDS.items():
        try:
            total, used, free = shutil.disk_usage(f"{letter}:\\")
            free_gb = free / (1024**3)
            if free_gb < thresholds["critical"]:
                status = "CRITICAL"
                color = RED
            elif free_gb < thresholds["warning"]:
                status = "WARNING"
                color = YELLOW
            else:
                status = "OK"
                color = GREEN
            results.append({
                "component": f"{letter}盘磁盘空间",
                "detail": f"{letter}: {free_gb:.1f}GB available",
                "status": status,
                "color": color,
                "value": round(free_gb, 1),
            })
        except Exception as e:
            results.append({
                "component": f"{letter}盘磁盘空间",
                "detail": f"检查失败: {e}",
                "status": "ERROR",
                "color": RED,
            })
    return results


def check_marvis_processes():
    """检查Marvis进程是否全部运行"""
    try:
        k = ctypes.windll.kernel32
        class ProcessEntry32(ctypes.Structure):
            _fields_ = [
                ('dwSize', wt.DWORD),
                ('cntUsage', wt.DWORD),
                ('th32ProcessID', wt.DWORD),
                ('th32DefaultHeapID', ctypes.POINTER(wt.ULONG)),
                ('th32ModuleID', wt.DWORD),
                ('cntThreads', wt.DWORD),
                ('th32ParentProcessID', wt.DWORD),
                ('pcPriClassBase', ctypes.c_long),
                ('dwFlags', wt.DWORD),
                ('szExeFile', ctypes.c_char * 260),
            ]

        snapshot = k.CreateToolhelp32Snapshot(0x00000002, 0)  # TH32CS_SNAPPROCESS
        pe = ProcessEntry32()
        pe.dwSize = ctypes.sizeof(ProcessEntry32)
        found = {}

        if k.Process32First(snapshot, ctypes.byref(pe)):
            while True:
                name = pe.szExeFile.decode('utf-8', 'ignore').lower()
                if 'marvis' in name:
                    found[name] = found.get(name, 0) + 1
                if not k.Process32Next(snapshot, ctypes.byref(pe)):
                    break
        k.CloseHandle(snapshot)

        results = []
        total_expected = sum(MARVIS_PROCESSES.values())
        total_found = sum(found.values())

        for proc_name, expected_count in MARVIS_PROCESSES.items():
            actual = found.get(proc_name, 0)
            if actual >= expected_count:
                status = "OK"
                color = GREEN
            elif actual > 0:
                status = "WARNING"
                color = YELLOW
            else:
                status = "MISSING"
                color = RED
            results.append({
                "component": f"Marvis进程 {proc_name}",
                "detail": f"期望{expected_count}/实际{actual}",
                "status": status,
                "color": color,
            })

        return results
    except Exception as e:
        return [{
            "component": "Marvis进程检查",
            "detail": f"检查失败: {e}",
            "status": "ERROR",
            "color": RED,
        }]


def check_port(port, name, required):
    """检查端口是否在监听"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex(("127.0.0.1", port))
        sock.close()

        if result == 0:
            return {
                "component": f"端口 {port} ({name})",
                "detail": "监听中",
                "status": "OK",
                "color": GREEN,
            }
        elif required:
            return {
                "component": f"端口 {port} ({name})",
                "detail": "未监听（必需端口）",
                "status": "WARNING",
                "color": YELLOW,
            }
        else:
            return {
                "component": f"端口 {port} ({name})",
                "detail": "未监听（可选）",
                "status": "INFO",
                "color": CYAN,
            }
    except Exception as e:
        return {
            "component": f"端口 {port} ({name})",
            "detail": f"检查失败: {e}",
            "status": "ERROR",
            "color": RED,
        }


def check_mcp_health():
    """检查MCP-HTTP适配器health端点"""
    try:
        import urllib.request
        req = urllib.request.Request("http://127.0.0.1:8765/health")
        req.add_header("Connection", "close")
        with urllib.request.urlopen(req, timeout=2) as resp:
            data = json.loads(resp.read())
            return {
                "component": "MCP-HTTP适配器",
                "detail": f"运行中，{data.get('tools', '?')}个工具",
                "status": "OK",
                "color": GREEN,
            }
    except Exception:
        return {
            "component": "MCP-HTTP适配器",
            "detail": "未运行（如需远程调用请启动）",
            "status": "INFO",
            "color": CYAN,
        }


def check_chrome():
    """检查Chrome/Chromium可用性"""
    for path in CHROME_CANDIDATES:
        if os.path.exists(path):
            return {
                "component": "Chrome/Chromium",
                "detail": f"存在: {path}",
                "status": "OK",
                "color": GREEN,
            }
    return {
        "component": "Chrome/Chromium",
        "detail": "未找到（Playwright自动化可能不可用）",
        "status": "WARNING",
        "color": YELLOW,
    }


def check_runtime():
    """检查Python/Node运行时"""
    results = []
    for name, path in [("Python", PYTHON_PATH), ("Node", NODE_PATH)]:
        if os.path.exists(path):
            try:
                ver = subprocess.check_output(
                    [path, "--version"],
                    stderr=subprocess.STDOUT,
                    timeout=5,
                    text=True
                ).strip()
                results.append({
                    "component": f"{name}运行时",
                    "detail": ver,
                    "status": "OK",
                    "color": GREEN,
                })
            except Exception:
                results.append({
                    "component": f"{name}运行时",
                    "detail": f"存在但无法执行: {path}",
                    "status": "WARNING",
                    "color": YELLOW,
                })
        else:
            results.append({
                "component": f"{name}运行时",
                "detail": f"不存在: {path}",
                "status": "CRITICAL",
                "color": RED,
            })
    return results


def check_ollama_models():
    """完整模式：检查Ollama模型列表"""
    try:
        output = subprocess.check_output(
            OLLAMA_MODELS_CMD,
            shell=True,
            timeout=10,
            text=True,
            stderr=subprocess.STDOUT
        )
        lines = [l for l in output.strip().split('\n') if l and not l.startswith('NAME')]
        return {
            "component": "Ollama模型",
            "detail": f"{len(lines)}个模型可用",
            "status": "OK",
            "color": GREEN,
        }
    except Exception:
        return {
            "component": "Ollama模型",
            "detail": "Ollama未运行或未安装",
            "status": "WARNING",
            "color": YELLOW,
        }


def check_git_status():
    """完整模式：检查关键Git仓库状态"""
    repos = [
        r"E:\龙虾AI主控中心",
        r"C:\Users\Administrator\WorkBuddy\automation-20260515020232",
    ]
    results = []
    for repo in repos:
        if not os.path.isdir(os.path.join(repo, ".git")):
            continue
        try:
            output = subprocess.check_output(
                ["git", "status", "--porcelain"],
                cwd=repo,
                timeout=5,
                text=True,
                stderr=subprocess.DEVNULL
            )
            changes = [l for l in output.strip().split('\n') if l]
            if changes:
                results.append({
                    "component": f"Git仓库 {os.path.basename(repo)}",
                    "detail": f"{len(changes)}个未提交变更",
                    "status": "INFO",
                    "color": CYAN,
                })
            else:
                results.append({
                    "component": f"Git仓库 {os.path.basename(repo)}",
                    "detail": "干净",
                    "status": "OK",
                    "color": GREEN,
                })
        except Exception:
            pass
    return results


# ============================================================
# 报告输出
# ============================================================

def print_report(results, quiet=False, json_out=False):
    """输出健康报告"""
    if json_out:
        json_data = {
            "timestamp": datetime.now().isoformat(),
            "total_checks": len(results),
            "critical": sum(1 for r in results if r["status"] == "CRITICAL"),
            "warning": sum(1 for r in results if r["status"] == "WARNING"),
            "ok": sum(1 for r in results if r["status"] == "OK"),
            "results": [{"component": r["component"], "detail": r["detail"], "status": r["status"]} for r in results],
        }
        print(json.dumps(json_data, ensure_ascii=False, indent=2))
        return json_data["critical"] > 0

    # 过滤静默模式
    if quiet:
        results = [r for r in results if r["status"] not in ("OK", "INFO")]

    if not results:
        print(f"{GREEN}✓ 工作站全部正常{RESET}")
        return False

    has_critical = any(r["status"] == "CRITICAL" for r in results)
    has_warning = any(r["status"] == "WARNING" for r in results)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"\n{'='*50}")
    print(f"  AI 工作站健康体检报告  {now}")
    print(f"{'='*50}\n")

    # 按类别分组
    categories = {}
    for r in results:
        cat = r["component"].split()[0] if " " in r["component"] else r["component"]
        if "磁盘" in r["component"]:
            cat = "磁盘空间"
        elif "Marvis" in r["component"]:
            cat = "Marvis进程"
        elif "端口" in r["component"]:
            cat = "端口状态"
        elif "MCP" in r["component"]:
            cat = "MCP服务"
        elif "Chrome" in r["component"]:
            cat = "浏览器"
        elif "运行时" in r["component"] or "Python" in r["component"] or "Node" in r["component"]:
            cat = "运行时"
        elif "Ollama" in r["component"]:
            cat = "AI模型"
        elif "Git" in r["component"]:
            cat = "版本控制"
        categories.setdefault(cat, []).append(r)

    for cat, items in categories.items():
        print(f"  [{cat}]")
        for r in items:
            icon = {"OK": "🟢", "WARNING": "🟡", "CRITICAL": "🔴", "INFO": "🔵", "ERROR": "🔴", "MISSING": "🔴"}.get(r["status"], "❓")
            print(f"    {icon} {r['component']}: {r['detail']}")
        print()

    print(f"{'='*50}")
    if has_critical:
        print(f"  总评: {RED}{BOLD}🔴 有{sum(1 for r in results if r['status']=='CRITICAL')}个严重故障{RESET}")
        print(f"  建议: 必须先修复严重故障再开工")
    elif has_warning:
        print(f"  总评: {YELLOW}{BOLD}🟡 有{sum(1 for r in results if r['status']=='WARNING')}个警告项{RESET}")
        print(f"  建议: 建议先处理警告项")
    else:
        print(f"  总评: {GREEN}{BOLD}🟢 工作站健康，可以开工{RESET}")
    print(f"{'='*50}\n")

    return has_critical


# ============================================================
# 主函数
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI Workstation Morning Health Check")
    parser.add_argument("--full", action="store_true", help="完整模式：含Ollama/Git检查")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    parser.add_argument("--quiet", action="store_true", help="仅输出异常项")
    args = parser.parse_args()

    start = time.time()

    results = []
    results.extend(check_disk_space())
    results.extend(check_marvis_processes())

    for port, name, required in PORT_CHECKS:
        results.append(check_port(port, name, required))

    results.append(check_mcp_health())
    results.append(check_chrome())
    results.extend(check_runtime())

    if args.full:
        results.append(check_ollama_models())
        results.extend(check_git_status())

    has_critical = print_report(results, quiet=args.quiet, json_out=args.json)

    elapsed = time.time() - start
    if not args.json:
        print(f"  (耗时 {elapsed:.1f}s)")

    sys.exit(1 if has_critical else 0)


if __name__ == "__main__":
    main()
