from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


def _env(name: str, default: str = "") -> str:
    """读取环境变量（不回显敏感值）。"""

    return str(os.environ.get(name, default) or "").strip()


def _hermes_base() -> str:
    """Hermes Base URL。"""

    return (_env("HERMES_BASE_URL", "http://127.0.0.1:8642") or "http://127.0.0.1:8642").rstrip("/")


def _requests():
    """延迟导入 requests。"""

    try:
        import requests  # type: ignore

        return requests
    except Exception as e:
        raise RuntimeError("缺少依赖 requests；请先安装后再使用本技能。") from e


def _headers_json() -> Dict[str, str]:
    """构造 Hermes 请求头（不输出敏感值）。"""

    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    tok = _env("HERMES_API_TOKEN", "")
    if tok:
        headers["Authorization"] = f"Bearer {tok}"
    return headers


def _state_dir(skill_dir: Optional[Path] = None) -> Path:
    """返回本技能状态目录。"""

    d = Path(skill_dir or Path(__file__).resolve().parent) / ".lobster_state"
    d.mkdir(parents=True, exist_ok=True)
    (d / "jobs").mkdir(parents=True, exist_ok=True)
    return d


def start_run(input_text: str, session_id: Optional[str] = None) -> Dict[str, Any]:
    """启动一次 Hermes run，返回 run_id。"""

    requests = _requests()
    url = f"{_hermes_base()}/v1/runs"
    payload: Dict[str, Any] = {"input": str(input_text or "")}
    if session_id:
        payload["session_id"] = str(session_id)
    r = requests.post(url, headers=_headers_json(), json=payload, timeout=20)
    if r.status_code not in (200, 202):
        raise RuntimeError(f"POST /v1/runs 失败：HTTP {r.status_code}")
    data = r.json() if "application/json" in (r.headers.get("content-type") or "") else {}
    run_id = str((data or {}).get("run_id") or "").strip()
    if not run_id:
        raise RuntimeError("POST /v1/runs 返回缺少 run_id")
    return {"ok": True, "run_id": run_id, "status_code": int(r.status_code)}


def wait_run(run_id: str, timeout_s: int = 60) -> Dict[str, Any]:
    """等待 run 完成（SSE events）。"""

    requests = _requests()
    rid = str(run_id or "").strip()
    if not rid:
        raise ValueError("run_id 不能为空")

    url = f"{_hermes_base()}/v1/runs/{rid}/events"
    headers = _headers_json()
    headers["Accept"] = "text/event-stream"
    started = time.time()
    last_event: Optional[Dict[str, Any]] = None
    with requests.get(url, headers=headers, stream=True, timeout=10) as r:
        if r.status_code != 200:
            raise RuntimeError(f"GET /v1/runs/{{id}}/events 失败：HTTP {r.status_code}")
        for raw in r.iter_lines(decode_unicode=True):
            if time.time() - started > float(timeout_s):
                return {"ok": False, "error": "timeout", "run_id": rid, "last_event": last_event}
            if not raw:
                continue
            line = str(raw).strip()
            if not line.startswith("data:"):
                continue
            data = line[5:].strip()
            if not data or data == "[DONE]":
                continue
            try:
                ev = json.loads(data)
                last_event = ev if isinstance(ev, dict) else {"raw": ev}
            except Exception:
                continue
            ev_type = str((last_event or {}).get("event") or "").strip()
            if ev_type == "run.completed":
                return {"ok": True, "run_id": rid, "event": last_event, "output": (last_event or {}).get("output")}
            if ev_type == "run.failed":
                return {"ok": False, "run_id": rid, "event": last_event, "error": (last_event or {}).get("error") or "run_failed"}
    return {"ok": False, "error": "sse_closed_early", "run_id": rid, "last_event": last_event}


def define_job(job_name: str, input_text: str, session_id: Optional[str] = None, skill_dir: Optional[Path] = None) -> Dict[str, Any]:
    """落盘一个可复用 job 定义（用于断点续跑/定时唤醒）。"""

    name = str(job_name or "").strip()
    if not name:
        raise ValueError("job_name 不能为空")

    st = _state_dir(skill_dir)
    job_path = st / "jobs" / f"{name}.json"
    payload: Dict[str, Any] = {"job_name": name, "input": str(input_text or ""), "session_id": (session_id or "").strip()}
    job_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "job_name": name, "job_path": str(job_path)}


def emit_job(job_name: str, skill_dir: Optional[Path] = None) -> Dict[str, Any]:
    """读取 job 定义并触发一次 Hermes run。"""

    name = str(job_name or "").strip()
    if not name:
        raise ValueError("job_name 不能为空")

    st = _state_dir(skill_dir)
    job_path = st / "jobs" / f"{name}.json"
    if not job_path.exists():
        raise RuntimeError("job 未定义，请先 define_job")

    job = json.loads(job_path.read_text(encoding="utf-8"))
    res = start_run(input_text=str(job.get("input") or ""), session_id=str(job.get("session_id") or "") or None)
    last_path = st / "jobs" / f"{name}.last_run.json"
    last_path.write_text(json.dumps({"job_name": name, **res}, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "job_name": name, "run": res, "last_run_path": str(last_path)}


def plan_windows_schedule(job_name: str, every_minutes: int) -> Dict[str, Any]:
    """生成 Windows schtasks 计划任务命令（默认只输出计划，不执行）。"""

    name = str(job_name or "").strip()
    minutes = int(every_minutes)
    if not name:
        raise ValueError("job_name 不能为空")
    if minutes <= 0:
        raise ValueError("every_minutes 必须 > 0")

    repo_root = Path(__file__).resolve().parents[3]
    skill_dir = Path(__file__).resolve().parent
    entry = skill_dir / "task_emit_job.ps1"
    cmd = f'schtasks /Create /F /SC MINUTE /MO {minutes} /TN "lobster_{name}" /TR "powershell -NoProfile -ExecutionPolicy Bypass -File \\"{entry}\\" -JobName \\"{name}\\""'
    return {"ok": True, "job_name": name, "every_minutes": minutes, "create_command": cmd, "note": "系统级修改：仅在你明确授权后才执行该命令。"}

