#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nvidia_avatar.py · 我的AI分身（NVIDIA 免费大脑版）
===================================================
复用 avatar.py 的灵魂(SOUL.md)与工具，把默认大脑换成 NVIDIA 免费通道，
让分身立刻能开口（当前 MiMo/DeepSeek/Ollama 大脑均不可用）。

零成本（NVIDIA NIM 免费额度）· 只新增本文件，不改动 avatar.py 原文件。
密钥安全：优先读环境变量 NVIDIA_API_KEY；未设置时从 atomcode_proxy.py
现有配置运行时读取（不在本文件硬编码新密钥）。

用法：
  python nvidia_avatar.py "一句话指令"       单轮
  python nvidia_avatar.py                     交互对话（输入 !工具名 调工具，/quit 退出）
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import avatar  # 复用 avatar.py 的 SOUL/工具/主循环

# 默认视觉模型已验证可用；也可换 meta/llama-3.2-90b-vision-instruct（慢）等
DEFAULT_NVIDIA_MODEL = "meta/llama-3.2-11b-vision-instruct"


def _nvidia_key():
    key = os.environ.get("NVIDIA_API_KEY")
    if key and key.startswith("nvapi-"):
        return key
    # 从 atomcode_proxy.py 现有配置读取，避免在本文件新增硬编码密钥
    proxy = r"E:\龙虾AI主控中心\我的AI分身\AtomCode\scripts\atomcode_proxy.py"
    try:
        with open(proxy, "r", encoding="utf-8") as f:
            for line in f:
                if 'NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "' in line:
                    return line.split('", "')[1].rsplit('")')[0]
    except Exception:
        pass
    return None


def nvidia_chat(brain, messages, timeout=180):
    import json
    import urllib.request
    key = _nvidia_key()
    if not key:
        raise RuntimeError("未找到 NVIDIA_API_KEY（需 nvapi- 开头）")
    model = brain if (isinstance(brain, str) and "/" in brain and brain != "nvidia") else DEFAULT_NVIDIA_MODEL
    body = json.dumps({
        "model": model,
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.4,
        "stream": False,
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://integrate.api.nvidia.com/v1/chat/completions",
        data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.loads(r.read().decode("utf-8"))
    msg = d["choices"][0]["message"]
    return msg.get("content") or msg.get("reasoning_content") or "(空响应)"


avatar.BRAIN_ROUTES["nvidia"] = nvidia_chat


def glm_chat(brain, messages, timeout=180):
    """GLM-5.3 大脑：优先 TeamoRouter 福利版(0.01折)，回退智谱直连。"""
    import json
    import urllib.request
    import os as _os
    key = _os.environ.get("GLM_API_KEY", "").strip()
    teamo_key = _os.environ.get("TEAMOROUTER_API_KEY", "").strip()
    if teamo_key:
        key = teamo_key
        model = "glm-5.3-flash-free"
        url = "https://teamorouter.cn/v1/chat/completions"
    else:
        if not key:
            raise RuntimeError("未设置 TEAMOROUTER_API_KEY 或 GLM_API_KEY")
        model = "glm-5.3-flash"
        url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    body = json.dumps({
        "model": model,
        "messages": messages,
        "max_tokens": 4096,
        "stream": False,
    }).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.loads(r.read().decode("utf-8"))
    msg = d["choices"][0]["message"]
    return msg.get("content") or msg.get("reasoning_content") or "(空响应)"


avatar.BRAIN_ROUTES["glm"] = glm_chat


def chat_with_fallback(brain, messages, timeout=180):
    """多模型 fallback：GLM-5.3-flash → NVIDIA(llama-vision)，大脑不断粮。"""
    import os as _os
    if _os.environ.get("GLM_API_KEY"):
        try:
            return glm_chat(brain, messages, timeout)
        except Exception as e:
            print("[fallback] GLM 失败(%s)，自动切换 NVIDIA..." % type(e).__name__)
    return nvidia_chat(brain, messages, timeout)


def pick_brain(name):
    # 显式指定且在路由内 -> 用之
    if name and name in avatar.BRAIN_ROUTES:
        return name, avatar.BRAIN_ROUTES[name]
    # 显式指定未知模型名 -> 仍走 ollama（保留原语义）
    if name and name not in avatar.BRAIN_ROUTES:
        return name, avatar.ollama_chat
    # 未指定 -> 优先 GLM-5.3-flash（智谱体验卡）
    import os as _os
    if _os.environ.get("GLM_API_KEY"):
        return "glm", glm_chat
    # 未指定 -> 优先 NVIDIA 免费大脑（避免死在无效的 MiMo key 上）
    if _nvidia_key():
        return "nvidia", nvidia_chat
    import os as _os
    if _os.environ.get("MIMO_API_KEY"):
        return "claude-sonnet-4-5", avatar.mimo_chat
    if _os.environ.get("DEEPSEEK_API_KEY"):
        return "deepseek-chat", avatar.deepseek_chat
    return avatar.DEFAULT_BRAIN, avatar.ollama_chat


avatar.pick_brain = pick_brain

if __name__ == "__main__":
    avatar.main()
