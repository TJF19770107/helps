---
title: 本地目录到乐享知识库镜像同步 Skill
summary: 一句话把本地文件夹 1:1 镜像上传到乐享知识库，含建目录、三段式上传、MIME/VOD 陷阱、分页幂等、扩展名黑名单与同步报告。
tags: [乐享, 知识库, MCP, 同步, 镜像上传, 四化]
source: 2026-08-31 extracted_knowledge 实测跑通；2026-09-01 pipeline/.workbuddy/AI分身出片 复跑
distilled_by: 龙虾五步法 V3.6 + 四化迭代
distilled_at: 2026-08-31
version: v1.1
protocol: 全域模板 #331
---

# 本地目录 → 乐享知识库镜像同步

> 触发词：`乐享同步` / `镜像上传乐享` / `本地目录传乐享` / `乐享folder sync` / `四化迭代知识库`。
> CLI 对话框快捷触发：`1234 四化迭代知识库` / `四化迭代知识库` / `乐享同步`；直接执行批量脚本时输入 `!sync`。
> 一句话：给本地目录和乐享目标父节点，自动建目录、传文件、出报告，文件名与层级 1:1 不变。
> 「四化迭代知识库」触发时，先完成 Obsidian/本地复盘，再执行本技能乐享回灌；未给路径时默认同步 `豆包主会话全集/extracted_knowledge` 到 `示例知识库/豆包主对话YYYYMMDD/extracted_knowledge`。用户给了源路径或目标父节点时，用户路径优先。

## 固定常量

- MCP 端点：`https://mcp.lexiang-app.com/mcp?company_from=6b07973e956b11f1b7af52cac8085d19&preset=meta`
- 鉴权：`Authorization: Bearer <LEXIANG_TOKEN>`，token 只进内存，不落盘不进报告
- 默认知识库：示例知识库 `space_id=1de96cbcd92a4c479c7adacfa4f4724a`
- 默认目标父节点：豆包主对话YYYYMMDD 下的 `extracted_knowledge`
- 参考脚本：`我的AI分身/豆包主会话全集/temp/lexiang_batch_sync.py`（通用批量版；单目录旧脚本 `lexiang_mirror_sync.py` 保留）

## 标准流程

1. 读本地源目录，收集全部子目录与文件；报告文件自身排除。
2. 在乐享目标父节点下按层级 `entry_create_entry(folder)` 补齐缺失目录；`entry_list_children` 必须全分页去重，父节点可能超过 100 项。
3. 文件上传三段式：`file_apply_upload` 拿 `session_id` 与 `upload_url` → HTTP PUT 原始字节 → `file_commit_upload`。
4. 上传顺序：先子文件夹文件，后根目录文件；同名已存在即跳过，不覆盖乐享旧文件。乐享列表里的文件名常隐去扩展名，幂等比对必须同时看 `原名` 与 `去扩展名`。
5. 输出同步报告：新建目录、成功清单、跳过清单、失败清单、云端校验结果。

## 已踩坑与铁律

- 普通文件 `apply_upload` 返回 `data.session.session_id` 和 `data.session.objects[0].upload_url`。
- 音频/视频走 VOD：返回 `data.client_upload_session`，对象是单数 `object`，PUT 必须带 `object.auth.Authorization` 和 `x-cos-security-token: object.auth.XCosSecurityToken`。
- Windows Python/urllib 对部分预签名 URL 会触发 COS 签名差异；PUT 推荐用 `curl.exe --upload-file`，只设置申报的 Content-Type，内容不转换。
- Windows Python 对 `.md` 猜不出 MIME，必须显式映射：`.md → text/markdown`，`.json → application/json`；否则服务端按扩展名登记 text/markdown，PUT 时 `SignatureDoesNotMatch` 403。
- `entry_list_children` 要带 `page_token` 翻页，直到空页或 token 重复；单父节点可能超过 100 项，只看一页会重复建目录。
- 0 字节文件（如 `.gitkeep`）与平台不支持的扩展名会被 `apply_upload` 拒绝（code 51 或 30010005）；按规则标记跳过，不中断整体。
- `.ps1/.bat/.cmd/.exe/.dll` 等扩展名被乐享平台拒绝；不改名、不转格式，标记待手动处理。
- token 有效期到 2026-09-30，到期需到 lexiangla.com/mcp 刷新。

## 验收标准

1. 乐享端子项数量与本地一致（文件夹数 + 可上传文件数，空文件和平台拒绝项除外）。
2. 报告中失败清单为空；跳过项有明确原因。
3. token 未写入任何文件；报告落盘在源目录。
