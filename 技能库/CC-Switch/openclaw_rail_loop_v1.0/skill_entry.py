import time
from typing import Any, Dict, List, Optional


def _call_vnpy(cmd: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    import hermes_lobster_server as srv

    fn, err = srv._load_vnpy_bidirectional_skill_func()
    if not fn:
        return {"ok": False, "error": err or "vnpy_skill_unavailable"}
    try:
        return fn(cmd=cmd, params=params or {})
    except Exception as e:
        return {"ok": False, "error": f"vnpy_call_failed: {e}"}


def _llm_plan(objective: str, state: Dict[str, Any], trading: Dict[str, Any]) -> Dict[str, Any]:
    import hermes_lobster_server as srv

    prompt = (
        "你是量化任务自动化调度器。你必须在白名单动作内选择下一步。"
        "输出严格 JSON："
        '{"action":"vnpy|sleep|note|finish","cmd":"","params":{},"seconds":1,"note":""}'
        "\n白名单动作说明："
        "\n- vnpy：调用 VNPY 网关 RPC（cmd+params）"
        "\n- sleep：等待 seconds"
        "\n- note：追加一条 note 到日志"
        "\n- finish：结束循环"
        "\n\n目标：\n"
        + (objective or "")
        + "\n\n量化上下文：\n"
        + (str(trading) if trading else "（无）")
        + "\n\n当前状态（最近结果摘要）：\n"
        + str(state)[:8000]
    )
    res = srv.LLM.generate(prompt, json_mode=True)
    parsed = srv._extract_first_json(res.text or "")
    if not isinstance(parsed, dict):
        return {"action": "finish", "note": "planner_parse_failed"}
    return parsed


def skill_openclaw_rail_loop(req: Dict[str, Any]) -> Dict[str, Any]:
    req = req if isinstance(req, dict) else {}
    objective = str(req.get("objective") or "").strip()
    mode = str(req.get("mode") or "steps").strip().lower() or "steps"
    max_steps = int(req.get("max_steps") or 10)
    max_steps = max(1, min(50, max_steps))
    trading = req.get("trading") if isinstance(req.get("trading"), dict) else {}

    logs: List[Dict[str, Any]] = []
    state: Dict[str, Any] = {"last": None}

    if mode == "steps":
        steps = req.get("steps")
        if not isinstance(steps, list) or not steps:
            return {"ok": False, "error": "steps_required_for_steps_mode"}
        for i, step in enumerate(steps[:max_steps], start=1):
            if not isinstance(step, dict):
                continue
            stype = str(step.get("type") or "").strip().lower()
            if stype == "vnpy":
                cmd = str(step.get("cmd") or "").strip()
                params = step.get("params") if isinstance(step.get("params"), dict) else {}
                r = _call_vnpy(cmd=cmd, params=params)
                logs.append({"i": i, "type": "vnpy", "cmd": cmd, "params": params, "result": r})
                state["last"] = {"type": "vnpy", "cmd": cmd, "ok": bool(r.get("ok", True)), "result": r}
                continue
            if stype == "sleep":
                sec = float(step.get("seconds") or 1)
                sec = max(0.0, min(30.0, sec))
                time.sleep(sec)
                logs.append({"i": i, "type": "sleep", "seconds": sec})
                state["last"] = {"type": "sleep", "seconds": sec}
                continue
            if stype == "note":
                note = str(step.get("note") or "").strip()
                logs.append({"i": i, "type": "note", "note": note})
                state["last"] = {"type": "note", "note": note}
                continue
            logs.append({"i": i, "type": "unknown", "step": step})
        return {"ok": True, "mode": mode, "objective": objective, "logs": logs}

    if mode == "planner":
        if not objective:
            return {"ok": False, "error": "objective_required_for_planner_mode"}
        for i in range(1, max_steps + 1):
            plan = _llm_plan(objective=objective, state={"i": i, "last": state.get("last"), "logs_tail": logs[-3:]}, trading=trading)
            action = str(plan.get("action") or "").strip().lower()
            if action == "finish":
                logs.append({"i": i, "type": "finish", "plan": plan})
                break
            if action == "note":
                note = str(plan.get("note") or "").strip()
                logs.append({"i": i, "type": "note", "note": note, "plan": plan})
                state["last"] = {"type": "note", "note": note}
                continue
            if action == "sleep":
                sec = float(plan.get("seconds") or 1)
                sec = max(0.0, min(30.0, sec))
                time.sleep(sec)
                logs.append({"i": i, "type": "sleep", "seconds": sec, "plan": plan})
                state["last"] = {"type": "sleep", "seconds": sec}
                continue
            if action == "vnpy":
                cmd = str(plan.get("cmd") or "").strip()
                params = plan.get("params") if isinstance(plan.get("params"), dict) else {}
                r = _call_vnpy(cmd=cmd, params=params)
                logs.append({"i": i, "type": "vnpy", "cmd": cmd, "params": params, "result": r, "plan": plan})
                state["last"] = {"type": "vnpy", "cmd": cmd, "ok": bool(r.get("ok", True)), "result": r}
                continue
            logs.append({"i": i, "type": "invalid_plan", "plan": plan})
            break
        return {"ok": True, "mode": mode, "objective": objective, "logs": logs}

    return {"ok": False, "error": "unsupported_mode", "supported": ["steps", "planner"]}

