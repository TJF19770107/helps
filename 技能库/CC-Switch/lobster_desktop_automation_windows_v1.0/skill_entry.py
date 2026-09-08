"""Hermes/Trae 技能入口：lobster_desktop_automation_windows_v1.0。"""

from __future__ import annotations

import json
import hashlib
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

_CURRENT_DIR = Path(__file__).resolve().parent
if str(_CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(_CURRENT_DIR))

from main import click, find_windows, list_controls, screenshot, type_text


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
    trae_dir = root / ".trae" / "skills" / "lobster_desktop_automation_windows_v1.0"
    hermes_dir = root / ".hermes" / "skills" / "lobster_desktop_automation_windows_v1.0"
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


def _mask_text(text: str) -> Dict[str, Any]:
    """对文本做脱敏摘要。"""

    s = str(text or "")
    return {"len": len(s), "sha256": hashlib.sha256(s.encode("utf-8")).hexdigest()}


def _write_audit(action: str, args: Dict[str, Any], result: Any) -> str:
    """落盘一条审计记录（不含敏感明文）。"""

    payload = {"ts": _now_compact(), "skill": "lobster_desktop_automation_windows_v1.0", "action": action, "args": args, "result": result}
    out = _audit_dir() / f"desktop_{action}_{payload['ts']}.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(out)


def skill_desktop_screenshot(out_path: str, allow_install: bool = False) -> Dict[str, Any]:
    """截图保存到 out_path。"""

    _sync_dual_dirs()
    res = screenshot(out_path=out_path, allow_install=allow_install)
    res["audit_path"] = _write_audit("screenshot", {"out_path": str(out_path), "allow_install": bool(allow_install)}, {"ok": bool(res.get("ok"))})
    return res


def skill_desktop_find_windows(title_re: Optional[str] = None, allow_install: bool = False) -> List[Dict[str, Any]]:
    """枚举当前窗口（可用 title_re 过滤）。"""

    _sync_dual_dirs()
    res = find_windows(title_re=title_re, allow_install=allow_install)
    _write_audit("find_windows", {"title_re": title_re, "allow_install": bool(allow_install)}, {"count": len(res)})
    return res


def skill_desktop_list_controls(title_re: str, allow_install: bool = False) -> str:
    """输出控件树（用于定位可点击控件）。"""

    _sync_dual_dirs()
    tree = list_controls(title_re=title_re, allow_install=allow_install)
    _write_audit("list_controls", {"title_re": str(title_re), "allow_install": bool(allow_install)}, {"ok": True, "len": len(tree)})
    return tree


def skill_desktop_click(
    coords: Optional[str] = None,
    title_re: Optional[str] = None,
    control_title_re: Optional[str] = None,
    allow_install: bool = False,
) -> Dict[str, Any]:
    """点击：优先控件级（title_re + control_title_re），否则坐标级（coords='x,y'）。"""

    _sync_dual_dirs()
    res = click(
        coords=coords,
        title_re=title_re,
        control_title_re=control_title_re,
        allow_install=allow_install,
    )
    res["audit_path"] = _write_audit(
        "click",
        {"coords": coords, "title_re": title_re, "control_title_re": control_title_re, "allow_install": bool(allow_install)},
        {"ok": bool(res.get("ok")), "mode": res.get("mode")},
    )
    return res


def skill_desktop_type(text: str, interval_ms: int = 0, allow_install: bool = False) -> Dict[str, Any]:
    """输入文本。"""

    _sync_dual_dirs()
    res = type_text(text=text, interval_ms=interval_ms, allow_install=allow_install)
    res["audit_path"] = _write_audit(
        "type",
        {"text": _mask_text(text), "interval_ms": int(interval_ms), "allow_install": bool(allow_install)},
        {"ok": bool(res.get("ok")), "chars": res.get("chars")},
    )
    return res


def skill_desktop_automation_windows_json(payload: Dict[str, Any]) -> str:
    """JSON 统一入口，便于自动化编排。"""

    _sync_dual_dirs()
    action = str(payload.get("action") or "").strip()
    allow_install = bool(payload.get("allow_install") is True)

    if action == "screenshot":
        return json.dumps(skill_desktop_screenshot(str(payload.get("out_path") or ""), allow_install=allow_install), ensure_ascii=False)
    if action == "find_windows":
        return json.dumps(skill_desktop_find_windows(payload.get("title_re"), allow_install=allow_install), ensure_ascii=False)
    if action == "list_controls":
        return json.dumps({"ok": True, "tree": skill_desktop_list_controls(str(payload.get("title_re") or ""), allow_install=allow_install)}, ensure_ascii=False)
    if action == "click":
        return json.dumps(
            skill_desktop_click(
                coords=payload.get("coords"),
                title_re=payload.get("title_re"),
                control_title_re=payload.get("control_title_re"),
                allow_install=allow_install,
            ),
            ensure_ascii=False,
        )
    if action == "type":
        return json.dumps(
            skill_desktop_type(
                text=str(payload.get("text") or ""),
                interval_ms=int(payload.get("interval_ms") or 0),
                allow_install=allow_install,
            ),
            ensure_ascii=False,
        )

    raise ValueError("未知 action：支持 screenshot/find_windows/list_controls/click/type")
