from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def _env(name: str, default: str = "") -> str:
    """读取环境变量（不回显敏感值）。"""

    return str(os.environ.get(name, default) or "").strip()


def _pick_bearer_token() -> Tuple[str, str]:
    """选择 Bearer Token（仅返回 token 与来源变量名，不返回明文到日志）。"""

    v = _env("TRAE_API_TOKEN", "")
    if v:
        return v, "TRAE_API_TOKEN"
    v = _env("DOUBAO_USER_TRIGGER_TOKEN", "")
    if v:
        return v, "DOUBAO_USER_TRIGGER_TOKEN"
    return "", ""


def _base_url() -> str:
    """本地 bridge base_url。"""

    return (_env("LOBSTER_LOCAL_BRIDGE_BASE_URL", "http://127.0.0.1:18091") or "http://127.0.0.1:18091").rstrip("/")


def _http_get_json(path: str, timeout_s: float = 10.0) -> Dict[str, Any]:
    """对本地 bridge 发起 GET 并解析 JSON（不回显 Authorization 明文）。"""

    url = f"{_base_url()}/{str(path or '').lstrip('/')}"
    tok, tok_env = _pick_bearer_token()
    headers = {"Accept": "application/json"}
    if tok:
        headers["Authorization"] = f"Bearer {tok}"

    req = Request(url=url, headers=headers, method="GET")

    res: Dict[str, Any] = {
        "ok": False,
        "request": {
            "method": "GET",
            "url": url,
            "authorization_present": bool(tok),
            "token_env": tok_env or "",
        },
        "response": {},
    }

    try:
        with urlopen(req, timeout=float(timeout_s)) as r:
            body = (r.read() or b"").decode("utf-8", "replace")
            res["response"] = {"status": int(getattr(r, "status", 0) or 0), "body_text": body}
    except HTTPError as e:
        body = (e.read() or b"").decode("utf-8", "replace")
        res["response"] = {"status": int(e.code), "body_text": body, "error": "HTTPError"}
    except URLError as e:
        res["response"] = {"error": "URLError", "detail": str(e)}
    except Exception as e:
        res["response"] = {"error": type(e).__name__, "detail": str(e)}

    parsed: Optional[Dict[str, Any]] = None
    try:
        parsed = json.loads(str(res["response"].get("body_text") or ""))
    except Exception:
        parsed = None

    res["parsed"] = parsed
    res["ok"] = bool(parsed is not None and parsed.get("ok") is True and 200 <= int(res["response"].get("status") or 0) < 300)
    return res


def local_lobster_skills_health() -> Dict[str, Any]:
    """调用 /api/trae/skills/health。"""

    return _http_get_json("/api/trae/skills/health")


def local_lobster_skills_list() -> Dict[str, Any]:
    """调用 /api/trae/skills/list，并校验 ok:true 且 skills 为数组。"""

    res = _http_get_json("/api/trae/skills/list")
    parsed = res.get("parsed") if isinstance(res.get("parsed"), dict) else None
    skills_val = parsed.get("skills") if parsed else None
    res["validation"] = {
        "ok_is_true": bool(parsed is not None and parsed.get("ok") is True),
        "skills_is_array": isinstance(skills_val, list),
        "skills_is_empty_array": isinstance(skills_val, list) and len(skills_val) == 0,
        "note": "验收：ok:true 且 skills 为数组；skills 为 {} 视为无效响应。",
    }
    res["ok"] = bool(res.get("ok") is True and res["validation"]["skills_is_array"] is True)
    return res


def main() -> int:
    """CLI 主入口：stdin JSON -> stdout JSON。"""

    try:
        import sys

        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        action = str(payload.get("action") or "skills_list").strip()

        if action == "skills_health":
            out = local_lobster_skills_health()
        elif action == "skills_list":
            out = local_lobster_skills_list()
        else:
            out = {"ok": False, "error": f"unknown_action: {action}"}

        print(json.dumps(out, ensure_ascii=False))
        return 0 if out.get("ok") is True else 2
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

