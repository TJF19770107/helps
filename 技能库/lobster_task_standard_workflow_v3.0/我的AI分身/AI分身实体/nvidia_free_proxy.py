# -*- coding: utf-8 -*-
"""nvidia_free_proxy.py - NVIDIA 免费模型池：自动切换 + 手动下拉选择。

无 Docker、低内存。Codex/任意 OpenAI 兼容 Agent 指向 127.0.0.1:13331/v1。

- model=auto 或空：任务感知自动切换（看图用视觉模型，否则用文本模型）
- model=<具体模型>：强制用该模型（手动锁定，单次请求生效）
- 浏览器打开 http://127.0.0.1:13331 有下拉框，手动选「默认模型」

实测（2026-08-29）：本账号仅 llama-3.2-11b-vision / gemma-4-31b 可调；
其余模型返回 404「Function Not found for account」或超时，需到
build.nvidia.com 登录后逐模型「激活」才会可用。
"""
import json, os, threading, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("NVIDIA_PROXY_PORT", "13331"))
KEY = os.environ.get("NVIDIA_API_KEY", "")
NVIDIA = "https://integrate.api.nvidia.com/v1/chat/completions"

# 已实测可调用的模型（自动切换只在这两个里选）
TEXT_CHAIN = [
    "google/gemma-4-31b-it",
]
VISION_CHAIN = [
    "meta/llama-3.2-11b-vision-instruct",
]
# 此账号未激活/超时的模型（仅下拉框展示，不参与自动切换）
DEAD = [
    "deepseek-ai/deepseek-v4-pro-0813",
    "deepseek-ai/deepseek-v4-flash-0731",
    "meta/llama-3.2-90b-vision-instruct",
    "mistralai/mistral-large",
    "nv-mistralai/mistral-nemo-12b-instruct",
    "microsoft/phi-3-vision-128k-instruct",
    "nvidia/vila",
]
CHAIN = TEXT_CHAIN + VISION_CHAIN
ALL = CHAIN + DEAD
VISION = set(VISION_CHAIN)

LOCK = threading.Lock()
PINNED = "auto"

def has_image(messages):
    for m in messages:
        c = m.get("content")
        if isinstance(c, list):
            for part in c:
                if isinstance(part, dict) and part.get("type") == "image_url":
                    return True
        elif isinstance(c, str) and ("data:image/" in c or ".png" in c.lower() or ".jpg" in c.lower()):
            return True
    return False

def call_model(model, messages, max_tokens):
    body = {"model": model, "messages": messages, "max_tokens": max_tokens, "stream": False}
    req = urllib.request.Request(NVIDIA, data=json.dumps(body).encode("utf-8"),
                                 headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    r = urllib.request.urlopen(req, timeout=180)
    d = json.loads(r.read().decode("utf-8"))
    d["_used_model"] = model
    return d

def nvidia_chat(messages, max_tokens=2048, model=None):
    if model and model != "auto" and model in ALL:
        return call_model(model, messages, max_tokens)
    with LOCK:
        pinned = PINNED
    if pinned != "auto" and pinned in ALL:
        return call_model(pinned, messages, max_tokens)
    chain = (VISION_CHAIN + TEXT_CHAIN) if has_image(messages) else (TEXT_CHAIN + VISION_CHAIN)
    last = None
    for m in chain:
        try:
            return call_model(m, messages, max_tokens)
        except Exception as e:
            last = e
            continue
    raise last

def set_pinned(model):
    global PINNED
    with LOCK:
        PINNED = model if model in ALL else "auto"
        return PINNED

class H(BaseHTTPRequestHandler):
    def _send(self, code, obj, html=False):
        data = (obj if isinstance(obj, bytes) else json.dumps(obj, ensure_ascii=False).encode("utf-8"))
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8" if html else "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _page(self):
        with LOCK:
            cur = PINNED
        opts = ["<option value='auto'%s>auto（自动）</option>" % (" selected" if cur == "auto" else "")]
        for m in CHAIN:
            tag = " [视觉]" if m in VISION else ""
            opts.append("<option value='%s'%s>%s%s（可用）</option>" % (m, " selected" if cur == m else "", m, tag))
        for m in DEAD:
            opts.append("<option value='%s' disabled>%s（未激活，去 build.nvidia.com 激活）</option>" % m)
        return ("<!doctype html><html lang='zh'><head><meta charset='utf-8'>"
                "<meta name='viewport' content='width=device-width,initial-scale=1'>"
                "<title>NVIDIA 免费模型池</title></head>"
                "<body style='font-family:system-ui,sans-serif;max-width:760px;margin:40px auto;padding:0 20px;color:#1a1a2e'>"
                "<h2>NVIDIA 免费模型池</h2>"
                "<p>端点 <code>127.0.0.1:%d/v1</code>。<code>model=auto</code> 自动切换，或显式 <code>model=&lt;模型&gt;</code>。</p>"
                "<p>选择默认模型后点「应用」，对未显式指定 model 的请求生效。</p>"
                "<form method='get' action='/api/set_model'>"
                "<select name='model' style='padding:8px 12px;font-size:15px;width:100%%'>%s</select>"
                "<button type='submit' style='margin-top:12px;padding:9px 20px;font-size:15px;background:#1f6feb;color:#fff;border:none;border-radius:6px;cursor:pointer'>应用</button>"
                "</form><p>当前默认：<b>%s</b></p>"
                "<p style='color:#777;font-size:13px'>未激活的模型会灰显；登录 build.nvidia.com 逐个激活后刷新即可用。</p></body></html>") % (PORT, "".join(opts), cur)

    def do_GET(self):
        if self.path in ("/", "/index"):
            self._send(200, self._page().encode("utf-8"), html=True)
        elif self.path.startswith("/v1/models"):
            self._send(200, {"object": "list", "data": [{"id": m, "object": "model", "owned_by": "NVIDIA"} for m in CHAIN]})
        elif self.path.startswith("/api/set_model"):
            q = self.path.split("?", 1)[1] if "?" in self.path else ""
            model = None
            for kv in q.split("&"):
                if kv.startswith("model="):
                    model = kv[len("model="):]
            set_pinned(model)
            self._send(200, {"ok": True, "pinned": PINNED})
        elif self.path in ("/api/state", "/api/ping", "/health"):
            with LOCK:
                cur = PINNED
            self._send(200, {"status": "ok", "pinned": cur, "available": CHAIN, "dead": DEAD})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        try:
            ln = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(ln) if ln else b"{}"
            body = json.loads(raw.decode("utf-8") or "{}")
            if self.path.startswith("/v1/chat/completions"):
                d = nvidia_chat(body.get("messages", []), body.get("max_tokens", 2048), body.get("model", "auto"))
                self._send(200, d)
            elif self.path.startswith("/api/set_model"):
                set_pinned(body.get("model"))
                self._send(200, {"ok": True, "pinned": PINNED})
            else:
                self._send(404, {"error": "not found"})
        except Exception as e:
            self._send(502, {"error": {"message": str(e)}})

    def log_message(self, *a):
        pass

if __name__ == "__main__":
    print("NVIDIA 免费池 @ 127.0.0.1:%d | 可用 %d + 未激活 %d" % (PORT, len(CHAIN), len(DEAD)))
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
