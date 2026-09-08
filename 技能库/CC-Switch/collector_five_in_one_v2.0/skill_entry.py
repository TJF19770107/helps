from __future__ import annotations

import shutil
import sys
from pathlib import Path
from typing import Any, Dict, Optional

_CURRENT_DIR = Path(__file__).resolve().parent
if str(_CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(_CURRENT_DIR))

from main import run_skill


def _skill_dir() -> Path:
    return Path(__file__).resolve().parent


def _project_root() -> Path:
    skill_dir = _skill_dir()
    if skill_dir.parent.name == "skills" and skill_dir.parent.parent.name in (".trae", ".hermes"):
        return skill_dir.parent.parent.parent
    return skill_dir.parent


def _sync_dual_dirs() -> Dict[str, str]:
    root = _project_root()
    trae_dir = root / ".trae" / "skills" / "collector_five_in_one_v2.0"
    hermes_dir = root / ".hermes" / "skills" / "collector_five_in_one_v2.0"
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


def skill_collector_five_in_one(req: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    req = req if isinstance(req, dict) else {}
    mode = str(req.get("mode") or "auto").strip().lower()
    rounds = int(req.get("rounds") or 1)
    override_daily_cap = bool(req.get("override_daily_cap", False))
    notify = bool(req.get("notify", False))
    config_path = req.get("config_path")
    config_path = str(config_path).strip() if isinstance(config_path, str) and config_path.strip() else None

    sync_result = _sync_dual_dirs()
    out = run_skill(
        mode=mode,
        rounds=rounds,
        override_daily_cap=override_daily_cap,
        notify=notify,
        config_path=config_path,
    )
    out["sync"] = sync_result
    return out

