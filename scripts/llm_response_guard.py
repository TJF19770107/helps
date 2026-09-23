#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
龙虾 LLM 响应守卫 v1.0  (llm_response_guard.py)
================================================
专治「假成功」第 38 形态（判定层错配在 LLM 调用面上的投影）:
    L3 传输层全绿(HTTP 200 / rc=0 / JSON 合法)，L4 内容层却是空的或严重缩水。

2026-09-24 本机实测硬证据(TeamoRouter 18091, deepseek-v4-flash-free):
    max_tokens=16  -> HTTP200, content="", reasoning_tokens=16, finish_reason=length
    max_tokens=64  -> HTTP200, content=51字, reasoning_tokens=2918, completion=2949 (超发 46x)
    max_tokens=300 -> HTTP200, content=83字, reasoning_tokens=6754, completion=6802 (超发 22.7x)
    且 resp_model = deepseek-v4-flash-0731 / -ga-260731 ≠ 请求的 -free (model 漂移)

七类反模式:
    V1 EMPTY_CONTENT     HTTP200 但 content 为空(推理吃光预算)          -> CRIT
    V2 TRUNCATED         finish_reason=length 正文被腰斩                 -> WARN
    V3 REASONING_OVERRUN reasoning_tokens 相对请求预算超发 N 倍          -> CRIT/WARN
    V4 MODEL_DRIFT       resp_model ≠ req_model (子版本漂移/家族跳档)     -> WARN/CRIT
    V5 USAGE_MISSING     usage 缺失或 completion_tokens=0 (计费不可信)    -> WARN
    V6 NON_JSON_200      HTTP200 但 body 非 JSON(网关 HTML 伪装页)       -> CRIT
    V7 MOJIBAKE          正文含大量替换符/纯 \\uXXXX 转义(编码错层)        -> WARN

防误报设计(第 11 形态:守卫自己造假失败 —— 必含豁免):
    · content 空但存在 tool_calls          -> 合法,降级 INFO
    · resp_model 是 req_model 的前缀延伸    -> 子版本漂移,只 WARN 不 CRIT
    · finish_reason=length 但正文已达期望下限 -> 可配 --min-content 后免报
    · 非推理模型(usage 无 reasoning_tokens) -> 不套 V3

零积分:纯 stdlib,不发请求也可 audit 离线响应文件。
"""
import argparse, json, os, re, sys, time, urllib.request, urllib.error

VERSION = "1.0.0"

CRIT, WARN, INFO, OK = "CRIT", "WARN", "INFO", "OK"
_SEV_ORDER = {OK: 0, INFO: 1, WARN: 2, CRIT: 3}

# 已知「免费 slug -> 可能静默落到的别名族」。命中同族只 WARN，跳出同族才 CRIT。
FREE_FAMILY = ("free", "flash-free", "pro-free", "lite-free")
# 已知收费档特征(命中即 CRIT，因为免费请求落到收费 = 静默烧钱)
PAID_HINT = ("glm-5.3-flash", "gpt-5.4", "gpt-5.5", "paid", "pro-", "-turbo", "4o")


def _sev_max(items):
    s = OK
    for it in items:
        if _SEV_ORDER.get(it.get("sev", OK), 0) > _SEV_ORDER[s]:
            s = it["sev"]
    return s


def _mk(code, sev, msg, evidence=None):
    return {"code": code, "sev": sev, "msg": msg, "evidence": evidence or {}}


def _norm_model(m):
    return (m or "").strip().lower()


def _is_same_family(req, resp):
    """同族判定：去后缀后前缀相同，或 resp 以 req 主干开头。"""
    r, p = _norm_model(req), _norm_model(resp)
    if not r or not p:
        return False
    if r == p:
        return True
    # 主干 = 去掉 -free / -NNNN / -ga-xxxx 等尾部标记
    trunk = re.sub(r"(-free|-lite|-pro|-ga|-\d{3,8})+$", "", r)
    if trunk and p.startswith(trunk):
        return True
    if p.startswith(r):
        return True
    return False


def _looks_paid(model):
    m = _norm_model(model)
    return any(h in m for h in PAID_HINT)


def judge(resp_json, req_model=None, req_max_tokens=None, min_content=1,
          overrun_crit=10.0, overrun_warn=3.0, http_code=200, raw_text=None,
          elapsed=None):
    """核心判定：输入 OpenAI 兼容响应 dict，输出 findings 列表 + 总评。"""
    f = []

    # ---- V6: 非 JSON / 伪装页 ----
    if resp_json is None:
        head = (raw_text or "")[:120]
        return [_mk("V6_NON_JSON_200", CRIT,
                    "HTTP %s 但响应体不是合法 JSON，疑似网关伪装页/HTML 错误页" % http_code,
                    {"raw_head": head})], CRIT

    choices = resp_json.get("choices") or []
    if not choices:
        f.append(_mk("V0_NO_CHOICE", CRIT, "choices 为空，无任何候选输出", {}))
        return f, CRIT

    ch = choices[0]
    msg = ch.get("message") or {}
    content = msg.get("content")
    content = content if isinstance(content, str) else (
        "" if content is None else json.dumps(content, ensure_ascii=False))
    tool_calls = msg.get("tool_calls") or []
    finish = ch.get("finish_reason")

    # 各家 reasoning 字段命名不一
    reasoning = ""
    for k in ("reasoning_content", "reasoning", "reasoning_text", "thinking"):
        v = msg.get(k)
        if v:
            reasoning = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
            break

    usage = resp_json.get("usage") or {}
    ctok = usage.get("completion_tokens")
    ptok = usage.get("prompt_tokens")
    det = usage.get("completion_tokens_details") or {}
    rtok = det.get("reasoning_tokens")
    if rtok is None:
        rtok = usage.get("reasoning_tokens")

    ev = {
        "http": http_code,
        "content_len": len(content),
        "content_head": content[:80],
        "reasoning_len": len(reasoning),
        "finish_reason": finish,
        "req_model": req_model,
        "resp_model": resp_json.get("model"),
        "completion_tokens": ctok,
        "reasoning_tokens": rtok,
        "prompt_tokens": ptok,
        "elapsed": elapsed,
    }

    # ---- V1: 空正文 ----
    if len(content.strip()) == 0:
        if tool_calls:
            f.append(_mk("V1_EMPTY_CONTENT", INFO,
                         "content 为空但存在 tool_calls（函数调用场景合法），不判失败",
                         {"tool_calls": len(tool_calls)}))
        else:
            f.append(_mk("V1_EMPTY_CONTENT", CRIT,
                         "HTTP %s 但 content 为空 —— L3 绿 / L4 空，典型假成功" % http_code,
                         {"reasoning_tokens": rtok,
                          "hint": "免费池多为推理模型，max_tokens 过小会被 reasoning_tokens 吃光"}))
    elif min_content and len(content.strip()) < min_content:
        f.append(_mk("V1_SHORT_CONTENT", WARN,
                     "正文 %d 字，低于期望下限 %d" % (len(content.strip()), min_content),
                     {"content_len": len(content.strip())}))

    # ---- V2: 截断 ----
    if finish == "length":
        f.append(_mk("V2_TRUNCATED", WARN,
                     "finish_reason=length，输出被 max_tokens 腰斩，内容不可用",
                     {"finish_reason": finish, "content_len": len(content)}))
    elif finish == "content_filter":
        f.append(_mk("V2_FILTERED", CRIT, "finish_reason=content_filter，内容被安全策略拦截", {}))

    # ---- V3: reasoning 超发（成本黑洞）----
    if rtok:
        base = req_max_tokens if req_max_tokens else (ctok or 0)
        if req_max_tokens and req_max_tokens > 0:
            ratio = rtok / float(req_max_tokens)
            if ratio >= overrun_crit:
                f.append(_mk("V3_REASONING_OVERRUN", CRIT,
                             "reasoning_tokens=%d 是请求预算 %d 的 %.1f 倍 —— 额度被静默烧穿"
                             % (rtok, req_max_tokens, ratio),
                             {"ratio": round(ratio, 2), "reasoning_tokens": rtok,
                              "req_max_tokens": req_max_tokens}))
            elif ratio >= overrun_warn:
                f.append(_mk("V3_REASONING_OVERRUN", WARN,
                             "reasoning_tokens=%d 为请求预算的 %.1f 倍，成本预期失真"
                             % (rtok, ratio), {"ratio": round(ratio, 2)}))
        if ctok and rtok >= ctok * 0.95:
            f.append(_mk("V3_REASONING_DOMINANT", WARN,
                         "推理占输出 %.0f%%（%d/%d），正文只占零头，max_tokens 不是真实成本上限"
                         % (100.0 * rtok / ctok, rtok, ctok),
                         {"reasoning_tokens": rtok, "completion_tokens": ctok}))

    # ---- V4: model 漂移 ----
    rm = req_model
    pm = resp_json.get("model")
    if rm and pm:
        if not _is_same_family(rm, pm):
            sev = CRIT if (any(x in _norm_model(rm) for x in FREE_FAMILY) and _looks_paid(pm)) else WARN
            f.append(_mk("V4_MODEL_DRIFT", sev,
                         "请求 %s 实际返回 %s —— 模型被静默替换" % (rm, pm),
                         {"req_model": rm, "resp_model": pm,
                          "paid_risk": _looks_paid(pm)}))
        elif _norm_model(rm) != _norm_model(pm):
            f.append(_mk("V4_MODEL_SUBVERSION", WARN,
                         "返回 %s 是请求 %s 的子版本变体（同族，通常无害但需留证）" % (pm, rm),
                         {"req_model": rm, "resp_model": pm}))

    # ---- V5: usage 缺失 ----
    if not usage:
        f.append(_mk("V5_USAGE_MISSING", WARN, "响应无 usage 字段，无法核算成本", {}))
    elif ctok == 0 and len(content) > 0:
        f.append(_mk("V5_USAGE_ZERO", WARN,
                     "completion_tokens=0 但正文非空，计费口径不可信", {"completion_tokens": ctok}))

    # ---- V7: 乱码 / 转义错层 ----
    if content:
        repl = content.count("\ufffd")
        esc = len(re.findall(r"\\u[0-9a-fA-F]{4}", content))
        cn = len(re.findall(r"[\u4e00-\u9fff]", content))
        if repl >= 3:
            f.append(_mk("V7_MOJIBAKE", WARN, "正文含 %d 个替换符，编码错层" % repl, {"repl": repl}))
        elif esc > 0 and cn == 0 and len(content) > 20:
            f.append(_mk("V7_ESCAPED", WARN,
                         "正文是纯 \\uXXXX 转义串（%d 处），未解码就落盘会变成天书" % esc, {"esc": esc}))

    return f, _sev_max(f) if f else OK


# ---------------------------------------------------------------- HTTP
def http_call(base, key, model, prompt, max_tokens, timeout=120, extra=None):
    url = base.rstrip("/") + "/chat/completions"
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens}
    if extra:
        body.update(extra)
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer " + (key or "")})
    op = urllib.request.build_opener(urllib.request.ProxyHandler({}))  # 本机地址不走代理
    t = time.time()
    try:
        r = op.open(req, timeout=timeout)
        raw, code = r.read().decode("utf-8", "replace"), r.status
    except urllib.error.HTTPError as e:
        raw, code = e.read().decode("utf-8", "replace"), e.code
    except Exception as e:
        return None, {"fatal": repr(e)}, None, round(time.time() - t, 1)
    el = round(time.time() - t, 1)
    try:
        j = json.loads(raw)
    except Exception:
        j = None
    return j, {"http": code, "raw_head": raw[:200]}, code, el


def render(findings, verdict, ev, as_json=False, title=""):
    if as_json:
        return json.dumps({"title": title, "verdict": verdict, "findings": findings,
                           "evidence": ev}, ensure_ascii=False, indent=2)
    icon = {CRIT: "[CRIT]", WARN: "[WARN]", INFO: "[INFO]", OK: "[ OK ]"}
    lines = []
    if title:
        lines.append("== %s ==" % title)
    lines.append("VERDICT: %s" % verdict)
    if ev:
        lines.append("EVIDENCE: " + json.dumps({k: v for k, v in ev.items() if v is not None},
                                               ensure_ascii=False))
    if not findings:
        lines.append("  无异常（L4 内容层校验通过）")
    for x in findings:
        lines.append("  %s %-22s %s" % (icon.get(x["sev"], "[ ? ]"), x["code"], x["msg"]))
    return "\n".join(lines)


# ---------------------------------------------------------------- selftest
def _case(name, resp, req_model=None, req_mt=None, expect_codes=None, expect_verdict=None,
          min_content=1):
    """expect_codes: 必须命中的 code 集合；expect_verdict: 期望总评。"""
    f, v = judge(resp, req_model, req_mt, min_content=min_content)
    got = {x["code"] for x in f}
    ok = True
    detail = []
    if expect_codes is not None:
        if not set(expect_codes).issubset(got):
            ok = False
            detail.append("missing=%s" % sorted(set(expect_codes) - got))
    if expect_verdict is not None and v != expect_verdict:
        ok = False
        detail.append("verdict=%s want=%s" % (v, expect_verdict))
    return ok, name, v, sorted(got), ";".join(detail)


def selftest():
    cases = []

    # --- 真·故障用例（必须抓到）---
    cases.append(_case(
        "T01 实测#1: HTTP200 content空(推理吃光)",
        {"choices": [{"message": {"content": "", "reasoning_content": "让我想想"},
                      "finish_reason": "length"}],
         "model": "deepseek-v4-flash-0731",
         "usage": {"completion_tokens": 16, "prompt_tokens": 92,
                   "completion_tokens_details": {"reasoning_tokens": 16}}},
        "deepseek-v4-flash-free", 16,
        expect_codes=["V1_EMPTY_CONTENT", "V2_TRUNCATED"], expect_verdict=CRIT))

    cases.append(_case(
        "T02 实测#2: reasoning 超发 46x",
        {"choices": [{"message": {"content": "判定层错配是指…", "reasoning_content": "x" * 9399},
                      "finish_reason": "stop"}],
         "model": "deepseek-v4-flash-ga-260731",
         "usage": {"completion_tokens": 2949, "prompt_tokens": 92,
                   "completion_tokens_details": {"reasoning_tokens": 2918}}},
        "deepseek-v4-flash-free", 64,
        expect_codes=["V3_REASONING_OVERRUN", "V3_REASONING_DOMINANT"], expect_verdict=CRIT))

    cases.append(_case(
        "T03 静默跳到收费档",
        {"choices": [{"message": {"content": "好的"}, "finish_reason": "stop"}],
         "model": "glm-5.3-flash", "usage": {"completion_tokens": 5}},
        "deepseek-v4-flash-free", 500,
        expect_codes=["V4_MODEL_DRIFT"], expect_verdict=CRIT))

    cases.append(_case(
        "T04 网关 HTML 伪装页(HTTP200 非JSON)",
        None, "deepseek-v4-flash-free", 100,
        expect_codes=["V6_NON_JSON_200"], expect_verdict=CRIT))

    cases.append(_case(
        "T05 choices 为空",
        {"choices": [], "model": "x"}, "x", 100,
        expect_codes=["V0_NO_CHOICE"], expect_verdict=CRIT))

    cases.append(_case(
        "T06 正文纯 \\uXXXX 未解码",
        {"choices": [{"message": {"content": "\\u5224\\u5b9a\\u5c42\\u9519\\u914d"},
                      "finish_reason": "stop"}], "model": "x",
         "usage": {"completion_tokens": 10}},
        "x", 100, expect_codes=["V7_ESCAPED"], expect_verdict=WARN))

    cases.append(_case(
        "T07 替换符乱码",
        {"choices": [{"message": {"content": "判定\ufffd\ufffd\ufffd层"}, "finish_reason": "stop"}],
         "model": "x", "usage": {"completion_tokens": 8}},
        "x", 100, expect_codes=["V7_MOJIBAKE"], expect_verdict=WARN))

    cases.append(_case(
        "T08 usage 缺失",
        {"choices": [{"message": {"content": "正常回答"}, "finish_reason": "stop"}], "model": "x"},
        "x", 100, expect_codes=["V5_USAGE_MISSING"], expect_verdict=WARN))

    # --- 防误报用例（形态#11：守卫自己造假失败）---
    cases.append(_case(
        "F01 content空但有 tool_calls（合法，不得判 CRIT）",
        {"choices": [{"message": {"content": "", "tool_calls": [{"id": "1", "type": "function"}]},
                      "finish_reason": "tool_calls"}], "model": "x",
         "usage": {"completion_tokens": 8}},
        "x", 100, expect_codes=["V1_EMPTY_CONTENT"], expect_verdict=INFO))

    cases.append(_case(
        "F02 子版本变体同族（只 WARN 不 CRIT）",
        {"choices": [{"message": {"content": "正常回答内容"}, "finish_reason": "stop"}],
         "model": "deepseek-v4-flash-ga-260731",
         "usage": {"completion_tokens": 20, "completion_tokens_details": {"reasoning_tokens": 0}}},
        "deepseek-v4-flash-free", 500,
        expect_codes=["V4_MODEL_SUBVERSION"], expect_verdict=WARN))

    cases.append(_case(
        "F03 完全健康的响应（必须 OK，零告警）",
        {"choices": [{"message": {"content": "这是一段完整正常的中文回答。"},
                      "finish_reason": "stop"}],
         "model": "deepseek-v4-flash-free",
         "usage": {"completion_tokens": 30, "prompt_tokens": 10,
                   "completion_tokens_details": {"reasoning_tokens": 0}}},
        "deepseek-v4-flash-free", 500, expect_verdict=OK))

    cases.append(_case(
        "F04 非推理模型不套 V3（无 reasoning 字段不得报超发）",
        {"choices": [{"message": {"content": "普通模型回答"}, "finish_reason": "stop"}],
         "model": "gpt-5.6-luna-fast",
         "usage": {"completion_tokens": 12, "prompt_tokens": 10}},
        "gpt-5.6-luna-fast", 200, expect_verdict=OK))

    cases.append(_case(
        "F05 小预算但 reasoning 占比低（不得误判超发）",
        {"choices": [{"message": {"content": "短答"}, "finish_reason": "stop"}],
         "model": "x", "usage": {"completion_tokens": 10,
                                 "completion_tokens_details": {"reasoning_tokens": 2}}},
        "x", 100, expect_verdict=OK))

    passed = sum(1 for c in cases if c[0])
    for ok, name, v, got, detail in cases:
        print("  %s %-46s verdict=%-4s codes=%s%s" %
              ("PASS" if ok else "FAIL", name, v,
               ",".join(got) if got else "-", ("  << " + detail) if detail else ""))
    print("\nSELFTEST: %d/%d %s" % (passed, len(cases), "PASS" if passed == len(cases) else "FAIL"))
    return 0 if passed == len(cases) else 1


# ---------------------------------------------------------------- budget
def budget(model, base=None, key=None, probe=False, expect_out=300):
    """推理模型的 max_tokens 预算建议。实测倍数：64->2949(46x) / 300->6802(22.7x)。"""
    print("模型: %s" % model)
    print("实测依据(2026-09-24, deepseek-v4-flash-free @18091):")
    print("  max_tokens=64  -> completion_tokens=2949 (46.1x), 耗时 36.2s")
    print("  max_tokens=300 -> completion_tokens=6802 (22.7x), 耗时 73.6s")
    print("\n建议: 推理模型的 max_tokens 是「输出上限」不是「成本上限」。")
    for mult, tag in ((20, "保守"), (30, "推荐"), (46, "实测上限")):
        print("  %s: 期望正文 %d token -> max_tokens >= %d" % (tag, expect_out, expect_out * mult))
    print("\n铁律:")
    print("  1. 免费额度按自然日刷新， reasoning_tokens 同样计入 -> 超发等于静默烧额度")
    print("  2. 落盘前必须校验 content 非空（V1），否则拿到空串还以为成功")
    print("  3. 必须校验 resp_model == req_model（V4），防静默跳收费档")
    print("  4. max_tokens 越大耗时越长（实测 3.9s/36s/74s），别盲目调大")
    if probe and base:
        print("\n--probe 实测模式：")
        j, meta, code, el = http_call(base, key, model, "说1", 512)
        print("   http=%s elapsed=%ss resp_model=%s" % (code, el, (j or {}).get("model")))
    return 0


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="龙虾 LLM 响应守卫 v%s" % VERSION)
    sub = ap.add_subparsers(dest="cmd")

    c = sub.add_parser("check", help="实发一次请求并做 L4 内容层体检")
    c.add_argument("--base", default="http://127.0.0.1:18091/v1")
    c.add_argument("--key-env", default="TEAMOROUTER_API_KEY")
    c.add_argument("--model", default="deepseek-v4-flash-free")
    c.add_argument("--prompt", default="用一句话说明什么是判定层错配。")
    c.add_argument("--max-tokens", type=int, default=512)
    c.add_argument("--min-content", type=int, default=1)
    c.add_argument("--timeout", type=int, default=120)
    c.add_argument("--json-out", help="把完整响应落盘，便于离线 audit")
    c.add_argument("--json", action="store_true")

    a = sub.add_parser("audit", help="离线判定已保存的响应 JSON（零成本）")
    a.add_argument("--file", required=True)
    a.add_argument("--req-model")
    a.add_argument("--req-max-tokens", type=int)
    a.add_argument("--min-content", type=int, default=1)
    a.add_argument("--json", action="store_true")

    b = sub.add_parser("budget", help="推理模型 max_tokens 预算建议")
    b.add_argument("--model", default="deepseek-v4-flash-free")
    b.add_argument("--expect-out", type=int, default=300)
    b.add_argument("--probe", action="store_true")
    b.add_argument("--base", default="http://127.0.0.1:18091/v1")
    b.add_argument("--key-env", default="TEAMOROUTER_API_KEY")

    sub.add_parser("selftest", help="内置用例自检（含 5 条防误报）")
    sub.add_parser("version")
    args = ap.parse_args()

    if args.cmd == "selftest":
        return selftest()
    if args.cmd == "version":
        print("llm_response_guard v%s" % VERSION)
        return 0
    if args.cmd == "budget":
        return budget(args.model, args.base, os.environ.get(args.key_env),
                      args.probe, args.expect_out)
    if args.cmd == "audit":
        if not os.path.isfile(args.file):
            print("CRIT: 文件不存在 %s" % args.file)
            return 2
        txt = open(args.file, encoding="utf-8", errors="replace").read()
        try:
            j = json.loads(txt)
        except Exception:
            j = None
        f, v = judge(j, args.req_model, args.req_max_tokens, min_content=args.min_content)
        ev = {}
        if j:
            ev = {"resp_model": j.get("model"), "usage": j.get("usage")}
        print(render(f, v, ev, args.json, "audit %s" % os.path.basename(args.file)))
        return 0 if v != CRIT else 1
    if args.cmd == "check":
        key = os.environ.get(args.key_env, "")
        j, meta, code, el = http_call(args.base, key, args.model, args.prompt,
                                      args.max_tokens, args.timeout)
        if j is None and "fatal" in meta:
            print("CRIT: 请求失败 %s" % meta["fatal"])
            return 2
        if args.json_out:
            with open(args.json_out, "w", encoding="utf-8") as fh:
                json.dump(j if j is not None else meta, fh, ensure_ascii=False, indent=2)
        f, v = judge(j, args.model, args.max_tokens, min_content=args.min_content,
                     http_code=code or 200, raw_text=meta.get("raw_head"), elapsed=el)
        ev = {"http": code, "elapsed": el, "req_model": args.model,
              "resp_model": (j or {}).get("model"), "usage": (j or {}).get("usage")}
        print(render(f, v, ev, args.json, "check %s" % args.model))
        return 0 if v != CRIT else 1

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
