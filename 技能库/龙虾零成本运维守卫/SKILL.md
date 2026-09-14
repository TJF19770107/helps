---
name: 龙虾零成本运维守卫
version: v1.6
owner: 汤小龙（AI 分身）
created: 2026-09-09
updated: 2026-09-13
cost_mode: P0（全本地 stdlib，零积分）
agent_created: true
---

# 龙虾零成本运维守卫 v1.6

> 一句话：**凡是要「推远端 / 起服务 / 分发五库」之前，先跑守卫体检，把灾难挡在本地。**
> 六个脚本 + 一个修复版守卫，纯标准库，零积分，只读优先，不写业务数据。

**触发词**：推送守卫 / git 假删除 / 推送前体检 / 镜像仓推送 / 双仓同步 / python 运行时坏了 /
`No module named 'encodings'` / 代理脚本启动就崩 / 推送被拒 / 远端引用缺失 /
**仓库是不是没了 / Repository Not Found / 令牌失效 / 凭据库 / 内嵌明文 token / credential helper 挂起** /
**五库分发 / 五落点 / 知识库归档 / 分发回执 / 推送挂起不返回** /
**守卫崩了 / 计划任务结果码 / 守卫自身失效 / 静默停摆 / StopIteration / 谁在看守卫 / 守卫的守卫**

---

## 一、为什么有这个技能（真实事故，不是臆想）

| 时间 | 事故 | 代价 |
|---|---|---|
| 2026-09-09 01:28 | 并发会话同推一个仓 → 本地旧克隆 rebase 后 `git status` 冒出 **3652 个 D 条目 / 107 万行删除**，差点 `git add -A` 提交 | 全库险些清空，靠 push 被拦才止损 |
| 2026-09-09 19:00 | `.workbuddy\...\python\3.13.12` 只剩 exe+DLL，`import encodings` 崩溃；依赖它的 6 个 venv 一并报废 | 铁律#2 指定的解释器不可用，代理一旦重启全线瘫痪 |
| 2026-09-09 巡检 | CNB 远端 URL 内嵌明文 token（94 位） | `git remote -v` 一贴就泄露 |
| **2026-09-10 06:00** | **误判事故**：CNB 回「仓库不存在」→ 昨日据此写待办「仓库可能被删」；实测身份探针 `/user` = **401**，真因是**令牌失效**，仓库大概率还在 | 按错误结论去重建仓库 = 白干，且丢失历史判断 |
| **2026-09-11 06:00** | **自伤事故**：v1.2 做完 SEC01 脱敏后 remote 变成 `https://user@host/...`，诊断器 `parse_remote` 不剥 `user@` → host 变 `user@host` → 平台画像查不到 → **身份探针被永久跳过，只剩弱判定**；同时死令牌 push 仍会挂起 | v1.2 引以为傲的强判定在真实环境里根本没生效，等于白修 |
| **2026-09-12 06:00** | **守卫自身失效静默化**：`catalog_guard_deepseek.py` 写死 `CLONE_FROM="gpt-5.6-luna"`，该 slug 随上游轮换从 catalog 消失 → `next()` 抛 `StopIteration` → 未捕获 → **每 15 分钟崩一次，崩了不知多久，没有任何人知道**；被守卫的免费模型 `deepseek-v4-pro-free` 因此长期缺失 | 免费模型目录裸奔；而「计划任务 LastResult=1」这个唯一线索**没有任何人在看** |

前五者共同点：**静默故障 / 静默误导**——表面一切正常（老进程还在跑、推送还没执行），或**错误信息本身在骗人**，一触发就不可收拾。
守卫的价值 = 把「事后救火」变成「事前熔断」，把「平台说什么」变成「自己验什么」。

**但第六件事拆穿了一个更狠的前提：守卫自己也会病，而且病了没人知道。**
前五种是「它报了成功，其实没干」；第六种是**「它根本没报，你也根本没问」**。
所以 v1.4 补上最后一块拼图 —— **守卫的守卫（`guard_health_audit.py`）**。

### 假安全 / 假故障形态总表（v1.4）

| # | 形态 | 表现 | 防线 |
|---|---|---|---|
| 1 | 假成功 | 命令 rc=0 但什么也没干 | 复检副作用 |
| 2 | 假失败 | 看着挂了其实好着（如 GUI 退出码、调度器状态 0x41301） | 数据面优先于结果码 |
| 3 | 假删除 | 旧克隆 rebase 后成片 `D` | DEL01 熔断 |
| 4 | 假一致 | `ls-remote` 回查一致，但本地 HEAD 没前进 | **校验 HEAD 前进** |
| 5 | **假安全（守卫失效）** | 守卫崩了，唯一线索是没人看的 LastResult | **守卫的守卫 + 状态回执** |
| 6 | **假红（语义被特例吞掉）** | 调度器状态码 0x41301「正在运行」被自指例外判成「未捕获异常」→ 审计器自锁永久红 | **语义表做「减刑器」而非「抢答器」，且必须置于所有特例之上** |
| 7 | **假告警（记账与送达脱钩）** | 去重记账写在 `--push` 分支里 → 不推送就永不记账 → 冷却期失效，同一红项每次都算「新增」 | **记账绑定「是否已送达」，不绑定「用哪条通道送」** |

---

## 一·五、v1.5 新增：审计器自锁假红事故（2026-09-13 06:00）

**现象**：`Lobster_GuardHealthAudit` 计划任务结果码 **267009**，审计器据此判自己
「上次执行失败（未捕获异常）」→ 红 → exit 1 → 下一轮继续判自己红 → **自锁**。

**根因（两层）**：
1. `267009 = 0x41301 = SCHED_S_TASK_RUNNING` —— Windows 在说「这个实例正在运行」，
   不是「脚本崩了」。
2. `classify()` 里**自指例外排在第 227 行，语义表 `SCHED_S` 排在第 267 行**。
   自指分支只放行 `res in (0, 1)`，**把状态码吞成了脚本失败**。

**为什么手动跑永远复现不出来（时序型假故障）**：
审计器**被调度器拉起时**，它查询 schtasks 的那一刻**它自己还在运行** →
调度器如实回答 0x41301；等它退出（exit 1）后，落库的结果码才变成 1。
所以手动执行读到的是 1（绿），只有计划任务里才会读到 267009（红）。

**修法（关键设计取舍）**：
语义表不能简单「前置抢答」——否则 `Lobster_HKTunnel` 会退化成用弱证据（状态码）判绿，
丢掉更强的端口探针。正解是做成**减刑器**：

```python
sched = SCHED_S.get(res) if res is not None else None   # 预取，不抢答
sched_ok = bool(sched and sched[1] == "OK")

def soften(level, reason, e=None):
    if level == "RED" and sched_ok:      # 证据链判红，但 Windows 说这不是失败
        return ("YELLOW", f"{reason}；但结果码 {res} = 调度器状态 {sched[0]}", e)
    return (level, reason, e)
```

通用教训：**凡是「状态码 → 结论」的映射，若被特例分支绕过，映射形同虚设。**

**顺带修的两处**：
- 让元守卫**反过来逼守卫升级**：结果码 0 但**没有状态回执** → 判黄
  （「弱证据：无法证明守卫真的执行成功」），而不是继续给绿。
- 抽出 `guard_receipt.py` 通用回执模块，守卫接入只需两行。

---

## 二、脚本清单

| 脚本 | 作用 | 位置 |
|---|---|---|
| `scripts/git_mirror_safe_push.py` | 推送前 12 项体检 + 熔断 + 可选执行推送 + ls-remote 回查 | 本技能包 / `企业微信群定制接单项目\scripts\` |
| `scripts/python_runtime_guard.py` | 解释器与 venv 健康巡检，输出推荐默认解释器 | 同上 |
| `scripts/remote_repo_doctor.py` | **远端仓库可达性分步诊断**：区分「令牌失效」与「仓库被删」，根治 URL 内嵌明文 token | 同上 |
| `scripts/opsguard_daily.py` | 每日编排器（**Python 编排，不写 bat**），日志落 `MCP服务\logs\` | 同上 |
| `scripts/five_lib_dispatch.py` | **v1.3 新增·五库分发一键编排**：门禁 → 落盘 → 推送 → 回查 → 回执，逐端打勾 | 同上 |
| `scripts/guard_health_audit.py` | **v1.4 新增·守卫的守卫**：扫描全部 `Lobster_*` 计划任务，按「状态回执 → 端口探针 → 结果码语义」三级证据判红黄绿，含静默停摆检测 | 同上 |
| `scripts/catalog_guard_deepseek.py` | **v1.4 修复**：免费模型目录守卫，模板候选链替代写死模板，全程不崩 + 落状态回执 | 同上 |
| `scripts/guard_receipt.py` | **v1.5 新增·通用状态回执模块**：守卫两行接入，原子写盘，永不抛异常拖垮守卫 | 同上 / `MCP服务\` |
| `scripts/guard_alert.py` | **v1.5 新增·红项主动告警**：指纹去重 + 冷却期 + 恢复清账 + 可选的零积分企微推送 | 同上 |
| `scripts/guard_health_audit.py` | **v1.5 修复**：语义表改「减刑器」，修调度器状态码自锁假红；新增「无回执判黄」 | 同上 |
| `scripts/guard_receipt_cli.py` | **v1.6 新增·回执命令行接入点**：让 `.bat` 等非 Python 守卫一行落回执 | 同上 |
| `scripts/guard_receipt_probe.py` | **v1.6 新增·常驻守卫探针回执器**：给「永不退出」的守卫做外部端口实测并代写回执 | 同上 |
| `scripts/remote_repo_doctor.py` | **v1.6 修复**：代理/链路故障识别，不再把「SOCKS 连接被掐」误判成「仓库不存在」 | 同上 |

### v1.5 守卫接入回执（两行，任何守卫通用）

```python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from guard_receipt import write_receipt
except Exception:
    write_receipt = None        # 回执模块缺失，不许拖垮守卫本体

# ...守卫逻辑结束前：
write_receipt("my_guard", healthy=ok, detail="人话结论",
              version="1.0", exit_code=rc, extra={...})
```

回执落在 `.workbuddy/guard_status/<guard>.json`，**原子替换**（`.tmp` + `os.replace`），
审计器不会读到写了一半的 JSON。

### v1.5 踩坑补遗（当天修 bug 时又抓到两个）

**① 等级词表不一致 → 整个审计器崩溃（`KeyError: 'OK'`）**

`SCHED_S` 里写的是 `OK/WARN`，而报告层只认 `GREEN/YELLOW/RED/UNKNOWN/INFO`。
新任务以 `0x41303(NOT_YET_RUN)` 第一次走到该分支即炸：

```
File "guard_health_audit.py", line 346, in <lambda>
    rows.sort(key=lambda r: order[r["level"]])
KeyError: 'OK'
```

> **教训**：分层系统里，**语义层词汇必须显式翻译成输出层词汇**，
> 否则「加一个新状态码」这种最小改动就能让整个监督体系停摆。
> 顺带加了一道兜底：任何未收录等级降级为 `UNKNOWN`，**绝不让单点拼写问题毁掉全局监控**。

值得记一笔的是：**这次崩溃纯靠昨天（v1.1）加的 `audit_crash.log` 在 1 秒内定位**。
计划任务的 stdout 没人看，没有 traceback 落盘，这种退出码就只能靠猜。
**给无人值守脚本加「异常 traceback 落盘」，投入 5 行，回报是每次崩溃省 30 分钟。**

**② 「从未运行」不是空值，是哨兵日期 `1999/11/30 0:00:00`**

Windows 从不给空值：任务没跑过时 `schtasks` 输出的是哨兵日期。代码当真实日期解析
→ 算出「已 **234822h** 未运行」→ 把刚注册、还没到触发点的健康任务判成静默停摆。

```python
if dt.year < 2000:      # 1970 前的哨兵一律视为「从未运行」，不计停摆
    return None
```

### v1.5 主动告警

```bash
python guard_alert.py                 # 读审计回执 → 红项写 ALERT.md
python guard_alert.py --push          # 额外推企微（受 12h 冷却约束）
python guard_alert.py --json          # 机器可读
python guard_alert.py --dry-run       # 只看会发什么
```

常驻任务 `Lobster_GuardAlert`（07:35 起每 6h，比审计晚 5 分钟）。
**默认只写本地 `ALERT.md`，不推送**——告警要主动，但不能把人吵醒。

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
| **宿主重安装但解压中断**（2026-09-09 真因） | 目录 mtime 是「刚刚几分钟内」；`~/.workbuddy/binaries/python/.cache/downloads` 留有几十 MB 的 `cpython-3.13.*-install_only.tar.gz`，registry.json 该版本 `verified:false`，旁边可能有 `3.13.12.old.*` 残骸 | **用另一个完好的解释器（如 3.10.11）作搬运工具，tarfile 解开该 tar.gz、剥离顶层 `python/`、跳过 `*.pdb`，覆盖回 3.13.12 目录**（实测 3 分钟恢复 3.13.14 + OpenSSL 3.5.7） |
| **真·被清理/误删** | mtime 是几天前，且磁盘清理任务刚跑过 | 用守卫输出里「推荐默认解释器」临时顶上，再重装该版本 |

**判定顺序**：先 `ls` 看 mtime → 看有没有 `.cache/downloads/*.tar.gz` 残包 → 隔 2 分钟复测（可能是并发会话正在修）→ 仍坏才重装。别一上来就重建 6 个 venv。

**⚠️ 连带影响（比崩溃本身更危险）**：所有硬编码该 python.exe 的计划任务会**空转但 Result=0**（`Lobster_CodexModelGuard` / `Lobster_CatalogGuard_Deepseek` 等），即「任务成功但什么都没干」。恢复后必须手动补跑一次守卫类任务，把静默期间漏掉的漂移补回来。

### venv 连带故障

`G:\g_venv_*` 的 `pyvenv.cfg` 里 `home=` 指向某个解释器；**基础解释器一坏，venv 全部报废**，
且报错一模一样。修复：

```bash
<可用解释器> -m venv G:\g_venv_ars      # 重建
<venv>\Scripts\python.exe -m pip install pyyaml markdown duckdb
```

---

## 五、脚本三：远端仓库诊断器 `remote_repo_doctor.py`（v1.2 新增）

### 核心铁律：**身份探针优先于对象探针**

> GitHub / CNB / GitLab 对「认证失败」和「仓库不存在」**一律返回 404 Repository Not Found**，
> 这是刻意设计——不向未授权者泄露仓库是否存在。
>
> **所以：看到 404 绝不能直接判定「仓库被删」。**

正确顺序：先用一个**与仓库无关**的接口（`/user`）验凭据还活着没有，再谈仓库。

| 身份探针 | 对象探针 | 结论 | 处置 |
|---|---|---|---|
| **401/403** | 404 | **令牌失效**（404 是伪装） | 重新签发令牌，不要动仓库 |
| 200 | 404 | 凭据没问题，仓库真没了 / 该账号无权限 | 网页端查归属、查 token scope |
| 200 | OK | 正常 | — |
| 无令牌可用 | 任意 | **弱判定**，不可下结论 | 补令牌再跑；先排代理 |

### 用法

```bash
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"

# 单个 remote
"$PY" scripts/remote_repo_doctor.py --repo "G:/tmp/lobster-knowledge-base" --remote cnb

# 全部 remote（GitHub 走 HK 隧道）
"$PY" scripts/remote_repo_doctor.py --repo <PATH> --all --proxy socks5://127.0.0.1:1081

# 直接给 URL，无需本地仓库
"$PY" scripts/remote_repo_doctor.py --url https://github.com/owner/repo.git

# 根治内嵌明文 token：备份 -> 红线留档 -> 写凭据库 -> URL 脱敏 -> 修 local helper
"$PY" scripts/remote_repo_doctor.py --repo <PATH> --remote cnb --fix-inline-cred
```

**退出码**：`0`=健康｜`2`=WARN｜`3`=FAIL｜`4`=参数/环境错误

### 检查码

| 码 | 级别 | 含义 |
|---|---|---|
| SEC01 | FAIL | 远端 URL 内嵌明文凭证（可用 `--fix-inline-cred` 一键根治） |
| SEC02 | OK/WARN | 凭据库是否已有该 host 条目 |
| OBJ00 | INFO | 匿名访问仓库页的原始码（**404 只作参考，不作结论**） |
| **IDN01** | FAIL/INFO | **身份探针**——本脚本的灵魂，用来拆穿 404 伪装 |
| OBJ01 | OK/FAIL | `git ls-remote`（清代理版）权威结果 |
| VERDICT | — | 判定矩阵输出，带明确处置指令 |

### `--fix-inline-cred` 五步（已实测一把过）

1. `FIX01` 备份 `.git/config` → `.git/config.bak_<时间戳>`（**回滚就靠它**）
2. `FIX02` 明文 token 留档到 `_security_red_lines\<host>_token_backup_<日期>.txt`（不进 git / 不进四端）
3. `FIX03` 写入凭据库（`store` 优先，GCM 兜底）
4. `FIX04` remote URL 脱敏为 `https://<user>@host/...`
5. `FIX05` 本仓库 local `credential.helper` 置空重置 + 挂 `store`

**回滚**：`cp .git/config.bak_<时间戳> .git/config`

### ⚠️ 三个 credential helper 深坑（本机实测，代价 = 挂死 6 分钟）

1. **`git -c credential.helper=store` 是「追加」不是「替换」**——全局配的 GCM 照样被调用。
   想替换必须先 `-c credential.helper=` 清空再设值：
   `git -c credential.helper= -c credential.helper=store credential approve`
2. **GCM 会拉起 GUI 子进程并继承 stdout 管道**——`subprocess.run(timeout=N)` 杀了 git 也没用，
   `communicate()` 因管道被孙进程持有而**永久阻塞**（超时形同虚设）。
   解法：stdout 重定向到临时文件 + `GCM_INTERACTIVE=never` + `GIT_TERMINAL_PROMPT=0` + 显式 `kill()`。
3. **`-c` 是 git 全局选项，必须在子命令之前**：`git -c ... credential approve`，
   写成 `git credential -c ... approve` 会被当成 credential 的参数。

### 已知平台差异

- **CNB**：凭据缺失时**不发 401 challenge**，直接回 404，导致 credential helper 压根不被触发
  （脱敏后服务端 `token:` 为空即此现象）。如需无明文又能认证，走 `http.<url>.extraHeader` 或保留 `user@` 前缀。
- **GitHub**：会正常 challenge，credential helper 工作良好（实测 `store` 一把过）。

---

## 六、龙虾五步法定位

| 步 | 本技能承担什么 |
|---|---|
| ① 检查 | 推送前 / 起服务前，跑守卫体检，拿红黄绿报告 |
| ② 分析 | 检查码定位根因（假删除？代理？detached？运行时窗口期？**还是令牌失效伪装成 404？**） |
| ③ 修复 | 按每条 `fix` 提示执行；脚本不擅自改仓库（`--execute` 只在全绿时 push） |
| ④ 迭代 | 每次新坑追加检查码（v1.1 补 A 状态漏检+豁免；v1.2 新增 IDN01 身份探针与凭据库三坑） |
| ⑤ 沉淀 | 本 SKILL + 五库归档 |

---

## 七、成本说明

- 两个脚本 **100% Python 标准库**，不联网、不调模型、不装依赖 → **0 积分**。
- 与「免费模型网关」「TeamoRouter 额度守卫」同属 P0 成本防线。
- 建议挂计划任务每日巡检一次，输出落 `MCP服务\logs\`。

---

### 网络通道坑（2026-09-09 实测）

- **GitHub 直连 `git fetch` 会挂 >6 分钟**（curl 直连却 200，说明是 git 的 TLS/连接行为被 GFW 拖死）
  → 必须 `git -c http.proxy=socks5://127.0.0.1:1081 -c https.proxy=socks5://127.0.0.1:1081 ...`（HK 隧道端口需 LISTENING）
- **gh-proxy.com 也不通**（本次 exit 124）→ 优先 socks5 1081
- **CNB `TJF19770107/lobster-knowledge-base` 2026-09-09 19:20 起 404**（01:28 还能推）
  → **2026-09-10 已定性：不是仓库被删，是令牌失效。**
  证据链：`api.cnb.cool/user` 带凭据 = **401**（与仓库无关，纯身份接口）→ 凭据已死；
  同时 `git ls-remote` 报「仓库不存在」是 CNB 的标准伪装。
  **处置只有一条：重新签发令牌。** ~~网页端确认是否被删~~（结论作废，别照做）

## 八、实录

### 2026-09-09 首次执行

- 负向测试 A：沙箱造 40 个假删除 → `DEL01 BLOCK`，exit 3 ✅
- 负向测试 B：暂存 `.workbuddy/note.md` + `secret.txt`(含 `sk-`) → `SEC02 + SEC03 BLOCK` ✅
- 正向测试：真实镜像仓体检 → 抓出 `SEC01`（远端 URL 明文 token，输出已自动脱敏为 `***`）与 `GIT04`（global 代理 127.0.0.1:7890）✅
- 运行时：19:00 捕获 `3.13.12` 残缺（encodings 崩溃）→ 19:05 复测 3.13.14 全绿，判定为**安装窗口期**，虚惊一场 ✅
- 副产修复：ARS 三脚本（lit_search / sql_query / citation_check）在 3.10.11 下全部可跑（纯 stdlib + sqlite 降级），
  即 venv 报废也不影响零积分链路 → **降级路径已验证**。

### 2026-09-10 v1.2（远端仓库诊断器）

- **负向实测（CNB）**：`SEC01 FAIL` + `IDN01 身份探针 401` + `OBJ01 仓库不存在`
  → `VERDICT` 正确输出「**令牌失效是根因**，404 是平台伪装，不可据此判定仓库被删」exit 3 ✅
  → **直接纠正了 v1.1 写进待办的错误结论**
- **正向实测（GitHub × 2 remote）**：`SEC01 OK` + `SEC02 OK` + `OBJ01 rc=0` → `VERDICT OK` exit 0 ✅
  - 亮点：GitHub 私有仓库**匿名访问仓库页同样返回 404**，但 ls-remote 成功
    → 同一个 404，结论天差地别，铁律得以实证
- **SEC01 根治**：`--fix-inline-cred` 五步一把过，remote URL 由
  `https://user:***@cnb.cool/...` → `https://user@cnb.cool/...`，凭据入 `~/.git-credentials` ✅
- **踩坑三步曲（都记进第五节）**：`-c` 追加不替换 → GCM 继承管道假挂（挂 6 分钟）→ `-c` 位置错误
- **残留待办**：CNB 不发 401 challenge，脱敏后 helper 不触发；需汤哥重新签发令牌后再验

### 2026-09-11 v1.3（强判定修复 + 五库分发器）

- **修复一：`user@` 未剥离导致平台画像失效**（自伤 bug）
  - 现象：`SEC02 说有凭据` 但 `IDN01 跳过身份探针`，只能出弱判定
  - 根因：`INLINE_CRED_RE` 只认 `user:pass@`，脱敏后的 `https://user@host/...` 不匹配
    → host 被解析成 `TJF19770107@cnb.cool` → `PLATFORMS` 查不到 → 判定退化
  - 修复：`parse_remote` 里补 `host = re.sub(r"^[^/@\s]+@", "", host)`
- **修复二：令牌来源顺序（凭据库优先于环境变量）**
  - 实测：环境里 `CNB_TOKEN` / `CNB_GIT_TOKEN` 各 **27 位**（平台 API 令牌），
    而 git 真正用来推送的是凭据库里那条 **94 位 `cnb_` 开头**的令牌
  - 拿 API 令牌去打身份探针 → 结论与真实 git 行为不符
  - 铁律：**诊断 git 就得用 git 的那份凭据**。顺序 = URL 内嵌 > `~/.git-credentials` > env > `git credential fill`
- **新增检查码 `IDN00`**：打印令牌来源 + 脱敏形态（只留前缀 4 位与长度），明文永不落盘
- **新增 `five_lib_dispatch.py`**：见下节

---

## 九、v1.3 新增：五库分发一键编排器 `five_lib_dispatch.py`

> 解决的是「每天都要手工做五遍、还总有一端静默失败」的重复劳动（四化之「自动化」）。

### 五端职责（诚实边界，不吹全自动）

| 端 | 手段 | 自动化程度 |
|---|---|---|
| ① Obsidian | `copytree`（跳过 `.git`/`__pycache__`/`node_modules`） | **全自动** |
| ④ CNB | 门禁 → commit → 清代理 push → `ls-remote` 回查 | **全自动** |
| ⑤ GitHub | 门禁 → commit → socks5 push → `ls-remote` 回查 | **全自动** |
| ② 乐享 | MCP（Agent 调用） | 半自动：脚本生成载荷 + `--record-receipt` 记回执 |
| ③ IMA | MCP（推荐 `import_urls` 导乐享页） | 半自动：同上 |

### 核心设计：门禁前置，死凭据不再挂起

```text
push 之前 → 先跑 remote_repo_doctor 拿强判定
   IDN01 = 401  →  BLOCKED，跳过推送（不调 git，不挂起）
   IDN01 = 200  →  继续：安全体检 → commit(只 add 具体路径) → push → ls-remote 回查
```

**实测对比（本机 CNB 死令牌）**：

| 做法 | 耗时 | 结果 |
|---|---|---|
| 直接 `git push cnb` | **6 分钟+ 挂死** | 等凭据助手超时，最后还是失败 |
| `five_lib_dispatch.py --target cnb` | **1 秒** | `⛔ BLOCKED` + 明确处置建议 |

**实测（GitHub 健康端）**：`IDN01 200` + `OBJ01 rc=0` → `VERDICT OK`，推送 + 回查一致。

### 用法

```bash
# 前置自检
python scripts/five_lib_dispatch.py --status

# 单端
python scripts/five_lib_dispatch.py --target obsidian --src <技能目录>
python scripts/five_lib_dispatch.py --target cnb    --repo G:/tmp/lobster-knowledge-base
python scripts/five_lib_dispatch.py --target github --repo G:/tmp/lobster-knowledge-base --branch fresh-main

# 一键五端（MCP 端生成载荷，Agent 补调 MCP 后记回执）
python scripts/five_lib_dispatch.py --all --src <技能目录> --repo <镜像仓> --title "标题"

# MCP 端回执 / 查看今日报告
python scripts/five_lib_dispatch.py --record-receipt lexiang --url https://lexiangla.com/pages/xxx
python scripts/five_lib_dispatch.py --report
```

### 🔴 CNB 通道真相（2026-09-11 实测推翻前两天的结论）

连续两天（09-10 / 09-11）都判定「CNB 令牌失效，需汤哥重签」——**这个结论是错的**。真相是：

> **同一个平台存在多套独立凭据，死的是其中一套，不是全部。**

| 凭据 | 位置 | 状态（09-11 实测） |
|---|---|---|
| git-credentials | `~/.git-credentials`（94 位 `cnb_`） | ❌ 身份探针 401 |
| **cnb CLI 登录态** | `~/.cnb/token` → `access_token`（94 位） | ✅ 身份探针 200，**push 成功** |
| 环境变量 | `CNB_TOKEN` / `CNB_GIT_TOKEN`（27 位） | ⚠️ 窄权限 API 令牌，不是 git 令牌 |

**而且 URL 里不能带用户名**：

```bash
# ❌ 带 user@：git 拿 user 去换凭据，服务端回 `token:` 为空 → 伪装成「仓库不存在」
git push https://TJF19770107@cnb.cool/... fresh-main

# ✅ 无用户名 + GIT_ASKPASS（askpass 返回 username=cnb / password=access_token）
GIT_ASKPASS="G:/WorkBuddy_Data/cnb_askpass.sh" \
  git -c credential.helper= -c http.proxy= -c https.proxy= \
  push https://cnb.cool/TJF19770107/lobster-knowledge-base.git fresh-main
```

服务端回包里的 **`remote: token:` 为空** 是这条链路最关键的指纹——它说明「凭据根本没送到」，
而不是「仓库没了」。

**已固化**：诊断器会逐个试探全部候选令牌（`IDN00` 列出来源与脱敏形态），谁 200 用谁；
分发器对 cnb 自动走 askpass 通道。**不再出现「一条令牌死了就说令牌失效」的误判。**

顺带发现：本地历史与 CNB 端在 `d028030` 处分叉（CNB 多一个 `3e6f328` backfill 8 篇），
用 `merge` 合并而非 force push，`3e6f328..4bc7e8d` 一把推通，**没有丢任何一端的产出**。

### ⚠️ 「假成功」第 4 形态：回查一致，但改动根本没上去

首轮跑通时脚本报了 `✅ 推送成功，ls-remote 回查一致`——**其实是假的**。三个连环坑：

| # | 坑 | 后果 |
|---|---|---|
| 1 | `git status --porcelain` 默认 `core.quotepath=true`，中文路径被转义成八进制 `resources/\346\212\200\350\203\275/...` | 拿到的路径是假的 |
| 2 | 用这个转义串 `git add` → 路径不存在 → 暂存区为空 → `commit rc=1` | 什么都没提交 |
| 3 | commit 没成 → 本地 HEAD 还是旧的 → `push` 推了个寂寞 → `ls-remote` 回查**当然一致** | **误报成功** |

**这条最阴险**：`ls-remote` 回查是上一版引以为傲的防线，但它只能证明「远端 == 本地」，
证明不了「本地已经前进」。commit 失败时三者都旧，防线自动失效。

**三道补丁（已在 v1.3 落地）**：

1. `git -c core.quotepath=false status --porcelain` —— 取真实 UTF-8 路径
2. commit 后**复检工作区必须干净**，否则 FAIL
3. 回查一致时**追加校验 HEAD 是否前进**：有改动却没前进 → 判 FAIL（新增 `UPTODATE` 状态与之区分）

修复后复测：`commit ok (3 项)` → `推送成功 HEAD=800b63b→f504bff`，远端独立回查 `f504bff` 一致 ✅

> 通用教训：**校验成功不能只看「前后一致」，必须看「状态确实发生了变化」。**

### 铁律（写进肌肉记忆）

1. **门禁先于推送**：`IDN01=401` 时绝不调 `git push`，那是拿 6 分钟换一句「失败」。
2. **只 `git add` 具体路径，永不 `add -A`**（3652 假删除的教训）。
3. **推送返回 0 不等于成功**：必须 `ls-remote` 回查远端 ref == 本地 HEAD。
4. **通道不能混**：GitHub 走 `socks5://127.0.0.1:1081`；CNB 必须 `-c http.proxy=` 清空代理。
5. **MCP 端不留空洞**：调用完立刻 `--record-receipt`，回执落 `待分发任务\五库分发回执_<日期>.json`。
6. 分支不一致时**不擅自切分支**，直接 SKIP 并报告。

---

## 十、v1.4 新增：守卫的守卫 `guard_health_audit.py`

### 命题：**谁在守卫守卫者？**

2026-09-12 实测：`Lobster_CatalogGuard_Deepseek` 每 15 分钟崩一次（`StopIteration`），
崩了不知多久。链条是：

```
写死模板 CLONE_FROM="gpt-5.6-luna"
   └─ 上游轮换，该 slug 从 catalog 消失
        └─ next() 抛 StopIteration，未捕获
             └─ rc=1，仅体现为 LastResult=1
                  └─ 没人看计划任务结果码
                       └─ 被守卫的 deepseek-v4-pro-free 长期缺失 = 免费模型目录裸奔
```

**最阴险的一环不是崩溃，是「崩溃没有被任何人观测到」。**
一个不报警的守卫，等价于没有守卫。

### 核心原则：**结果码 ≠ 健康度，能打数据面就别信状态码**

同日反例，三者并列看最清楚：

| 任务 | LastResult | 状态码直觉 | 数据面真相 |
|---|---|---|---|
| `Lobster_HTTP2Socks_7897` | `-2147020576` | 像炸了 | 端口 7897 **LISTENING** → 好得很 |
| `Lobster_HKTunnel` | `267009` (`0x41301`) | 非 0 | 调度器状态 `RUNNING`，端口 1081 在听 → 正常 |
| `Lobster_ObsidianLaunch` | `-805306369` | 像炸了 | 拉的是 `Obsidian.exe`，**GUI 退出码无健康语义** → 免检 |

结论：**非 0 有三大类 —— 真失败 / 调度器状态 / 无关进程的退出码。不分类就判红，等于制造假故障。**

### 三级证据链（强 → 弱）

| 级别 | 证据 | 说明 |
|---|---|---|
| ① | 守卫自落的**状态回执** `.workbuddy/guard_status/*.json` | 最强。守卫自己说 healthy 才算数 |
| ② | **端口探针**（`socket.connect_ex`） | 次强。服务类守卫专用 |
| ③ | 计划任务**结果码语义映射** | 最弱，仅用于分流 |

外加第 4 个维度：**静默停摆检测** —— 结果码再好看，超过 `STALE_HOURS`(72h) 没跑过，
一律降为黄。守卫「不报错也不干活」是最难发现的状态。

### 结果码语义表（Windows 计划任务）

| 码 | 常量 | 判定 |
|---|---|---|
| `0` | — | 绿 |
| `0x41300` (267008) | `SCHED_S_TASK_READY` | 绿 · 就绪未触发 |
| `0x41301` (267009) | `SCHED_S_TASK_RUNNING` | 绿 · 正在跑 |
| `0x41302` (267010) | `TASK_DISABLED` | 黄 |
| `0x41303` (267011) | 尚未运行过 | 绿 |
| `0x41304` (267012) | 无更多运行次数 | 绿 |
| `0x41305` (267013) | 未排程 | 黄 |
| `1`–`255` | 脚本退出码 | **红** |
| 其他 `0x8…` / `0xC…` | 未知 | 黄 · 需人工确认 |

### 用法

```bash
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
cd "E:/龙虾AI主控中心/我的AI分身/企业微信群定制接单项目"

"$PY" scripts/guard_health_audit.py            # 红黄绿报告
"$PY" scripts/guard_health_audit.py --json     # 机器可读
"$PY" scripts/guard_health_audit.py --prefix Lobster
```

**退出码**：`0`=无红项｜`1`=存在红项｜`2`=审计器自身失败

常驻：计划任务 `Lobster_GuardHealthAudit`（07:30 起每 6 小时）。

### 让自家守卫能被审计：落状态回执

任何新建守卫，收尾处照抄这段即可接入审计：

```python
def _write_status(ok, code, detail, **kw):
    try:
        os.makedirs(STATUS_DIR, exist_ok=True)
        payload = {"guard": "<守卫名>", "version": "1.0",
                   "checked_at": datetime.datetime.now().isoformat(timespec="seconds"),
                   "healthy": bool(ok), "exit_code": int(code),
                   "detail": detail, **kw}
        tmp = STATUS_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        os.replace(tmp, STATUS_FILE)   # 原子替换，审计器不会读到半截文件
    except Exception as e:
        print(f"状态回执写入失败(忽略): {e}")
```

最后一道防线 —— **守卫绝不裸崩**：

```python
if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"未捕获异常(已兜住): {type(e).__name__}: {e}")
        sys.exit(9)
```

### 踩坑（本机实测）

1. **`schtasks` 输出是 `cp936` 且键名本地化** —— 解码顺序 `cp936 → utf-16-le → utf-8`；键名中英文都要认。
2. **未收录的键行会被当成续行，把任务名粘成一坨** —— v1.0 首跑时任务名变成
   `Lobster_CatalogGuard_Deepseek 下次运行时间: 2026/9/12 6:07:28`。
   修法：命中 `key: value` 正则即视为新键；不在映射表里的键置 `None`，后续行不再拼接。
   **必须收录「下次运行时间」**，否则它就会被并进任务名。
3. **回执名匹配不上任务名** —— `catalog_guard_deepseek` vs `Lobster_CatalogGuard_Deepseek`，
   下划线/大小写不一致。修法：`re.sub(r"[^a-z0-9]", "", s.lower())` 归一化后再做子串匹配。
4. **`New-ScheduledTaskTrigger -Daily` 的对象没有 `RepetitionInterval` 属性**
   （`SetValueInvocationException`）。正确写法改用 `-Once` 触发器（宿主为 Windows PowerShell）：

   ```text
   $trig = New-ScheduledTaskTrigger -Once -At "07:30" `
       -RepetitionInterval (New-TimeSpan -Hours 6) `
       -RepetitionDuration (New-TimeSpan -Days 3650)   # 禁用 MaxValue
   ```

5. **不要按名字硬匹配模板/依赖** —— 上游一轮换就 `StopIteration`。
   改用**候选链**：同族精确 → 同前缀族 → 任意 `-free` → 常量 → 兜底任意，且全程不抛异常。

### 铁律（写进肌肉记忆）

1. **非 0 结果码 ≠ 故障。** 先分类（真失败 / 调度器状态 / GUI 退出码），再判色。
2. **能打数据面就别信状态码。** 回执 > 端口 > 结果码。
3. **守卫必须自落状态回执**，否则审计器只能猜。
4. **守卫绝不能裸崩** —— 最外层 `try/except` + 非零结构化退出码。
5. **不要写死外部依赖名**（模板 slug、模型名、路径），一律用候选链 + 兜底。
6. **静默停摆比报错更危险**：定期审计「多久没跑了」，而不只是「跑没跑成功」。

---

## 十一、实录 · 2026-09-12 v1.4

- **选题**：昨日待办「CNB 令牌 14:20 到期，观察是否自动 refresh」→ 顺手实测，顺带发现更大问题。
- **CNB 令牌结论（昨日待办#1 结案）**：**会自动刷新，无需汤哥手动。**
  实测令牌 `expires_at` 已过 5 小时，直接跑 `cnb git get-content-without-path` → `status: 200`，
  且 `~/.cnb/token` mtime 从 `09-11 16:48` 刷新到 `09-12 05:56`。
  即：**CLI 带 refresh_token，调用即续期；机器空闲时令牌会自然过期，但一调用就活。**
  ⇒ 对分发流程的含义：**推 CNB 前先跑一次 `cnb` 命令强制续期**，别管文件里的过期时间。
- **主要产出**：修好 `catalog_guard_deepseek.py`（v1.0→v1.1，模板候选链 + 兜底不崩 + 状态回执），
  实测补回 `deepseek-v4-pro-free`（模板自动选到同族 `deepseek-v4-pro`）。
- **新增** `guard_health_audit.py` v1.0：7 项任务体检，**红 0 / 黄 0 / 未知 0 / 绿 6 / 免检 1**。
- **方法论沉淀**：提出「**假安全第 5 形态 = 守卫自身失效静默化**」，
  与前 4 种假成功并列；并给出反直觉判据「**结果码 ≠ 健康度**」。

## 十一、v1.6 新增：常驻型守卫的回执范式（2026-09-14）

### 11.1 发现问题：守卫不是只有一种

v1.5 把回执覆盖率从 1/6 推到 3/6，剩下 3 个（Fleet_AutoRestore / HKTunnel / HTTP2Socks）
迟迟接不进去。原因不是懒，是**范式不对**：

| 类型 | 特征 | 结束写回执可行？ | 正确范式 |
|---|---|---|---|
| **批处理型** | 跑完退出（fleet_autostart.bat、opsguard_daily.py） | ✅ 结尾写一次 | `guard_receipt.py` / `guard_receipt_cli.py` |
| **常驻型** | 永不退出（`goto :loop`、`while True: accept()`） | ❌ 永远走不到结尾 | **外部周期探针代写** 或 **内部心跳线程** |

常驻守卫的计划任务结果码**恒为 `267009` (0x41301 SCHED_S_TASK_RUNNING)**，
它描述的是「实例正在运行」，与健康度无关。想让审计器拿到强证据，只能换范式。

### 11.2 三个新组件（按守卫类型对号入座）

**① `guard_receipt_cli.py` —— 给 .bat / 非 Python 守卫**
```bat
"%PY%" "...\scripts\guard_receipt_cli.py" fleet_autorestore %FLEET_OK% "%FLEET_MSG%" 0 1.4
```
永远返回 0 —— 回执写失败不许拖垮宿主守卫。

**② `guard_receipt_probe.py` —— 常驻守卫的外部探针**
不看它「有没有在跑」，看它「端不端得出服务」：L1 端口 LISTENING → L2 数据面 → L3 依赖链。
新增常驻守卫只需往 `RESIDENT_GUARDS` 加一条，不动主逻辑。

**③ 心跳回执 —— 常驻服务本体自证**
`http2socks_7897.py` 内起一条 daemon 线程每 60s 自证一次（在听 + 上游 1081 可达）。
**「7897 在听但 1081 不通」要如实写成 unhealthy 并标注是依赖侧故障**——不准假装健康，也不准连坐。

### 11.3 回执名匹配铁律（踩过才知道）

审计器把「回执名」和「计划任务名」都归一化（只留 a-z0-9 小写）后判断**子串包含**：

```
LobsterFleet_AutoRestore  -> "fleet_autorestore"  ✅ 子串
Lobster_HKTunnel          -> "hktunnel"           ✅
Lobster_HTTP2Socks_7897   -> "http2socks"         ✅
```
写成 `fleet`（太短易误配）或 `fleet_autostart`（非子串）**都匹配不上，白写**。

### 11.4 v1.6 踩坑三则

1. **Python docstring 里写 Windows 路径 → 编译期 SyntaxError**
   `"""... C:\Users\... python.exe ..."""` 中的 `\U` 被当 Unicode 转义
   （`\U` 需 8 位十六进制）→ `truncated \UXXXXXXXX escape`，而报错只指到 docstring 首行，**极难定位**。
   → 文档型 docstring 一律用 `r"""`，或把路径写成 `C:/Users/...`。
2. **bat 追加子程序时，`":chk" in txt` 判断会被 `call :chk 15721` 误触发**
   → 防重判断必须锚定标签定义本身：`marker = "\r\n:chk\r\n"`。
   教训：**「字符串是否出现」≠「定义是否存在」**，判断要锚定唯一形态。
3. **守卫把链路故障记到仓库头上（误报）**
   身份探针 200（令牌有效）+ git 报 `Failed to receive SOCKS response, proxy closed connection`
   → 判定矩阵原本判 FAIL「凭据有效但仓库不可达」，OpsGuard 于是天天给仓库记红，
   实际挂的是 7897→1081→香港 这条链路。
   → 按**错误文本特征**分流：`socks|proxy|tunnel|closed connection|timed out` → OBJ01 降 WARN + 新增 PRX01，
   并明确「链路恢复前不计入仓库健康度」。**`-c http.proxy=` 只清 git config 级代理，清不掉链路级故障。**

### 11.5 收效

审计从 **绿 6/黄 1/红 1** → **绿 7/黄 0/红 1**（黄项清零，即「靠猜」的守卫清零）。
红项 1 个是 `Lobster_OpsGuard_Daily` 的 CNB 通道（真实问题：令牌/权限，非误报）。
