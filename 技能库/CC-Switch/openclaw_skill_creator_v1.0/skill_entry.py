import json
import re
from typing import Any, Dict, List, Optional


def _slugify(name: str) -> str:
    s = (name or "").strip().lower()
    s = re.sub(r"[^a-z0-9_\\-\\.]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "skill"


def _ensure_list(x: Any) -> List[Dict[str, Any]]:
    if isinstance(x, list):
        return [i for i in x if isinstance(i, dict)]
    return []


def _default_quant_defaults() -> Dict[str, Any]:
    return {
        "symbols": [],
        "timeframe": "1m",
        "session": "day",
        "risk": {"max_position_pct": 0.2, "max_drawdown_pct": 0.1, "max_orders_per_day": 50},
        "data": {"source": "local", "start": "", "end": ""},
        "broker": {"name": "", "account": ""},
    }


def skill_openclaw_skill_creator(spec: Dict[str, Any]) -> Dict[str, Any]:
    spec = spec if isinstance(spec, dict) else {}
    skill_name = _slugify(str(spec.get("skill_name") or "my_skill_v1.0"))
    description = str(spec.get("description") or "").strip()
    inputs = _ensure_list(spec.get("inputs"))
    outputs = _ensure_list(spec.get("outputs"))
    quant_defaults = spec.get("quant_defaults") if isinstance(spec.get("quant_defaults"), dict) else {}
    merged_quant = _default_quant_defaults()
    merged_quant.update(quant_defaults)

    hermes_dir = f".hermes/skills/{skill_name}"
    trae_dir = f".trae/skills/{skill_name}"
    fn_name = f"skill_{_slugify(skill_name).replace('.', '_')}"
    endpoint = f"/hermes/skill/{_slugify(skill_name).replace('.', '_')}"
    safe_desc = (description or "Describe what it does. Invoke when ...").replace('"', "'")

    hermes_skill_md = "\n".join(
        [
            "---",
            f'name: "{skill_name}"',
            f'description: "{safe_desc}"',
            "---",
            "",
            f"# {skill_name}",
            "",
            "## 能力",
            "",
            "- TODO",
            "",
            "## 统一入口",
            "",
            f"- 函数入口：`{fn_name}(payload: dict) -> dict`",
            "",
            "## 量化默认参数（可覆盖）",
            "",
            "```json",
            json.dumps({"trading": merged_quant}, ensure_ascii=False, indent=2),
            "```",
            "",
        ]
    )

    trae_skill_md = "\n".join(
        [
            "---",
            f'name: "{skill_name}"',
            f'description: "{safe_desc}"',
            "---",
            "",
            f"# {skill_name}",
            "",
            "## 调用方式（统一走 Hermes 网关）",
            "",
            f"- URL：`http://127.0.0.1:18080{endpoint}`",
            "- 方法：`POST`",
            "- Body：JSON（包含你的业务参数 + 可选 trading 参数）",
            "",
        ]
    )

    skill_entry_py = "\n".join(
        [
            "from typing import Any, Dict",
            "",
            "",
            f"def {fn_name}(payload: Dict[str, Any]) -> Dict[str, Any]:",
            "    payload = payload if isinstance(payload, dict) else {}",
            '    return {"ok": True, "payload": payload}',
            "",
        ]
    )

    contract = {
        "endpoint": endpoint,
        "method": "POST",
        "request_json": {"inputs": inputs, "trading": merged_quant},
        "response_json": {"ok": True, "result": {"outputs": outputs}},
        "entry_function": fn_name,
    }

    return {
        "ok": True,
        "skill_name": skill_name,
        "contract": contract,
        "files": {
            f"{hermes_dir}/SKILL.md": hermes_skill_md,
            f"{trae_dir}/SKILL.md": trae_skill_md,
            f"{hermes_dir}/skill_entry.py": skill_entry_py,
        },
    }
