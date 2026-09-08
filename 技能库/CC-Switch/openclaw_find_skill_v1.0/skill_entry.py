import os
import re
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
                return raw.decode(enc, errors="ignore")
            except Exception:
                continue
        return raw.decode("utf-8", errors="ignore")
    except Exception:
        return ""


def _extract_frontmatter(text: str) -> Dict[str, str]:
    s = text or ""
    m = re.match(r"\s*---\s*\r?\n([\s\S]*?)\r?\n---\s*\r?\n", s)
    if not m:
        return {}
    fm = m.group(1)
    out: Dict[str, str] = {}
    for line in fm.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k:
            out[k] = v
    return out


def _iter_skill_md_paths() -> List[Path]:
    root = _repo_root()
    paths: List[Path] = []
    for base in (root / ".hermes" / "skills", root / ".trae" / "skills"):
        if not base.is_dir():
            continue
        for p in base.glob("*/SKILL.md"):
            if p.is_file():
                paths.append(p)
    return paths


def skill_openclaw_find_skill(query: Dict[str, Any]) -> Dict[str, Any]:
    query = query if isinstance(query, dict) else {}
    q = str(query.get("q") or "").strip()
    limit = int(query.get("limit") or 10)
    limit = max(1, min(50, limit))
    if not q:
        return {"ok": False, "error": "q_required"}

    ql = q.lower()
    hits: List[Dict[str, Any]] = []
    for p in _iter_skill_md_paths():
        txt = _read_text(p)
        if ql not in (txt or "").lower():
            continue
        fm = _extract_frontmatter(txt)
        skill_name = fm.get("name") or p.parent.name
        desc = fm.get("description") or ""
        hits.append(
            {
                "name": skill_name,
                "description": desc,
                "path": str(p),
                "scope": "hermes" if ".hermes" in str(p).replace("\\\\", "/") else "trae",
            }
        )

    hits = hits[:limit]
    return {"ok": True, "q": q, "matches": hits, "count": len(hits)}
