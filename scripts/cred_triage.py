#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
cred_triage.py - 龙虾凭据分层与云端故障分层诊断守卫 v1.0
纯 stdlib / 零积分 / 只读（除 --apply 外不改动任何凭据）

解决三类「假成功 / 假失败」：
  1. 窄凭据被高优先级来源（环境变量）注入 -> 静默遮蔽本地宽凭据 -> 假性能力缺失
     （报错文本说「scope 不够」，真因是「你用错了那把钥匙」）
  2. 异步受理被读成失败（status:200 + sn + "received but didn't finish" = 成功受理）
  3. 云平台失败一出错就改配置（实为五层中某一层，配置层可能完全正确）

子命令
  layers  [--tool cnb|gh|git] [--json]        凭据来源分层盘点 + 遮蔽预警
  probe   [--tool cnb|gh]     [--json]        逐层摘除法身份探针（真发 HTTP）
  verdict --file F | --text S  [--json]       异步受理裁定
  cloud5  [--json]                            云平台五层定位清单
  selftest                                    四场景离线自检（不发网络）

硬红线：令牌只进内存，输出一律脱敏（前4后2 + 长度）。
"""
import os
import io
import re
import sys
import json
import time
import argparse
import urllib.request
import urllib.error

VERSION = "1.0.0"

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

HOME = os.path.expanduser("~")

# ---------------------------------------------------------------- 脱敏

def mask(tok):
    if not tok:
        return "(none)"
    s = str(tok)
    if len(s) <= 8:
        return "*" * len(s) + " (len=%d)" % len(s)
    return "%s***%s (len=%d)" % (s[:4], s[-2:], len(s))


# ---------------------------------------------------------------- 凭据来源分层模型

def _read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _git_credentials_tokens():
    """解析 ~/.git-credentials 的 store 行：https://user:pass@host"""
    out = []
    p = os.path.join(HOME, ".git-credentials")
    if not os.path.exists(p):
        return out
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                m = re.match(r"^[a-z+]+://([^:/\s]+):([^@/\s]+)@([^\s/]+)", line)
                if m:
                    out.append({"host": m.group(3), "user": m.group(1),
                                "token": m.group(2), "src": p, "line": i + 1})
    except Exception:
        pass
    return out


# shorts = 该层命中后是否会「短路」掉更低优先级层。
# 只有 env 注入才是真短路（CLI 源码 if (env) return;）；
# file→file 是并列来源，标 shorts=False，否则会触发守卫误报（形态 #11）。
def layers_cnb():
    """CNB CLI 源码优先级：env CNB_TOKEN_FOR_CODEBUDDY > env CNB_TOKEN > ~/.cnb/token"""
    ls = []
    env_a = os.environ.get("CNB_TOKEN_FOR_CODEBUDDY")
    ls.append({"prio": 1, "layer": "env", "shorts": True, "name": "CNB_TOKEN_FOR_CODEBUDDY",
               "value": env_a, "note": "CLI 源码里优先级最高，命中即 return"})
    env_b = os.environ.get("CNB_TOKEN")
    ls.append({"prio": 2, "layer": "env", "shorts": True, "name": "CNB_TOKEN",
               "value": env_b, "note": "命中即 return，本地文件不再读取"})
    tokfile = os.path.join(HOME, ".cnb", "token")
    val = None
    if os.path.exists(tokfile):
        j = _read_json(tokfile)
        if isinstance(j, dict):
            val = j.get("access_token")
        if not val:
            try:
                val = open(tokfile, encoding="utf-8").read().strip()
            except Exception:
                val = None
    ls.append({"prio": 3, "layer": "file", "shorts": False, "name": tokfile,
               "value": val, "note": "宽 OAuth 令牌（JSON.access_token）"})
    ls.append({"prio": 4, "layer": "default", "shorts": False, "name": "(anonymous)",
               "value": None, "note": "无凭据 -> 私有资源一律 404 伪装"})
    return ls


def layers_gh():
    ls = []
    for k in ("GITHUB_TOKEN", "GH_TOKEN"):
        ls.append({"prio": 1, "layer": "env", "shorts": True, "name": k,
                   "value": os.environ.get(k), "note": "高优先级注入，命中即短路"})
    for c in _git_credentials_tokens():
        if "github" in c["host"]:
            ls.append({"prio": 2, "layer": "file", "shorts": False,
                       "name": "~/.git-credentials@%s" % c["host"],
                       "value": c["token"], "note": "git store 行 L%d（并列来源）" % c["line"]})
    hp = os.path.join(HOME, ".config", "gh", "hosts.yml")
    val = None
    if os.path.exists(hp):
        try:
            for line in open(hp, encoding="utf-8", errors="replace"):
                m = re.search(r"oauth_token:\s*(\S+)", line)
                if m:
                    val = m.group(1)
                    break
        except Exception:
            pass
    ls.append({"prio": 3, "layer": "file", "shorts": False, "name": hp, "value": val,
               "note": "gh CLI 登录态（并列来源，非被遮蔽）"})
    ls.append({"prio": 4, "layer": "default", "shorts": False, "name": "(anonymous)", "value": None,
               "note": "匿名访问私有仓同样 404，不可据此判「仓库被删」"})
    return ls


def layers_git():
    ls = []
    ls.append({"prio": 1, "layer": "env", "shorts": True, "name": "GIT_ASKPASS / GCM",
               "value": os.environ.get("GIT_ASKPASS"), "note": "常被宿主注入"})
    gc = os.path.join(HOME, ".gitconfig")
    val = None
    if os.path.exists(gc):
        try:
            txt = open(gc, encoding="utf-8", errors="replace").read()
            m = re.search(r"helper\s*=\s*(.+)", txt)
            if m:
                val = m.group(1).strip()
        except Exception:
            pass
    ls.append({"prio": 2, "layer": "file", "shorts": False, "name": gc + ":credential.helper",
               "value": val, "note": "这是读取 store 的机制本身，与 store 是链路不是遮蔽"})
    for c in _git_credentials_tokens():
        ls.append({"prio": 3, "layer": "file", "shorts": False,
                   "name": "~/.git-credentials@%s" % c["host"],
                   "value": c["token"], "note": "store 行 L%d" % c["line"]})
    ls.append({"prio": 4, "layer": "default", "shorts": False, "name": "(interactive)", "value": None,
               "note": "回落交互 -> 自动化里表现为 could not read Username / 180s 卡死"})
    return ls


TOOLS = {"cnb": layers_cnb, "gh": layers_gh, "git": layers_git}

# 身份探针（与仓库无关，用来区分「凭据坏」与「对象不存在」）
IDENTITY = {
    "cnb": ("https://api.cnb.cool/user", {"Accept": "application/json"}),
    "gh": ("https://api.github.com/user", {"Accept": "application/vnd.github+json"}),
}


def http_get(url, token, extra_headers=None, timeout=20):
    h = {"User-Agent": "lobster-cred-triage/%s" % VERSION}
    if token:
        h["Authorization"] = "Bearer %s" % token
    if extra_headers:
        h.update(extra_headers)
    req = urllib.request.Request(url, headers=h, method="GET")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read(400).decode("utf-8", "replace")
            return r.status, body, int((time.time() - t0) * 1000)
    except urllib.error.HTTPError as e:
        try:
            body = e.read(300).decode("utf-8", "replace")
        except Exception:
            body = ""
        return e.code, body, int((time.time() - t0) * 1000)
    except Exception as e:
        return 0, repr(e)[:200], int((time.time() - t0) * 1000)


# ---------------------------------------------------------------- 子命令：layers

def cmd_layers(args):
    fn = TOOLS.get(args.tool)
    if not fn:
        print("未知 tool: %s（可选 %s）" % (args.tool, "/".join(TOOLS)))
        return 2
    ls = fn()
    hits = [x for x in ls if x.get("value")]
    for x in ls:
        x["hit"] = bool(x.get("value"))
        x["masked"] = mask(x.get("value"))
        x.pop("value", None)
    # 遮蔽判定：只有当「更高的命中层 shorts=True」时才算真遮蔽。
    # file→file 并列来源不算，否则守卫误报（形态 #11）会毁掉可信度。
    hit_prios = [x["prio"] for x in hits]
    shadow = []
    for x in ls:
        if not x["hit"]:
            x["verdict"] = "GRAY-未命中"
            continue
        blockers = [y for y in ls if y["hit"] and y["prio"] < x["prio"] and y.get("shorts")]
        if blockers:
            shadow.append({"blocked": x["name"], "by": blockers[0]["name"]})
            x["verdict"] = "YELLOW-被遮蔽(by %s)" % blockers[0]["name"]
        else:
            x["verdict"] = "GREEN-生效中"
    out = {"tool": args.tool, "layers": ls,
           "active_prio": min(hit_prios) if hit_prios else None,
           "shadowed_by_env": shadow}
    shadow = [s["blocked"] for s in shadow]
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    print("== 凭据来源分层 · tool=%s ==" % args.tool)
    print("%-4s %-8s %-42s %-26s %s" % ("优先级", "层", "来源", "脱敏值", "判定"))
    for x in ls:
        print("%-4s %-8s %-42s %-26s %s" % (
            x["prio"], x["layer"], x["name"][:42], x["masked"], x["verdict"]))
    if shadow:
        print("\n[!] 遮蔽预警：以下低优先级宽凭据被高层屏蔽，永远不会生效：")
        for s in shadow:
            print("    -", s)
        print("    -> 跑 `cred_triage.py probe --tool %s` 做摘除法实证" % args.tool)
    else:
        print("\n[ok] 无跨层遮蔽。")

    # 同 host 多凭据：长度不同说明宽窄并存，store 命中顺序决定命运
    hosts = {}
    for x in ls:
        m = re.search(r"@([\w.\-]+)$", x["name"])
        if m and x["hit"]:
            hosts.setdefault(m.group(1), []).append(x["masked"])
    dup = {h: v for h, v in hosts.items() if len(v) > 1 and len(set(v)) > 1}
    if dup:
        print("\n[!] 同 host 多凭据（宽窄并存，命中顺序决定命运）：")
        for h, v in dup.items():
            print("    %s -> %s" % (h, " | ".join(v)))
        print("    -> 短(窄)令牌若排在前面，git 会先命中它，表现为「权限莫名不够」")
    return 0


# ---------------------------------------------------------------- 子命令：probe

def cmd_probe(args):
    tool = args.tool
    if tool not in IDENTITY:
        print("该 tool 无内置身份探针：%s" % tool)
        return 2
    url, hdrs = IDENTITY[tool]
    ls = TOOLS[tool]()
    rows = []
    for x in ls:
        v = x.get("value")
        if not v:
            rows.append({"layer": x["layer"], "name": x["name"], "masked": "(none)",
                         "status": "-", "verdict": "SKIP-未命中"})
            continue
        st, body, ms = http_get(url, v, hdrs)
        vd = "GREEN-可用" if st == 200 else ("RED-被拒" if st in (401, 403) else "GRAY-%s" % st)
        rows.append({"layer": x["layer"], "name": x["name"], "masked": mask(v),
                     "status": st, "ms": ms, "verdict": vd,
                     "body": body.replace("\n", " ")[:160]})
    ok = [r for r in rows if r["status"] == 200]
    bad = [r for r in rows if r["status"] in (401, 403)]
    if ok and bad:
        bad_prio = min([TOOLS[tool]()[rows.index(b)]["prio"] if rows.index(b) < len(TOOLS[tool]()) else 99
                        for b in bad], default=99)
        concl = ("RED · 窄凭据遮蔽宽凭据：高层 %s 被拒(%s)，但低层 %s 通过 200。"
                 % (bad[0]["name"], bad[0]["status"], ok[0]["name"]))
        fix = ("摘掉高优先级环境变量后再试（Windows: set %s= ；bash: unset %s）"
               % (bad[0]["name"], bad[0]["name"]))
    elif ok:
        concl = "GREEN · 生效层可用：%s" % ok[0]["name"]
        fix = "无需处理"
    elif bad:
        concl = "RED · 所有命中层均被拒，凭据本身失效或 scope 不足 -> 重签令牌"
        fix = "重签令牌（不要动仓库，404 是伪装）"
    else:
        concl = "GRAY · 未命中任何凭据层 -> 匿名"
        fix = "补凭据；匿名下 404 不等于对象不存在"
    out = {"tool": tool, "url": url, "rows": rows, "conclusion": concl, "fix": fix}
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    print("== 逐层摘除法身份探针 · tool=%s ==" % tool)
    print("身份端点：%s  （与仓库无关，用来区分「凭据坏」与「对象不存在」）\n" % url)
    print("%-8s %-40s %-22s %-6s %s" % ("层", "来源", "脱敏值", "状态", "判定"))
    for r in rows:
        print("%-8s %-40s %-22s %-6s %s" % (
            r["layer"], r["name"][:40], r["masked"], r["status"], r["verdict"]))
        if r.get("body"):
            print("         ↳ %s" % r["body"][:140])
    print("\n结论：%s" % concl)
    print("修复：%s" % fix)
    return 0


# ---------------------------------------------------------------- 子命令：verdict（异步受理裁定）

ASYNC_HINT = ("received", "didn't finish", "did not finish", "pending", "queued",
              "running", "building", "accepted", "processing", "in progress",
              "尚未完成", "处理中", "排队", "已受理")
ID_KEYS = ("sn", "id", "build_id", "task_id", "job_id", "pipeline_id", "run_id",
           "request_id", "buildId", "taskId", "entry_id", "media_id")


def _extract(obj, keys, path=""):
    found = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in keys and isinstance(v, (str, int)) and str(v).strip():
                found[path + k] = str(v)
            found.update(_extract(v, keys, path + k + "."))
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:10]):
            found.update(_extract(v, keys, "%s[%d]." % (path, i)))
    return found


def cmd_verdict(args):
    if args.file:
        raw = open(args.file, encoding="utf-8", errors="replace").read()
    else:
        raw = args.text or ""
    if not raw.strip():
        print("需要 --file 或 --text")
        return 2
    obj = None
    try:
        obj = json.loads(raw)
    except Exception:
        pass
    blob = raw
    ids = _extract(obj, ID_KEYS) if obj is not None else {}
    if not ids:
        for k in ID_KEYS:
            m = re.search(r"[\"']?%s[\"']?\s*[:=]\s*[\"']?([A-Za-z0-9_\-]{4,})" % k, blob)
            if m:
                ids[k] = m.group(1)

    status = None
    m = re.search(r"[\"']?status[\"']?\s*[:=]\s*[\"']?(\d{3}|[a-z_]+)", blob, re.I)
    if m:
        status = m.group(1)
    lower = blob.lower()
    hint = [h for h in ASYNC_HINT if h in lower]
    has_id = bool(ids)

    if status and str(status).strip() in ("200", "201", "202", "ok", "success") and has_id and hint:
        v, level = "ACCEPTED · 已受理（不是失败！）", "GREEN"
        action = "拿到业务 ID 后另查终态，别把受理当完成，更别当失败"
    elif status and str(status).strip() in ("200", "201", "202", "ok", "success") and has_id:
        v, level = "DONE_OR_ACCEPTED · 成功且带业务 ID", "GREEN"
        action = "同步接口看 ID；异步接口另查终态确认"
    elif status and str(status).strip() in ("200", "201", "202", "ok", "success") and not has_id:
        v, level = "SUSPECT_FAKE_SUCCESS · 说成功但没业务 ID", "RED"
        action = "形态「假成功」：回执漂亮但无凭据可追，必须回读/回查验收"
    elif hint and has_id:
        v, level = "ACCEPTED · 异步受理中", "GREEN"
        action = "轮询终态接口，超时上限内未终态才报超时"
    elif re.search(r"\b(4\d\d|5\d\d)\b", str(status or "")) or re.search(
            r"[\"']?(errcode|error|code)[\"']?\s*[:=]\s*[\"']?([45]\d\d|[1-9]\d{3,})", blob):
        v, level = "FAILED · 真失败", "RED"
        action = "注意：报错文本指向的对象 ≠ 真正出问题的对象，先做来源分层再归因"
    else:
        v, level = "UNKNOWN · 无法裁定", "YELLOW"
        action = "补齐 status / 业务 ID 再裁；不可凭关键词猜测"

    out = {"verdict": v, "level": level, "status": status,
           "business_ids": ids, "async_hints": hint, "action": action}
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    print("== 异步受理裁定器 ==")
    print("status      : %s" % status)
    print("业务 ID     : %s" % (ids if ids else "(无)"))
    print("异步提示词  : %s" % (hint if hint else "(无)"))
    print("裁定        : [%s] %s" % (level, v))
    print("下一步      : %s" % action)
    print("\n铁律：status:200 + 业务 ID + 「已受理/未完成」= 成功受理；")
    print("      终态必须另查；把受理读成失败 = 「假失败」，把受理读成完成 = 「假成功」。")
    return 0


# ---------------------------------------------------------------- 子命令：cloud5

CLOUD5 = [
    ("L1 配置解析", "yaml/配置是否被正确解析、分支触发是否命中",
     "看流水线首屏是否出现预期的 job/service 列表；解析失败=根本没跑"),
    ("L2 runner 分配", "是否分到机器/标签是否匹配（如 cnb:arch:amd64:gpu）",
     "看环境规格回显（核数/显存）；分到 ≠ 能用"),
    ("L3 services 启动", "依赖容器/服务是否全部起来",
     "逐个 service 看日志；一个起不来整条停"),
    ("L4 配额预冻结", "平台按 5min 粒度预冻结额度，不足直接终止",
     "看是否出现 quota/core-hours/insufficient；**这一层最常见的假象是「配置写错」**"),
    ("L5 stages 执行", "业务步骤本身",
     "只有走到这层，才该去改脚本/改命令"),
]


def cmd_cloud5(args):
    if args.json:
        print(json.dumps({"layers": [{"name": a, "what": b, "how": c} for a, b, c in CLOUD5]},
                         ensure_ascii=False, indent=2))
        return 0
    print("== 云平台失败五层定位（出错先分层，别急着改配置）==")
    for i, (n, w, h) in enumerate(CLOUD5, 1):
        print("\n%d) %s" % (i, n))
        print("   看什么：%s" % w)
        print("   怎么判：%s" % h)
    print("\n典型误判：L4 配额预冻结被拒 -> 报错像「环境起不来」-> 以为是 L1 配置错 -> 越改越错。")
    print("CNB 口径：GPU 0 核时/月免费，¥0.5/核时 x16核 = 8.0元/小时；CPU 1600 核时/月免费（联调走这条）。")
    return 0


# ---------------------------------------------------------------- selftest

def cmd_selftest(_a):
    cases = [
        ("异步受理（CNB start-workspace 真样本）",
         '{"status": 200, "sn": "cnb-abc123", "message": "cnb received, but didn\'t finish build yet"}',
         "ACCEPTED"),
        ("假成功（说 success 但无 ID）",
         '{"status": 200, "message": "success"}', "SUSPECT_FAKE_SUCCESS"),
        ("真失败（403 scope）",
         '{"status": 403, "errmsg": "Missing required scopes: account-profile:r"}', "FAILED"),
        ("完成态（带 ID 无异步词）",
         '{"status": 200, "build_id": "b-9f2", "state": "success"}', "DONE_OR_ACCEPTED"),
    ]
    ok = 0
    print("== 四场景离线自检（不联网）==")
    for name, payload, expect in cases:
        sys.argv_backup = sys.argv
        sys.argv = ["cred_triage.py", "verdict", "--text", payload, "--json"]
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            ap = build_parser()
            a2 = ap.parse_args(["verdict", "--text", payload, "--json"])
            cmd_verdict(a2)
        finally:
            sys.stdout = old
            sys.argv = sys.argv_backup
        try:
            got = json.loads(buf.getvalue())["verdict"]
        except Exception:
            got = "?"
        hit = expect in got
        ok += 1 if hit else 0
        print("%-38s expect=%-22s got=%-28s %s" % (name, expect, got, "PASS" if hit else "FAIL"))
    print("\n结果：%d/%d 通过" % (ok, len(cases)))
    return 0 if ok == len(cases) else 1


# ---------------------------------------------------------------- main

def build_parser():
    p = argparse.ArgumentParser(description="龙虾凭据分层与云端故障分层诊断守卫 v%s" % VERSION)
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("layers", help="凭据来源分层盘点")
    a.add_argument("--tool", default="cnb", choices=list(TOOLS))
    a.add_argument("--json", action="store_true")
    a.set_defaults(func=cmd_layers)
    b = sub.add_parser("probe", help="逐层摘除法身份探针")
    b.add_argument("--tool", default="cnb", choices=[k for k in IDENTITY])
    b.add_argument("--json", action="store_true")
    b.set_defaults(func=cmd_probe)
    c = sub.add_parser("verdict", help="异步受理裁定")
    c.add_argument("--file")
    c.add_argument("--text")
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_verdict)
    d = sub.add_parser("cloud5", help="云平台五层定位清单")
    d.add_argument("--json", action="store_true")
    d.set_defaults(func=cmd_cloud5)
    e = sub.add_parser("selftest", help="离线自检")
    e.set_defaults(func=cmd_selftest)
    return p


def main():
    ap = build_parser()
    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
