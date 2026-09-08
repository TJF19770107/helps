#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Codex 看图能力 · 视觉适配器入口
把图片转成结构化文本，让纯文本 Agent「看图」。
后端自动探测：gemini(有key) -> ollama(可达) -> tesseract(本地OCR)。
用法:
  python see_image.py <图片路径> [--prompt "..."] [--status]
"""
import argparse
import json
import os
import sys


def _find_harness_root():
    candidates = [
        os.environ.get("HARNESS_ROOT", ""),
        r"E:\龙虾AI主控中心\我的AI分身\企业微信群定制接单项目\deepseek-harness",
    ]
    for p in candidates:
        if p and os.path.isdir(os.path.join(p, "plugins", "modlens")):
            return p
    here = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        probe = os.path.join(here, "deepseek-harness")
        if os.path.isdir(os.path.join(probe, "plugins", "modlens")):
            return probe
        here = os.path.dirname(here)
    return None


HARNESS_ROOT = _find_harness_root()
if HARNESS_ROOT and HARNESS_ROOT not in sys.path:
    sys.path.insert(0, HARNESS_ROOT)

from plugins.modlens.modlens import ModLens  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="Codex 看图能力")
    ap.add_argument("image", nargs="?", help="图片路径 / data URL / URL")
    ap.add_argument("--prompt", default=None, help="解析提示词")
    ap.add_argument("--status", action="store_true", help="只看后端状态")
    args = ap.parse_args()

    if not HARNESS_ROOT:
        print(json.dumps({"ok": False, "error": "未找到 deepseek-harness（ModLens）"},
                         ensure_ascii=False, indent=2))
        return 1

    lens = ModLens()
    if args.status or not args.image:
        print(json.dumps(lens.status(), ensure_ascii=False, indent=2))
        return 0
    result = lens.analyze(args.image, args.prompt)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
