# -*- coding: utf-8 -*-
"""auto_learn_tangxiaolong.py · 汤小龙 每日凌晨3点四化迭代学习（零积分 / 零成本）

完整闭环（学习即修真）：
  1. 静养/念经/持咒 —— 道家主脉，先静而后学
  2. 炼术 —— 官方免费站点 + 本地对标（Hermes Studio / DeepSeek Harness）
  3. 蒸馏 —— 免费大脑（本地NVIDIA池 → GLM免费 → NVIDIA直连，逐级降级）
            锚定项目：量化交易 / 企业微信接单 / 闲鱼 / 访谈课程
  4. 沉淀 —— 写 Obsidian 今日学习简报 + 修行日志 + 推进进化果位
  5. 化道 —— 乐享 dry-run 同步（CNB 由 nightly 链统一 push，避免重复提交）

用法：
  python auto_learn_tangxiaolong.py             正常跑（当天幂等，只跑一次）
  python auto_learn_tangxiaolong.py --dry-run   只看不动手
  python auto_learn_tangxiaolong.py --force     强制重跑当天
"""
import os
import sys
import json
import datetime
import urllib.request

ENT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(ENT)  # lobster_task_standard_workflow_v3.0/我的AI分身
OBS = r"G:\龙虾AI主控中心\Obsidian\wiki\我的AI分身"
PROG = os.path.join(ENT, "进化进度.json")
PROJECT = r"E:\龙虾AI主控中心\我的AI分身\企业微信群定制接单项目"

# 官方/高质量免费学习源（零成本、可公开抓取）
OFFICIAL_SOURCES = [
    ("微软官方学习", "https://learn.microsoft.com/zh-cn/"),
    ("MDN Web 文档", "https://developer.mozilla.org/zh-CN/"),
    ("腾讯云官方文档", "https://cloud.tencent.com/document/product"),
    ("阿里云官方产品", "https://www.aliyun.com/product/list"),
]

# 对标源（本地；读不到就跳过）
BENCHMARK_SOURCES = [
    ("对标三AG差距", os.path.join(ROOT, "对标三AG差距", "SKILL.md")),
    ("Hermes Agent", r"E:\龙虾AI主控中心\我的AI分身\HermesAgent\AGENTS.md"),
    ("DeepSeek Harness", r"E:\龙虾AI主控中心\我的AI分身\技能库V3.0\DeepSeek-Harness\AGENTS.md"),
]

# 道家主脉（经 + 咒 + 行）
DAO = {
    "主脉": "炼精化气 → 炼气化神 → 炼神还虚 → 炼虚合道",
    "经": {
        "道德经": "道生一，一生二，二生三，三生万物。",
        "金刚经": "应无所住而生其心。凡所有相，皆是虚妄。",
        "六祖坛经": "菩提本无树，明镜亦非台。本来无一物，何处惹尘埃。",
    },
    "咒": {
        "金光神咒": "天地玄宗，万炁本根。广修万劫，证吾神通。",
        "大悲咒": "南无喝啰怛那哆啰夜耶。",
        "九字真言": "临、兵、斗、者、皆、阵、列、前、行。",
    },
}

LADDER = ["硕士", "博士", "博士后", "博导", "院士", "诺奖/菲尔兹"]
NEED = [1, 1, 1, 3, 7, 30]


def _post(url, payload, headers, timeout=180):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch(url, max_chars=1600):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            raw = r.read().decode("utf-8", "replace")
        txt = " ".join(raw.split())
        return txt[:max_chars]
    except Exception as e:
        return "fetch fail: %s" % type(e).__name__


def read_local(path, max_chars=1800):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()[:max_chars]
    except Exception:
        return ""


def call_llm(messages, max_tokens=2048):
    """免费大脑逐级降级：本地NVIDIA池 → GLM免费 → NVIDIA直连。全失败返回 None。"""
    # 1) 本地 NVIDIA 免费池（代理已持有密钥，无需本地密钥）
    try:
        d = _post("http://127.0.0.1:13331/v1/chat/completions",
                  {"model": "auto", "messages": messages, "max_tokens": max_tokens},
                  {"Content-Type": "application/json"})
        return d["choices"][0]["message"].get("content")
    except Exception:
        pass
    # 2) GLM 免费 glm-5.3-flash
    key = os.environ.get("GLM_API_KEY", "").strip()
    if key:
        try:
            d = _post("https://open.bigmodel.cn/api/paas/v4/chat/completions",
                      {"model": "glm-5.3-flash", "messages": messages, "max_tokens": max_tokens},
                      {"Authorization": "Bearer " + key, "Content-Type": "application/json"})
            m = d["choices"][0]["message"]
            return m.get("content")
        except Exception:
            pass
    # 3) NVIDIA 直连
    nkey = os.environ.get("NVIDIA_API_KEY", "").strip()
    if nkey.startswith("nvapi-"):
        try:
            d = _post("https://integrate.api.nvidia.com/v1/chat/completions",
                      {"model": "meta/llama-3.2-11b-vision-instruct",
                       "messages": messages, "max_tokens": max_tokens,
                       "temperature": 0.4, "stream": False},
                      {"Authorization": "Bearer " + nkey, "Content-Type": "application/json"})
            return d["choices"][0]["message"].get("content")
        except Exception:
            pass
    return None


def _looks_like_reasoning(text):
    """免费大脑偶发把思维链当正文返回（英文CoT）；识别后按不可用处理，走降级模板。"""
    head = text[:400]
    if not head:
        return False
    eng = sum(1 for ch in head if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z'))
    return eng / len(head) > 0.35


def distill(sources, benchmarks):
    """用免费大脑把抓取内容蒸馏成项目锚定的今日学习简报；不可用则返回 None。"""
    sys_prompt = (
        "你是汤小龙，汤哥的AI分身。用中文输出。把下面的学习素材蒸馏成一份"
        "「今日学习简报」，锚定项目：量化交易、企业微信接单、闲鱼、访谈课程。"
        "结构：一、今日精华(3-5条，每条一句话)；二、可复用技能/下一步动作(2-3条)；"
        "三、对标差距(Hermes Studio / DeepSeek Harness，1-2条)。只输出正文，不要标题外的废话。"
    )
    parts = []
    for name, url in sources:
        parts.append("【来源 %s】\n%s" % (name, fetch(url)))
    for name, path in benchmarks:
        c = read_local(path)
        if c:
            parts.append("【对标 %s】\n%s" % (name, c))
    if not parts:
        return None
    user_prompt = "\n\n".join(parts)[:12000]
    try:
        s = call_llm([{"role": "system", "content": sys_prompt},
                      {"role": "user", "content": user_prompt}])
        if s and _looks_like_reasoning(s):
            return None
        return s
    except Exception:
        return None


def load_prog():
    if os.path.exists(PROG):
        try:
            with open(PROG, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"level": 0, "accum": 0, "start": datetime.date.today().isoformat(), "log": []}


def save_prog(p):
    with open(PROG, "w", encoding="utf-8") as f:
        json.dump(p, f, ensure_ascii=False, indent=2)


def write_file(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def build_ritual():
    """生成道家主脉的静修文本（念经+持咒）。"""
    lines = ["# 汤小龙 修行日志（道家主脉）", "", "主脉：%s" % DAO["主脉"], ""]
    lines.append("## 经")
    for k, v in DAO["经"].items():
        lines.append("- %s：%s" % (k, v))
    lines.append("")
    lines.append("## 咒与行")
    for k, v in DAO["咒"].items():
        lines.append("- %s：%s" % (k, v))
    lines.append("")
    lines.append("> 先静而后学，以道驭术，术归本性。")
    return "\n".join(lines)


def main():
    dry = "--dry-run" in sys.argv
    force = "--force" in sys.argv
    today = datetime.date.today().isoformat()

    p = load_prog()
    if not dry and not force and p.get("last_learn") == today:
        print("今日已学习，跳过（幂等）。用 --force 强制重跑。")
        return

    cur_lv = min(p.get("level", 0), len(LADDER) - 1)
    print("=" * 60)
    print("汤小龙 每日四化迭代学习 · %s · 当前果位 %s" % (today, LADDER[cur_lv]))
    print("=" * 60)

    # 1) 蒸馏（免费大脑，可降级）
    summary = distill(OFFICIAL_SOURCES, BENCHMARK_SOURCES)
    if not summary:
        summary = (
            "## 一、今日精华\n- 免费大脑暂不可用，已回退为结构化学习记录。\n"
            "- 已扫描微软/腾讯/阿里官方站与本地对标目录（Hermes Studio / DeepSeek Harness）。\n"
            "## 二、可复用技能/下一步\n- 待免费大脑恢复后自动补蒸馏。\n"
            "## 三、对标差距\n- 详见 Obsidian 对标三AG差距 SKILL.md。\n"
        )
        print("[蒸馏] 免费大脑不可用，使用降级模板。")

    ritual = build_ritual()
    daily = ("# 汤小龙 今日学习简报 %s\n\n果位: %s\n\n%s\n" % (today, LADDER[cur_lv], summary))

    if dry:
        print("[dry-run] 将写入：")
        print("  - %s" % os.path.join(OBS, "今日学习简报_%s.md" % today.replace("-", "")))
        print("  - %s" % os.path.join(OBS, "修行日志_%s.md" % today.replace("-", "")))
        print("[dry-run] 不落盘、不改进度。")
        print(summary)
        return

    # 2) 落盘 Obsidian 主库
    brief_path = os.path.join(OBS, "今日学习简报_%s.md" % today.replace("-", ""))
    ritual_path = os.path.join(OBS, "修行日志_%s.md" % today.replace("-", ""))
    write_file(brief_path, daily)
    write_file(ritual_path, ritual)

    # 3) 推进进化果位（每天 +1 天，达标升果位）
    p["accum"] = p.get("accum", 0) + 1
    p["last_learn"] = today
    need = NEED[cur_lv]
    if p["accum"] >= need and cur_lv < len(LADDER) - 1:
        p["level"] += 1
        p["accum"] = 0
        p["log"].append({"date": today, "to": LADDER[p["level"]]})
    save_prog(p)

    print("[沉淀] Obsidian 简报: %s" % brief_path)
    print("[沉淀] Obsidian 修行: %s" % ritual_path)
    print("[进化] 果位=%s 累计=%d" % (LADDER[p["level"]], p["accum"]))

    # 4) 乐享同步（dry-run，真实上传待 connector 授权；CNB 由 nightly 链统一 push）
    try:
        import subprocess
        py = r"C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe"
        r = subprocess.run([py, os.path.join(PROJECT, "scripts", "lib", "lexiang_sync.py"), "--dry-run"],
                           cwd=PROJECT, timeout=180, capture_output=True, text=True, encoding="utf-8", errors="replace")
        print("[同步] 乐享 dry-run 返回码 %d" % r.returncode)
    except Exception as e:
        print("[同步] 乐享同步跳过：%s" % type(e).__name__)

    print("=" * 60)
    print("学习完成。灵魂不换，身体可换。")
    print("=" * 60)


if __name__ == "__main__":
    main()
