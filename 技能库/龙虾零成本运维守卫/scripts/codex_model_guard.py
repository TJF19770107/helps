#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Codex config.toml 模型漂移守卫  v1.0
------------------------------------------------
根因（2026-09-08 汤小龙自主进化查明）：
  C:\\Program Files\\Teamo\\teamorouter-desktop.exe 内置 Rust 模块 src\\codex\\config.rs /
  catalog.rs，会把服务端拉取的「当日 priority 模型」写进
  C:\\Users\\Administrator\\.codex-orch\\config.toml 的 "# >>> teamorouter-codex" 标记块。
  该 slug 每天轮换（gpt-5.6-luna / gpt-5.6-sol / gpt-5.6-terra / gpt-6-astra ...），
  旧 slug 次日即失效，折率未知 -> 触碰「切换必报 / 付费须确认」成本红线。

  另有第二写入者：Codex 桌面版（WindowsApps OpenAI.Codex）升级时重写整个 config.toml
  （判据：ChatGPT.exe 版本号 + cua_node hash 同时变化）。

功能：
  1. 读 config.toml 的 model 行，比对白名单（动态读 model-catalog.json + 安全硬编码集）
  2. 漂移 -> 备份 -> 改回首选安全模型 -> 写结构化漂移日志
  3. 校验 env 三件套（CODEX_MODEL / CODEX_BASE_URL / CODEX_HOME），env 优先级高于 config
  4. --check 只报告不改；默认 --fix 修正

零成本：纯本地标准库，不调用任何云端模型。
用法：
  python codex_model_guard.py            # 检查并修复
  python codex_model_guard.py --check    # 只报告
"""
import os
import re
import sys
import json
import time
import shutil
import winreg
from datetime import datetime

# v1.1 状态回执：零成本纯本地，失败不许拖垮守卫本体
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from guard_receipt import write_receipt
except Exception:
    write_receipt = None

CODEX_HOME = os.environ.get("CODEX_HOME") or r"C:\Users\Administrator\.codex-orch"
CONFIG = os.path.join(CODEX_HOME, "config.toml")
CATALOG = os.path.join(CODEX_HOME, "backups_state", "teamorouter-fast", "model-catalog.json")
LOGDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
DRIFT_LOG = os.path.join(CODEX_HOME, "model_drift_events.jsonl")

# 首选安全模型：0.01 折免费档，已在 18091 实测可用
PREFERRED = "gpt-5.6-luna"
# 安全硬编码集（即使 catalog 损坏也认）
SAFE_FALLBACK = {
    "gpt-5.6-luna",            # glm-5.3-flash-free  0.01折
    "deepseek-v4-flash-free",  # 免费
    "deepseek-v4-pro-free",    # 免费（后端 deepseek-v4-flash-ga-260731）
    "glm-5.3-flash-free",      # 0.01折
}
# 明确收费红线，出现必须告警
PAID_REDLINE = {"gpt-5.4-mini", "gpt-5.4", "gpt-5.5"}  # glm-5.3-flash / glm-5.3 / kimi-k3

ENV_EXPECT = {
    "CODEX_MODEL": PREFERRED,
    "CODEX_BASE_URL": "http://127.0.0.1:18091/v1",
    "CODEX_HOME": r"C:\Users\Administrator\.codex-orch",
}


def log(msg):
    print("[%s] %s" % (datetime.now().strftime("%H:%M:%S"), msg))


def read_env(name):
    for root, sub in ((winreg.HKEY_CURRENT_USER, r"Environment"),
                      (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment")):
        try:
            k = winreg.OpenKey(root, sub)
        except Exception:
            continue
        try:
            v, _ = winreg.QueryValueEx(k, name)
            return v
        except OSError:
            pass
    return None


def load_whitelist():
    wl = set(SAFE_FALLBACK)
    if os.path.exists(CATALOG):
        try:
            d = json.load(open(CATALOG, encoding="utf-8"))
            for m in d.get("models", []):
                slug = m.get("slug") or m.get("id")
                if slug:
                    wl.add(slug)
        except Exception as e:
            log("catalog 读取失败(%s)，仅用硬编码白名单" % e)
    # catalog 里也含收费马甲（gpt-5.4 -> glm-5.3 等），必须剔出白名单
    # 否则「未知 slug」判定会被它们蒙混过关
    return wl - PAID_REDLINE


def get_model_line(text):
    m = re.search(r'^model\s*=\s*"([^"]+)"', text, re.M)
    return m.group(1) if m else None


def set_model_line(text, new_model):
    return re.sub(r'^model\s*=\s*"[^"]+"', 'model = "%s"' % new_model, text, count=1, flags=re.M)


def append_drift_event(old, new, reason):
    os.makedirs(os.path.dirname(DRIFT_LOG), exist_ok=True)
    rec = {"ts": datetime.now().isoformat(timespec="seconds"), "old": old,
           "new": new, "reason": reason, "pid_src": "codex_model_guard"}
    try:
        with open(DRIFT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception as e:
        log("漂移日志写入失败: %s" % e)


def main():
    fix = "--check" not in sys.argv
    if not os.path.exists(CONFIG):
        log("config.toml 不存在: %s" % CONFIG)
        return 2

    text = open(CONFIG, encoding="utf-8", errors="ignore").read()
    cur = get_model_line(text)
    wl = load_whitelist()
    log("当前 model = %s" % cur)
    log("白名单 %d 个: %s" % (len(wl), ",".join(sorted(wl))))

    status = "OK"
    if cur in PAID_REDLINE:
        status = "PAID_REDLINE"
        log("!!! 收费红线模型: %s (0.01折白名单外，会烧钱)" % cur)
    elif cur not in wl:
        status = "UNKNOWN_SLUG"
        log("!!! 未知 slug（多为 TeamoRouter 当日轮换值，折率不明）: %s" % cur)

    if status != "OK":
        append_drift_event(cur, PREFERRED, status)
        if fix:
            bak = CONFIG + ".bak_guard_" + datetime.now().strftime("%Y%m%d_%H%M%S")
            shutil.copy2(CONFIG, bak)
            log("已备份 -> %s" % os.path.basename(bak))
            new_text = set_model_line(text, PREFERRED)
            # 只改 model 行，绝不动 wire_api / base_url（AGENTS.md 红线）
            open(CONFIG, "w", encoding="utf-8", newline="\n").write(new_text)
            log("已改回安全模型 %s" % PREFERRED)
            log("复检 model = %s" % get_model_line(open(CONFIG, encoding="utf-8").read()))
        else:
            log("--check 模式，未修改")

    # env 三件套校验（env 优先级 > config.toml，是真正的兜底）
    log("--- env 三件套 ---")
    env_ok = True
    for k, want in ENV_EXPECT.items():
        got = read_env(k)
        ok = (got == want)
        env_ok = env_ok and ok
        log("%s %s = %s %s" % ("[OK]" if ok else "[!!]", k, got,
                               "" if ok else "(期望 %s)" % want))
    if not env_ok:
        log("!!! env 兜底失效：config.toml 漂移将直接影响实际调用，需立即人工修复")

    ok = (status == "OK" and env_ok)
    rc = 0 if ok else 1
    log("结论: config=%s / env=%s" % (status, "OK" if env_ok else "BROKEN"))
    if write_receipt:
        p = write_receipt(
            "codex_model_guard", healthy=ok,
            detail="config=%s / env=%s / model=%s"
                   % (status, "OK" if env_ok else "BROKEN", cur),
            version="1.1", exit_code=rc,
            extra={"model": cur, "status": status, "env_ok": env_ok,
                   "preferred": PREFERRED})
        if p:
            log("[INFO] 状态回执 -> " + p)
    return rc


if __name__ == "__main__":
    sys.exit(main())
