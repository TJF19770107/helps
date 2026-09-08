#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙虾·视觉路由（看图能力）v1.0
--------------------
给无视觉的文本模型补齐「看图」：把本地图片 base64 发给 NVIDIA 免费视觉模型，
拿回中文描述。零成本（NVIDIA NIM 免费额度），不改 config，不重启。

用法：
  python vision_read.py <图片路径> [问题] [模型名]

默认模型 meta/llama-3.2-11b-vision-instruct（免费，速度快）。
候选视觉模型（2026-08 在线）：
  meta/llama-3.2-90b-vision-instruct  最强，但免费档慢
  meta/llama-3.2-11b-vision-instruct  默认，快
  microsoft/phi-3-vision-128k-instruct 轻量
  nvidia/vila / nvidia/neva-22b

注意：z-ai/glm-5.2 已于 2026-08-21 在 NVIDIA 下架（HTTP 410），勿再使用。
"""
import base64
import json
import os
import sys
import urllib.request
import urllib.error

NVIDIA_API_KEY = os.environ.get(
    "NVIDIA_API_KEY",
    ""
)
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
DEFAULT_MODEL = "meta/llama-3.2-11b-vision-instruct"

_MIME = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp",
         "gif": "gif", "bmp": "bmp"}


def read_image(path, question=None, model=DEFAULT_MODEL, max_tokens=800):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    mime = _MIME.get(ext, "png")
    if question is None:
        question = "请用中文详细描述这张图片的内容，包括所有可见文字和界面元素。"
    body = {
        "model": model,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": question},
            {"type": "image_url", "image_url": {"url": f"data:image/{mime};base64,{b64}"}}
        ]}],
        "max_tokens": max_tokens,
        "temperature": 0.2,
    }
    req = urllib.request.Request(
        NVIDIA_BASE_URL + "/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": "Bearer " + NVIDIA_API_KEY,
                 "Content-Type": "application/json"})
    r = urllib.request.urlopen(req, timeout=120)
    d = json.loads(r.read().decode("utf-8"))
    return d["choices"][0]["message"]["content"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python vision_read.py <图片路径> [问题] [模型名]")
        sys.exit(1)
    img = sys.argv[1]
    q = sys.argv[2] if len(sys.argv) > 2 else None
    m = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_MODEL
    try:
        print(read_image(img, q, m))
    except urllib.error.HTTPError as e:
        print("[HTTP %d] %s" % (e.code, e.read().decode("utf-8", "replace")[:400]))
        sys.exit(1)
    except Exception as e:
        print("[ERROR] %s: %s" % (type(e).__name__, str(e)[:300]))
        sys.exit(1)