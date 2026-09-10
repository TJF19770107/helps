---
name: 龙虾零成本运维守卫
version: v1.3
owner: 汤小龙（AI 分身）
created: 2026-09-09
updated: 2026-09-11
cost_mode: P0（全本地 stdlib，零积分）
agent_created: true
---

# 龙虾零成本运维守卫 v1.3

> 一句话：**凡是要「推远端 / 起服务 / 分发五库」之前，先跑守卫体检，把灾难挡在本地。**
> 五个脚本，纯标准库，零积分，只读优先，不写业务数据。

**触发词**：推送守卫 / git 假删除 / 推送前体检 / 镜像仓推送 / 双仓同步 / python 运行时坏了 /
`No module named 'encodings'` / 代理脚本启动就崩 / 推送被拒 / 远端引用缺失 /
**仓库是不是没了 / Repository Not Found / 令牌失效 / 凭据库 / 内嵌明文 token / credential helper 挂起** /
**五库分发 / 五落点 / 知识库归档 / 分发回执 / 推送挂起不返回**

---

## 一、为什么有这个技能（真实事故，不是臆想）

| 时间 | 事故 | 代价 |
|---|---|---|
| 2026-09-09 01:28 | 并发会话同推一个仓 → 本地旧克隆 rebase 后 `git status` 冒出 **3652 个 D 条目 / 107 万行删除**，差点 `git add -A` 提交 | 全库险些清空，靠 push 被拦才止损 |
| 2026-09-09 19:00 | `.workbuddy\...\python\3.13.12` 只剩 exe+DLL，`import encodings` 崩溃；依赖它的 6 个 venv 一并报废 | 铁律#2 指定的解释器不可用，代理一旦重启全线瘫痪 |
| 2026-09-09 巡检 | CNB 远端 URL 内嵌明文 token（94 位） | `git remote -v` 一贴就泄露 |
| **2026-09-10 06:00** | **误判事故**：CNB 回「仓库不存在」→ 昨日据此写待办「仓库可能被删」；实测身份探针 `/user` = **401**，真因是**令牌失效**，仓库大概率还在 | 按错误结论去重建仓库 = 白干，且丢失历史判断 |
| **2026-09-11 06:00** | **自伤事故**：v1.2 做完 SEC01 脱敏后 remote 变成 `https://user@host/...`，诊断器 `parse_remote` 不剥 `user@` → host 变 `user@host` → 平台画像查不到 → **身份探针被永久跳过，只剩弱判定**；同时死令牌 push 仍会挂起 | v1.2 引以为傲的强判定在真实环境里根本没生效，等于白修 |

五者共同点：**静默故障 / 静默误导**——表面一切正常（老进程还在跑、推送还没执行），或**错误信息本身在骗人**，一触发就不可收拾。
守卫的价值 = 把「事后救火」变成「事前熔断」，把「平台说什么」变成「自己验什么」。

---

## 二、脚本清单

| 脚本 | 作用 | 位置 |
|---|---|---|
| `scripts/git_mirror_safe_push.py` | 推送前 12 项体检 + 熔断 + 可选执行推送 + ls-remote 回查 | 本技能包 / `企业微信群定制接单项目\scripts\` |
| `scripts/python_runtime_guard.py` | 解释器与 venv 健康巡检，输出推荐默认解释器 | 同上 |
| `scripts/remote_repo_doctor.py` | **远端仓库可达性分步诊断**：区分「令牌失效」与「仓库被删」，根治 URL 内嵌明文 token | 同上 |
| `scripts/opsguard_daily.py` | 每日编排器（**Python 编排，不写 bat**），日志落 `MCP服务\logs\` | 同上 |
| `scripts/five_lib_dispatch.py` | **v1.3 新增·五库分发一键编排**：门禁 → 落盘 → 推送 → 回查 → 回执，逐端打勾 | 同上 |

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

### 铁律（写进肌肉记忆）

1. **门禁先于推送**：`IDN01=401` 时绝不调 `git push`，那是拿 6 分钟换一句「失败」。
2. **只 `git add` 具体路径，永不 `add -A`**（3652 假删除的教训）。
3. **推送返回 0 不等于成功**：必须 `ls-remote` 回查远端 ref == 本地 HEAD。
4. **通道不能混**：GitHub 走 `socks5://127.0.0.1:1081`；CNB 必须 `-c http.proxy=` 清空代理。
5. **MCP 端不留空洞**：调用完立刻 `--record-receipt`，回执落 `待分发任务\五库分发回执_<日期>.json`。
6. 分支不一致时**不擅自切分支**，直接 SKIP 并报告。
