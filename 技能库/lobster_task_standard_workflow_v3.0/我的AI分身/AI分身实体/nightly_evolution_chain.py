# -*- coding: utf-8 -*-
"""nightly_evolution_chain.py · 汤小龙夜间自动进化链（免费 / 0 积分）

由 Windows 计划任务 Lobster_TangXiaolong_Evolve 每天 03:00 触发。
链路（接龙）五步，每步独立执行、独立留痕，单步失败不阻断后续（自我净化可断点追溯）：
  1. 果位进化      evolve_tangxiaolong.py   （硕士→…→诺奖阶梯 + Obsidian 迭代记录）
  2. 四化迭代      run_1234.sh             （智能化/定制化/全自动化/自我净化，0 积分）
  3. 乐享知识库    lexiang_sync.py          （未授权则本地增量，已授权自动上传）
  4. CNB/GitHub    git push origin/direct   （走 mihomo 7890 代理，非交互凭据）
  5. 唤醒汤小龙    启动我的AI分身.py         （免费大脑：GLM / NVIDIA 备用）

约束：不自动 git commit（避免把工作区未提交改动一并打包），只 push 已提交内容。
"""
import os
import subprocess
import datetime

PY = r"C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe"
GIT_BASH = r"C:\Program Files\Git\bin\bash.exe"
GIT = r"C:\Program Files\Git\cmd\git.exe"
PROXY = "http://127.0.0.1:7890"

HERE = os.path.dirname(os.path.abspath(__file__))  # AI分身实体目录
PROJECT = r"E:\龙虾AI主控中心\我的AI分身\企业微信群定制接单项目"
LOG_DIR = os.path.join(PROJECT, ".workbuddy", "nightly")
os.makedirs(LOG_DIR, exist_ok=True)
LOG = os.path.join(LOG_DIR, "nightly_%s.log" % datetime.date.today().strftime("%Y%m%d"))


def log(msg):
    line = "[%s] %s" % (datetime.datetime.now().strftime("%H:%M:%S"), msg)
    print(line)
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def run_step(name, cmd, cwd, timeout=300):
    log("[%s] 执行: %s" % (name, " ".join(cmd)))
    env = dict(os.environ)
    # 非交互凭据 + 走 mihomo 代理，保证定时/无人值守也能连 CNB
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GCM_INTERACTIVE"] = "never"
    env["http_proxy"] = PROXY
    env["https_proxy"] = PROXY
    try:
        r = subprocess.run(cmd, cwd=cwd, timeout=timeout, env=env,
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        for line in (r.stdout or "").strip().splitlines()[-4:]:
            log("    | " + line)
        if r.returncode != 0 and r.stderr:
            for line in r.stderr.strip().splitlines()[-3:]:
                log("    ! " + line)
        log("[%s] 结束，返回码 %s" % (name, r.returncode))
        return r.returncode
    except subprocess.TimeoutExpired:
        log("[%s] 超时（>%ss），跳过" % (name, timeout))
        return -1
    except Exception as e:
        log("[%s] 异常：%s" % (name, e))
        return -1


def main():
    today = datetime.date.today().strftime("%Y-%m-%d")
    log("=" * 60)
    log("汤小龙夜间自动进化链启动 · %s（免费，0 积分）" % today)
    log("=" * 60)

    run_step("1-果位进化", [PY, os.path.join(HERE, "evolve_tangxiaolong.py")], HERE, 300)
    run_step("2-四化迭代", [GIT_BASH, "-c", "cd scripts && bash run_1234.sh"], PROJECT, 600)
    run_step("3-乐享同步", [PY, os.path.join(PROJECT, "scripts", "lib", "lexiang_sync.py"), "--dry-run"], PROJECT, 300)
    run_step("4a-CNB推送", [GIT, "push", "origin", "main"], PROJECT, 180)
    run_step("4b-GitHub推送", [GIT, "push", "direct", "main"], PROJECT, 180)
    run_step("5-唤醒汤小龙", [PY, os.path.join(HERE, "启动我的AI分身.py"), "完成今日四化迭代知识库沉淀"], HERE, 180)

    log("=" * 60)
    log("夜间链结束 · %s" % today)
    log("=" * 60)


if __name__ == "__main__":
    main()
