#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动我的AI分身.py · 一键全量加载（内置到分身实体主体）
=====================================================
触发：「启动我的AI分身」
动作：
  1. 加载灵魂（SOUL.md + 心理画像）
  2. 加载框架（五步法V3.6 + 全域模板#321 + 1234定义卡）
  3. 加载四库索引（Obsidian/IMA/乐享/CNB）
  4. 加载技能挂载清单（技能总索引 + 开口/看图/手脚/六根八识/对标三AG）
  5. 启动 NVIDIA 免费大脑，进入交互对话
用法：python 启动我的AI分身.py ["一句话指令"]
"""
import os
import sys
import avatar

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # 我的AI分身\
sys.path.insert(0, HERE)

import nvidia_avatar  # 含大脑路由 + NVIDIA chat
import avatar_tools_edit  # P3 代码编辑力
import avatar_tools_web  # Firecrawl/内置抓取
avatar_tools_web.register()  # 注册 !web 工具
avatar_tools_edit.register()  # 注册 !edit 工具

SOUL = os.path.join(HERE, "SOUL.md")
PORTRAIT = os.path.join(ROOT, "心理画像与对标差距分析_20260826.md")
ARCH = os.path.join(ROOT, "AI分身Agent架构与定义v1.0_20260826.md")
BOUNDARY = os.path.join(ROOT, "AI分身能力边界与完善计划v1.1_20260826.md")
INDEX = os.path.join(ROOT, "技能总索引.md")
LU_GEN = os.path.join(ROOT, "六根八识", "SKILL.md")
GAP3AG = os.path.join(ROOT, "对标三AG差距", "SKILL.md")
SKILL_OPS = os.path.join(HERE, "技能", "分身运维与大脑切换", "SKILL.md")
WU = os.path.dirname(ROOT)  # lobster_task_standard_workflow_v3.0\
QUANYU = os.path.join(WU, "龙虾全域官方模板-最终版.md")
CARD1234 = os.path.join(WU, "20260825_1234快捷体系_官方定义卡.md")
FIVESTEP = os.path.join(WU, "龙虾五步法V3.6·PR#21闭环版（成本优先置顶）SKILL.md")


def load(path, label, max_chars=6000):
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        print(f"  [✓] {label}: {len(text)}字")
        return text[:max_chars]
    except Exception as e:
        print(f"  [✗] {label}: {e}")
        return ""


def _ensure_nvidia_proxy():
    import socket, subprocess, os, time
    port = int(os.environ.get("NVIDIA_PROXY_PORT", "13331"))
    ok = False
    try:
        s = socket.create_connection(("127.0.0.1", port), timeout=2); s.close(); ok = True
    except Exception:
        ok = False
    if not ok:
        print("[NVIDIA] 启动免费模型池代理 @ 127.0.0.1:%d ..." % port)
        env = os.environ.copy()
        env["NVIDIA_API_KEY"] = env.get("NVIDIA_API_KEY", "")
        env["NVIDIA_PROXY_PORT"] = str(port)
        subprocess.Popen([r"C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe",
                          os.path.join(HERE, "nvidia_free_proxy.py")], env=env,
                         creationflags=subprocess.CREATE_NO_WINDOW)
        for _ in range(10):
            time.sleep(1)
            try:
                s = socket.create_connection(("127.0.0.1", port), timeout=1); s.close(); ok = True; break
            except Exception:
                pass
    print("[NVIDIA] 免费模型池 %s @ 127.0.0.1:%d" % ("已就绪" if ok else "启动失败", port))
    return ok


def main():
    # 自动拉起 NVIDIA 免费模型池（无需手动双击）
    _ensure_nvidia_proxy()
    # 宿主能力自动继承：扫描 MCP/插件/技能，刷新继承清单（零积分）
    import 扫描宿主能力
    扫描宿主能力.main()
    # 运行时加载技能注册表：by-host 宿主技能包真正进入汤小龙上下文
    import json as _json
    _reg_path = os.path.join(HERE, "技能注册表.json")
    if os.path.exists(_reg_path):
        with open(_reg_path, "r", encoding="utf-8") as _f:
            _reg = _json.load(_f)
        print(f"[运行时挂载] 已加载技能注册表：{_reg.get('total_skills', 0)} 个技能，宿主 {len(_reg.get('hosts', {}))} 个")
    print("=" * 50)
    print("  启动我的AI分身 · 全量加载")
    print("=" * 50)

    print("\n[1/5] 加载灵魂（L1）...")
    soul = load(SOUL, "SOUL.md 灵魂")
    portrait = ""  # 已并入 SOUL.md 最终版 v3.0（2026-08-29）

    print("\n[2/5] 加载框架（L2-L5）...")
    arch = ""  # 已并入 SOUL.md 最终版 v3.0（2026-08-29）
    boundary = ""  # 已并入 SOUL.md 最终版 v3.0（2026-08-29）
    wu = load(FIVESTEP, "龙虾五步法V3.6", max_chars=3000)
    quanyu = load(QUANYU, "全域官方模板", max_chars=3000)
    card = load(CARD1234, "1234定义卡", max_chars=3000)

    print("\n[3/5] 加载四库索引...")
    obs_wiki = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))), "Obsidian", "wiki", "我的AI分身")
    if os.path.isdir(obs_wiki):
        files = os.listdir(obs_wiki)
        print(f"  [✓] Obsidian 主库: {len(files)} 份文档")
    else:
        print(f"  [✗] Obsidian 主库: 目录不存在")
    print("  [✓] IMA / 乐享 / CNB: 连接器登记在 MCP_插件\\README.md")

    print("\n[4/5] 加载技能挂载清单...")
    index = load(INDEX, "技能总索引", max_chars=4000)
    lu_gen = load(LU_GEN, "六根八识", max_chars=2000)
    gap3ag = load(GAP3AG, "对标三AG差距", max_chars=2000)
    skill_ops = load(SKILL_OPS, "分身运维与大脑切换", max_chars=3000)
    import glob as _glob
    auto_skills = []
    for _sf in sorted(_glob.glob(os.path.join(HERE, "技能", "**", "SKILL.md"), recursive=True)):
        _n = os.path.basename(os.path.dirname(_sf))
        _t = load(_sf, _n, max_chars=3000)
        if _t:
            auto_skills.append(_t)
            print("  [auto] 内置技能: " + _n)

    print("\n[5/5] 启动大脑...")
    import os as _b
    _brain_display = ("glm-5.3-flash-free（TeamoRouter 福利版 0.01折）"
                      if _b.environ.get("TEAMOROUTER_API_KEY")
                      else ("glm-5.3-flash" if _b.environ.get("GLM_API_KEY") else "NVIDIA llama-vision（免费）"))
    print("  大脑: " + _brain_display)
    print("  灵魂不换，身体可换。")
    print("=" * 50)
    print("  汤小龙已就位。输入对话干活；/quit 退出")
    print("=" * 50 + "\n")

    # 构建完整系统提示
    system = "\n\n".join(filter(None, [soul, portrait, arch, boundary, wu, quanyu, card, index, lu_gen, gap3ag, skill_ops, *auto_skills]))
    system += "\n\n你是汤小龙。开始工作。"

    _ensure_nvidia_proxy()

# 复用 nvidia_avatar 的 chat
    messages = [{"role": "system", "content": system}]
    import os as _os
    chat_fn = nvidia_avatar.chat_with_fallback
    model = "auto"

    # 单轮模式
    if len(sys.argv) > 1:
        cmd = " ".join(sys.argv[1:])
        routed = avatar.maybe_run_command(cmd) if hasattr(avatar, "maybe_run_command") else None
        if routed is not None:
            print(routed)
            return
        messages.append({"role": "user", "content": cmd})
        try:
            print("汤小龙 >", chat_fn(model, messages))
        except Exception as e:
            print("调用大脑失败:", e)
        return

    # 交互模式
    while True:
        try:
            u = input("你 > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见，汤哥。"); break
        if u in ("/quit", "/exit", "退出"):
            print("再见，汤哥。"); break
        if not u:
            continue
        r = avatar.maybe_run_tool(u)
        if r is not None:
            print("工具结果:", r); continue
        c = avatar.maybe_run_command(u) if hasattr(avatar, "maybe_run_command") else None
        if c is not None:
            print("触发词结果:", c); continue
        messages.append({"role": "user", "content": u})
        try:
            ans = chat_fn(model, messages)
            print("\n汤小龙 >", ans, "\n")
            messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            print("调用大脑失败:", e)


if __name__ == "__main__":
    main()
