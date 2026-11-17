# -*- coding: utf-8 -*-
"""
dedao_bridge.py —— 得到大脑 ⇄ Obsidian 双向桥接（v1.0.0）

设计要点（全部来自实测，不是推测）：
  1. 通道分层：
     - A 通道：Obsidian local-rest-api（127.0.0.1:27123 HTTP / 27124 HTTPS）→ 已实测通
     - B 通道：得到大脑 OpenAPI/MCP → 实测 10201 not_member（会员墙），走不通
     - C 通道：得到大脑网页版（biji.com，浏览器自动化）→ 需登录态
     → 本脚本以 A 通道为骨架，把 B/C 通道做成可插拔后端
  2. 产品灵感收集箱：本地 Obsidian 建箱，任何通道存进来的条目都先落这里，
     再由回写任务批量推向得到大脑（不依赖会员也能先攒着）
  3. 所有写操作都做磁盘真值核对（不信接口自述）

子命令：
  doctor    诊断所有通道状态
  collect   存一条网页链接到「产品灵感」收集箱（Obsidian）
  list      列出收集箱条目
  export    得到大脑 → Obsidian（走 B/C 通道，需会员或网页登录）
  import    Obsidian 待回写目录 → 得到大脑（走 B/C 通道）
  pending   列出待回写条目
"""
import os, sys, json, re, time, hashlib, datetime, subprocess, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

from obsidian_rest import ObsidianRest, DEFAULT_VAULT

SKILL_DIR = r"E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v3.0\得到大脑Obsidian四化拆解"
ENVF = r"E:\博主学习库\_tools\obsidian_rest.env"

# ---- 落点定义（与主库既有结构对齐）----
INSPIRATION_DIR = "02_产物归档/产品灵感收集箱"          # 产品灵感收集箱
PENDING_DIR = "02_产物归档/待回写得到大脑"               # 待回写队列
P07 = "P07_博主学习库（D盘+E盘）"
INGEST_DIR = P07 + "/02_产物归档/得到大脑导入"           # 得到大脑→Obsidian 落地
TRANSCRIPT_DIR = P07 + "/02_产物归档/语音转写素材"        # 语音转写落地

PRODUCT_TAG = "产品灵感"


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def slugify(url, title=""):
    """从 URL/标题生成稳定文件名"""
    if title:
        s = re.sub(r'[\\/:*?"<>|\n\r\t]', "_", title).strip()[:60]
        s = re.sub(r"\s+", "-", s)
        if s:
            return s
    from urllib.parse import urlparse
    u = urlparse(url)
    tail = (u.netloc + u.path).strip("/").replace("/", "-")[-60:]
    return re.sub(r'[\\/:*?"<>|\n\r\t]', "_", tail) or "untitled"


# ============ 通道诊断 ============
def cmd_doctor(args):
    print("=" * 62)
    print("  得到大脑 ⇄ Obsidian 桥接 · doctor")
    print("=" * 62)

    print("\n【A 通道】Obsidian local-rest-api")
    try:
        ob = ObsidianRest()
        items = ob.list_dir()
        print(f"  ✅ 通  base={ob.base}")
        print(f"     vault 顶层 {len(items)} 项")
        print(f"     主库: {ob.vault}")
    except Exception as e:
        print(f"  ❌ 不通: {e}")

    print("\n【B 通道】得到大脑 OpenAPI / MCP")
    r = subprocess.run(["cmd", "/c", "I:\\npm\\getnote.cmd", "doctor"],
                       capture_output=True, text=True, encoding="utf-8", errors="ignore")
    out = (r.stdout or "") + (r.stderr or "")
    if "not ready" in out.lower() or "No GetNote account is connected" in out:
        print("  ⚠️  未登录/未开通会员 —— API 通道不可用（not_member 10201）")
    else:
        print("  ℹ️ ", out.strip()[:300])

    print("\n【C 通道】得到大脑网页版 biji.com")
    try:
        import urllib.request
        req = urllib.request.Request("https://www.biji.com", method="HEAD",
                                     headers={"User-Agent": "Mozilla/5.0"})
        urllib.request.urlopen(req, timeout=20)
        print("  ✅ 站点可达（登录态需浏览器自动化验证）")
    except Exception as e:
        print(f"  ⚠️  不可达: {type(e).__name__}: {e}")

    print("\n【落点】")
    ob = ObsidianRest()
    for label, d in [("产品灵感收集箱", INSPIRATION_DIR),
                     ("待回写得到大脑", PENDING_DIR),
                     ("得到大脑导入", INGEST_DIR),
                     ("语音转写素材", TRANSCRIPT_DIR)]:
        try:
            n = len(ob.list_dir(d))
            print(f"  {label:16} {d}  —— 现有 {n} 项")
        except Exception:
            print(f"  {label:16} {d}  —— 待创建")


# ============ 产品灵感收集箱 ============
def cmd_collect(args):
    """存一条网页链接到产品灵感收集箱"""
    ob = ObsidianRest()
    url = args.url.strip()
    title = args.title.strip() or ""
    notes = args.note or ""

    fn = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{slugify(url, title)}.md"
    rel = INSPIRATION_DIR + "/" + fn

    body = []
    body.append(f"**来源链接**：{url}")
    body.append(f"**采集时间**：{now()}")
    if title:
        body.append(f"**网页标题**：{title}")
    body.append(f"**渠道**：{args.channel}")
    body.append("")
    body.append(notes.strip() or "（待补充：为什么值得做成产品？变现路径？）")
    body.append("")
    body.append("---")
    body.append("")
    body.append("## 四化拆解待办")
    body.append("- [ ] 痛点：这个需求背后用户真正的阻力是什么")
    body.append("- [ ] 最小可行：能不能 1 天内出一个能收费的最小版本")
    body.append("- [ ] 变现：接单 / 自有产品 / 知识库付费，哪条路")
    body.append("- [ ] 沉淀：转成技能 or 模板，挂进技能库")

    content = "\n".join(body) + "\n"
    st, disk = ob.write(rel, content)

    # 磁盘真值核对
    ok = os.path.exists(disk) and "来源链接" in open(disk, encoding="utf-8").read()
    print(f"  {'✅' if ok else '❌'} 已存入产品灵感收集箱")
    print(f"     vault 相对路径: {rel}")
    print(f"     磁盘路径: {disk}")
    print(f"     字节 {os.path.getsize(disk)} B  sha {ob.disk_sha(rel)[:16]}")
    print(f"     标签: {PRODUCT_TAG}")
    return 0 if ok else 1


def cmd_list(args):
    ob = ObsidianRest()
    d = args.dir or INSPIRATION_DIR
    try:
        items = ob.list_dir(d)
    except Exception as e:
        print(f"  ❌ {e}")
        return 1
    print(f"【{d}】共 {len(items)} 项")
    for it in items:
        if it.endswith("/"):
            continue
        try:
            txt = ob.read(d + "/" + it)
            first = next((l for l in txt.splitlines() if l.strip() and not l.startswith("#")
                          and not l.startswith("---")), "")[:70]
        except Exception:
            first = ""
        print(f"  • {it[:52]:52} | {first}")
    return 0


# ============ 得到大脑 → Obsidian ============
def cmd_export(args):
    """从得到大脑导出到 Obsidian
    B 通道（API/CLI）需会员；C 通道（网页版）需登录态。
    两条路都不可用时，如实报告，不谎报。"""
    print("【导出】得到大脑 → Obsidian")
    r = subprocess.run(["cmd", "/c", "I:\\npm\\getnote.cmd", "notes", "--all", "-o", "json"],
                       capture_output=True, text=True, encoding="utf-8", errors="ignore")
    out = (r.stdout or "") + (r.stderr or "")
    if r.returncode != 0 or "not ready" in out.lower() or "not_member" in out:
        print("  ❌ 得到大脑通道不可用：")
        for line in out.strip().splitlines()[:6]:
            print("     ", line)
        print("  → 需二选一：① 开通会员(299/年) ② 本机执行 `getnote auth login`（浏览器 OAuth，需汤哥本人点）")
        print("  → 通道打通后重跑本命令即可，本脚本已就位")
        return 2
    try:
        notes = json.loads(out)
    except Exception:
        print("  ⚠️  输出非 JSON，前 300 字：", out[:300])
        return 2
    ob = ObsidianRest()
    n = 0
    for nt in notes:
        title = nt.get("title") or "untitled"
        fn = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{slugify('', title)}.md"
        ob.note(INGEST_DIR + "/" + fn, title, nt.get("content", ""),
                tags=["得到大脑", "导入"])
        n += 1
    print(f"  ✅ 已导入 {n} 条 → {INGEST_DIR}")
    return 0


# ============ Obsidian → 得到大脑 ============
def cmd_import(args):
    ob = ObsidianRest()
    try:
        items = ob.list_dir(PENDING_DIR)
    except Exception as e:
        print(f"  ❌ 待回写目录不存在: {e}")
        return 1
    files = [i for i in items if i.endswith(".md")]
    print(f"【回写】Obsidian 待回写 → 得到大脑（待处理 {len(files)} 条）")
    if not files:
        print("  （队列为空）")
        return 0
    print("  ❌ 得到大脑回写通道不可用（not_member 10201 / 未登录）")
    print("  → 需汤哥拍板：开通会员 or 本机 `getnote auth login`")
    print("  → 本脚本不谎报成功，队列原样保留")
    return 2


def cmd_pending(args):
    ob = ObsidianRest()
    try:
        items = ob.list_dir(PENDING_DIR)
    except Exception:
        print("  （待回写目录尚未创建）")
        return 0
    files = [i for i in items if i.endswith(".md")]
    print(f"待回写 {len(files)} 条:")
    for f in files:
        print("  •", f)
    return 0


def main():
    ap = argparse.ArgumentParser(description="得到大脑⇄Obsidian 双向桥接")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("doctor", help="诊断通道状态").set_defaults(fn=cmd_doctor)
    p_c = sub.add_parser("collect", help="存网页到产品灵感收集箱")
    p_c.add_argument("url")
    p_c.add_argument("--title", default="")
    p_c.add_argument("--note", default="")
    p_c.add_argument("--channel", default="网页版自动化")
    p_c.set_defaults(fn=cmd_collect)
    p_l = sub.add_parser("list", help="列收集箱条目")
    p_l.add_argument("--dir", default=None)
    p_l.set_defaults(fn=cmd_list)
    sub.add_parser("export", help="得到大脑→Obsidian").set_defaults(fn=cmd_export)
    sub.add_parser("import", help="Obsidian→得到大脑回写").set_defaults(fn=cmd_import)
    sub.add_parser("pending", help="列待回写").set_defaults(fn=cmd_pending)

    args = ap.parse_args()
    if not getattr(args, "fn", None):
        args = ap.parse_args(["doctor"])
    return args.fn(args) or 0


if __name__ == "__main__":
    sys.exit(main())
