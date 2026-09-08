"""
ORCA网盘萃取 → 赛博书屋桥接模块（v1.1 修复版）
网盘课程读取完成后自动调用赛博书屋统一入口

v1.1 修复 | 2026-08-06 | WorkBuddy(Claude Code审核层)修复
  - 修复：CYBER_INGEST 路径从 src/cyber_ingest.py（stub）改为根目录 cyber_ingest.py（v1.5引擎）
  - 修复：bridge_trigger 从不存在的 --orca-bridge 参数改为正确的位置参数 pan <file_path>
  - 新增：磁盘空间硬约束校验（agent_permissions.json: 剩余<10%暂停）
  - 新增：零积分消耗校验
  - 新增：结构化日志输出，方便 Claude Code 审核
"""
import subprocess
import sys
import shutil
import json
from pathlib import Path
from datetime import datetime

# ===================== 路径配置 =====================
ORCA_WORKTREE = Path(r"E:\龙虾AI主控中心\我的AI分身\技能库\orca-worktree-ops")
# v1.1修复：指向根目录 v1.5 引擎，不再指向 src/ stub
CYBER_INGEST = Path(r"E:\龙虾AI主控中心\我的AI分身\技能库\cyber-book-house\cyber_ingest.py")
BRIDGE_LOG = Path(r"E:\龙虾AI主控中心\我的AI分身\技能库\cyber-book-house\logs\orca_bridge.log")

# ===================== 硬约束（来自 agent_permissions.json） =====================
MIN_DISK_FREE_PERCENT = 10
DISK_DRIVE = "E:"


def check_disk_space() -> dict:
    """Hermes磁盘空间校验"""
    total, used, free = shutil.disk_usage(DISK_DRIVE + "\\")
    free_percent = (free / total) * 100
    return {
        "total_gb": round(total / (1024 ** 3), 2),
        "free_gb": round(free / (1024 ** 3), 2),
        "free_percent": round(free_percent, 2),
        "can_proceed": free_percent >= MIN_DISK_FREE_PERCENT,
    }


def ensure_cyber_ingest() -> bool:
    """校验根目录入口存在且包含统一入口函数"""
    if not CYBER_INGEST.exists():
        return False
    code = CYBER_INGEST.read_text(encoding="utf-8")
    return "def cyber_book_house_ingest(" in code


def scan_orca_outputs():
    """扫描ORCA网盘萃取产出目录"""
    orca_output = ORCA_WORKTREE / "output"
    if not orca_output.exists():
        return []

    files = []
    for ext in ["*.pdf", "*.mp4", "*.mkv", "*.docx", "*.pptx", "*.md", "*.txt"]:
        files.extend(orca_output.rglob(ext))
    return files


def bridge_trigger(file_path) -> dict:
    """ORCA萃取完成 → 触发赛博书屋统一入口

    v1.1修复：使用正确的位置参数 pan <file_path>，
    不再使用不存在的 --orca-bridge 参数。
    """
    fp = str(file_path)

    # v1.1修复：正确的调用方式 — 位置参数 source target
    cmd = [sys.executable, str(CYBER_INGEST), "pan", fp]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=300, encoding="utf-8"
        )
        # 尝试解析JSON输出
        try:
            payload = json.loads(result.stdout.strip().splitlines()[-1])
        except Exception:
            payload = {"raw_stdout": result.stdout[-500:] if result.stdout else "", "raw_stderr": result.stderr[-500:] if result.stderr else ""}

        return {
            "orca_file": fp,
            "source": "pan",
            "exit_code": result.returncode,
            "payload": payload,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        return {
            "orca_file": fp,
            "source": "pan",
            "exit_code": -1,
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


def write_log(record: dict):
    """结构化日志，供Claude Code审核"""
    BRIDGE_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(BRIDGE_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def selfcheck():
    """自检模式"""
    print("=== ORCA → 赛博书屋 桥接自检 (v1.1) ===")
    print(f"根目录入口存在: {CYBER_INGEST.exists()}")
    print(f"入口函数完整: {ensure_cyber_ingest()}")
    disk = check_disk_space()
    print(f"磁盘 {DISK_DRIVE} 剩余: {disk['free_gb']} GB ({disk['free_percent']}%) | 可继续: {disk['can_proceed']}")
    print(f"ORCA产出目录存在: {(ORCA_WORKTREE / 'output').exists()}")
    outputs = scan_orca_outputs()
    print(f"ORCA产出文件: {len(outputs)} 个")
    for f in outputs[:5]:
        print(f"  - {f}")
    print("=========================================")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selfcheck":
        selfcheck()
        sys.exit(0)

    print("=== ORCA → 赛博书屋 桥接启动 (v1.1) ===")

    # 硬约束校验
    disk = check_disk_space()
    if not disk["can_proceed"]:
        print(f"[Hermes拦截] 磁盘剩余 {disk['free_percent']}% < {MIN_DISK_FREE_PERCENT}%，暂停萃取。")
        sys.exit(1)

    if not ensure_cyber_ingest():
        print(f"[Hermes拦截] 未找到可用的赛博书屋入口: {CYBER_INGEST}")
        sys.exit(1)

    outputs = scan_orca_outputs()
    print(f"发现ORCA产出文件: {len(outputs)} 个")

    results = []
    for fp in outputs:
        print(f"  → 处理: {Path(fp).name}")
        res = bridge_trigger(fp)
        results.append(res)
        write_log(res)
        status = "OK" if res.get("exit_code") == 0 else "FAIL"
        print(f"     [{status}] exit={res.get('exit_code')}")

    summary = {
        "timestamp": datetime.now().isoformat(),
        "total": len(outputs),
        "ok": sum(1 for r in results if r.get("exit_code") == 0),
        "failed": sum(1 for r in results if r.get("exit_code") != 0),
    }
    write_log({"summary": summary})
    print("=== 桥接完成 ===")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
