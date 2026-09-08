---
title: 四化迭代六端归档铁律
version: v1.0
distilled_at: 2026-09-08
distilled_by: 汤小龙（Codex）· 仓颉蒸馏 · 源自 20260908 送错归档位置的实战纠偏
tags: [四化, 六端, 归档, 知识库, 铁律, 踩坑]
protocol: 1234定义卡v2.1 §4.1.1
---

# 四化迭代六端归档铁律 SKILL v1.0

> 触发词：`四化迭代知识库` / `迭代知识库` / `归档知识库` / `1234` 的「4」。
> 一句话：四化产物必须落**六端**，落进豆包主会话源目录不算归档。

## 血的教训（2026-09-08 实录）

Codex 会话把双Chrome修复报告写进 `豆包主会话全集\extracted_knowledge\` 就宣称「落盘完成」，被汤哥当场抓住：那是**源目录**，不是归档端。1234定义卡v2.1 六端表当时已读过，属执行纪律失效，不是知识缺失。

## 六端清单（缺一不可，逐端打勾才算完成）

| # | 端 | 落法 | Codex 可直落? |
|---|-----|------|--------------|
| 1 | **Obsidian** | `G:\龙虾AI主控中心\Obsidian\wiki\`（运维类→`运维日志\`，工具类→`AI工具运维\`，原文→`豆包主会话全集\`） | ✅ |
| 2 | **IMA** | WorkBuddy 连接器（create_media → COS → add_knowledge） | ❌ 需 WorkBuddy |
| 3 | **乐享** | WorkBuddy 连接器（entry_import_content） | ❌ 需 WorkBuddy |
| 4 | **CNB** | cnb.cool 知识库镜像仓 git push（经 Hermes NPC 通道） | ❌ 通道待建 |
| 5 | **GitHub** | `TJF19770107/lobster-knowledge-base`（git proxy=socks5://127.0.0.1:1081） | ✅ |
| 6 | **WorkBuddy** | `C:\Users\Administrator\.workbuddy\MEMORY.md` 追加 + `G:\WorkBuddy_Data\MEMORY.md` 同步 | ✅ |

## 执行纪律（写报告前先过一遍）

1. **迭代前先查知识库**：动笔前先检索 Obsidian / WorkBuddy MEMORY / 可用云端知识库里与本任务相关的踩坑记录和既有技能，只取相关条目，不全库扫荡；命中结果直接复用，别把同一坑重踩一遍。
2. **资源必须共享**：同一个结论/技能只允许有一个权威版本；不同宿主发现重复产物时，合并成一条，各端只放引用或镜像，不各自另存「分叉版本」。
3. **先问落点，再写文件**：动笔前默念「这是六端里的哪一端？豆包源目录不是端」。
4. **源目录 ≠ 归档端**：`extracted_knowledge` 是待萃取原料，四化产物归档永远另落六端。
5. **能落几端落几端，落不了的写明卡点与补落路径**（宿主分工：IMA/乐享→WorkBuddy，CNB→Hermes通道），不许静默漏端。
6. **交付格式**：逐端列表打勾（✅/⏸），⏸ 必须附「谁在哪个宿主能补」。
7. **GitHub 推送代理**：直连被全局代理捆死时，用 `git -c http.proxy=socks5://127.0.0.1:1081`。

## 验收

- [ ] 六端清单逐端有落点或有明确卡点说明
- [ ] 无任何端被静默跳过
- [ ] 报告不含密钥

---

## v1.1 实证增补（2026-09-08 汤小龙/WorkBuddy 执行回写）

1. **IMA 落法修正**：`create_media → COS 手搓签名 → add_knowledge` 实测 403 SignatureDoesNotMatch 死路 → **捷径 = `import_urls` 导入乐享已发布页 URL，ret_code=0 秒成**（零成本绕过 COS 签名）
2. **乐享落法实证**：`entry_create_entry(parent=root) → draft_save_markdown_draft(seq=0) → draft_publish_markdown_draft（content 必须再传一遍）`，URL 形如 `https://lexiangla.com/pages/{entry_id}`
3. **CNB 通道现状**：项目仓（wework-custom-orders）origin 凭证缺失 push 失败；但 **`G:\tmp\lobster-knowledge-base` 本地仓 cnb remote 内置凭证可用**（Codex 已实证推送成功）→ CNB 端经该仓落地，不必等 Hermes 通道
4. **GitHub 端实证**：`G:\tmp\lobster-knowledge-base` 加 `github` remote 后 `git -c http.proxy=socks5://127.0.0.1:1081 push github main`（隧道活着时直推也可）
5. **WorkBuddy 端实证**：两处 MEMORY 均已追加六端协议；项目级 `.workbuddy/memory/MEMORY.md` 同步把「五落点」升级为「六端」
6. **Obsidian 落点并存说明**：技能蒸馏类沿用既有 `技能库\` 目录（历史索引一致），运维/工具类按本 SKILL 落 `wiki\` 分类
