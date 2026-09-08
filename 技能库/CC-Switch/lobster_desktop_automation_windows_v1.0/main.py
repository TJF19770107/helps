from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class DependencyStatus:
    """依赖检查结果。"""

    pywinauto: bool
    pyautogui: bool


def _project_root_from_skill_dir(skill_dir: Path) -> Path:
    """从技能目录回溯项目根目录。"""

    if skill_dir.parent.name == "skills" and skill_dir.parent.parent.name in (".trae", ".hermes"):
        return skill_dir.parent.parent.parent
    return skill_dir.parent


def _try_import_deps() -> DependencyStatus:
    """探测可用依赖，不做任何安装动作。"""

    try:
        import pywinauto  # noqa: F401

        has_pywinauto = True
    except Exception:
        has_pywinauto = False

    try:
        import pyautogui  # noqa: F401

        has_pyautogui = True
    except Exception:
        has_pyautogui = False

    return DependencyStatus(pywinauto=has_pywinauto, pyautogui=has_pyautogui)


def ensure_dependencies(allow_install: bool = False) -> DependencyStatus:
    """检查依赖；默认不联网安装，除非显式允许。"""

    st = _try_import_deps()
    if st.pywinauto or st.pyautogui:
        return st

    if not allow_install:
        raise RuntimeError(
            "缺少依赖：需要 pywinauto 或 pyautogui 之一。"
            "本技能默认不自动联网安装；如需自动安装，请在调用时传入 allow_install=True，且确保你已明确授权联网安装。"
        )

    subprocess.check_call([sys.executable, "-m", "pip", "install", "pywinauto", "pyautogui"])
    return _try_import_deps()


def _parse_coords(coords: str) -> Tuple[int, int]:
    """解析 'x,y' 坐标。"""

    m = re.match(r"^\s*(\d+)\s*,\s*(\d+)\s*$", coords or "")
    if not m:
        raise ValueError("coords 必须为 'x,y' 格式，例如 '120,300'")
    return int(m.group(1)), int(m.group(2))


def screenshot(out_path: str, allow_install: bool = False) -> Dict[str, Any]:
    """保存一次屏幕截图到 out_path。"""

    st = ensure_dependencies(allow_install=allow_install)
    if not st.pyautogui:
        raise RuntimeError("当前环境缺少 pyautogui，无法截图。")

    import pyautogui

    p = Path(out_path).expanduser().resolve()
    p.parent.mkdir(parents=True, exist_ok=True)
    img = pyautogui.screenshot()
    img.save(str(p))
    return {"ok": True, "out_path": str(p)}


def find_windows(title_re: Optional[str] = None, allow_install: bool = False) -> List[Dict[str, Any]]:
    """列出当前桌面窗口（尽量通过 UIA 获取）。"""

    st = ensure_dependencies(allow_install=allow_install)
    if not st.pywinauto:
        return [{"ok": False, "error": "缺少 pywinauto，无法枚举窗口（可改用 pyautogui 坐标级操作）"}]

    from pywinauto import Desktop

    desktop = Desktop(backend="uia")
    wins = []
    for w in desktop.windows():
        try:
            title = w.window_text()
            if title_re and not re.search(title_re, title or ""):
                continue
            rect = w.rectangle()
            wins.append(
                {
                    "title": title,
                    "class_name": w.class_name(),
                    "rect": {"left": rect.left, "top": rect.top, "right": rect.right, "bottom": rect.bottom},
                }
            )
        except Exception:
            continue
    return wins


def list_controls(title_re: str, allow_install: bool = False) -> str:
    """输出指定窗口的控件树（用于定位）。"""

    st = ensure_dependencies(allow_install=allow_install)
    if not st.pywinauto:
        raise RuntimeError("缺少 pywinauto，无法列出控件。")

    from pywinauto import Desktop

    desktop = Desktop(backend="uia")
    w = desktop.window(title_re=title_re)
    w.wait("ready", timeout=10)
    return w.dump_tree()


def click(
    coords: Optional[str] = None,
    title_re: Optional[str] = None,
    control_title_re: Optional[str] = None,
    allow_install: bool = False,
) -> Dict[str, Any]:
    """点击：优先控件级（pywinauto），否则坐标级（pyautogui）。"""

    st = ensure_dependencies(allow_install=allow_install)

    if st.pywinauto and title_re and control_title_re:
        from pywinauto import Desktop

        desktop = Desktop(backend="uia")
        w = desktop.window(title_re=title_re)
        w.wait("ready", timeout=10)
        w.set_focus()
        ctl = w.child_window(title_re=control_title_re)
        ctl.wait("ready", timeout=10)
        ctl.click_input()
        return {"ok": True, "mode": "pywinauto", "title_re": title_re, "control_title_re": control_title_re}

    if not coords:
        raise ValueError("缺少参数：请提供 coords='x,y' 或同时提供 title_re + control_title_re")

    if not st.pyautogui:
        raise RuntimeError("当前环境缺少 pyautogui，无法按坐标点击。")

    import pyautogui

    x, y = _parse_coords(coords)
    pyautogui.click(x=x, y=y)
    return {"ok": True, "mode": "pyautogui", "coords": {"x": x, "y": y}}


def type_text(text: str, interval_ms: int = 0, allow_install: bool = False) -> Dict[str, Any]:
    """键入文本（可设置每字符间隔）。"""

    st = ensure_dependencies(allow_install=allow_install)
    if not st.pyautogui:
        raise RuntimeError("当前环境缺少 pyautogui，无法输入。")

    import pyautogui

    interval = max(0, int(interval_ms)) / 1000.0
    pyautogui.typewrite(text or "", interval=interval)
    return {"ok": True, "chars": len(text or ""), "interval_ms": int(interval_ms)}


def run_json(argv: Optional[List[str]] = None) -> str:
    """CLI 入口：以 JSON 读取输入并输出 JSON 结果。"""

    args = list(argv or sys.argv[1:])
    raw = sys.stdin.read() if not args else " ".join(args)
    payload = json.loads(raw) if raw.strip() else {}

    action = str(payload.get("action") or "").strip()
    allow_install = bool(payload.get("allow_install") is True)

    if action == "screenshot":
        out_path = str(payload.get("out_path") or "")
        return json.dumps(screenshot(out_path=out_path, allow_install=allow_install), ensure_ascii=False)
    if action == "find_windows":
        title_re = payload.get("title_re")
        return json.dumps(find_windows(title_re=title_re, allow_install=allow_install), ensure_ascii=False)
    if action == "list_controls":
        title_re = str(payload.get("title_re") or "")
        return json.dumps({"ok": True, "tree": list_controls(title_re=title_re, allow_install=allow_install)}, ensure_ascii=False)
    if action == "click":
        return json.dumps(
            click(
                coords=payload.get("coords"),
                title_re=payload.get("title_re"),
                control_title_re=payload.get("control_title_re"),
                allow_install=allow_install,
            ),
            ensure_ascii=False,
        )
    if action == "type":
        return json.dumps(
            type_text(
                text=str(payload.get("text") or ""),
                interval_ms=int(payload.get("interval_ms") or 0),
                allow_install=allow_install,
            ),
            ensure_ascii=False,
        )

    raise ValueError("未知 action：支持 screenshot/find_windows/list_controls/click/type")


def main() -> int:
    """命令行主入口。"""

    try:
        print(run_json())
        return 0
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

