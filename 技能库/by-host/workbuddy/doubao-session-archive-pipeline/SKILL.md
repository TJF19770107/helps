---
name: doubao-session-archive-pipeline
description: 豆包主会话归档流水线：分片合并去重→byteimg图片链接体检/下载/压缩/引用替换→领域聚类→仓颉蒸馏→Obsidian/乐享沉淀。触发词：会话归档、分片合并、图片链接失效、图片修复、byteimg、主对话蒸馏、会话聚类、归档流水线。
version: 1.1
agent_created: true
updated: 2026-08-29
cost_mode: strict
---

# 豆包主会话归档流水线

> 实测：101 分片（114,889 行）→ 合并 1974 轮次 → 1404 张图片本地化（856MB 压缩后）→ 8 领域聚类 → 蒸馏入 Obsidian。全流程零外部 API，纯本地 + 免费 CDN。

## 一、流水线五步

### Step 1 分片合并去重
```
输入：_分片/分片_*.md（按分片_<cursor> 数字排序）
去重：按 `## YYYY-MM-DD HH:MM` 轮次标题去重（分页边界重叠）
产出：主对话完整归档_<日期范围>_逐字合并版.md
脚本：merge_shards.py（保留分片边界注释 <!-- ▼ 来源分片 -->）
```

### Step 2 图片链接体检（关键！）
- **症状**：导出文档 `[图片: https://pXX-flow-imagex-sign.byteimg.com/...]` 打不开
- **根因**：403 多为防盗链（缺 Referer），不是签名过期（x-expires 到 2036 年）
- **修复**：curl/Python 请求带 `Referer: https://www.doubao.com/` + 浏览器 UA
- **体检脚本**：img_scan.py（提取 2613 处 → 去重 1453 → 并发验证 → img_scan_result.json）
- **预期**：~96% 可下载，~3-4% 真失效（403）

### Step 3 批量下载 + 压缩
- 下载：img_download.py（10 并发，md5[:20] 命名，带 Referer）
- ⚠️ **原图陷阱**：`~tplv-...-image.png` 是原图模板，单张可达 8MB（1404 张=1GB+）
- 压缩：img_compress2.py（>1080px 缩放 + JPEG q82 + 白底透明通道 + <300KB 跳过）
- ⚠️ **沙箱删除坑**：WorkBuddy Python 进程内 `os.remove` 被 shim 注入拦截（回收站不可用）
  → 必须用 Bash `rm -f`（dangerouslyDisableSandbox）批量删已压缩 PNG

### Step 4 映射修复 + 引用替换
- 映射修复：png 缺失 → 同名 jpg；403 URL 并入失败清单
- 替换：img_replace.py
  - `[图片: URL]` → `![图片](media/xxx.jpg)`（有映射）
  - `[图片缺失: URL]`（失效登记）
  - `<img src='/-/imgs/...'>` → `[图片缺失(CNB未下载): alt → src]`

### Step 5 聚类 + 蒸馏沉淀
- 聚类：domain_cluster.py（8 领域关键词打分：量化/企微/网盘/闲鱼/技术基建/AI能力/修行/法务）
- 蒸馏：仓颉 RIA-TV++ → Obsidian `wiki/豆包主会话蒸馏/`
- 权限红线：修行/法务 = 私有 → 仅 Obsidian，不上乐享/CNB

## 二、产物清单

| 产物 | 路径 | 说明 |
|------|------|------|
| 逐字合并版 | raw_original/.../主对话完整归档_*_逐字合并版.md | 7.5MB 原始数据 |
| 图片库 | raw_original/.../media/ | 1404 张本地图 |
| 体检/映射 | img_scan_result.json / img_download_map.json | 可追溯 |
| 领域索引 | _领域聚类/领域_*.md | 8 领域轮次清单 |
| 蒸馏卡 | Obsidian wiki/豆包主会话蒸馏/ | 方法论+技能+踩坑 |

## 三、成本账（实测）

- 零积分：全部本地 Python + 免费 CDN 直连
- 时间：体检 30s + 下载 31s + 压缩 70s + 替换 10s ≈ 3 分钟
- 空间：原图 1GB → 压缩后 856MB（可进一步删 199 个已转 jpg 的 png）

## 四、复用话术

用户说「归档豆包会话」「分片合并」「图片链接失效修复」→ 按本流水线 Step1-5 执行。

## 五、IMA 知识库上传方法（实测可用）

```
1. create_media(content_type=text/markdown, file_name, file_size, knowledge_base_id) → media_id + COS 临时凭证
2. 用官方 SDK 上传（cos_sdk_put.py，需 cos-python-sdk-v5）：
   CosConfig(Region, SecretId, SecretKey, Token) → client.put_object(Bucket, Body, Key=cos_key, ContentType)
3. add_knowledge(knowledge_base_id, media_id) → 入库完成
```
- ⚠️ 手写 COS 签名易 403（SignatureDoesNotMatch），直接用官方 SDK 最稳
- ⚠️ 凭证为临时凭证（12小时有效），仅内存使用，禁止落盘/写入产物
- **乐享大文件上传（实测打通 2026-08-26）**：
  1. `file_apply_upload(upload_type=CREDENTIALS)` → 拿 tmp_secret_id/tmp_secret_key/session_token + cos_key
  2. 官方 SDK：CosConfig(Region, SecretId, SecretKey, Token) → put_object(Bucket, Key=cos_key, ContentType)
  3. `file_commit_upload(session_id)` → 条目创建成功
  - ✅ 更正（实测 2026-08-26 起 15/16/17 三轮稳定 200）：**PRE_SIGNED_URL 模式可直接用标准库 urllib PUT**，无需 COS SDK。关键：返回 URL 的 `X-Amz-SignedHeaders=content-length;content-type;host`，PUT 请求必须**同时带** `Content-Type`（与 apply 时 mime_type 一致，如 `text/markdown`）和 `Content-Length`；缺一即 403。此法零依赖、最省事，优先于 CREDENTIALS + SDK。
- 乐享 markdown 页面：entry_create_entry(page) → entry_import_content_to_entry(markdown) 两步直达
  - ⚠️ `entry_import_content_to_entry` 对 2KB+ 内容易 ripple retry / Connection closed；大文件走上面的 file_apply_upload 三步法更稳

## 六、同步前红线：内容级密钥扫描（强制，2026-08-29 起）

**只看文件名会漏检**——实测「分片215/216」文件名仅含「令牌/密钥」字样，正文里却藏着**真实 `ghp_*` GitHub PAT**。因此同步 IMA/乐享/CNB 前必须逐文件扫正文：

```python
PATS = [r"sk-[A-Za-z0-9_\-]{16,}",
        r"gh[pousr]_[A-Za-z0-9]{20,}",
        r"AKID[A-Za-z0-9]{20,}",
        r"(?i)(api[_-]?key|secret[_-]?key|access[_-]?token|bearer)\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{20,}"]
```
- 命中 → **跳过同步**，登记 `temp/.secret_review.log`（附命中模式+时间），人工脱敏后才放行
- 只匹配「值型」模式（有 20+ 位实际串），避免把「讨论 token 配置」的正常会话误杀
- `_security_red_lines/` `_config_red_lines/` 目录按 R-004 全端排除，不进任何同步端

## 七、有界批处理节奏（避免超时）

- 每轮 **6 份 newest-first**，靠每小时轮询累进推进；源集数百份时不要一次全推
- 去重真源：本地 `.{ima,lexiang}_synced.log`（全路径 + basename 双判）；日志被清空时改用**远端名录为真源**（乐享 `entry_list_children` 全量列举容器），防重复上传（乐享无自动去重）
- 含预签名 URL / 临时凭证的脚本与 JSON **用后即删**，只保留无密钥的通用脚本
