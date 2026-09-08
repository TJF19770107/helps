"""Hermes/Trae 技能入口：wechat_crawler_v1.1。"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, Optional

_CURRENT_DIR = Path(__file__).resolve().parent
if str(_CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(_CURRENT_DIR))

from main import run_skill, ensure_dependencies


def _skill_dir() -> Path:
    """返回当前技能目录。"""

    return Path(__file__).resolve().parent


def _project_root() -> Path:
    """返回项目根目录。"""

    skill_dir = _skill_dir()
    if skill_dir.parent.name == "skills" and skill_dir.parent.parent.name in (".trae", ".hermes"):
        return skill_dir.parent.parent.parent
    return skill_dir.parent


def _sync_dual_dirs() -> Dict[str, str]:
    """同步 `.trae` 与 `.hermes` 两处技能目录，确保 Hermes 可直接加载。"""

    root = _project_root()
    trae_dir = root / ".trae" / "skills" / "wechat_crawler_v1.1"
    hermes_dir = root / ".hermes" / "skills" / "wechat_crawler_v1.1"
    trae_dir.mkdir(parents=True, exist_ok=True)
    hermes_dir.mkdir(parents=True, exist_ok=True)

    if _skill_dir().as_posix().startswith(trae_dir.as_posix()):
        src, dst = trae_dir, hermes_dir
    else:
        src, dst = hermes_dir, trae_dir

    for name in ("main.py", "skill_entry.py", "SKILL.md", "README.md"):
        src_file = src / name
        dst_file = dst / name
        if src_file.exists():
            shutil.copy2(src_file, dst_file)
    return {"src": str(src), "dst": str(dst)}


def skill_wechat_crawler(mp_url: str, max_pages: Optional[int] = None, resume: bool = True) -> str:
    """对外统一调用入口：抓取公众号历史消息并返回 Markdown 摘要。"""

    if not isinstance(mp_url, str) or "mp.weixin.qq.com" not in mp_url:
        raise ValueError("mp_url 必须是有效的公众号链接（mp.weixin.qq.com）")

    ensure_dependencies()
    sync_result = _sync_dual_dirs()
    result = run_skill(mp_url=mp_url.strip(), max_pages=max_pages, resume=resume)
    result["sync"] = sync_result
    return result.get("markdown") or json.dumps(result, ensure_ascii=False, indent=2)


def skill_wechat_crawler_json(mp_url: str, max_pages: Optional[int] = None, resume: bool = True) -> Dict[str, Any]:
    """JSON 版本入口，便于函数编排或自动化调用。"""

    ensure_dependencies()
    _sync_dual_dirs()
    return run_skill(mp_url=mp_url.strip(), max_pages=max_pages, resume=resume)
