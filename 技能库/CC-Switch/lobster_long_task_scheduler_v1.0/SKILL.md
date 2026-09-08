---
name: "lobster_long_task_scheduler_v1.0"
description: "通过 Hermes /v1/runs + 本地状态文件实现长任务断点续跑，并可生成 Windows 定时唤醒计划（默认不自动注册）。Invoke when 需要长任务不中断/定时唤醒/后台续跑。"
---

# 长任务：断点续跑 + 定时唤醒（Hermes runs）

## 安全边界

- 本技能不会打印任何 Token 明文；仅使用环境变量读取。
- “注册 Windows 计划任务/后台驻留”属于系统级修改：默认只生成命令与任务定义，不会自动写入系统，除非你明确授权并显式开启执行开关。

## 环境变量（仅变量名）

- `HERMES_BASE_URL`（默认 `http://127.0.0.1:8642`）
- `HERMES_API_TOKEN`（Bearer Token）

## 对外接口（函数）

- `skill_long_task_start(input_text: str, session_id: str | None = None) -> dict`
- `skill_long_task_wait(run_id: str, timeout_s: int = 60) -> dict`
- `skill_long_task_define_job(job_name: str, input_text: str, session_id: str | None = None) -> dict`
- `skill_long_task_emit_job(job_name: str) -> dict`
- `skill_long_task_plan_windows_schedule(job_name: str, every_minutes: int) -> dict`（默认不执行）

## 安全门控规则

- 本技能不会注册计划任务；只输出 `schtasks /Create ...` 命令文本。
- `input_text` 可能含敏感内容：默认仅记录长度与哈希用于可追溯，不落盘明文。

## 日志与可追溯

- 默认落盘路径：`.trae/skills/lobster_long_task_scheduler_v1.0/.lobster_state/reports/`
- job 定义落盘：`.trae/skills/lobster_long_task_scheduler_v1.0/.lobster_state/jobs/`

## 与 gstack/MEM 的对齐方式（不做系统修改）

- 每次调用后生成的审计 JSON + last_run 可作为后续复盘提炼输入。
