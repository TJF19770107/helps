"""Hermes/Trae 技能入口：lobster_long_task_scheduler_v1.0。"""

from __future__ import annotations

import json
import hashlib
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

_CURRENT_DIR = Path(__file__).resolve().parent
if str(_CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(_CURRENT_DIR))

from main import define_job, emit_job, plan_windows_schedule, start_run, wait_run


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
    trae_dir = root / ".trae" / "skills" / "lobster_long_task_scheduler_v1.0"
    hermes_dir = root / ".hermes" / "skills" / "lobster_long_task_scheduler_v1.0"
    trae_dir.mkdir(parents=True, exist_ok=True)
    hermes_dir.mkdir(parents=True, exist_ok=True)

    if _skill_dir().as_posix().startswith(trae_dir.as_posix()):
        src, dst = trae_dir, hermes_dir
    else:
        src, dst = hermes_dir, trae_dir

    for name in ("main.py", "skill_entry.py", "SKILL.md", "task_emit_job.ps1"):
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

    payload = {"ts": _now_compact(), "skill": "lobster_long_task_scheduler_v1.0", "action": action, "args": args, "result": result}
    out = _audit_dir() / f"longtask_{action}_{payload['ts']}.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(out)


def skill_long_task_start(input_text: str, session_id: Optional[str] = None) -> Dict[str, Any]:
    """启动 Hermes run。"""

    _sync_dual_dirs()
    res = start_run(input_text=input_text, session_id=session_id)
    res["audit_path"] = _write_audit("start", {"input": _mask_text(input_text), "session_id": session_id}, {"ok": bool(res.get("ok")), "status_code": res.get("status_code")})
    return res


def skill_long_task_wait(run_id: str, timeout_s: int = 60) -> Dict[str, Any]:
    """等待 run 完成（SSE）。"""

    _sync_dual_dirs()
    res = wait_run(run_id=run_id, timeout_s=int(timeout_s))
    res["audit_path"] = _write_audit("wait", {"run_id": str(run_id), "timeout_s": int(timeout_s)}, {"ok": bool(res.get("ok")), "event": (res.get("event") or {}).get("event") if isinstance(res.get("event"), dict) else None})
    return res


def skill_long_task_define_job(job_name: str, input_text: str, session_id: Optional[str] = None) -> Dict[str, Any]:
    """定义 job 并落盘。"""

    _sync_dual_dirs()
    res = define_job(job_name=job_name, input_text=input_text, session_id=session_id, skill_dir=_skill_dir())
    res["audit_path"] = _write_audit("define_job", {"job_name": str(job_name), "input": _mask_text(input_text), "session_id": session_id}, {"ok": bool(res.get("ok")), "job_path": res.get("job_path")})
    return res


def skill_long_task_emit_job(job_name: str) -> Dict[str, Any]:
    """触发已定义 job。"""

    _sync_dual_dirs()
    res = emit_job(job_name=job_name, skill_dir=_skill_dir())
    res["audit_path"] = _write_audit("emit_job", {"job_name": str(job_name)}, {"ok": bool(res.get("ok")), "run_id": ((res.get("run") or {}) if isinstance(res.get("run"), dict) else {}).get("run_id")})
    return res


def skill_long_task_plan_windows_schedule(job_name: str, every_minutes: int) -> Dict[str, Any]:
    """生成 Windows schtasks 计划任务命令（默认不执行）。"""

    _sync_dual_dirs()
    res = plan_windows_schedule(job_name=job_name, every_minutes=int(every_minutes))
    res["audit_path"] = _write_audit("plan_windows_schedule", {"job_name": str(job_name), "every_minutes": int(every_minutes)}, {"ok": bool(res.get("ok"))})
    return res


def skill_long_task_scheduler_json(payload: Dict[str, Any]) -> str:
    """JSON 统一入口。"""

    _sync_dual_dirs()
    action = str(payload.get("action") or "").strip()
    if action == "start":
        return json.dumps(skill_long_task_start(str(payload.get("input") or ""), payload.get("session_id")), ensure_ascii=False)
    if action == "wait":
        return json.dumps(skill_long_task_wait(str(payload.get("run_id") or ""), int(payload.get("timeout_s") or 60)), ensure_ascii=False)
    if action == "define_job":
        return json.dumps(
            skill_long_task_define_job(
                job_name=str(payload.get("job_name") or ""),
                input_text=str(payload.get("input") or ""),
                session_id=payload.get("session_id"),
            ),
            ensure_ascii=False,
        )
    if action == "emit_job":
        return json.dumps(skill_long_task_emit_job(str(payload.get("job_name") or "")), ensure_ascii=False)
    if action == "plan_windows_schedule":
        return json.dumps(
            skill_long_task_plan_windows_schedule(
                job_name=str(payload.get("job_name") or ""),
                every_minutes=int(payload.get("every_minutes") or 60),
            ),
            ensure_ascii=False,
        )
    raise ValueError("未知 action：支持 start/wait/define_job/emit_job/plan_windows_schedule")
