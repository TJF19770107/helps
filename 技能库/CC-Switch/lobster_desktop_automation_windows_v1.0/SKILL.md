---
name: "lobster_desktop_automation_windows_v1.0"
description: "在 Windows 上提供截图/窗口定位/控件枚举/点击/输入等桌面自动化能力（对标 Computer Use）。Invoke when 需要跨应用联动或自动化操作本机桌面。"
---

# Windows 桌面自动化（Computer Use 基座）

## 安全边界（必读）

- 本技能仅封装“本机桌面自动化”能力：截图、窗口定位、控件枚举、点击、输入。
- 任何涉及账号登录、支付、删除数据、安装软件、改系统设置的自动化动作，必须先得到用户明确授权。
- 依赖包缺失时，本技能默认只做“只读诊断/提示”，不会自行联网安装依赖。
- 默认不记录你输入的明文内容；对输入文本仅记录长度与哈希（用于可追溯但不泄露内容）。

## 依赖与前置

- 推荐依赖（其一可用即可起步）：`pywinauto`（UIA 控件级）、`pyautogui`（坐标级）
- 若你希望我自动安装依赖，需要你显式授权“允许联网安装 Python 依赖”（见下方验收步骤）。

## 对外接口（函数）

- `skill_desktop_screenshot(out_path: str) -> dict`
- `skill_desktop_find_windows(title_re: str | None = None) -> list[dict]`
- `skill_desktop_list_controls(title_re: str) -> str`
- `skill_desktop_click(coords: str | None = None, title_re: str | None = None, control_title_re: str | None = None) -> dict`
- `skill_desktop_type(text: str, interval_ms: int = 0) -> dict`

## 参数规范

- `out_path`：建议写入项目目录（例如 `E:\\Hermes_Return\\desktop\\shot.png` 或仓库内路径），避免误写系统目录。
- `title_re`：窗口标题正则（用于控件级定位）。
- `control_title_re`：控件标题正则（用于控件级点击）。
- `coords`：`"x,y"` 格式（坐标级点击），例如 `"120,300"`。
- `interval_ms`：每字符间隔毫秒数（输入节奏控制）。

## 安全门控规则

- `allow_install=false`（默认）：禁止联网安装依赖；只做只读诊断/提示。
- 需要安装依赖时，必须先由用户明确授权，然后才允许 `allow_install=true`。

## 日志与可追溯

- 默认落盘路径：`.trae/skills/lobster_desktop_automation_windows_v1.0/.lobster_state/reports/`
- 记录内容：动作类型、时间戳、参数脱敏摘要、结果状态（不含任何密钥明文与输入明文）。

## 与 gstack/MEM 的对齐方式（不做系统修改）

- 每次调用后生成的审计 JSON 可作为后续“记忆固化/复盘提炼”的输入，由 `lobster_skill_hub_invoke` 按需汇总入库。

## 验收（不含敏感信息）

1) 只读诊断（无需授权）
- 调用 `skill_desktop_find_windows()` 能返回当前可见窗口列表（若缺依赖会返回缺口提示）。

2) 完整验收（需要你授权后我才会执行）
- 安装依赖（可能联网下载）  
- 运行一次截图到指定路径  
- 在你指定的测试窗口内完成一次“点击 + 输入”
