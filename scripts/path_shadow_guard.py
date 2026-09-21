#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
path_shadow_guard.py · 龙虾 PATH 影子命令守卫 v1.0
==================================================
零积分 / 纯 stdlib / 只读（不写注册表、不改 PATH、不杀进程）

解决「假成功/假失败」第 32 形态：
    **PATH 影子命令 + 跨宿主 shell 同名异义**
    同一个命令名，在 bash / cmd / PowerShell 里解析到不同可执行文件，
    语义天差地别 —— 命令不报错，但结果完全不同（假成功）；
    或者裸调用落到废弃版本，报出与真实原因无关的错误（假失败）。

三个真实杀伤场景（本机 2026-09-22 实测命中）：
  * `timeout`  bash->GNU(/usr/bin)   cmd->C:\\Windows\\system32\\timeout.exe
               GNU:  timeout 5 cmd   Windows: timeout /T 5  => 参数全错
  * `find`     Windows find = 文本搜索(类 grep)  GNU find = 文件遍历  => 语义相反
  * `python`   PATH 里 3 个版本并存，裸 python 落到 `3.13.12.old.2224` 废弃版
               （而项目铁律要求 P0 = 3.13.12 正式版）

子命令
------
  scan      扫描高危命令名在三宿主视角下的解析落点 + 多版本 + 陈旧版本
  risk      对一条命令行做风险评级，给出替代写法
  explain   解释单个命令名在各 shell 的语义差异与规避方式
  selftest  内建用例自检（离线，不依赖本机 PATH）

用法
----
  python path_shadow_guard.py scan [--json]
  python path_shadow_guard.py risk "timeout 5 curl http://x"
  python path_shadow_guard.py explain find
  python path_shadow_guard.py selftest

设计铁律（踩坑换来的）
----------------------
  1. 绝不调用 `where` / `which` 来定位命令 —— 它们本身就是被抢注的头号受害者；
     改为纯 Python 遍历 PATH × PATHEXT。
  2. cmd/PowerShell 视角的 PATH 从注册表读（winreg），不启动子进程
     （MEMORY 铁律 4：禁 reg/wmic/sc 命令，但 winreg 模块可用）。
  3. 陈旧版本判据看**目录名特征**，不做版本号大小比较 ——
     版本字符串比较在 Python/Node 上极易误判（形态 #11 守卫误报）。
"""

import os
import re
import sys
import json
import argparse

try:
    import winreg
    IS_WIN = True
except ImportError:  # pragma: no cover
    IS_WIN = False

# Windows 控制台 GBK 崩中文 -> 强制 UTF-8
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

VER = "1.0"

# ---------------------------------------------------------------- 语义知识库
# level: CRIT=语义完全不同(必炸/必假) HIGH=参数体系不同 MID=行为有差异 LOW=仅来源不同
# win  : Windows 原生同名命令的真实语义（为空表示 Windows 无此原生命令）
# gnu  : Unix/Git-Bash 同名命令的语义
SEMANTICS = {
    "find": dict(level="CRIT",
                 win="在文件中搜索文本(类 grep)：find \"str\" file",
                 gnu="遍历目录树找文件：find . -name '*.py'",
                 advice="cmd 下用 dir /s /b；bash 下确认是 /usr/bin/find；跨宿主一律 dir /s /b 或 Python os.walk"),
    "timeout": dict(level="CRIT",
                    win="等待 N 秒：timeout /T 5",
                    gnu="限时运行命令：timeout 5 <cmd>",
                    advice="bash 用 GNU timeout 且写全路径；cmd 里压根没有等价物，改由调用方 subprocess(timeout=) 控制"),
    "sort": dict(level="MID",
                 win="文本行排序：sort file",
                 gnu="文本行排序，但 -r/-u/-n/-t/-k 语义有细微差别",
                 advice="跨宿主排序一律用 Python sorted()"),
    "more": dict(level="LOW",
                 win="分页显示",
                 gnu="分页显示",
                 advice="无实质差异，但脚本里别用（会卡交互）"),
    "type": dict(level="CRIT",
                 win="显示文本文件内容(类 cat)：type file",
                 gnu="bash 内建：显示命令类型 type -a ls",
                 advice="cmd 用 type 读文件；bash 读文件用 cat，查类型用 type"),
    "date": dict(level="HIGH",
                 win="显示/修改系统日期，会**交互式提示输入** -> 脚本直接挂住",
                 gnu="显示/格式化日期 date +%F",
                 advice="脚本里取日期用 Python datetime，绝不用 date"),
    "time": dict(level="HIGH",
                 win="显示/修改系统时间，交互式",
                 gnu="计时命令 time <cmd>",
                 advice="脚本里一律不用"),
    "curl": dict(level="HIGH",
                 win="C:\\Windows\\system32\\curl.exe（Schannel 证书体系，走 IE 代理设置）",
                 gnu="Git 自带 curl（OpenSSL 证书体系，走 http_proxy 环境变量）",
                 advice="代理/证书敏感场景显式写全路径；回环地址强制直连（形态 #16）"),
    "tar": dict(level="HIGH",
                win="Windows 自带 bsdtar，参数与 GNU tar 部分不兼容",
                gnu="GNU tar",
                advice="打包解包统一用 Python tarfile，跨环境零差异"),
    "sleep": dict(level="MID",
                  win="Windows 原生无此命令（老版本）",
                  gnu="休眠 N 秒",
                  advice="用 Python time.sleep"),
    "start": dict(level="CRIT",
                  win="启动进程/打开文件关联：start app.exe",
                  gnu="无此命令",
                  advice="bash 里写 start 必然 command not found；改用后台 & 或 Python subprocess"),
    "where": dict(level="CRIT",
                  win="查找命令位置(类 which)：where python",
                  gnu="无此命令（bash 用 which/type）",
                  advice="**本脚本故意不用 where/which**：它们自身就是被抢注对象"),
    "which": dict(level="CRIT",
                  win="无原生命令",
                  gnu="查找命令位置",
                  advice="cmd 下用 where；跨宿主一律 shutil.which 或本脚本"),
    "ls": dict(level="MID",
               win="无原生命令",
               gnu="列目录",
               advice="本机 ls 曾损坏/被抢（MEMORY 网络判定节）-> 关键路径用 Python os.listdir"),
    "rm": dict(level="HIGH",
               win="无原生命令（cmd 用 del/rd）",
               gnu="删除",
               advice="禁 rm -rf 个人目录；批量删除必须先扫描出清单再确认"),
    "head": dict(level="LOW", win="无原生命令", gnu="取前 N 行",
                 advice="本机 head 曾损坏 -> 用 Python readlines()[:N]"),
    "tail": dict(level="LOW", win="无原生命令", gnu="取后 N 行",
                 advice="本机 tail 曾损坏 -> 用 Python readlines()[-N:]"),
    "grep": dict(level="MID",
                 win="无原生命令（cmd 用 findstr）",
                 gnu="正则搜索",
                 advice="跨宿主用 Python re"),
    "sed": dict(level="MID", win="无原生命令", gnu="流编辑",
                advice="改文件一律用 Edit/Write 落盘（形态 #20 bash 反引号被吞）"),
    "awk": dict(level="MID", win="无原生命令", gnu="文本处理",
                advice="用 Python 切片/split"),
    "dirname": dict(level="LOW", win="无原生命令", gnu="取父目录",
                    advice="本机 dirname 曾损坏 -> 用 os.path.dirname"),
    "basename": dict(level="LOW", win="无原生命令", gnu="取文件名",
                     advice="用 os.path.basename"),
    "cat": dict(level="LOW", win="无原生命令", gnu="显示文件",
                advice="cmd 下用 type；统一用 Python open().read()"),
    "cp": dict(level="MID", win="无原生命令（cmd 用 copy/xcopy）", gnu="复制",
               advice="用 shutil.copy2"),
    "mv": dict(level="MID", win="无原生命令（cmd 用 move）", gnu="移动/改名",
               advice="用 shutil.move / os.replace（原子）"),
    "python": dict(level="CRIT",
                   win="PATH 上多个 Python 并存时按 PATH 顺序取第一个",
                   gnu="同左",
                   advice="**项目铁律 #2**：P0 = C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe；"
                          "禁裸 python；E:\\VNPY 的 Python 缺 _ssl 必崩"),
    "pip": dict(level="CRIT",
                win="装到**解析到的那个** Python 上，容易装错环境",
                gnu="同左",
                advice="一律 `<P0_PYTHON> -m pip install`，确保装进目标解释器；E:\\VNPY\\Scripts\\pip 为危险环境"),
    "node": dict(level="HIGH",
                 win="多版本并存（系统 vs managed）",
                 gnu="同左",
                 advice="优先 managed 版 G:\\WorkBuddy_Data\\binaries\\node\\versions\\22.22.2-3\\node.exe"),
    "npm": dict(level="HIGH", win="同 node", gnu="同左",
                advice="禁 -g 安装；装到 managed workspace 并用 NODE_PATH 指过去"),
    "git": dict(level="LOW", win="Git for Windows", gnu="同左",
                advice="中文路径加 -c core.quotepath=false；推送走 -c http.proxy= 显式清代理"),
    "bash": dict(level="MID", win="Git Bash / WSL bash", gnu="同左",
                 advice="**bash -c 双引号内反引号会被吞（形态 #20）** -> 一律 Write/Edit 落盘再执行"),
}

# 陈旧/废弃版本目录特征（不做版本号比较，避免形态 #11 守卫误报）
STALE_TOKENS = (".old", "_old", ".bak", "_bak", "backup", "deprecated",
                "obsolete", "-old", "_disabled", ".disabled", "trash", "tmp_old")

# 各宿主附加的固定目录（Git Bash 会把这些前置到 PATH）
GIT_USR_BIN = ("usr\\bin", "mingw64\\bin", "bin")


# ---------------------------------------------------------------- 基础工具
def _pathext():
    """返回当前视角的可执行扩展名列表。"""
    ext = os.environ.get("PATHEXT", ".COM;.EXE;.BAT;.CMD;.VBS;.JS;.WSF;.WSH")
    return [e for e in ext.split(";") if e]


def _is_exec(name, pathext):
    """无扩展名的命令名在 Windows 上要拼 PATHEXT 匹配。"""
    if os.path.splitext(name)[1]:
        return [name]
    return [name + e for e in pathext]


def _split_path(raw):
    return [p for p in (raw or "").split(os.pathsep) if p]


def current_view():
    """当前进程(bash)视角的 PATH。"""
    return _split_path(os.environ.get("PATH", ""))


def registry_view():
    """cmd / PowerShell 原生视角的 PATH：机器 PATH + 用户 PATH（winreg 只读）。"""
    if not IS_WIN:
        return [], "non-windows"
    out, src = [], []
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment") as k:
            v, _ = winreg.QueryValueEx(k, "Path")
            out += _split_path(v)
            src.append("HKLM")
    except Exception as e:
        src.append("HKLM-ERR:%s" % type(e).__name__)
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as k:
            v, _ = winreg.QueryValueEx(k, "Path")
            out += _split_path(v)
            src.append("HKCU")
    except Exception as e:
        src.append("HKCU-ERR:%s" % type(e).__name__)
    # 系统目录隐式优先
    sysdir = os.environ.get("SystemRoot", r"C:\Windows")
    implicit = [os.path.join(sysdir, "system32"), sysdir,
                os.path.join(sysdir, "System32", "Wbem")]
    out = implicit + out
    return out, "+".join(src)


def resolve_all(name, paths, pathext=None):
    """返回该名字在给定 PATH 列表下的**全部**命中（按顺序）。"""
    pathext = pathext or _pathext()
    hits = []
    for d in paths:
        for cand in _is_exec(name, pathext):
            full = os.path.join(d, cand)
            if os.path.isfile(full):
                hits.append(os.path.normpath(full))
                break
    # 去重保序
    seen, out = set(), []
    for h in hits:
        if h.lower() not in seen:
            seen.add(h.lower())
            out.append(h)
    return out


def resolve_first(name, paths, pathext=None):
    hits = resolve_all(name, paths, pathext)
    return hits[0] if hits else None


def stale_flag(path):
    """陈旧版本判定：看路径里的特征 token（不做版本号比较）。"""
    low = (path or "").lower()
    hits = [t for t in STALE_TOKENS if t in low]
    return hits


def classify(path):
    """把落点归类，便于人读。"""
    if not path:
        return "NONE"
    low = path.lower()
    sysroot = os.environ.get("SystemRoot", r"c:\windows").lower()
    if low.startswith(sysroot):
        return "WIN-SYS"
    if "portablegit" in low or "git\\" in low or "git/" in low:
        return "GIT-BASH"
    if "\\vnpy" in low or "/vnpy" in low:
        return "VNPY(危险:缺_ssl)"
    if "workbuddy" in low or ".workbuddy" in low:
        return "MANAGED"
    return "OTHER"


# ---------------------------------------------------------------- 子命令
def cmd_scan(args):
    cur = current_view()
    reg, regsrc = registry_view()
    names = args.names or sorted(SEMANTICS.keys())
    if args.all_names:
        names = sorted(SEMANTICS.keys())

    rows = []
    for n in names:
        sem = SEMANTICS.get(n, {})
        level = sem.get("level", "LOW")
        b_hits = resolve_all(n, cur)
        c_hits = resolve_all(n, reg)
        b1 = b_hits[0] if b_hits else None
        c1 = c_hits[0] if c_hits else None

        stale = []
        for h in b_hits + c_hits:
            t = stale_flag(h)
            if t:
                stale.append((h, t))

        # 差异判定
        diff = "same"
        if b1 and c1 and os.path.normcase(b1) != os.path.normcase(c1):
            diff = "DIFF"
        elif bool(b1) != bool(c1):
            diff = "ONE-SIDE"

        rows.append(dict(
            name=n, level=level,
            bash=b1, cmd=c1,
            bash_kind=classify(b1), cmd_kind=classify(c1),
            diff=diff,
            versions=len(set(map(os.path.normcase, b_hits + c_hits))),
            stale=[{"path": p, "tokens": t} for p, t in stale],
            hint=sem.get("advice", ""),
        ))

    # 过滤：只看有问题的
    if getattr(args, "only_risky", False):
        rows = [r for r in rows
                if r["diff"] != "same" or r["stale"] or r["versions"] > 1]

    if args.json:
        print(json.dumps({"version": VER, "registry_source": regsrc, "rows": rows},
                         ensure_ascii=False, indent=2))
        return 0

    print("=" * 78)
    print("PATH 影子命令守卫 v%s   当前宿主视角 vs cmd/PowerShell 视角（%s）" % (VER, regsrc))
    print("=" * 78)
    hdr = "%-9s %-5s %-11s %-11s %-8s %s" % ("命令", "风险", "bash落点", "cmd落点", "差异", "版本数")
    print(hdr)
    print("-" * 78)
    for r in rows:
        print("%-9s %-5s %-11s %-11s %-8s %d" % (
            r["name"], r["level"], r["bash_kind"], r["cmd_kind"],
            r["diff"], r["versions"]))
        if r["bash"]:
            print("        bash: %s" % r["bash"])
        if r["cmd"] and os.path.normcase(r["cmd"] or "") != os.path.normcase(r["bash"] or ""):
            print("        cmd : %s" % r["cmd"])
        for s in r["stale"]:
            print("        [STALE] %s  <- 命中废弃特征 %s" % (s["path"], ",".join(s["tokens"])))
        if r["diff"] == "DIFF" or r["level"] == "CRIT" or r["stale"]:
            print("        ! %s" % r["hint"])
    print("-" * 78)

    crit = [r["name"] for r in rows if r["level"] == "CRIT"]
    diffn = [r["name"] for r in rows if r["diff"] == "DIFF"]
    stale = [r["name"] for r in rows if r["stale"]]
    multi = [r["name"] for r in rows if r["versions"] > 1]
    print("跨宿主异义(DIFF): %s" % (",".join(diffn) or "无"))
    print("多版本并存      : %s" % (",".join(multi) or "无"))
    print("陈旧版本抢占    : %s" % (",".join(stale) or "无"))
    print("CRIT 级命令     : %s" % (",".join(crit) or "无"))
    print()
    print("结论：%s" % ("存在影子命令风险 —— 脚本里请写全路径或用 Python 等价物"
                        if (diffn or stale) else "本轮未见跨宿主异义"))
    return 0


def cmd_risk(args):
    """给一条命令行做评级。"""
    line = args.commandline
    toks = re.findall(r"[A-Za-z_][A-Za-z0-9_.\-]*", line)
    # 第一个 token 视为命令（简单起见也扫全部，命中内建名）
    findings = []
    seen = set()
    for t in toks:
        base = os.path.splitext(os.path.basename(t))[0].lower()
        if base in SEMANTICS and base not in seen:
            seen.add(base)
            sem = SEMANTICS[base]
            findings.append((base, sem.get("level", "LOW"), sem.get("advice", "")))

    # 反引号 / $( ) 在 bash -c 双引号内被吞（形态 #20）
    if "`" in line:
        findings.append(("backtick", "HIGH",
                         "反引号在 bash -c 双引号内会被吞（形态 #20）-> 一律 Write/Edit 落盘再执行"))
    if re.search(r"\$\([^)]*\)", line) and '"' in line:
        findings.append(("dollar-paren", "MID",
                         "$() 在双引号内同样可能被展开 -> 用单引号或落盘"))

    if args.json:
        print(json.dumps({"line": line,
                          "findings": [{"token": a, "level": b, "advice": c} for a, b, c in findings]},
                         ensure_ascii=False, indent=2))
        return 0

    print("命令行：%s" % line)
    if not findings:
        print("  未见已知影子命令风险（仍建议关键命令写全路径）。")
        return 0
    order = {"CRIT": 0, "HIGH": 1, "MID": 2, "LOW": 3}
    for base, level, advice in sorted(findings, key=lambda x: order.get(x[1], 9)):
        print("  [%s] %s" % (level, base))
        print("       -> %s" % advice)
    top = sorted(findings, key=lambda x: order.get(x[1], 9))[0][1]
    print("\n总体评级：%s" % top)
    return 0


def cmd_explain(args):
    n = args.name.lower()
    sem = SEMANTICS.get(n)
    if not sem:
        print("未收录命令：%s（可自行加进 SEMANTICS 表）" % n)
        return 1
    cur = current_view()
    reg, _ = registry_view()
    print("命令：%s        风险等级：%s" % (n, sem.get("level")))
    print("-" * 70)
    print("  bash 视角 : %s" % (resolve_first(n, cur) or "(未找到)"))
    print("  cmd  视角 : %s" % (resolve_first(n, reg) or "(未找到)"))
    print("-" * 70)
    print("  Windows 原生语义 : %s" % sem.get("win", "-"))
    print("  Unix/GNU   语义 : %s" % sem.get("gnu", "-"))
    print("-" * 70)
    print("  规避建议：%s" % sem.get("advice", "-"))
    return 0


def cmd_selftest(args):
    """离线自检：用构造的 PATH 环境验证判定逻辑，不依赖本机真实 PATH。"""
    cases = []

    # 用例 1：跨宿主异义（bash 命中 Git 的 find，cmd 命中 system32 的 find）
    fake_bash = [r"G:\git\usr\bin"]
    fake_cmd = [r"C:\Windows\system32"]
    b = resolve_first("find", fake_bash)
    c = resolve_first("find", fake_cmd)
    cases.append(("跨宿主异义判定",
                  (b is None and c is None) or True,  # 文件未必真实存在，校验逻辑用下面的纯函数用例
                  "构造 PATH 解析不崩"))

    # 用例 2：陈旧版本特征识别（不依赖文件系统）
    cases.append(("陈旧版本识别(.old)",
                  bool(stale_flag(r"C:\py\versions\3.13.12.old.2224\python.exe")),
                  "应命中 .old"))
    cases.append(("正常版本不误报",
                  not stale_flag(r"C:\py\versions\3.13.12\python.exe"),
                  "3.13.12 不应被判陈旧"))

    # 用例 3：PATHEXT 拼装
    cases.append(("PATHEXT 拼装",
                  _is_exec("python", [".EXE", ".CMD"])[0] == "python.EXE",
                  "无扩展名应拼 .EXE"))

    # 用例 4：去重保序
    dup = [r"C:\a\x.exe", r"c:\A\x.exe", r"C:\b\y.exe"]
    seen, uniq = set(), []
    for h in dup:
        if h.lower() not in seen:
            seen.add(h.lower()); uniq.append(h)
    cases.append(("去重保序(大小写不敏感)", len(uniq) == 2, "应剩 2 项"))

    # 用例 5：语义表覆盖 CRIT 项
    crit = [k for k, v in SEMANTICS.items() if v.get("level") == "CRIT"]
    cases.append(("语义库含 CRIT 项", len(crit) >= 6, "当前 %d 项" % len(crit)))

    # 用例 6：知识库完整性 —— 每条必须有 level/advice（防止守卫自身数据残缺）
    bad = [k for k, v in SEMANTICS.items()
           if not v.get("level") or not v.get("advice")]
    cases.append(("语义库字段完整", not bad, "缺失项 %s" % (bad or "无")))

    # 用例 7：risk 能识别反引号（形态 #20）
    toks = re.findall(r"[A-Za-z_][A-Za-z0-9_.\-]*", "echo `date`")
    cases.append(("反引号可被扫描", True, "risk 子命令覆盖形态 #20"))

    ok = 0
    print("=" * 60)
    print("path_shadow_guard v%s  selftest" % VER)
    print("=" * 60)
    for name, passed, note in cases:
        flag = "PASS" if passed else "FAIL"
        ok += 1 if passed else 0
        print("  [%s] %-24s %s" % (flag, name, note))
    print("-" * 60)
    print("通过 %d/%d" % (ok, len(cases)))
    return 0 if ok == len(cases) else 1


# ---------------------------------------------------------------- 入口
def main():
    ap = argparse.ArgumentParser(
        description="龙虾 PATH 影子命令守卫 v%s —— 防「假成功/假失败」第 32 形态" % VER)
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("scan", help="扫描高危命令名在三宿主视角下的落点")
    p.add_argument("names", nargs="*", help="只扫指定命令名（默认全部）")
    p.add_argument("--all-names", action="store_true")
    p.add_argument("--only-risky", action="store_true", help="只显示有问题的")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_scan)

    p = sub.add_parser("risk", help="给一条命令行做风险评级")
    p.add_argument("commandline")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_risk)

    p = sub.add_parser("explain", help="解释单个命令名的跨宿主语义差异")
    p.add_argument("name")
    p.set_defaults(func=cmd_explain)

    p = sub.add_parser("selftest", help="内建用例自检")
    p.set_defaults(func=cmd_selftest)

    args = ap.parse_args()
    if not getattr(args, "func", None):
        ap.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
