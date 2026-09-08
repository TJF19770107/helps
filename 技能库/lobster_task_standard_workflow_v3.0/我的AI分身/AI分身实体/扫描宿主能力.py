#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫描宿主能力.py · 汤小龙宿主能力自动继承（零积分纯本地）
=====================================================
每次启动汤小龙时自动执行：
  1. 扫描 Codex 两个 config.toml 的 [mcp_servers.*] / [plugins.*]
  2. 扫描全部技能目录的 SKILL.md
  3. 生成/刷新《宿主MCP技能继承清单.md》，汤小龙据此可直接调用宿主全部能力
"""
import glob
import os
import re
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "宿主MCP技能继承清单.md")
REGISTRY = os.path.join(HERE, "技能注册表.json")

CONFIGS = [
    os.path.expanduser("~/.codex/config.toml"),
    os.path.expanduser("~/.codex-orch/config.toml"),
    os.path.expanduser("~/.codex-hermes/config.toml"),
]
CLAUDE_JSON = os.path.expanduser("~/.claude.json")
CLAUDE_SKILLS = os.path.expanduser("~/.claude/skills")
DOUBAO_PROXY_PORT = "18000"  # doubao-proxy MCP（豆包能力桥接通道，Codex/Claude 均挂载）
TEAMO_PROXY_JSON = os.path.expanduser("~/.codex-orch/teamorouter-http-proxy.json")
# 免费别名自愈表（汤哥铁律：桌面下拉框选任何模型都强制走 0.01 折/免费）
FREE_ALIAS = {
    "gpt-5.4": "glm-5.3-flash-free",
    "gpt-5.4-mini": "glm-5.3-flash-free",
    "gpt-5.5": "deepseek-v4-flash-free",
    "gpt-5.6-luna": "glm-5.3-flash-free",
    "glm-5.3": "glm-5.3-flash-free",
    "glm-5.3-flash": "glm-5.3-flash-free",
    "kimi-k3": "deepseek-v4-flash-free",
}
SKILL_DIRS = [
    os.path.expanduser("~/.codex/skills"),
    os.path.expanduser("~/.codex-orch/skills"),
    os.path.expanduser("~/.agents/skills"),
    r"G:\WorkBuddy_Data\skills",
    CLAUDE_SKILLS,
    r"C:\Users\Administrator\.marvis\skills\market",
    r"C:\Users\Administrator\.marvis\skills\custom",
    r"C:\Users\Administrator\.openclaw\skills",
]
HOST_EXTRAS = {
    "marvis_mcp": r"C:\Users\Administrator\.marvis\skills\mcp_configs",
    "openclaw": r"C:\Users\Administrator\.openclaw\openclaw.json",
    "opencodex": os.path.expanduser("~/.codex-orch/opencodex.config.toml"),
    "deepseek_harness_docs": r"E:\龙虾AI主控中心\我的AI分身\企业微信群定制接单项目\docs",
}
BY_HOST = os.path.join(os.path.abspath(os.path.join(HERE, "..", "..", "..")), "by-host")


def scan_config(path):
    mcps, plugins = [], []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                m = re.match(r"^\[mcp_servers\.([\w-]+)\]", line.strip())
                if m:
                    mcps.append(m.group(1))
                m = re.match(r"^\[plugins\.\"([^\"]+)\"\]", line.strip())
                if m:
                    plugins.append(m.group(1))
    except OSError:
        pass
    return mcps, plugins


def scan_skills():
    rows = []
    for d in SKILL_DIRS:
        found = glob.glob(os.path.join(d, "**", "SKILL.md"), recursive=True)
        rows.append((d, len(found)))
    return rows


def guard_free_alias():
    """自愈 teamorouter-desktop 别名表：被更新覆盖则自动恢复免费改写，返回是否修复过"""
    try:
        import json
        with open(TEAMO_PROXY_JSON, "r", encoding="utf-8") as f:
            d = json.load(f)
        am = d.setdefault("alias_map", {})
        if all(am.get(k) == v for k, v in FREE_ALIAS.items()):
            return False
        am.update(FREE_ALIAS)
        with open(TEAMO_PROXY_JSON, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[别名自愈] 失败: {e}")
        return False


DEFAULT_MODEL = "gpt-5.6-luna"  # 网关别名映射到 glm-5.3-flash-free（0.01折）
ORCH_CONFIG = os.path.expanduser("~/.codex-orch/config.toml")
ORCH_CATALOG = os.path.expanduser(
    "~/.codex-orch/backups_state/teamorouter-fast/model-catalog.json")
CANDIDATE_CATALOG = r"E:\龙虾AI主控中心\MCP服务\model-catalog.M001.candidate.json"
FREE_SLUGS = ("deepseek-v4-flash-free", "deepseek-v4-pro-free", "gpt-5.6-luna")


def _backup(path):
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = f"{path}.bak_selfheal_{stamp}"
    with open(path, "rb") as src, open(bak, "wb") as dst:
        dst.write(src.read())
    return bak


def guard_default_model():
    """config.toml 默认模型行被刷新覆盖时，先备份再写回 0.01 折别名。"""
    try:
        with open(ORCH_CONFIG, "r", encoding="utf-8") as f:
            raw = f.read()
        cur = re.search(r'(?m)^model\s*=\s*"(.*)"', raw)
        if cur and cur.group(1) == DEFAULT_MODEL:
            return False
        _backup(ORCH_CONFIG)
        new = re.sub(r'(?m)^model\s*=\s*".*"', f'model = "{DEFAULT_MODEL}"', raw)
        if new == raw:
            new = f'model = "{DEFAULT_MODEL}"\n' + raw
        with open(ORCH_CONFIG, "w", encoding="utf-8") as f:
            f.write(new)
        return True
    except Exception as e:
        print(f"[守卫] 默认模型修复失败: {e}")
        return False


def guard_free_catalog():
    """下拉框目录丢失免费模型时，先备份再从候选目录整份恢复。"""
    try:
        import json
        with open(ORCH_CATALOG, "r", encoding="utf-8") as f:
            slugs = {m.get("slug") for m in json.load(f).get("models", [])}
        if all(s in slugs for s in FREE_SLUGS):
            return False
        if not os.path.exists(CANDIDATE_CATALOG):
            print(f"[守卫] 候选目录缺失: {CANDIDATE_CATALOG}")
            return False
        _backup(ORCH_CATALOG)
        with open(CANDIDATE_CATALOG, "rb") as src, open(ORCH_CATALOG, "wb") as dst:
            dst.write(src.read())
        return True
    except Exception as e:
        print(f"[守卫] 目录修复失败: {e}")
        return False


def main():
    healed_cfg = guard_default_model()
    print(f"[守卫] 默认模型行{'已修复' if healed_cfg else '完好'}")
    healed_cat = guard_free_catalog()
    print(f"[守卫] 下拉框免费模型目录{'已恢复' if healed_cat else '完好'}")
    healed = guard_free_alias()
    print(f"[别名自愈] TeamoRouter 免费改写{'已恢复' if healed else '完好'}")
    lines = [
        "# 汤小龙 · 宿主MCP技能继承清单",
        "",
        f"> 自动生成：{datetime.now():%Y-%m-%d %H:%M:%S}（零积分纯本地扫描）",
        "> 用途：启动汤小龙时自动刷新；汤小龙可依据本清单直接调用宿主全部 MCP/插件/技能。",
        "",
    ]
    all_mcps = []
    for cfg in CONFIGS:
        mcps, plugins = scan_config(cfg)
        all_mcps += mcps
        lines.append(f"## 配置文件：`{cfg}`")
        lines.append("")
        lines.append(f"- MCP 服务器（{len(mcps)} 个）：{'、'.join(mcps) if mcps else '（无）'}")
        lines.append(f"- 插件（{len(plugins)} 个）：{'、'.join(plugins) if plugins else '（无）'}")
        lines.append("")
    lines.append("## 技能目录扫描")
    lines.append("")
    total = 0
    for d, n in scan_skills():
        total += n
        lines.append(f"- `{d}` → {n} 个 SKILL.md")
    lines.append("")
    lines.append(f"**MCP 合计（去重）：{len(set(all_mcps))} 个 ｜ 技能合计：{total} 个**")
    lines.append("")

    # ===== Claude Code 宿主（mcpServers + 技能已并入上方目录扫描）=====
    claude_mcps = []
    try:
        with open(CLAUDE_JSON, "r", encoding="utf-8") as f:
            import json
            cj = json.load(f)
            claude_mcps = list((cj.get("mcpServers") or {}).keys())
    except Exception:
        pass
    lines.append(f"## Claude Code 宿主继承：`{CLAUDE_JSON}`")
    lines.append("")
    lines.append(f"- MCP（{len(claude_mcps)} 个）：{'、'.join(claude_mcps) if claude_mcps else '（无）'}")
    lines.append(f"- 其中 doubao-proxy（端口 {DOUBAO_PROXY_PORT}）= 豆包宿主能力桥接通道，豆包的对话/文档/抓取能力经此 MCP 被汤小龙继承")
    lines.append("")
    lines.append("## WorkBuddy 宿主继承")
    lines.append("")
    lines.append("- WorkBuddy 即本桌面 Codex 宿主：`~/.codex-orch/config.toml` 的 MCP + plugins 即 WorkBuddy 原生能力，已并入上方扫描")
    lines.append("- WorkBuddy 技能库 `G:\\WorkBuddy_Data\\skills` 已并入上方技能目录扫描")
    lines.append("")
    lines.append("## 动态继承机制")
    lines.append("")
    lines.append("- 每次启动汤小龙自动刷新本清单；另有计划任务 Lobster_AvatarCapabilitySync 定时刷新，实现动态继承")

    # ===== 追加宿主：Marvis / OpenClaw / OpenCodex / DeepSeek Harness =====
    lines.append("")
    lines.append("## 追加宿主继承（Marvis / OpenClaw / OpenCodex / DeepSeek Harness）")
    lines.append("")
    mcp_dir = HOST_EXTRAS["marvis_mcp"]
    try:
        mcps = [os.path.splitext(f)[0] for f in os.listdir(mcp_dir) if f.endswith(".json")]
    except OSError:
        mcps = []
    lines.append(f"- **Marvis**（`C:\\Users\\Administrator\\.marvis`）：MCP 配置 {len(mcps)} 个（{'、'.join(mcps) if mcps else '无'}）；skills/market + custom 已并入上方技能扫描")
    oc = HOST_EXTRAS["openclaw"]
    providers = []
    try:
        import json as _json
        raw = open(oc, "r", encoding="utf-8").read()
        # openclaw.json 使用宽松语法，逐段提取 provider 名即可
        import re as _re
        providers = sorted(set(_re.findall(r'"([a-zA-Z0-9_-]+)":\s*\{\s*"baseUrl"', raw)))
    except OSError:
        pass
    lines.append(f"- **OpenClaw**（`{oc}`）：大脑提供方 {len(providers)} 个（{'、'.join(providers) if providers else '未知'}）；skills 23 个已并入技能扫描")
    lines.append(f"- **OpenCodex**（`{HOST_EXTRAS['opencodex']}`）：Codex 运行时提供方/模型目录已登记，接入 18091 免费通道")
    lines.append("- **DeepSeek Harness**：提供方配置映射表位于 `docs\\DeepSeekHarness_Provider配置界面字段一一对应映射表_20260818.md`，免费大脑 deepseek-v4-flash-free（CNB/TeamoRouter）已作为汤小龙默认推理层接入")

    # ===== 运行时挂载注册：把 by-host 技能包注册进汤小龙运行环境 =====
    registry = {"generated_at": datetime.now().isoformat(timespec="seconds"), "hosts": {}}
    total_registered = 0
    if os.path.isdir(BY_HOST):
        for host in sorted(os.listdir(BY_HOST)):
            host_dir = os.path.join(BY_HOST, host)
            if not os.path.isdir(host_dir):
                continue
            skills = sorted(glob.glob(os.path.join(host_dir, "**", "SKILL.md"), recursive=True))
            registry["hosts"][host] = {
                "path": host_dir,
                "skill_count": len(skills),
                "skills": [os.path.basename(os.path.dirname(s)) for s in skills],
            }
            total_registered += len(skills)
    registry["total_skills"] = total_registered
    with open(REGISTRY, "w", encoding="utf-8") as f:
        import json as _json
        _json.dump(registry, f, ensure_ascii=False, indent=2)
    lines.append("")
    lines.append("## 运行时挂载注册（by-host → 汤小龙技能注册表）")
    lines.append("")
    for host, info in registry["hosts"].items():
        lines.append(f"- `{host}`：注册 {info['skill_count']} 个技能（源：{info['path']}）")
    lines.append(f"**运行时注册技能合计：{total_registered} 个 → `技能注册表.json`（启动汤小龙时加载）**")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[继承] 宿主能力扫描完成 → {OUT}")
    print(f"[继承] MCP {len(set(all_mcps))} 个 ｜ 技能 {total} 个")


if __name__ == "__main__":
    main()
