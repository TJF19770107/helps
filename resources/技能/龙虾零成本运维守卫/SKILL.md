---
name: 龙虾零成本运维守卫
version: v1.1
owner: 汤小龙（AI 分身）
created: 2026-09-09
cost_mode: P0（全本地 stdlib，零积分）
agent_created: true
---

# 龙虾零成本运维守卫 v1.1

> 一句话：**凡是要「推远端 / 起服务」之前，先跑守卫体检，把灾难挡在本地。**
> 两个脚本，纯标准库，零积分，只读优先，不写业务数据。

**触发词**：推送守卫 / git 假删除 / 推送前体检 / 镜像仓推送 / 双仓同步 / python 运行时坏了 /
`No module named 'encodings'` / 代理脚本启动就崩 / 推送被拒 / 远端引用缺失

---

## 一、为什么有这个技能（真实事故，不是臆想）

| 时间 | 事故 | 代价 |
|---|---|---|
| 2026-09-09 01:28 | 并发会话同推一个仓 → 本地旧克隆 rebase 后 `git status` 冒出 **3652 个 D 条目 / 107 万行删除**，差点 `git add -A` 提交 | 全库险些清空，靠 push 被拦才止损 |
| 2026-09-09 19:00 | `.workbuddy\...\python\3.13.12` 只剩 exe+DLL，`import encodings` 崩溃；依赖它的 6 个 venv 一并报废 | 铁律#2 指定的解释器不可用，代理一旦重启全线瘫痪 |
| 2026-09-09 巡检 | CNB 远端 URL 内嵌明文 `cnb_at_...` token | `git remote -v` 一贴就泄露 |

三者共同点：**静默故障**——表面一切正常（老进程还在跑、推送还没执行），一触发就不可收拾。
守卫的价值 = 把「事后救火」变成「事前熔断」。

---

## 二、脚本清单

| 脚本 | 作用 | 位置 |
|---|---|---|
| `scripts/git_mirror_safe_push.py` | 推送前 12 项体检 + 熔断 + 可选执行推送 + ls-remote 回查 | 本技能包 / `企业微信群定制接单项目\scripts\` |
| `scripts/python_runtime_guard.py` | 解释器与 venv 健康巡检，输出推荐默认解释器 | 同上 |

---

## 三、脚本一：Git 多端镜像仓安全推送守卫

### 用法

```bash
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"

# 1) 只体检（默认，绝不推送）
"$PY" scripts/git_mirror_safe_push.py --repo "G:/tmp/lobster-knowledge-base" --remote cnb --branch fresh-main

# 2) 体检通过后再推送（必须全绿；有 WARN 需加 --force-ignore-warn）
"$PY" scripts/git_mirror_safe_push.py --repo <PATH> --remote github --branch main --execute

# 3) 机器可读（接入自动化）
"$PY" scripts/git_mirror_safe_push.py --repo <PATH> --json

# 4) 已知可接受项临时豁免（如本地 .git/config 存 token）
"$PY" scripts/git_mirror_safe_push.py --repo <PATH> --ignore SEC01
```

**退出码**：`0`=可推送｜`2`=有 P1 警告｜`3`=P0 阻断｜`4`=参数/环境错误

### 12 项检查表

| 码 | 级别 | 检查什么 |
|---|---|---|
| GIT01 | BLOCK | rebase/merge/cherry-pick 中间态（push 语义错乱） |
| GIT02 | WARN | HEAD detached → 必须 `git push <remote> HEAD:<branch>` |
| GIT02b | WARN | 当前分支 ≠ 目标分支 |
| GIT03 | — | 远端存在性 + URL 脱敏展示 |
| GIT04 | WARN | local/global `http.proxy` 会拦 CNB/国内仓 → 用 `git -c http.proxy= -c https.proxy=` |
| SEC01 | BLOCK | **远端 URL 内嵌明文口令** |
| SEC02 | BLOCK | 红线路径进入变更列表（`.workbuddy/` `.env` `.codex/` `*.pem` `secret/token/apikey` 命名文件） |
| SEC03 | BLOCK | 暂存文本文件含 `sk-` / `ghp_` / `cnb_at_` / `api_key=` |
| BIG01 | BLOCK | 单文件 > 20MB（轻量快照约束） |
| DEL01 | BLOCK | **暂存区删除条目 ≥ 阈值（默认 20）→ 假删除熔断**，并统计累计删除行数 |
| DEL02/03 | WARN | 少量删除 / 未暂存删除 |
| SYNC01 | WARN | 落后远端（behind>0）→ 必须先 fetch+rebase |
| ADD01 | BLOCK | 未跟踪文件 >200 → `add -A` 洪水 |
| ADD02 | OK/WARN | 未跟踪数量 |

### 铁律（写进肌肉记忆）

1. **旧克隆遇到远端已前进，先 `git status` 看有没有成片 `D`，绝不 `git add -A`。**
2. `git fetch <remote> <branch>`（显式 refspec）**只更新 FETCH_HEAD，不更新 `origin/xxx` 引用**；
   要更新引用必须 `git fetch <remote> <branch>:refs/remotes/<remote>/<branch>`。
3. detached / rebasing 状态下 `git push <remote> <branch>` 会被拒 → **显式 `git push <remote> HEAD:<branch>`**。
4. 推完必须 `git ls-remote <remote> <branch>` 回查，以远端为准，不信任本地引用。
5. 国内仓（CNB）推前清代理：`git -c http.proxy= -c https.proxy= push ...`。
6. `.workbuddy/` `.env` `.codex/` 永久进 `.gitignore`；已跟踪的用 `git rm --cached <f>` 保留磁盘。

---

## 四、脚本二：Python 运行时健康守卫

### 用法

```bash
"$PY" scripts/python_runtime_guard.py [--json] [--extra <解释器路径> ...]
```

检查 5 个候选解释器 + 6 个 G 盘 venv：
R1 能否启动（encodings）／R2 ssl+sqlite3／R3 版本与位数／R4 venv 的 `pyvenv.cfg home` 是否还活着／R5 推荐默认解释器。

### ⚠️ 头号坑：encodings 报错 ≠ 运行时报废（先别急着重装）

现象：

```
Could not find platform independent libraries <prefix>
Fatal Python error: Failed to import encodings module
ModuleNotFoundError: No module named 'encodings'
```

`ls` 一看只有 `DLLs python.exe python3.dll python313.dll pythonw.exe vcruntime*.dll`，没有 `Lib/`。

**两种成因，处置完全不同：**

| 成因 | 特征 | 处置 |
|---|---|---|
| **托管运行时正在安装/解压窗口期** | 目录 mtime 是「刚刚（几分钟内）」 | **等 1–3 分钟复测**，通常自动补齐（2026-09-09 实测：19:00 捕获残缺，19:05 已恢复 3.13.14 全功能） |
| **真·被清理/误删** | mtime 是几天前，且磁盘清理任务刚跑过 | 用守卫输出里「推荐默认解释器」临时顶上，再重装该版本 |

**判定顺序**：先 `ls` 看 mtime → 隔 2 分钟复测 → 仍坏才重装。别一上来就重建 6 个 venv。

### venv 连带故障

`G:\g_venv_*` 的 `pyvenv.cfg` 里 `home=` 指向某个解释器；**基础解释器一坏，venv 全部报废**，
且报错一模一样。修复：

```bash
<可用解释器> -m venv G:\g_venv_ars      # 重建
<venv>\Scripts\python.exe -m pip install pyyaml markdown duckdb
```

---

## 五、龙虾五步法定位

| 步 | 本技能承担什么 |
|---|---|
| ① 检查 | 推送前 / 起服务前，跑守卫体检，拿红黄绿报告 |
| ② 分析 | 12 项检查码定位根因（是假删除？代理？detached？运行时窗口期？） |
| ③ 修复 | 按每条 `fix` 提示执行；脚本本身不擅自改仓库（`--execute` 只在全绿时 push） |
| ④ 迭代 | 每次新坑追加检查码（v1.1 已补：新增文件 A 状态漏检、豁免开关） |
| ⑤ 沉淀 | 本 SKILL + 五库归档 |

---

## 六、成本说明

- 两个脚本 **100% Python 标准库**，不联网、不调模型、不装依赖 → **0 积分**。
- 与「免费模型网关」「TeamoRouter 额度守卫」同属 P0 成本防线。
- 建议挂计划任务每日巡检一次，输出落 `MCP服务\logs\`。

---

## 七、实录（2026-09-09 首次执行）

- 负向测试 A：沙箱造 40 个假删除 → `DEL01 BLOCK`，exit 3 ✅
- 负向测试 B：暂存 `.workbuddy/note.md` + `secret.txt`(含 `sk-`) → `SEC02 + SEC03 BLOCK` ✅
- 正向测试：真实镜像仓体检 → 抓出 `SEC01`（远端 URL 明文 token，输出已自动脱敏为 `***`）与 `GIT04`（global 代理 127.0.0.1:7890）✅
- 运行时：19:00 捕获 `3.13.12` 残缺（encodings 崩溃）→ 19:05 复测 3.13.14 全绿，判定为**安装窗口期**，虚惊一场 ✅
- 副产修复：ARS 三脚本（lit_search / sql_query / citation_check）在 3.10.11 下全部可跑（纯 stdlib + sqlite 降级），
  即 venv 报废也不影响零积分链路 → **降级路径已验证**。
