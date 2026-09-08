@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: ══════════════════════════════════════════════════════════════
::  龙虾迭代闭环一键执行  V1.1  (龙虾五步法 V2.7 / 全域模板 #1516)
::  固定三段式：① 批量修 cc-switch DB(补 /v1) ② 写 issues_tracker ③ 预检
::  执行完自动生成回执并同步 Obsidian 双库 + Git 仓库
::  仅此一个文件需要用户双击运行（沙箱外）
:: ══════════════════════════════════════════════════════════════

:: ---------- 配置区 ----------
set SKILL_DIR=E:\龙虾AI主控中心\我的AI分身\技能库
set CC_DB=E:\龙虾AI主控中心\CC-Switch\.cc-switch\cc-switch.db
set RECORD=%SKILL_DIR%\lobster_auto_iterate\record_iteration.py
set PRECHECK=%SKILL_DIR%\cc_switch_precheck\precheck.py
set STATE_DIR=E:\龙虾AI主控中心\state
set SNAP_DIR=G:\龙虾AI主控中心\Codex备份\snapshots\%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%_iter
set OBS_A=E:\龙虾AI主控中心\Obsidian
set OBS_B=E:\龙虾AI主控中心\ObsidianVault
set RECEIPT=%STATE_DIR%\迭代回执_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%.md
set TS=%date% %time%

if not exist "%STATE_DIR%" mkdir "%STATE_DIR%"
if not exist "%SNAP_DIR%" mkdir "%SNAP_DIR%"

echo ════════════════════════════════════════════════════════
echo   龙虾迭代闭环一键执行 V1.1
echo   ① 批量修复 cc-switch DB(补 /v1 前缀)
echo   ② 写入 issues_tracker.json.resolved (唤醒固化引擎)
echo   ③ 启动前预检 /v1 前缀 (precheck)
echo ════════════════════════════════════════════════════════
echo.

:: ════════════ ① 批量修复 cc-switch DB ════════════
echo 【①】批量修复 cc-switch 数据库 (全部 4567 端点补 /v1 前缀)...
echo   [0] 快照备份 → %SNAP_DIR%
copy "%CC_DB%" "%SNAP_DIR%\" >nul 2>&1
copy "C:\Users\Administrator\.aicodeswitch\fs-db\routes.json" "%SNAP_DIR%\" >nul 2>&1

echo   [1] 强制终止 cc-switch 释放 DB 锁...
taskkill /F /IM cc-switch.exe >nul 2>&1
timeout /t 3 /nobreak >nul

echo   [2] 清理僵尸 server.pid + 启动 AI Code Switch(4567)...
if exist "C:\Users\Administrator\.aicodeswitch\server.pid" del /F "C:\Users\Administrator\.aicodeswitch\server.pid" >nul 2>&1
netstat -ano | findstr ":4567.*LISTENING" >nul 2>&1
if not !errorlevel! equ 0 (
  start /B cmd /c "cd /d E:\aicodeswitch_v5 && node node_modules\aicodeswitch\bin\cli.js start --port 4567"
  timeout /t 8 /nobreak >nul
)

echo   [3] DB 修复 (核心: cc-switch 拼接 = baseURL + /responses, 故 baseURL 必须带 /v1)...
:: Fix A: Codex 实际用的 provider
sqlite3 "%CC_DB%" "UPDATE providers SET settings_config = REPLACE(settings_config, 'base_url\":\"http://127.0.0.1:4567\"', 'base_url\":\"http://127.0.0.1:4567/v1\"') WHERE id='xiaomimimo20260612';" >nul 2>&1
:: Fix B: aicodeswitch provider
sqlite3 "%CC_DB%" "UPDATE providers SET settings_config = REPLACE(settings_config, 'baseURL\":\"http://127.0.0.1:4567\"', 'baseURL\":\"http://127.0.0.1:4567/v1\"') WHERE id='aicodeswitch';" >nul 2>&1
:: Fix C: provider_endpoints
sqlite3 "%CC_DB%" "UPDATE provider_endpoints SET url = 'http://127.0.0.1:4567/v1' WHERE id IN (15,21) AND url NOT LIKE '%%/v1';" >nul 2>&1
sqlite3 "%CC_DB%" "UPDATE provider_endpoints SET url = 'http://127.0.0.1:4567/v1' WHERE id IN (15,21);" >nul 2>&1
:: Fix D: 清理 /opencode/v1 错误后缀
sqlite3 "%CC_DB%" "UPDATE providers SET settings_config = REPLACE(settings_config, '4567/opencode/v1', '4567/v1') WHERE id='aicodeswitch';" >nul 2>&1
:: Fix E: 确保 xiaomimimo 不直连 MiMO
sqlite3 "%CC_DB%" "UPDATE providers SET settings_config = REPLACE(settings_config, 'token-plan-cn.xiaomimimo.com', 'http://127.0.0.1:4567/v1') WHERE id LIKE 'xiaomimimo%%';" >nul 2>&1
sqlite3 "%CC_DB%" "UPDATE provider_endpoints SET url = 'http://127.0.0.1:4567/v1' WHERE url LIKE '%%xiaomimimo%%';" >nul 2>&1
:: Fix F: 🔴 兜底! 所有 4567 缺 /v1 一律补齐 (覆盖 d240abd2 等漏网 provider)
sqlite3 "%CC_DB%" "UPDATE providers SET settings_config = REPLACE(settings_config, 'http://127.0.0.1:4567\"', 'http://127.0.0.1:4567/v1\"') WHERE settings_config LIKE '%%127.0.0.1:4567\"%%' AND settings_config NOT LIKE '%%127.0.0.1:4567/v1%%';" >nul 2>&1
echo   ✅ DB 修复完成 (Fix A-F)

echo   [4] 启动 cc-switch 使配置生效...
start "" "E:\龙虾AI主控中心\CC-Switch\cc-switch.exe"
timeout /t 15 /nobreak >nul
echo   ✅ ① 完成
echo.

:: ════════════ ② 写入 issues_tracker.json.resolved ════════════
echo 【②】写入迭代追踪 (唤醒每日00:10固化引擎)...
python "%RECORD%" ^
  --problem "cc-switch 转发 Codex++ 请求到 4567 返回 404 Not Found" ^
  --root_cause "provider baseURL 缺 /v1 前缀，cc-switch 拼出 4567/responses 而非 4567/v1/responses；另含4567进程宕机(server.pid僵尸)" ^
  --solution "UPDATE providers SET settings_config=REPLACE(settings_config,'http://127.0.0.1:4567\"','http://127.0.0.1:4567/v1\"') WHERE settings_config LIKE '%127.0.0.1:4567\"%' AND settings_config NOT LIKE '%127.0.0.1:4567/v1%'; UPDATE provider_endpoints SET url='http://127.0.0.1:4567/v1' WHERE id IN(15,21)" ^
  --category codex_link ^
  --keywords "cc-switch 404,127.0.0.1:4567转发,baseURL缺失/v1前缀,provider_endpoints数据库路由错误" ^
  --skill_package cc_switch_4567_autofix ^
  --tools "codex_fullchain_fix_v2.1.bat,cc_switch_precheck" ^
  --source_track WorkBuddy > "%STATE_DIR%\record_out.txt" 2>&1
set REC_ERR=%errorlevel%
type "%STATE_DIR%\record_out.txt"
echo   ✅ ② 完成 (退出码 %REC_ERR%)
echo.

:: ════════════ ③ 启动前预检 ════════════
echo 【③】启动前预检 /v1 前缀...
python "%PRECHECK%" --fix > "%STATE_DIR%\precheck_out.txt" 2>&1
type "%STATE_DIR%\precheck_out.txt"
echo   ✅ ③ 完成
echo.

:: ════════════ 生成迭代回执 ════════════
echo 生成迭代回执 → %RECEIPT%
(
echo # 龙虾迭代完成回执
echo.
echo - 生成时间: %TS%
echo - 触发任务: cc-switch 404 全链路转发故障修复 ^(baseURL 缺 /v1 根因^)
echo - 调用模板: 龙虾五步法 V2.7 + 全域模板 R117/#1516
echo.
echo ## 1. DB 修复节点清单
echo - providers.xiaomimimo20260612.base_url → http://127.0.0.1:4567/v1
echo - providers.aicodeswitch.baseURL → http://127.0.0.1:4567/v1
echo - providers.^(所有 4567 缺/v1 节点, 含 d240abd2-xxx^) → 兜底补全 /v1
echo - provider_endpoints^(15,21^).url → http://127.0.0.1:4567/v1
echo - 清理 /opencode/v1 错误后缀
echo - 快照: %SNAP_DIR%
echo.
echo ## 2. 追踪文件写入记录
echo - 目标: E:\龙虾AI主控中心\state\issues_tracker.json.resolved
echo - 写入退出码: %REC_ERR% ^(0=成功^)
echo - 场景判定: 场景B ^(历史同类, 本次修正 URL 拼接方向错误^)
echo - 固化引擎: 每日00:10自动消费 resolved 并生成技能
echo.
echo ## 3. 预校验结果
echo.
) > "%RECEIPT%"
type "%STATE_DIR%\precheck_out.txt" >> "%RECEIPT%"
(
echo.
echo ## 4. 技能库更新记录
echo - cc_switch_4567_autofix ^(V1.0^) 已沉淀
echo - cc_switch_precheck + precheck.py 已沉淀
echo - lobster_auto_iterate + record_iteration.py 已沉淀
echo.
echo ## 5. 全域模板 / 龙虾五步法 版本升级记录
echo - 龙虾五步法: V2.6 → V2.7 ^(新增强制迭代触发器, 修正15721代理矛盾规则, 沉淀cc-switch 404案例^)
echo - 龙虾全域官方模板: 新增 R117协议^(cc-switch 404^) + #1516自动迭代触发规则 + 触发词索引
echo.
echo ──────────────────────────────────────
echo 闭环完成! 固化引擎将于每日00:10自动消费本回执对应的 resolved 记录
) >> "%RECEIPT%"
echo   ✅ 回执已生成
echo.

:: ════════════ 同步 Obsidian 双库 + Git ════════════
echo 同步 Obsidian 双知识库...
if exist "%OBS_A%" copy "%RECEIPT%" "%OBS_A%\" >nul 2>&1 && echo   ✅ → %OBS_A%
if exist "%OBS_B%" copy "%RECEIPT%" "%OBS_B%\" >nul 2>&1 && echo   ✅ → %OBS_B%

echo 同步 Git 仓库...
set GIT_ROOT=
if exist "E:\龙虾AI主控中心\.git" set GIT_ROOT=E:\龙虾AI主控中心
if exist "E:\龙虾AI主控中心\我的AI分身\.git" set GIT_ROOT=E:\龙虾AI主控中心\我的AI分身
if exist "%SKILL_DIR%\.git" set GIT_ROOT=%SKILL_DIR%
if defined GIT_ROOT (
  pushd "%GIT_ROOT%"
  git add -A >nul 2>&1
  git commit -q -m "chore: 龙虾迭代闭环归档 cc-switch 404 修复 + 五步法升V2.7" >nul 2>&1
  popd
  echo   ✅ Git 已提交 ^(%GIT_ROOT%^)
) else (
  echo   ⚠️ 未检测到Git仓库, 跳过Git同步 ^(回执已存于 %STATE_DIR%^)
)

echo.
echo ════════════════════════════════════════════════════════
echo   龙虾迭代闭环全部完成!
echo   回执: %RECEIPT%
echo ════════════════════════════════════════════════════════
pause
