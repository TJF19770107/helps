# -*- coding: utf-8 -*-
"""
AI 多模态产品工作台 · 生文流水线 v2（阶段一文字链 · 分步防超时版）
链路：大纲 → 剧本骨架 → 逐分镜展开 → 逐镜生图提示词 → 角色卡
通道：15740 免费池，故障转移 + 0.01折兜底
防假成功（第38形态）：L4 内容校验 / 模型漂移记录 / 产物回读 / 全链失败退出码1
防超时（2026-09-29 实测）：源站 Cloudflare 100s 网关上限 → 复杂长生成必 524，
  故拆成小步调用，每步输出压在 ~3000 tokens 内。
用法：
  python 生文流水线.py --outline "大纲" --outdir 产出目录
  python 生文流水线.py --outline-file 大纲.md --outdir 产出目录
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

PROXY = os.environ.get("WB_TEXT_CHANNEL", "http://127.0.0.1:15740")
CHAIN = ["deepseek-v4-flash-free", "glm-5.3-flash-free", "deepseek-v4-pro-free",
         "gpt-5.6-luna-fast"]  # 末位0.01折兜底
MAX_TOKENS = 3000
RETRIES = 2  # 每模型重试次数（免费池拥堵瞬态常见）

P_SKELETON = """你是短剧编剧。基于大纲产出剧本骨架，严格输出 JSON（不要markdown代码块）：
{{"title":"作品名","genre":"类型","logline":"一句话故事","characters":["角色名1","角色名2"],"scene_titles":["分镜1标题(10字内)","分镜2标题","分镜3标题","分镜4标题","分镜5标题"]}}
只给骨架，不要展开剧情。大纲：{outline}"""

P_SCENE = """你是短剧编剧。为分镜写详细内容，严格输出 JSON（不要markdown代码块）：
{{"scene_no":{no},"location":"地点","time":"时间","action":"画面动作描述60-90字,具体可视化","dialogue":["角色名:台词","角色名:台词"],"duration_sec":8,"mood":"氛围"}}
作品《{title}》类型{genre}。本分镜标题：{st}。前后分镜标题：{ctx}。"""

P_BOARD = """你是AI绘画提示词工程师。为这个分镜写文生图提示词，严格输出 JSON（不要markdown代码块）：
{{"scene_no":{no},"positive_prompt":"英文提示词: subject+action+scene+lighting+style+quality","negative_prompt":"英文负面提示词","style":"统一风格关键词","aspect_ratio":"9:16"}}
分镜：{scene}"""

P_CHARS = """你是角色设定师。基于角色名列表和作品信息产出角色卡，严格输出 JSON（不要markdown代码块）：
{{"characters":[{{"name":"名","age":"年龄","appearance":"外貌:发色/瞳色/服装(供生图一致性)","personality":"性格","role":"定位","catchphrase":"口头禅或空"}}]}}
一次最多4个角色，多了只挑最重要的。作品《{title}》（{genre}）{logline}。角色：{chars}"""


def call_llm(prompt: str):
    """故障转移+重试。返回 (ok, content, model, usage, err)"""
    last_err = None
    for model in CHAIN:
        for attempt in range(1, RETRIES + 1):
            payload = json.dumps({"model": model,
                                  "messages": [{"role": "user", "content": prompt}],
                                  "max_tokens": MAX_TOKENS}).encode("utf-8")
            req = urllib.request.Request(f"{PROXY}/v1/chat/completions", data=payload,
                                         headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=150) as r:
                    d = json.loads(r.read().decode("utf-8"))
                msg = (d.get("choices") or [{}])[0].get("message", {}).get("content", "")
                usage = d.get("usage") or {}
                if not msg or len(msg.strip()) < 10:  # L4: 正文层
                    last_err = f"{model}: L4空正文({len(msg)}字)"
                    continue
                return True, msg, d.get("model", "?"), usage, None
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError,
                    json.JSONDecodeError, OSError) as e:
                body = ""
                if isinstance(e, urllib.error.HTTPError):
                    try:
                        body = e.read().decode("utf-8", "replace")[:120]
                    except Exception:
                        pass
                last_err = f"{model}: {type(e).__name__} {str(e)[:80]} {body}"
                if "524" in body or "402" in body or "5xx" in body:
                    break  # 该模型拥堵，直接换下一个
            time.sleep(2)
    return False, None, None, None, last_err


def extract_json(text: str) -> dict:
    """容错提取：剥代码块 + raw_decode 取首个完整 JSON 对象（忽略尾部多余输出）"""
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if m:
        text = m.group(1)
    s = text.find("{")
    if s == -1:
        raise ValueError("无JSON结构")
    obj, _ = json.JSONDecoder().raw_decode(text[s:])
    return obj


def step(name, prompt, want_json=True):
    t0 = time.time()
    ok, content, model, usage, err = call_llm(prompt)
    if not ok:
        print(f"[FAIL] {name}: {err}", file=sys.stderr)
        sys.exit(1)
    drift = "" if model and ("flash" in model or "free" in model) else " (漂移记录)"
    print(f"  [{name}] model={model} 正文{len(content)}字 tok={usage.get('completion_tokens')} {round(time.time()-t0,1)}s{drift}", flush=True)
    if want_json:
        try:
            return extract_json(content), model
        except (ValueError, json.JSONDecodeError) as e:
            print(f"[FAIL] {name}: JSON解析失败 {e} | 原文前200字: {content[:200]}", file=sys.stderr)
            sys.exit(1)
    return content, model


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--outline")
    g.add_argument("--outline-file")
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    outline = args.outline or open(args.outline_file, encoding="utf-8").read()
    os.makedirs(args.outdir, exist_ok=True)
    manifest = {"date": time.strftime("%Y-%m-%d %H:%M:%S"), "channel": PROXY,
                "mode": "分步防超时v2", "models": [], "files": []}

    # 1 骨架
    sk, m = step("骨架", P_SKELETON.format(outline=outline))
    manifest["models"].append(m)
    title, genre = sk.get("title", "未命名"), sk.get("genre", "")
    scene_titles = sk.get("scene_titles", [])
    if len(scene_titles) < 3:
        print(f"[FAIL] 骨架分镜数异常: {scene_titles}", file=sys.stderr)
        sys.exit(1)

    # 2 逐分镜展开（小步调用）
    scenes = []
    for i, st in enumerate(scene_titles, 1):
        ctx = " / ".join(scene_titles[max(0, i - 2):i + 1])
        sc, m = step(f"分镜{i}", P_SCENE.format(no=i, title=title, genre=genre, st=st, ctx=ctx))
        sc["scene_no"] = i
        scenes.append(sc)
        manifest["models"].append(m)

    # 3 逐镜生图提示词
    boards = []
    for sc in scenes:
        b, m = step(f"提示词{sc['scene_no']}", P_BOARD.format(no=sc["scene_no"],
                    scene=json.dumps(sc, ensure_ascii=False)))
        boards.append(b)
        manifest["models"].append(m)

    # 4 角色卡（4个一批）
    names = sk.get("characters", [])
    all_chars = []
    for i in range(0, len(names), 4):
        cs, m = step(f"角色卡{i//4+1}", P_CHARS.format(title=title, genre=genre,
                    logline=sk.get("logline", ""), chars="、".join(names[i:i + 4])))
        all_chars.extend(cs.get("characters", []))
        manifest["models"].append(m)

    # 落盘
    outs = {
        "01_分镜剧本.json": {"title": title, "genre": genre, "logline": sk.get("logline"),
                             "characters": names, "scenes": scenes},
        "02_分镜生图提示词.json": {"storyboards": boards},
        "03_角色卡.json": {"characters": all_chars},
    }
    for fn, data in outs.items():
        p = os.path.join(args.outdir, fn)
        json.dump(data, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # 人读版剧本
    p4 = os.path.join(args.outdir, "04_剧本（人读版）.md")
    lines = [f"# {title}", f"> {sk.get('logline','')}", ""]
    for sc in scenes:
        lines += [f"## 分镜 {sc.get('scene_no')} · {sc.get('location','')} · {sc.get('time','')}（{sc.get('duration_sec',8)}s）",
                  sc.get("action", ""), ""]
        lines += [f"- **{d}**" for d in sc.get("dialogue", [])] + [""]
    open(p4, "w", encoding="utf-8").write("\n".join(lines))

    # L4 终检：产物回读
    for fn in list(outs) + ["04_剧本（人读版）.md"]:
        p = os.path.join(args.outdir, fn)
        size = os.path.getsize(p)
        if size < 50:
            print(f"[FAIL] 产物过小 {p} ({size}B)", file=sys.stderr)
            sys.exit(1)
        manifest["files"].append({"path": os.path.abspath(p), "bytes": size})

    json.dump(manifest, open(os.path.join(args.outdir, "manifest.json"), "w",
              encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n[PASS] 文字链完成（{len(scenes)}分镜 {len(all_chars)}角色）: {args.outdir}")
    for f in manifest["files"]:
        print(f"  {f['bytes']:>7}B  {f['path']}")


if __name__ == "__main__":
    main()
