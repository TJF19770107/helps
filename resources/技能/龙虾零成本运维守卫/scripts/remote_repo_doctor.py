#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
remote_repo_doctor.py  v1.0  (龙虾零成本运维守卫 v1.2 组件)
远端仓库可达性「分步诊断器」——专治「仓库是不是没了？」这类误判。

核心铁律：**身份探针优先于对象探针**
  绝大多数代码托管平台（GitHub / CNB / GitLab）对「认证失败」与「仓库不存在」
  一律返回 404「Repository Not Found」，目的是不泄露仓库是否存在。
  因此看到 404 **绝不能**直接判定「仓库被删」——
  必须先用「身份探针」（/user 这类与仓库无关的接口）确认凭据是否还活着：
    - 身份探针 401/403  -> 凭据失效  -> 404 是假象，真因是令牌，去换令牌
    - 身份探针 200      -> 凭据有效  -> 404 才是真的「仓库不存在/无权限」

零积分：纯 stdlib（urllib + subprocess），不调任何模型。

用法:
  python remote_repo_doctor.py --repo <本地仓库路径> [--remote <名>] [--all]
  python remote_repo_doctor.py --url  https://host/owner/repo.git
  python remote_repo_doctor.py --repo . --fix-inline-cred     # 内嵌明文 token -> 凭据库
  python remote_repo_doctor.py --repo . --json                # 机器可读输出

退出码:
  0 = 全部健康  2 = 有告警(WARN)  3 = 有阻断(FAIL)  4 = 参数/环境错误
"""
import argparse
import base64
import json
import os
import re
import shutil
import ssl
import subprocess
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE  # 仅用于探测连通性，不传输敏感判断

UA = "lobster-remote-repo-doctor/1.0"

# 平台画像：api_root + 身份探针路径 + 对象探针路径
PLATFORMS = {
    "github.com": {
        "api": "https://api.github.com",
        "identity": "/user",
        "object": "/repos/{owner}/{repo}",
        "auth_headers": lambda t: {"Authorization": "Bearer " + t},
        "anon_identity_code": 401,   # 匿名访问 /user 的返回码
    },
    "cnb.cool": {
        "api": "https://api.cnb.cool",
        "identity": "/user",
        "object": "/repos/{owner}/{repo}",
        "auth_headers": lambda t: {"Authorization": "Bearer " + t},
        "anon_identity_code": 401,
    },
    "gitee.com": {
        "api": "https://gitee.com/api/v5",
        "identity": "/user",
        "object": "/repos/{owner}/{repo}",
        "auth_headers": lambda t: {"Authorization": "token " + t},
        "anon_identity_code": 401,
    },
}

SECRET_RE = re.compile(r"(?i)(sk-[A-Za-z0-9_\-]{8,}|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}"
                       r"|github_pat_[A-Za-z0-9_]{20,}|cnb_[A-Za-z0-9]{10,}"
                       r"|(?:^|[:@/])[A-Za-z0-9_\-]{32,}(?=$|[@/:?])|[0-9a-f]{40})")
INLINE_CRED_RE = re.compile(r"^(https?://)([^/@\s]+):([^/@\s]+)@(.+)$")

findings = []  # (level, code, msg)
PROXY = ""  # 全局代理，可用 --proxy 覆盖；默认清空走直连（国内平台直连更快）


def add(level, code, msg):
    findings.append((level, code, msg))
    icon = {"FAIL": "[FAIL]", "WARN": "[WARN]", "OK": "[ OK ]", "INFO": "[INFO]"}[level]
    print(f"{icon} {code}  {msg}")


def mask(s):
    """脱敏：任何疑似密钥串统一打码，避免日志二次泄漏。"""
    if not s:
        return s
    s = re.sub(r"(https?://)([^/@\s]+):([^/@\s]+)@", r"\1\2:***@", s)
    s = SECRET_RE.sub(lambda m: (m.group(0)[:3] + "***" + m.group(0)[-2:])
                      if len(m.group(0)) > 8 else "***", s)
    return s


def git(args, cwd=None, timeout=180):
    try:
        r = subprocess.run(["git"] + args, cwd=cwd, capture_output=True,
                           text=True, timeout=timeout, errors="ignore")
        return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()
    except subprocess.TimeoutExpired:
        return -1, "", "timeout after %ss" % timeout
    except FileNotFoundError:
        return -2, "", "git not found"


def http_probe(url, headers=None, timeout=25):
    """返回 (code, body_snippet)；code 为 'ERR' 表示网络层失败。"""
    h = {"User-Agent": UA, "Accept": "application/json"}
    if headers:
        h.update(headers)
    try:
        req = Request(url, headers=h)
        with urlopen(req, timeout=timeout, context=CTX) as r:
            return r.status, r.read(300).decode("utf-8", "ignore")
    except HTTPError as e:
        try:
            body = e.read(200).decode("utf-8", "ignore")
        except Exception:
            body = ""
        return e.code, body
    except URLError as e:
        return "ERR", str(e.reason)[:120]
    except Exception as e:
        return "ERR", type(e).__name__ + " " + str(e)[:80]


def parse_remote(url):
    """解析 remote URL -> dict(platform, owner, repo, inline_user, inline_token, safe_url, web_url)"""
    info = {"raw": url, "safe_url": mask(url), "inline_user": None,
            "inline_token": None, "platform": None, "owner": None, "repo": None}
    m = INLINE_CRED_RE.match(url)
    if m:
        info["inline_user"], info["inline_token"] = m.group(2), m.group(3)
        scheme, rest = m.group(1), m.group(4)
    else:
        scheme, rest = ("https://" if url.startswith("http") else ""), url
    mm = re.match(r"^(?:https?://)?([^/:]+)[/:](.+?)(?:\.git)?$", rest)
    if not mm:
        return info
    host, path = mm.group(1), mm.group(2)
    info["platform"] = host if host in PLATFORMS else None
    parts = [p for p in re.split(r"[:/]", path) if p]
    if len(parts) >= 2:
        info["owner"], info["repo"] = parts[-2], parts[-1]
    info["web_url"] = scheme + host + "/" + "/".join(parts)
    return info


def credential_fill(host):
    """问凭据库要账号密码（不打印），只回报有没有。"""
    # 双重坑（实测挂死 6 分钟）：
    #  1) helper=GCM 时，fill 无匹配条目会拉起 GUI 交互进程；
    #  2) 该 GUI 进程继承 stdout 管道 -> 即使 subprocess 超时 kill 掉 git，
    #     communicate() 仍因管道被孙进程持有而永久阻塞（timeout 形同虚设）。
    # 解法：stdout 重定向到临时文件（不用管道）+ GCM_INTERACTIVE=never + 显式 kill
    #       + 用 `-c credential.helper= -c credential.helper=store` 屏蔽 GCM（追加≠替换）
    # 快路径（零子进程）：直接读 ~/.git-credentials
    try:
        pf = os.path.expanduser("~/.git-credentials")
        if os.path.exists(pf):
            with open(pf, "r", errors="ignore") as f:
                if any(host in ln and "@" in ln for ln in f):
                    return True, "file-hit"
    except Exception:
        pass
    env = dict(os.environ)
    env["GCM_INTERACTIVE"] = "never"
    env["GIT_TERMINAL_PROMPT"] = "0"
    tmp = os.path.join(os.environ.get("TEMP", "."), "_lkr_cred_%d.tmp" % os.getpid())
    try:
        with open(tmp, "w", errors="ignore") as fo:
            p = subprocess.Popen(["git", "-c", "credential.helper=",
                                  "-c", "credential.helper=store",
                                  "credential", "fill"], stdin=subprocess.PIPE,
                                 stdout=fo, stderr=subprocess.DEVNULL, text=True, env=env)
            try:
                p.communicate(input=f"protocol=https\nhost={host}\n\n", timeout=20)
            except subprocess.TimeoutExpired:
                p.kill()
                try:
                    p.communicate(timeout=5)
                except Exception:
                    pass
                return False, "TIMEOUT(凭据助手挂起，已降级为无凭据)"
        with open(tmp, "r", errors="ignore") as fi:
            out = fi.read()
    except Exception as e:
        return False, type(e).__name__ + " " + str(e)[:60]
    finally:
        try:
            os.remove(tmp)
        except Exception:
            pass
    return "password=" in out, out


def credential_approve(host, user, token):
    """写入 git 凭据库（GCM 优先，失败退回 store）。"""
    payload = f"protocol=https\nhost={host}\nusername={user}\npassword={token}\n\n"
    last_err = ""
    env = dict(os.environ)
    env["GCM_INTERACTIVE"] = "never"
    env["GIT_TERMINAL_PROMPT"] = "0"
    # 坑1：`-c credential.helper=store` 是**追加**不是替换，全局配的 GCM 仍会被调用并挂死。
    #      必须先 `-c credential.helper=` 清空列表再设值。
    # 坑2：`-c` 是 git 全局选项，必须在子命令 credential 之前。
    # 坑3：GCM 在本机（无 GUI 会话/计划任务上下文）会挂起 -> 默认优先用 store，GCM 仅作兜底。
    for helper in ("store", None):
        cmd = ["git"]
        if helper:
            cmd += ["-c", "credential.helper=", "-c", "credential.helper=" + helper]
        cmd += ["credential", "approve"]
        # 同样规避 GCM 继承管道导致的假挂：stdout 走临时文件、stderr 丢弃、显式 kill
        tmp = os.path.join(os.environ.get("TEMP", "."), "_lkr_appr_%d.tmp" % os.getpid())
        try:
            with open(tmp, "w", errors="ignore") as fo:
                errf = tmp + ".err"
                fe = open(errf, "w", errors="ignore")
                p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=fo,
                                     stderr=fe, text=True, env=env)
                try:
                    p.communicate(input=payload, timeout=25)
                    rc = p.returncode
                except subprocess.TimeoutExpired:
                    p.kill()
                    try:
                        p.communicate(timeout=5)
                    except Exception:
                        pass
                    rc = -1
            if rc == 0:
                try:
                    fe.close()
                except Exception:
                    pass
                return True, helper or "system-default(GCM)"
            try:
                fe.close()
                with open(errf, "r", errors="ignore") as f2:
                    last_err = f2.read().strip()[:120]
            except Exception:
                last_err = ""
        except Exception as e:
            last_err = type(e).__name__
        finally:
            for f_ in (tmp, tmp + ".err"):
                try:
                    os.remove(f_)
                except Exception:
                    pass
    return False, "all helpers failed; last=" + (last_err or "?")


def diagnose(url, do_fix=False, repo_path=None, remote_name=None):
    info = parse_remote(url)
    add("INFO", "URL01", "目标: " + info["safe_url"])
    if not info["owner"] or not info["repo"]:
        add("FAIL", "URL02", "无法从 URL 解析 owner/repo")
        return
    # 必须先把内嵌凭证剥掉再取 host，否则会把「用户名」当成 host
    # （实测坑：https://user:tok@cnb.cool/... 直接 split(":")[0] 得到的是 user）
    host = re.sub(r"^https?://", "", info["raw"])
    host = re.sub(r"^[^/@\s]+:[^/@\s]+@", "", host)   # 剥 user:token@
    host = re.sub(r"^[^/@\s]+@", "", host)            # 剥 user@
    host = host.split("/")[0].split(":")[0]

    # ---------- 1. 内嵌明文凭证（SEC01）----------
    if info["inline_token"]:
        add("FAIL", "SEC01",
            f"远端 URL 内嵌明文凭证（user={info['inline_user']}, token长度={len(info['inline_token'])}）"
            " -> .git/config 一旦进备份/同步即泄漏")
        if do_fix and repo_path and remote_name:
            fix_inline_cred(repo_path, remote_name, info, host)
            info = parse_remote(git(["remote", "get-url", remote_name], cwd=repo_path)[1])
    else:
        add("OK", "SEC01", "远端 URL 无内嵌凭证")

    # ---------- 2. 凭据库存量 ----------
    has_cred, _ = credential_fill(host)
    add("OK" if has_cred else "WARN", "SEC02",
        "凭据库已有 %s 条目" % host if has_cred else "凭据库无 %s 条目（每次推需交互或依赖 URL 明文）" % host)

    token = info["inline_token"]
    plat = PLATFORMS.get(info["platform"])

    # ---------- 3. 匿名对象探针（最容易骗人的一步）----------
    anon_code, _ = http_probe(info["web_url"])
    add("INFO", "OBJ00", f"匿名访问仓库页 -> {anon_code}"
        + ("（404 未必等于被删，见下）" if anon_code == 404 else ""))

    # ---------- 4. 身份探针（真因判定关键）----------
    identity_ok = None
    if plat and token:
        code, _ = http_probe(plat["api"] + plat["identity"], headers=plat["auth_headers"](token))
        if code == 200:
            identity_ok = True
            add("OK", "IDN01", f"{info['platform']} 身份探针 200 -> 凭据有效")
        else:
            identity_ok = False
            add("FAIL", "IDN01",
                f"{info['platform']} 身份探针 {code} -> **凭据已失效**（令牌过期/被撤销/权限不足）")
    elif not token:
        add("INFO", "IDN01", "无可用令牌（URL 无内嵌且凭据库未取到明文），跳过身份探针")
    else:
        add("INFO", "IDN01", f"平台 {host} 无预置画像，跳过 API 身份探针，仅用 git 判定")

    # ---------- 5. git 对象探针（权威）----------
    args = ["-c", "http.proxy=" + PROXY, "-c", "https.proxy=" + PROXY, "ls-remote", "--heads"]
    if repo_path:
        rc, out, err = git(args + [remote_name or "origin"], cwd=repo_path)
    else:
        rc, out, err = git(args + [url])
    git_ok = (rc == 0)
    err_masked = mask((err or "").replace("\n", " | ")[:200])
    add("OK" if git_ok else "FAIL", "OBJ01",
        f"git ls-remote -> rc={rc}" + ("" if git_ok else f"  {err_masked}"))

    # ---------- 6. 判定矩阵（本脚本的价值所在）----------
    print("\n--- 判定 ---")
    if git_ok:
        add("OK", "VERDICT", "仓库可达且凭据有效，无需处置")
    elif identity_ok is False:
        add("FAIL", "VERDICT",
            "**令牌失效是根因**：身份探针 401 证明凭据已死；"
            f"此时 {host} 返回的 404「仓库不存在」是平台标准伪装，**不可据此判定仓库被删**。\n"
            f"        处置：去 {info['platform'] or host} 重新签发令牌 -> "
            f"`git -c credential.helper=store credential approve` 写入凭据库 -> 复跑本脚本。")
    elif identity_ok is True:
        add("FAIL", "VERDICT",
            "凭据有效但仓库不可达 -> 仓库确实不存在，或该令牌账号无访问权限。"
            "处置：网页端确认仓库归属 / 检查令牌 scope。")
    else:
        add("WARN", "VERDICT",
            "无法完成身份探针（无令牌/无平台画像），结论为弱判定："
            "git ls-remote 失败，可能是网络、代理或权限任一原因。\n"
            "        处置：先 `git -c http.proxy= -c https.proxy= ls-remote` 排代理；"
            "再补令牌跑本脚本拿强判定。")
    return info


def fix_inline_cred(repo_path, remote_name, info, host):
    """把内嵌明文 token 迁进凭据库，并把 remote URL 改成无明文形式。"""
    cfg = os.path.join(repo_path, ".git", "config")
    bak = cfg + ".bak_" + time.strftime("%Y%m%d_%H%M%S")
    try:
        shutil.copy2(cfg, bak)
        add("INFO", "FIX01", "已备份 .git/config -> " + bak)
    except Exception as e:
        add("FAIL", "FIX00", "备份 .git/config 失败: %s" % e)
        return
    # 红线留档：明文只留在不进 git、不进四端的本地红线目录
    try:
        red = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "_security_red_lines")
        os.makedirs(red, exist_ok=True)
        p = os.path.join(red, f"{host}_token_backup_{time.strftime('%Y%m%d')}.txt")
        with open(p, "w", encoding="utf-8") as f:
            f.write(f"# 本地红线留档，禁止进 git / 禁止进四端同步\n"
                    f"host={host}\nuser={info['inline_user']}\ntoken={info['inline_token']}\n")
        add("OK", "FIX02", "明文令牌留档（不进 git）-> " + p)
    except Exception as e:
        add("WARN", "FIX02", "红线留档失败: %s" % e)
    ok, helper = credential_approve(host, info["inline_user"], info["inline_token"])
    if not ok:
        add("FAIL", "FIX03", "写入凭据库失败(%s)，已中止，remote URL 保持原样" % helper)
        return
    add("OK", "FIX03", "已写入凭据库 helper=%s" % helper)
    new_url = re.sub(r"^(https?://)[^/@\s]+:[^/@\s]+@",
                     r"\1" + info["inline_user"] + "@", info["raw"])
    rc, _, err = git(["remote", "set-url", remote_name, new_url], cwd=repo_path)
    if rc != 0:
        add("FAIL", "FIX04", "改写 remote 失败: " + mask(err))
        return
    add("OK", "FIX04", "remote URL 已脱敏 -> " + mask(new_url))

    # FIX05（必须）：光写入 store 不够——默认 helper 是 GCM，而 GCM 读的是自己的库，
    # 结果 git 仍取不到刚存的凭据（实测服务端回 `token:` 为空 = 未带认证）。
    # 在本仓库 local 层先置空重置 helper 列表，再挂 store，才能确保 git 用得上。
    git(["config", "--local", "credential.helper", ""], cwd=repo_path)
    rc5, _, e5 = git(["config", "--local", "--add", "credential.helper", "store"], cwd=repo_path)
    if rc5 != 0:
        add("WARN", "FIX05", "设置 local helper=store 失败: " + mask(e5))
    else:
        cur = git(["config", "--local", "--get-all", "credential.helper"], cwd=repo_path)[1]
        add("OK", "FIX05", "本仓库 helper 已改为 " + (cur.replace("\n", ",") or "?")
            + "（空值重置 + store，屏蔽会挂起的 GCM）")


def main():
    ap = argparse.ArgumentParser(description="远端仓库可达性分步诊断器")
    ap.add_argument("--repo", help="本地仓库路径")
    ap.add_argument("--remote", default="origin", help="remote 名，默认 origin")
    ap.add_argument("--all", action="store_true", help="诊断该仓库所有 remote")
    ap.add_argument("--url", help="直接给远端 URL（无需本地仓库）")
    ap.add_argument("--fix-inline-cred", action="store_true", help="迁移内嵌明文 token 到凭据库")
    ap.add_argument("--json", action="store_true", help="机器可读输出")
    ap.add_argument("--proxy", default="", help="git ls-remote 用的代理，如 socks5://127.0.0.1:1081；默认清空")
    a = ap.parse_args()
    global PROXY
    PROXY = a.proxy

    targets = []
    if a.url:
        targets.append((a.url, None, None))
    elif a.repo:
        repo = os.path.abspath(a.repo)
        if not os.path.isdir(os.path.join(repo, ".git")):
            print("[FAIL] ENV01 不是 git 仓库: " + repo)
            return 4
        names = []
        if a.all:
            names = git(["remote"], cwd=repo)[1].split()
        else:
            names = [a.remote]
        for n in names:
            u = git(["remote", "get-url", n], cwd=repo)[1]
            if u:
                targets.append((u, repo, n))
    else:
        print("[FAIL] ENV02 需要 --repo 或 --url")
        return 4

    if not targets:
        print("[FAIL] ENV03 未找到任何 remote")
        return 4

    for i, (u, rp, rn) in enumerate(targets):
        if i:
            print("\n" + "=" * 66 + "\n")
        print(f"### remote: {rn or '(url)'}   {time.strftime('%Y-%m-%d %H:%M:%S')}")
        diagnose(u, do_fix=a.fix_inline_cred, repo_path=rp, remote_name=rn)

    lv = [f[0] for f in findings]
    if a.json:
        print("\n" + json.dumps([{"level": l, "code": c, "msg": mask(m)} for l, c, m in findings],
                                ensure_ascii=False, indent=2))
    print("\n=== 汇总 FAIL=%d WARN=%d ===" % (lv.count("FAIL"), lv.count("WARN")))
    if "FAIL" in lv:
        return 3
    if "WARN" in lv:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
