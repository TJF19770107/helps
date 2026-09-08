"""Hermes/Trae 技能入口：lobster_local_lobster_publish_v1.0。"""

from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

_CURRENT_DIR = Path(__file__).resolve().parent
if str(_CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(_CURRENT_DIR))

from main import local_lobster_skills_health, local_lobster_skills_list


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
    """同步 `.trae` 与 `.hermes` 两处技能目录，确保本地智能体均可加载。"""

    root = _project_root()
    trae_dir = root / ".trae" / "skills" / "lobster_local_lobster_publish_v1.0"
    hermes_dir = root / ".hermes" / "skills" / "lobster_local_lobster_publish_v1.0"
    trae_dir.mkdir(parents=True, exist_ok=True)
    hermes_dir.mkdir(parents=True, exist_ok=True)

    if _skill_dir().as_posix().startswith(trae_dir.as_posix()):
        src, dst = trae_dir, hermes_dir
    else:
        src, dst = hermes_dir, trae_dir

    for name in ("main.py", "skill_entry.py", "SKILL.md"):
        src_file = src / name
        dst_file = dst / name
        if src_file.exists():
            shutil.copy2(src_file, dst_file)
    return {"src": str(src), "dst": str(dst)}


def _audit_dir() -> Path:
    """返回审计日志目录。"""

    d = _skill_dir() / ".lobster_state" / "reports"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _now_compact() -> str:
    """生成可用于文件名的时间戳。"""

    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _write_audit(action: str, result: Dict[str, Any]) -> str:
    """落盘一条审计记录（不含任何 Token 明文）。"""

    payload = {"ts": _now_compact(), "skill": "lobster_local_lobster_publish_v1.0", "action": action, "result": result}
    out = _audit_dir() / f"local_lobster_{action}_{payload['ts']}.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(out)


def skill_local_lobster_skills_health() -> Dict[str, Any]:
    """本地健康检查：GET /api/trae/skills/health。"""

    _sync_dual_dirs()
    res = local_lobster_skills_health()
    res["audit_path"] = _write_audit("skills_health", {"ok": bool(res.get("ok")), "status": res.get("response", {}).get("status")})
    return res


def skill_local_lobster_skills_list() -> Dict[str, Any]:
    """本地技能列表：GET /api/trae/skills/list（验收：skills 为数组）。"""

    _sync_dual_dirs()
    res = local_lobster_skills_list()
    parsed = res.get("parsed") if isinstance(res.get("parsed"), dict) else None
    skills = parsed.get("skills") if parsed else None
    res["audit_path"] = _write_audit(
        "skills_list",
        {
            "ok": bool(res.get("ok")),
            "status": res.get("response", {}).get("status"),
            "skills_is_array": bool(res.get("validation", {}).get("skills_is_array")),
            "skills_len": int(len(skills) if isinstance(skills, list) else 0),
        },
    )
    return res


def skill_local_lobster_publish_acceptance() -> Dict[str, Any]:
    """一键验收：health + list，并落盘验收摘要。"""

    _sync_dual_dirs()
    h = skill_local_lobster_skills_health()
    l = skill_local_lobster_skills_list()
    ok = bool(h.get("ok") is True and l.get("ok") is True)
    summary = {
        "ok": ok,
        "health_ok": bool(h.get("ok") is True),
        "list_ok": bool(l.get("ok") is True),
        "health_audit_path": str(h.get("audit_path") or ""),
        "list_audit_path": str(l.get("audit_path") or ""),
    }
    summary["audit_path"] = _write_audit("acceptance", summary)
    return summary

