# 轻量快照 light_snapshot_20260919

生成时间: 2026-09-19 16:24:58
用途: 本次「重启根因排查 + 守卫加固」的回滚备份（<20MB）

## 包含
- scripts/python_runtime_guard.py  -> 加固后的守卫（G盘解释器判为飞行风险）
- reports/reboot_diag*.txt         -> 重启根因诊断证据
- SKILL.md                         -> 四化迭代六端归档铁律
- RESTORE.py                       -> rollback / reapply / verify
- MANIFEST.json                    -> 各文件 sha256

## 根因一句话
G: = Seagate Expansion (USB 外置盘) 实测 Event ID 153 I/O 重试泛滥 + python313.dll 掉盘崩溃；
WorkBuddy/守卫/MCP 的运行时在 G 盘，G 盘一抖即集体崩溃 -> 被迫重启。
