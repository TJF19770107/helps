"""Hermes/Trae 技能入口：lobster_webdav_ops_v1.0。"""

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

from main import run_json, webdav_download, webdav_list, webdav_mkdir, webdav_upload


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
    trae_dir = root / ".trae" / "skills" / "lobster_webdav_ops_v1.0"
    hermes_dir = root / ".hermes" / "skills" / "lobster_webdav_ops_v1.0"
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


def _require_confirm(confirm: bool) -> None:
    """写操作门禁。"""

    if confirm is not True:
        raise PermissionError("写操作被门禁拦截：请在获得用户明确授权后显式 confirm=true")


def _write_audit(action: str, args: Dict[str, Any], result: Any) -> str:
    """落盘一条审计记录（不含任何凭据明文）。"""

    payload = {"ts": _now_compact(), "skill": "lobster_webdav_ops_v1.0", "action": action, "args": args, "result": result}
    out = _audit_dir() / f"webdav_{action}_{payload['ts']}.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(out)


def skill_webdav_list(remote_path: str = "/") -> Dict[str, Any]:
    """列目录。"""

    _sync_dual_dirs()
    res = webdav_list(remote_path=remote_path)
    res["audit_path"] = _write_audit("list", {"remote_path": str(remote_path)}, {"ok": bool(res.get("ok")), "items": len(res.get("items") or [])})
    return res


def skill_webdav_download(remote_path: str, local_path: str, confirm: bool = False) -> Dict[str, Any]:
    """下载文件。"""

    _sync_dual_dirs()
    _require_confirm(confirm)
    res = webdav_download(remote_path=remote_path, local_path=local_path)
    res["audit_path"] = _write_audit("download", {"remote_path": str(remote_path), "local_path": str(local_path)}, {"ok": bool(res.get("ok"))})
    return res


def skill_webdav_upload(local_path: str, remote_path: str, confirm: bool = False) -> Dict[str, Any]:
    """上传文件。"""

    _sync_dual_dirs()
    _require_confirm(confirm)
    res = webdav_upload(local_path=local_path, remote_path=remote_path)
    res["audit_path"] = _write_audit("upload", {"local_path": str(local_path), "remote_path": str(remote_path)}, {"ok": bool(res.get("ok"))})
    return res


def skill_webdav_mkdir(remote_path: str, confirm: bool = False) -> Dict[str, Any]:
    """创建目录。"""

    _sync_dual_dirs()
    _require_confirm(confirm)
    res = webdav_mkdir(remote_path=remote_path)
    res["audit_path"] = _write_audit("mkdir", {"remote_path": str(remote_path)}, {"ok": bool(res.get("ok")), "http": res.get("http")})
    return res


def skill_webdav_ops_json(payload: Dict[str, Any]) -> str:
    """JSON 统一入口，便于自动化编排。"""

    _sync_dual_dirs()
    action = str(payload.get("action") or "").strip()
    confirm = bool(payload.get("confirm") is True)
    if action in ("download", "upload", "mkdir"):
        _require_confirm(confirm)
    out = run_json(payload)
    _write_audit(action or "unknown", {"remote_path": payload.get("remote_path"), "local_path": payload.get("local_path"), "confirm": confirm}, {"ok": bool(out.get("ok")) if isinstance(out, dict) else True})
    return json.dumps(out, ensure_ascii=False)
