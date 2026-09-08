import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def _repo_root() -> Path:
    try:
        import hermes_lobster_server as srv

        return Path(srv.BASE_DIR).parent
    except Exception:
        return Path(os.getcwd())


def _read_text(p: Path, max_bytes: int = 200_000) -> str:
    try:
        raw = p.read_bytes()[: max(0, max_bytes)]
        for enc in ("utf-8", "gb18030", "gbk"):
            try:
                return raw.decode(enc, errors="ignore").strip()
            except Exception:
                continue
        return raw.decode("utf-8", errors="ignore").strip()
    except Exception:
        return ""


def _locate_skill_md(skill_name: str) -> Optional[Path]:
    root = _repo_root()
    candidates = [
        root / ".hermes" / "skills" / skill_name / "SKILL.md",
        root / ".trae" / "skills" / skill_name / "SKILL.md",
    ]
    for p in candidates:
        if p.is_file():
            return p
    return None


def _llm_generate(prompt: str) -> str:
    import hermes_lobster_server as srv

    res = srv.LLM.generate(prompt, json_mode=False)
    return (res.text or "").strip()


def skill_openclaw_document_skills(target: Dict[str, Any]) -> Dict[str, Any]:
    target = target if isinstance(target, dict) else {}
    skill_names = target.get("skill_names")
    if not isinstance(skill_names, list):
        skill_names = []
    skill_names = [str(x).strip() for x in skill_names if str(x or "").strip()][:10]
    extra_context = str(target.get("extra_context") or "").strip()
    trading = target.get("trading") if isinstance(target.get("trading"), dict) else {}

    blocks: List[Tuple[str, str]] = []
    for name in skill_names:
        p = _locate_skill_md(name)
        if not p:
            blocks.append((name, ""))
            continue
        blocks.append((name, _read_text(p, max_bytes=200_000)))

    joined = "\n\n".join([f"=== SKILL: {n} ===\n{c}" for n, c in blocks]).strip()
    if not joined:
        return {"ok": False, "error": "no_skill_content", "hint": "provide skill_names that exist in .hermes/skills or .trae/skills"}

    prompt = (
        "你是量化交易项目的技能文档工程师。请把给定 SKILL 文档改写成更可执行、更适合量化落地的版本。"
        "输出 Markdown，包含：能力概述、参数说明（含 trading 参数）、调用示例（HTTP 与 Python 各一份）、验收清单、风险提示。"
        "\n\n量化参数偏好（如有）：\n"
        + (str(trading) if trading else "（无）")
        + "\n\n补充上下文：\n"
        + (extra_context or "（无）")
        + "\n\n原始 SKILL 内容：\n"
        + joined[:24000]
    )
    md = _llm_generate(prompt)
    return {"ok": True, "result_markdown": md, "skills": skill_names}

