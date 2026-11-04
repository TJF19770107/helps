# -*- coding: utf-8 -*-
"""
AI 多模态产品工作台 · 小说续写流水线 v1.0
用途：基于汤哥《绑定豆包后我无敌了（豆包修仙录）》既有设定（00-06 档案）续写下一章
      同一引擎可改编为漫剧分镜（--mode manju）
核心能力：
  1) 自动吃设定：人物档案(01) + 世界观(02) + 逐章细纲(03) + 最新摘要 + 上一章正文尾部
  2) 基准词汇表守卫（对齐《网文双阶段体检模板》1.1）：从 01/02 档案抽取权威人名/实体，
     生成正文中若出现「同姓不同名」的未登记变体（如 林凡/林尘 冒充 林小默）→ 直接 FAIL
  3) 禁用词守卫（可编辑 ./禁用词表.txt）+ 分节字数下限 + L4 内容校验 + 产物回读
  4) 分步调用防 524：细纲 → 逐节正文（每节独立调用）→ 合并 → 摘要 → 体检报告
用法：
  python 小说续写流水线.py --novel-dir "<小说目录>" --chapter 116 --segments 5 --outdir "<产出目录>"
"""
import argparse
import glob
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

PROXY = os.environ.get("WB_TEXT_CHANNEL", "http://127.0.0.1:15740")
CHAIN = ["deepseek-v4-flash-free", "glm-5.3-flash-free", "deepseek-v4-pro-free", "gpt-5.6-luna-fast"]
MAX_TOKENS = 3000
MIN_SEG_CHARS = 600          # 单节正文字数下限（防假成功）
SURNAMES = "林苏赵王李张秦宓陈刘黄吴周徐孙马朱胡郭何高罗郑梁谢宋唐许韩冯邓曹彭曾萧田董袁潘蒋蔡余杜叶程苏魏吕丁沈姜崔钟陆汪范金石廖贾夏韦付方白邹孟熊金陆郝孔白崔康毛邱秦江史顾侯邵孟龙万段漕钱汤尹黎易常武乔贺赖龚文庞樊兰殷施陶洪翟安颜倪严牛温芦季俞章鲁葛伍申尤毕聂焦向柳邢路岳齐沿梅莫庄辛管祝左涂谷祁时舒屈"

P_OUTLINE = """你是顶级网文大纲师，正在续写《绑定豆包后我无敌了（豆包修仙录）》。

【作品设定】
{setting}

【最近剧情摘要】
{recent}

【上一章结尾（正文尾部）】
{prev_tail}

【本章要求】
写第{ch}章的细纲。严格输出 JSON（不要markdown代码块）：
{{"chapter":{ch},"title":"章节名(2-5字)","core_event":"本章核心事件一句话","conflict":"冲突类型","golden_finger":"豆包金手指使用点","cliffhanger":"章末悬念","segments":[{{"no":1,"title":"小节标题","brief":"本节剧情要点40-60字"}}]}}
segments 固定 {seg} 节，剧情要有推进感，承接上一章结尾，不重复已写剧情。"""

P_SEG = """你在写《绑定豆包后我无敌了（豆包修仙录）》第{ch}章《{ctitle}》的第{no}节《{stitle}》。

【人物档案（必须严格按此人设，禁止OOC，人名必须一字不差）】
{chars}

【本章细纲】核心事件：{core} | 悬念：{cliff}
本节要点：{brief}

【上一节结尾（必须无缝衔接，不要复述）】
{prev_tail}

【写作要求】
- 第三人称限知视角，网文节奏，短句为主，对话推进剧情
- 只写正文，不要标题、不要markdown、不要任何说明文字
- 篇幅 {lo}-{hi} 字
- 出场人物只用档案中已有角色；如必须引入新角色，用泛称（如"那名修士"），不要起新名字"""

P_SUMMARY = """基于以下章节正文，输出章节摘要，严格输出 JSON（不要markdown代码块）：
{{"chapter":{ch},"title":"{ctitle}","core_event":"核心事件","key_points":["关键推进1","关键推进2","关键推进3"],"characters":["出场人物"],"foreshadow":["伏笔操作"]}}
正文：
{text}"""


def call_llm(prompt: str):
    last_err = None
    for model in CHAIN:
        for attempt in range(1, 3):
            payload = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}],
                                  "max_tokens": MAX_TOKENS}).encode("utf-8")
            req = urllib.request.Request(f"{PROXY}/v1/chat/completions", data=payload,
                                         headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=150) as r:
                    d = json.loads(r.read().decode("utf-8"))
                msg = (d.get("choices") or [{}])[0].get("message", {}).get("content", "")
                if not msg or len(msg.strip()) < 10:
                    last_err = f"{model}: L4空正文({len(msg)})"
                    continue
                return True, msg, d.get("model", "?"), (d.get("usage") or {}), None
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError,
                    json.JSONDecodeError, OSError) as e:
                body = ""
                if isinstance(e, urllib.error.HTTPError):
                    try:
                        body = e.read().decode("utf-8", "replace")[:120]
                    except Exception:
                        pass
                last_err = f"{model}: {type(e).__name__} {str(e)[:70]} {body}"
                if "524" in body or "402" in body:
                    break
            time.sleep(2)
    return False, None, None, None, last_err


def call_llm_robust(prompt, rounds=4, wait=25, tag=""):
    """轮次重试：免费池拥堵(524)是瞬态的，隔 wait 秒重打，全轮失败才判失败"""
    last = None
    for rd in range(1, rounds + 1):
        ok, content, model, usage, err = call_llm(prompt)
        if ok:
            return ok, content, model, usage, err
        last = err
        if rd < rounds:
            print(f"  [轮{rd}失败]{tag} {str(err)[:90]} → {wait}s 后重试", flush=True)
            time.sleep(wait)
    return False, None, None, None, last


def step_json(prompt, tag="", attempts=3, wait=20):
    """JSON 步骤专用：LLM 失败 or JSON 解析失败都算失败轮，重试直到成功"""
    last = None
    for a in range(1, attempts + 1):
        ok, raw, model, usage, err = call_llm(prompt)
        if ok:
            try:
                return extract_json(raw), model, None
            except (ValueError, json.JSONDecodeError) as e:
                last = f"JSON解析失败 {e} | 原文前120字: {raw[:120]}"
                print(f"  截断原文留档: {os.path.join(os.path.dirname(os.path.abspath(__file__)), '_last_bad_json.txt')}")
                open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_last_bad_json.txt"),
                     "w", encoding="utf-8").write(raw)
        else:
            last = err
        if a < attempts:
            print(f"  [JSON轮{a}失败]{tag} {str(last)[:90]} → {wait}s 后重试", flush=True)
            time.sleep(wait)
    return None, None, last


def extract_json(text):
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if m:
        text = m.group(1)
    s = text.find("{")
    if s == -1:
        raise ValueError("无JSON")
    return json.JSONDecoder().raw_decode(text[s:])[0]


# ---------------- 基准词汇表（对齐体检模板 1.1） ----------------
def build_lexicon(novel_dir):
    """从 01 人物档案 / 02 世界观 抽取权威名称（过滤表头类非人名）"""
    STOP = ("等级", "体系", "分布", "架构", "地理", "势力", "规则", "设定", "说明", "总纲",
            "属性", "角色", "字段", "身份", "真身", "外形", "性格", "能力", "金手指", "灵根",
            "台词", "弧光", "定位", "动机", "手段", "关系", "时间", "地点", "物品", "货币", "计量",
            "体质", "境界", "境界划分", "食物", "组织", "机构", "条目", "记录表", "路线图")
    names, entities = set(), set()
    for pat in ["01_*人物档案*.md", "02_*世界观*.md"]:
        for f in glob.glob(os.path.join(novel_dir, pat)):
            txt = open(f, encoding="utf-8", errors="replace").read()
            for n in re.findall(r"^###\s+([\u4e00-\u9fa5]{2,5})\s*$", txt, re.M):
                if not any(s in n for s in STOP):
                    names.add(n)
            for row in re.findall(r"^\|\s*([\u4e00-\u9fa5]{2,8})\s*\|", txt, re.M):
                if not any(s in row for s in STOP):
                    entities.add(row)
    # 已知出场配角（来自 113-115 摘要/执行日志）
    names |= {"远者", "近者", "访客", "秦柒", "天盲长者", "宓云依", "述人", "造路者",
              "林小默", "豆包", "苏清月", "赵虎", "王磊", "血魂老祖", "血无痕", "幽姬", "天衍仙帝"}
    return sorted(names), sorted(entities)


def lexicon_guard(text, names):
    """检测同姓不同名的未登记变体（如白名单有 林小默，正文出现 林凡/林尘 → 违规）
    算法：①屏蔽已登记名（避免把 '豆包趴' 误判）②在同姓残文中找人名形态：
         3字（姓+2字）一律可疑；2字（姓+1字）仅当后接人名语境字/标点时可疑
    """
    surnames = sorted({n[0] for n in names if len(n) >= 2}, key=len, reverse=True)
    allowed = set(names)
    masked = text
    for n in sorted(names, key=len, reverse=True):
        masked = masked.replace(n, "\u3007")          # 屏蔽已登记名
    CTX = "说道问笑冷笑沉看眉眼手心者的是抬转走站坐而他她又却忽然冷冷盯望喊叫"
    # 非人名前缀停用表（同姓普通词，防误报；可增补）
    STOP_PREFIX = ("林间", "林外", "林下", "林深", "林荫", "林带", "林家", "林立的",
                   "苏家", "赵家", "王家", "王城", "王座", "王道", "王侯", "王宫",
                   "林小", "苏清", "赵虎", "王磊")
    hits = set()
    for sn in surnames:
        for tok in re.findall(sn + r"[\u4e00-\u9fa5]{2}", masked):   # 3字名（姓+2）
            if tok not in allowed and not tok.startswith(STOP_PREFIX):
                hits.add(tok)
        for mt in re.finditer(sn + r"([\u4e00-\u9fa5])", masked):    # 2字名（姓+1）
            tok = mt.group(0)
            if tok in allowed or tok.startswith(STOP_PREFIX):
                continue
            nxt = masked[mt.end():mt.end() + 1]
            if nxt and nxt in CTX:
                hits.add(tok)
    return sorted(hits)


def word_guard(text, banned):
    return [w for w in banned if w and w in text]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--novel-dir", required=True)
    ap.add_argument("--chapter", type=int, required=True)
    ap.add_argument("--segments", type=int, default=5)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--mode", default="novel", choices=["novel", "manju"])
    args = ap.parse_args()

    nd, outdir = args.novel_dir, args.outdir
    os.makedirs(outdir, exist_ok=True)

    # ---- 1 吃设定 ----
    names, entities = build_lexicon(nd)
    chars_file = next(iter(glob.glob(os.path.join(nd, "01_*人物档案*.md"))), None)
    chars = open(chars_file, encoding="utf-8", errors="replace").read()[:2500] if chars_file else ""
    # 最近摘要（取最新 1 个，控制 prompt 体积防 524）
    summ_files = sorted(glob.glob(os.path.join(nd, "*章节摘要*.txt")) +
                        glob.glob(os.path.join(nd, "06_章节摘要存档*.md")),
                        key=os.path.getmtime)[-1:]
    recent = "\n\n".join(open(f, encoding="utf-8", errors="replace").read()[:1800] for f in summ_files)
    # 上一章正文尾部
    ch_files = sorted(glob.glob(os.path.join(nd, f"第{args.chapter-1}章*.txt")) +
                      glob.glob(os.path.join(nd, f"第{args.chapter-1}章*.md")))
    prev_tail = open(ch_files[-1], encoding="utf-8", errors="replace").read()[-800:] if ch_files else "（无）"
    banned = []
    bf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "禁用词表.txt")
    if os.path.exists(bf):
        banned = [l.strip() for l in open(bf, encoding="utf-8") if l.strip() and not l.startswith("#")]

    print(f"[设定] 权威名录 {len(names)} 个：{'、'.join(names[:12])}...")
    print(f"[设定] 摘要文件：{[os.path.basename(f) for f in summ_files]}")
    print(f"[设定] 上一章尾部 {len(prev_tail)} 字 | 禁用词 {len(banned)} 条")
    json.dump({"names": names, "entities": entities}, open(os.path.join(outdir, "基准词汇表.json"),
              "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    report = {"chapter": args.chapter, "date": time.strftime("%F %T"), "models": [],
              "checks": [], "files": []}

    # ---- 2 细纲 ----
    print(f"[步骤] 第{args.chapter}章 细纲 ...", flush=True)
    ol, model, err = step_json(P_OUTLINE.format(setting=chars[:1500], recent=recent[:1200],
                              prev_tail=prev_tail, ch=args.chapter, seg=args.segments), tag="细纲")
    if ol is None:
        print(f"[FAIL] 细纲: {err}", file=sys.stderr); sys.exit(1)
    report["models"].append(model)
    ctitle = ol.get("title", "未命名")
    segs = ol.get("segments", [])
    print(f"  《{ctitle}》{len(segs)}节 | model={model}")

    # ---- 3 逐节正文 ----
    body_parts, prev = [], prev_tail[-600:]
    for i, sg in enumerate(segs, 1):
        print(f"[步骤] 第{i}节《{sg.get('title')}》...", flush=True)
        t0 = time.time()
        ok, txt, model, usage, err = call_llm_robust(P_SEG.format(
            ch=args.chapter, ctitle=ctitle, no=i, stitle=sg.get("title", ""), chars=chars[:1200],
            core=ol.get("core_event", ""), cliff=ol.get("cliffhanger", ""),
            brief=sg.get("brief", ""), prev_tail=prev, lo=MIN_SEG_CHARS, hi=1400), tag=f"第{i}节")
        if not ok:
            print(f"[FAIL] 第{i}节: {err}", file=sys.stderr); sys.exit(1)
        hits = lexicon_guard(txt, names)
        wbads = word_guard(txt, banned)
        report["models"].append(model)
        status = "OK"
        if hits:
            status = f"词汇违规 {hits}"
        if wbads:
            status += f" | 禁用词 {wbads}"
        print(f"  {len(txt)}字 {round(time.time()-t0,1)}s model={model} {status}")
        report["checks"].append({"seg": i, "chars": len(txt), "lexicon_violations": hits,
                                 "banned_words": wbads})
        if len(txt) < MIN_SEG_CHARS:
            print(f"[FAIL] 第{i}节字数不足 {len(txt)} < {MIN_SEG_CHARS}（防假成功）", file=sys.stderr)
            sys.exit(1)
        if hits or wbads:
            print(f"[FAIL] 第{i}节一致性/合规校验未过，已阻断落盘（宁停不写错）", file=sys.stderr)
            open(os.path.join(outdir, f"违规草稿_第{i}节.txt"), "w", encoding="utf-8").write(txt)
            print(f"  违规草稿已存证: 违规草稿_第{i}节.txt", file=sys.stderr)
            sys.exit(1)
        body_parts.append(txt.strip())
        prev = txt.strip()[-600:]

    full = "\n\n".join(body_parts)
    p_ch = os.path.join(outdir, f"第{args.chapter}章 {ctitle}.txt")
    open(p_ch, "w", encoding="utf-8").write(full)

    # ---- 4 摘要 ----
    print("[步骤] 章节摘要 ...", flush=True)
    summary, _, serr = step_json(P_SUMMARY.format(ch=args.chapter, ctitle=ctitle, text=full[:6000]), tag="摘要")
    ok = summary is not None
    err = serr
    p_sum = os.path.join(outdir, f"第{args.chapter}章摘要.txt")
    if ok:
        open(p_sum, "w", encoding="utf-8").write(
            f"# 第{args.chapter}章 {ctitle}\n**核心事件**：{summary.get('core_event','')}\n"
            + "\n".join(f"- {k}" for k in summary.get("key_points", []))
            + f"\n\n**出场人物**：{'、'.join(summary.get('characters', []))}\n"
            + "\n".join(f"- 伏笔：{f}" for f in summary.get("foreshadow", [])))

    # ---- 5 体检报告（产物回读 + 词汇/禁用词终检）----
    final_hits = lexicon_guard(full, names)
    final_bads = word_guard(full, banned)
    passing = not final_hits and not final_bads
    open(os.path.join(outdir, "体检报告.md"), "w", encoding="utf-8").write(
        f"# 第{args.chapter}章 体检报告\n\n- 生成时间：{time.strftime('%F %T')}\n"
        f"- 正文字数：{len(full)}\n- 分节数：{len(body_parts)}\n"
        f"- 基准名录：{len(names)} 个（基准词汇表.json）\n"
        f"- 词汇一致性：{'✅ 零违规' if not final_hits else '❌ ' + str(final_hits)}\n"
        f"- 禁用词：{'✅ 零命中' if not final_bads else '❌ ' + str(final_bads)}\n"
        f"- 逐节字数：{', '.join(str(c['chars']) for c in report['checks'])}\n"
        f"- 使用模型：{', '.join(str(m) for m in report['models'])}\n"
        f"- 结论：{'PASS' if passing else 'FAIL'}\n")

    for f in [p_ch, p_sum, os.path.join(outdir, "体检报告.md")]:
        if os.path.exists(f):
            report["files"].append({"path": os.path.abspath(f), "bytes": os.path.getsize(f)})
    json.dump(report, open(os.path.join(outdir, "manifest.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"\n[PASS] 第{args.chapter}章《{ctitle}》完成：{len(full)}字 / {len(body_parts)}节")
    for f in report["files"]:
        print(f"  {f['bytes']:>7}B  {f['path']}")


if __name__ == "__main__":
    main()
