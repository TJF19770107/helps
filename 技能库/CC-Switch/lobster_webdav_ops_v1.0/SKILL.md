---
name: "lobster_webdav_ops_v1.0"
description: "通用 WebDAV 文件操作（列目录/下载/上传/建目录）并可生成学习索引输入。Invoke when 需要对接 WebDAV 网盘或批量处理远端文件。"
---

# WebDAV 通用文件操作（网盘能力基座）

## 安全边界

- 凭据仅允许通过环境变量注入：`LOBSTER_WEBDAV_URL`、`LOBSTER_WEBDAV_USER`、`LOBSTER_WEBDAV_PASS`。
- 本技能不会输出任何凭据明文；只返回“是否已设置/请求是否成功”等状态信息。
- 网页版网盘自动登录属于账号敏感操作，默认不做；若要做，必须你显式授权，并优先走“只读抓取/最小权限”。

## 对外接口（函数）

- `skill_webdav_list(remote_path: str = "/") -> dict`
- `skill_webdav_download(remote_path: str, local_path: str, confirm: bool = False) -> dict`
- `skill_webdav_upload(local_path: str, remote_path: str, confirm: bool = False) -> dict`
- `skill_webdav_mkdir(remote_path: str, confirm: bool = False) -> dict`

## 约定

- `remote_path` 以 `/` 开头（例如：`/docs/`、`/docs/a.txt`）。
- `LOBSTER_WEBDAV_URL` 为 WebDAV 根 URL（例如 Nextcloud 常见为 `https://host/remote.php/webdav`）。

## 安全门控规则

- 只读：`list` 默认允许执行。
- 写入类动作（需要用户明确授权后才能执行）：`download/upload/mkdir` 必须显式传入 `confirm=true`。

## 日志与可追溯

- 默认落盘路径：`.trae/skills/lobster_webdav_ops_v1.0/.lobster_state/reports/`
- 记录内容：动作类型、时间戳、路径摘要、结果状态（不含任何凭据明文）。

## 与 gstack/MEM 的对齐方式（不做系统修改）

- 每次调用后生成的审计 JSON 可作为后续记忆固化/复盘提炼输入。
