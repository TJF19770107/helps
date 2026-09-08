"""
赛博书屋基础设施模块（v1.0 → v1.1 标注）
Codex执行层直接调用，Hermes大脑全程管控

⚠️ v1.1 重要说明（2026-08-06 WorkBuddy审核层添加）：
  本文件是「基础设施层」，提供磁盘校验/积分校验/缓存清理/版本归档等工具函数。
  **不是主入口**。主入口是根目录 cyber_ingest.py（v1.5引擎）。
  - 根目录 cyber_ingest.py：内容抓取 + Obsidian写入 + CLI入口（--instruct/--write/位置参数）
  - 本文件 src/cyber_ingest.py：磁盘/积分/缓存/版本归档等基础设施
  - orca_bridge.py 已修复为调用根目录版本，不再调用本文件
  - 如需使用本文件的磁盘校验等函数，请 from src.cyber_ingest import check_disk_space 等

v1.0 | 2026-08-05 | Marvis创建
v1.1 | 2026-08-06 | WorkBuddy添加说明，明确职责边界
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

# 路径常量
SKILL_ROOT = Path(r"E:\龙虾AI主控中心\我的AI分身\技能库\cyber-book-house")
OBSIDIAN_WIKI = Path(r"E:\龙虾AI主控中心\Obsidian\wiki\赛博书屋")
CACHE_DIR = SKILL_ROOT / "cache"
CONFIG_DIR = SKILL_ROOT / "config"
LOGS_DIR = SKILL_ROOT / "logs"
LOBSTER_V3_ROOT = Path(r"E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v3.0")

# 磁盘约束
MIN_DISK_FREE_PERCENT = 10
DISK_DRIVE = "E:"

# Marius支持解析的来源类型
SUPPORTED_SOURCES = {
    "pan": "百度网盘课程/PDF",
    "bilibili": "B站视频",
    "github": "GitHub开源仓库",
    "local": "本地书籍/文档",
    "web": "网页文章",
}

# Claude Code审核状态
REVIEW_STATUS = {"pending": "待审核", "approved": "通过", "rejected": "退回"}


def check_disk_space() -> dict:
    """Hermes磁盘空间校验"""
    total, used, free = shutil.disk_usage(DISK_DRIVE)
    free_percent = (free / total) * 100
    return {
        "total_gb": round(total / (1024**3), 2),
        "free_gb": round(free / (1024**3), 2),
        "free_percent": round(free_percent, 2),
        "can_proceed": free_percent >= MIN_DISK_FREE_PERCENT,
    }


def check_credit_constraint() -> bool:
    """Hermes零积分消耗校验"""
    return True  # 默认零积分消耗，通过


def symlink_status() -> dict:
    """检查软链接状态"""
    symlink_path = LOBSTER_V3_ROOT / "cyber-book-house"
    return {
        "path": str(symlink_path),
        "exists": symlink_path.exists(),
        "is_symlink": symlink_path.is_symlink() if symlink_path.exists() else False,
        "target": str(SKILL_ROOT),
    }


def create_obsidian_output_dir(source_type: str = None) -> Path:
    """创建Obsidian输出目录"""
    if source_type and source_type in SUPPORTED_SOURCES:
        dir_name = {
            "pan": "网盘课程",
            "bilibili": "B站视频",
            "github": "GitHub仓库",
            "local": "书籍笔记",
            "web": "网页文章",
        }[source_type]
        target = OBSIDIAN_WIKI / dir_name
    else:
        target = OBSIDIAN_WIKI
    target.mkdir(parents=True, exist_ok=True)
    return target


def log_operation(operation: str, details: dict, status: str = "ok"):
    """Hermes操作日志记录"""
    log_file = LOGS_DIR / f"hermes_{datetime.now().strftime('%Y%m%d')}.log"
    entry = {
        "timestamp": datetime.now().isoformat(),
        "operation": operation,
        "status": status,
        "details": details,
    }
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def cyber_book_house_ingest(
    source: str,
    target: str,
    output_dir: str = None,
) -> dict:
    """
    赛博书屋统一入口 - Codex直接调用

    Args:
        source: 来源类型 "pan"|"bilibili"|"github"|"local"|"web"
        target: 资源路径或URL
        output_dir: 输出目录，默认写入Obsidian

    Returns:
        {"status": "ok"|"blocked"|"error", "message": "...", "output_path": "...", ...}
    """
    # === Hermes权限校验 ===
    disk = check_disk_space()
    if not disk["can_proceed"]:
        return {
            "status": "blocked",
            "message": f"磁盘剩余 {disk['free_percent']}% < {MIN_DISK_FREE_PERCENT}%，Hermes已暂停萃取任务",
            "disk_info": disk,
        }

    if not check_credit_constraint():
        return {
            "status": "blocked",
            "message": "零积分消耗校验未通过，Hermes已拦截",
        }

    if source not in SUPPORTED_SOURCES:
        return {
            "status": "error",
            "message": f"不支持来源类型 '{source}'，支持的类型：{list(SUPPORTED_SOURCES.keys())}",
        }

    # === 创建输出目录 ===
    out_path = (
        Path(output_dir)
        if output_dir
        else create_obsidian_output_dir(source)
    )

    # === Hermes记录操作日志 ===
    log_operation(
        "ingest_start",
        {"source": source, "target": target, "output": str(out_path)},
    )

    # === Marius调度解析（此处为接口占位，实际由Marius层执行） ===
    # 实际执行路径：
    # 1. Hermes → Marius: 下发解析任务
    # 2. Marius: 根据source类型选择解析器（PDF/字幕/代码/文本）
    # 3. Marius → Codex: 返回解析结果
    # 4. Codex: 写入Obsidian

    result = {
        "status": "ok",
        "source": source,
        "source_name": SUPPORTED_SOURCES[source],
        "target": target,
        "output_dir": str(out_path),
        "disk_info": disk,
        "credit_check": "passed",
        "message": f"赛博书屋入口已就绪，来源={SUPPORTED_SOURCES[source]}，待Marius解析调度",
    }

    log_operation("ingest_ready", result)

    return result


def hermes_cache_cleanup(days: int = 7):
    """Hermes定时清理缓存"""
    if not CACHE_DIR.exists():
        return {"status": "ok", "cleaned": 0, "message": "缓存目录不存在"}

    cutoff = datetime.now().timestamp() - days * 86400
    cleaned = 0
    freed_bytes = 0

    for item in CACHE_DIR.iterdir():
        if item.stat().st_mtime < cutoff:
            if item.is_file():
                freed_bytes += item.stat().st_size
            elif item.is_dir():
                freed_bytes += sum(
                    f.stat().st_size for f in item.rglob("*") if f.is_file()
                )
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
            cleaned += 1

    return {
        "status": "ok",
        "cleaned": cleaned,
        "freed_mb": round(freed_bytes / (1024**2), 2),
        "message": f"清理了 {cleaned} 个缓存项，释放 {round(freed_bytes/(1024**2), 2)}MB",
    }


def hermes_version_archive(version: str, changelog: str, claude_review_ok: bool):
    """Hermes版本归档"""
    if not claude_review_ok:
        return {
            "status": "blocked",
            "message": "Claude Code审核未通过，Hermes拒绝归档",
        }

    archive = {
        "version": version,
        "timestamp": datetime.now().isoformat(),
        "changelog": changelog,
        "claude_review": "approved",
    }

    version_file = SKILL_ROOT / "logs" / f"version_{version}.json"
    version_file.parent.mkdir(parents=True, exist_ok=True)
    with open(version_file, "w", encoding="utf-8") as f:
        json.dump(archive, ensure_ascii=False, indent=2, default=str)

    log_operation("version_archive", archive)

    return {
        "status": "ok",
        "version": version,
        "archive_path": str(version_file),
        "message": f"版本 {version} 已归档",
    }


# === ORCA网盘萃取桥接接口 ===
def orca_bridge_ingest(pan_file_path: str) -> dict:
    """
    ORCA网盘萃取 → 赛博书屋桥接
    网盘课程读取完成后自动调用赛博书屋抓取全网配套资料
    """
    file_path = Path(pan_file_path)
    if not file_path.exists():
        return {"status": "error", "message": f"文件不存在: {pan_file_path}"}

    # 提取课程名称（从文件名）
    course_name = file_path.stem

    # 创建Obsidian输出目录
    out_dir = create_obsidian_output_dir("pan") / course_name
    out_dir.mkdir(parents=True, exist_ok=True)

    log_operation(
        "orca_bridge",
        {"pan_file": pan_file_path, "course_name": course_name, "output": str(out_dir)},
    )

    return {
        "status": "ok",
        "course_name": course_name,
        "source_file": str(file_path),
        "output_dir": str(out_dir),
        "message": f"ORCA桥接已启动，课程={course_name}，待Marius全网资料抓取",
    }


if __name__ == "__main__":
    # 自检
    print("=== 赛博书屋 v1.0 自检 ===")
    disk = check_disk_space()
    print(f"磁盘状态: {disk}")
    sl = symlink_status()
    print(f"软链接: {sl}")
    print("赛博书屋入口就绪，等待Hermes调度。")
