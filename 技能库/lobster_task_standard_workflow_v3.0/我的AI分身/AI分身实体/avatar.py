#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
avatar.py · 我的AI分身（实体化 CLI agent）
============================================
大脑：Ollama 本地模型（默认 zero-cost，离线可用）
灵魂：SOUL.md（自动加载）
身体：独立进程，不依赖 WorkBuddy —— 像 Codex/Claude Code 一样的独立 agent

用法：
  python avatar.py                # 交互对话
  python avatar.py "一句话指令"   # 单轮指令（跑工具）
  python avatar.py --brain deepseek-r1:7b   # 换大脑（本机已装）

可选大脑（环境变量或 --brain）：
  deepseek-r1:7b   本地推理，零成本离线   ★默认
  qwen3:0.6b       本地轻量，最快
  gemma4:e4b       本地通用
  qwen2.5vl:7b     本地视觉（看图）
  cloud            走 ollama cloud 模型（deepseek-v4-flash:0731-cloud 等）
"""
import os, sys, json, subprocess, argparse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SOUL = os.path.join(HERE, "SOUL.md")
DEFAULT_BRAIN = "deepseek-r1:7b"
LEXIANG_SKILL = r"E:\龙虾AI主控中心\我的AI分身\技能库\lexiang-folder-sync\SKILL.md"
LEXIANG_BATCH = r"E:\龙虾AI主控中心\我的AI分身\豆包主会话全集\temp\lexiang_batch_sync.py"
WORKFLOW_HOME = r"E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v3.0\我的AI分身"

def load_soul():
    try:
        with open(SOUL, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return "你是汤小龙，汤哥的AI分身。指令式、高效、成本优先。"

def ollama_chat(brain, messages, timeout=180):
    """调本机 Ollama，零成本"""
    body = json.dumps({"model": brain, "messages": messages, "stream": False}).encode()
    req = urllib.request.Request("http://127.0.0.1:11434/api/chat", data=body,
                                 headers={"content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())["message"]["content"]

def mimo_chat(brain, messages, timeout=180):
    """调小米 MiMo V2.5 Pro（Anthropic 兼容端点，token-plan-cn 免费计划）"""
    import os as _os
    key = _os.environ.get("MIMO_API_KEY") or _os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("未设置 MIMO_API_KEY / OPENAI_API_KEY")
    body = json.dumps({"model": brain, "max_tokens": 2048, "messages": messages}).encode()
    req = urllib.request.Request("https://token-plan-cn.xiaomimimo.com/anthropic/v1/messages",
                                 data=body, headers={
                                     "x-api-key": key, "anthropic-version": "2023-06-01",
                                     "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.loads(r.read().decode())
    return "".join(b.get("text", "") for b in d.get("content", []))

def deepseek_chat(brain, messages, timeout=180):
    """调 DeepSeek API（OpenAI 兼容）"""
    import os as _os
    key = _os.environ.get("DEEPSEEK_API_KEY")
    if not key or key.startswith("atom"):
        raise RuntimeError("DEEPSEEK_API_KEY 无效或未设置（需 sk- 开头）")
    body = json.dumps({"model": brain, "messages": messages, "stream": False}).encode()
    req = urllib.request.Request("https://api.deepseek.com/chat/completions", data=body,
                                 headers={"authorization": f"Bearer {key}",
                                          "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.loads(r.read().decode())
    return d["choices"][0]["message"]["content"]

# 大脑路由表：按可用性自动探测（给 key 即插即用）
BRAIN_ROUTES = {
    "ollama": ollama_chat,
    "mimo": mimo_chat,
    "deepseek": deepseek_chat,
}

def pick_brain(name):
    """返回 (brain_name, chat_fn)。探测顺序：指定 → mimo → deepseek → ollama"""
    if name and name in BRAIN_ROUTES:
        return name, BRAIN_ROUTES[name]
    if name and name not in BRAIN_ROUTES:
        # 用户指定了 ollama 模型名或未知 → 走 ollama
        return name, ollama_chat
    import os as _os
    if _os.environ.get("MIMO_API_KEY"):
        return "claude-sonnet-4-5", mimo_chat
    if _os.environ.get("DEEPSEEK_API_KEY"):
        return "deepseek-chat", deepseek_chat
    return DEFAULT_BRAIN, ollama_chat

# ---------- 工具注册（手脚） ----------
TOOLS = {}

def tool(name, desc):
    def deco(fn):
        TOOLS[name] = (fn, desc)
        return fn
    return deco

@tool("render_video", "零成本出片：python <skill>/make_koubo_sample3.py（或 make.py/make_enterprise.py）")
def render_video(script="make_koubo_sample3.py"):
    d = r"E:\龙虾AI主控中心\我的AI分身\AI分身接单出片Skill库\00_零成本口播片\资产"
    p = os.path.join(d, script)
    if not os.path.exists(p):
        return f"脚本不存在: {p}"
    py = r"C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe"
    r = subprocess.run([py, p], capture_output=True, text=True, timeout=600)
    return (r.stdout or r.stderr)[-800:]

@tool("note", "写工作日志：note <内容> —— 追加到 .workbuddy/memory/YYYY-MM-DD.md")
def note(content):
    import datetime
    d = r"E:\龙虾AI主控中心\我的AI分身\豆包主会话全集\.workbuddy\memory"
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, datetime.date.today().isoformat() + ".md")
    with open(p, "a", encoding="utf-8") as f:
        f.write(f"\n- [AI分身实体] {content}\n")
    return f"已记入 {p}"

@tool("search_kb", "查知识库：search_kb <关键词> —— grep Obsidian 我的AI分身目录")
def search_kb(kw):
    r = subprocess.run(["rg", "-l", kw, r"E:\龙虾AI主控中心\Obsidian\wiki\我的AI分身"],
                       capture_output=True, text=True, timeout=30)
    return (r.stdout or r.stderr)[:800]

TOOL_HINT = "\n".join(f"- {n}: {d}" for n, (_, d) in TOOLS.items())

def maybe_run_tool(user_text):
    """极简工具路由：匹配 !工具名 参数"""
    for name, (fn, _) in TOOLS.items():
        if user_text.strip().startswith("!" + name):
            arg = user_text.strip()[len(name)+1:].strip()
            try:
                return fn(arg)
            except Exception as e:
                return f"工具 {name} 执行失败: {e}"
    return None


def maybe_run_command(user_text):
    """触发词路由：让对话框里的 1234 / 四化迭代知识库 / 乐享同步 明确进入对应技能，不再只当普通对话。"""
    text = (user_text or "").strip()
    low = text.lower()
    if "1234" in text or "四化迭代知识库" in text or "乐享同步" in text or "镜像上传乐享" in text:
        hints = []
        if os.path.exists(LEXIANG_SKILL):
            hints.append(f"乐享同步技能卡：{LEXIANG_SKILL}")
        if os.path.exists(LEXIANG_BATCH):
            hints.append(f"乐享批量上传脚本：{LEXIANG_BATCH}")
        hints.append(f"分身入口：{WORKFLOW_HOME}")
        print("[触发路由] 命中：乐享同步 / 四化迭代知识库 / 1234")
        print("  " + "\n  ".join(hints))
        if text.lower().startswith("!sync"):
            py = sys.executable or r"C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe"
            try:
                r = subprocess.run([py, LEXIANG_BATCH], capture_output=True, text=True, timeout=600)
                return (r.stdout or r.stderr)[-1500:]
            except Exception as e:
                return f"乐享批量同步执行失败: {e}"
        return "已加载乐享同步路由。如需实际执行：输入 !sync 调用批量脚本；token 只走环境变量，不落盘。"
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", default=None)
    ap.add_argument("--brain", default=None, help="ollama/mimo/deepseek 或 ollama 模型名，默认自动探测")
    args = ap.parse_args()

    soul = load_soul()
    system = soul + "\n\n## 可用工具（输入 !工具名 参数 调用）\n" + TOOL_HINT + "\n\n你是汤小龙。开始工作。"

    messages = [{"role": "system", "content": system}]
    brain, chat_fn = pick_brain(args.brain)
    print("🦞 汤小龙已启动 | 大脑:", brain, "| 灵魂: SOUL.md")
    print("   输入对话干活；!render_video / !note / !search_kb 调工具；/quit 退出\n")

    if args.cmd:
        r = maybe_run_tool(args.cmd)
        if r is not None:
            print(r)
        else:
            c = maybe_run_command(args.cmd)
            if c is not None:
                print(c)
            else:
                messages.append({"role": "user", "content": args.cmd})
                try:
                    print("\n" + chat_fn(brain, messages))
                except Exception as e:
                    print("调用大脑失败:", e)
                    print("→ 可用令牌：设置 MIMO_API_KEY（MiMo免费计划）或 DEEPSEEK_API_KEY（DeepSeek）后重试；")
                    print("  或 --brain ollama 用本地模型（需 Ollama 模型模板完好）")
        return

    while True:
        try:
            u = input("你 > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见，汤哥。"); break
        if u in ("/quit", "/exit", "退出"):
            print("再见，汤哥。"); break
        if not u:
            continue
        r = maybe_run_tool(u)
        if r is not None:
            print("🦞 工具结果:", r); continue
        c = maybe_run_command(u)
        if c is not None:
            print("🦞 触发词结果:", c); continue
        messages.append({"role": "user", "content": u})
        try:
            ans = chat_fn(brain, messages)
            print("\n🦞 汤小龙 >", ans, "\n")
            messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            print("调用大脑失败:", e)
            print("→ 可用令牌：设置 MIMO_API_KEY（MiMo免费计划）或 DEEPSEEK_API_KEY（DeepSeek）后重试")

if __name__ == "__main__":
    main()
