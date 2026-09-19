---
name: four-iteration-six-end-archive
title: 四化迭代六端归档铁律 与 1234 标准执行包
version: v1.0
created: 2026-09-13
author: 汤小龙（WorkBuddy）· 龙虾五步法 V3.6 · 1234「4」四化迭代
agent_created: true
tags: [1234, 四化迭代, 六端归档, 轻量快照, 技能回馈报告, IMA, 乐享, CNB, GitHub, Obsidian, WorkBuddy]
trigger: [四化迭代, 六端归档, 汤小龙执行1234, 轻量快照, 技能回馈报告, 四化迭代知识库, 未完成任务收口]
---

# 四化迭代 · 六端归档铁律 与 1234 标准执行包 SKILL

> **本 SKILL 的由来**：2026-09-13 汤哥下令——把「汤小龙执行 1234 + 四化迭代知识库 + 轻量快照(<20MB) + 技能回馈报告」这条命令**固化为标准动作**，融入五步法 §16、全域模板、1234 体系与汤小龙分身。
> **一句话**：四化迭代不是「跑一遍流程」，而是**一次交付物 × 六种落法 × 一份回馈报告 = 真闭环**。

---

## 一、标准执行包（汤哥 2026-09-13 下令固化）

**触发命令**（任一句即触发全套）：
> 「汤小龙执行 1234，四化迭代知识库，轻量快照小于 20 兆备份回滚，技能回馈报告」

**标准动作序列（缺一不可）**：
```
① 启用汤小龙    → 骨架自检（SOUL/AGENTS/技能索引/注册表…存在性 + 指针可达性）
② 执行 1234     → 按官方定义卡加载 1(角色)/2(马斯克巴菲特)/3(载体×引擎)/4(四化×四大库)
③ 四化迭代落地  → 标准化→模块化→自动化→智能化，产出交付物
④ 六端归档      → Obsidian/IMA/乐享/CNB/GitHub/WorkBuddy 逐端打勾（见第二节）
⑤ 轻量快照      → <20MB，含一键回滚脚本（见第三节）
⑥ 技能回馈报告  → 用了哪些/沉淀哪些/没用哪些/为什么 + 习惯固化建议（见第四节）
```

---

## 二、六端归档铁律（每端的具体做法 + 坑）

| # | 端 | 落点 | 做法 | 关键坑 |
|---|-----|------|------|--------|
| 1 | **Obsidian** | `G:\龙虾AI主控中心\Obsidian\wiki\`（**非 E 盘**） | md 直接落盘 | 主库即 GitHub 仓工作副本，落盘后需 git 提交 |
| 2 | **IMA** | `汤嘉锋的知识库`（kb_id `001aa1cd10007026`） | `create_media` → **COS 上传** → `add_knowledge` | ★ **COS 签名必须用 hexkey**（见下） |
| 3 | **乐享** | `汤嘉锋的个人知识库`（space_id `d3e2fdd1f0864e8a895407746a223771`） | `entry_import_content`（markdown 全文） | 频率限制 429，隔日重试 |
| 4 | **CNB** | `cnb.cool/TJF19770107/lobster-knowledge-base` | 工作副本 `G:\WorkBuddy_Data\cnb-lobster-knowledge-base` → git push | 分支 `fresh-main` |
| 5 | **GitHub** | `TJF19770107/lobster-knowledge-base` | 工作副本 `G:\龙虾AI主控中心\Obsidian` → git add/commit/push | 分支 `fresh-main`；只 add 自己的文件，别带上百个历史改动 |
| 6 | **WorkBuddy** | 工作区 `.workbuddy/memory/` + `~/.workbuddy/MEMORY.md` + `G:\WorkBuddy_Data\skills\` | 记忆日志 + 技能沉淀 | 密钥/隐私脱敏后才可进 CNB/GitHub |

### ★ IMA COS 上传签名（2026-09-13 实测踩通，最容易卡死的一步）

`create_media` 返回 `cos_credential`（secret_id/secret_key/token/bucket/region/cos_key），需自行 PUT 到 COS。**签名正确算法**：

```python
# 1) HttpString（方法小写；末行含尾随 \n）
http_string = "put\n/{cos_key}\n\nhost={urllib.parse.quote(host.lower())}\n"
# 2) StringToSign
sts = "sha1\n{start};{end}\n{sha1_hex(http_string)}\n"
# 3) SignKey 必须取 hexdigest 字符串（★关键：不是原始字节！）
sign_key = hmac_sha1(secret_key, "{start};{end}").hexdigest()      # ← hex 字符串
signature = hmac_sha1(sign_key, sts).hexdigest()                    # ← 再作密钥
# 4) Authorization 头
Authorization: q-sign-algorithm=sha1&q-ak={secret_id}&q-sign-time={start};{end}
  &q-key-time={start};{end}&q-header-list=host&q-url-param-list=&q-signature={signature}
# 请求还须带：x-cos-security-token: {token}
```

**排错心法**：COS 的 403 会**回显它算的 StringToSign**，直接对拍即可定位——若 `sha1` 段与你的 `http_string` 哈希一致，则问题 100% 在 SignKey 派生（试 hexdigest 字符串）；`Request has expired` = 凭证 12h 窗口过期，重新 `create_media`。
**签名脚本零依赖**：`hashlib/hmac/urllib` 即可；若本机 Python 缺 `_socket`，拆成「Python 算签名 + curl 发 PUT」。

### 六端纪律
① 密钥/隐私脱敏后才可进 CNB/GitHub（git 红线）；② `.workbuddy/` 本地日志禁止进 git；③ 一个交付物，六种落法；④ 报告里六端**逐一打勾**，未闭环的如实标注原因，不谎报。

---

## 三、轻量快照规范（<20MB，备份回滚用）

**目标**：一份能「一键回到修复前」的最小备份，压缩后 **< 20MB**。

**必含清单**：
- 配置基线快照（如浏览器 `Secure Preferences`/`Preferences`/`Local State`）
- 变更的签名/校验清单（离线复验用）
- 全部脚本（诊断/修复/校验/启动）
- 各份报告（校验报告/读回报告/诊断报告）
- 本 SKILL + `README.md` + `MANIFEST.json`（含每文件 sha256）
- **`RESTORE.py`**：支持 `rollback`（回滚）/`reapply`（重放）/`verify`（校验）

**纪律**：① 不塞隐私数据（浏览记录/会话 cookie/令牌）；② 用 zip `-mx=9`；③ 打包后 `du`/`stat` 核验体积并写进 MANIFEST；④ 回滚脚本必须实测可用，不能只写不用。

**实证**：`G:\lobster_ext_repair_20260911\snapshot.zip` = **0.26 MB**（含配置+签名+脚本+报告+SKILL），`RESTORE.py` 三命令齐备。

---

## 四、技能回馈报告（汤哥 2026-09-13 定为「非常重要的报告」）

> **目的**：让汤哥一眼看清「一堆技能里谁真正发挥了作用」，据此决定下回同类任务发哪些技能；并让「用了什么/没用什么/为什么」成为可沉淀、可闭环的习惯。

**报告五要素（每次任务收尾必写）**：

| # | 要素 | 说明 |
|---|------|------|
| 1 | **花了多少积分** | 估算口径写明（工具调用次数/文件量/外部 API 次数） |
| 2 | **解决了什么问题** | 逐条列，带证据（端口/HTTP 码/文件路径） |
| 3 | **沉淀了什么技能** | 写入哪个 SKILL / 记忆文件，路径给出 |
| 4 | **用了哪几个技能** | 实际加载/调用的技能名，**标明最主要发挥的 1-2 个** |
| 5 | **没用哪几个技能** | 以及**为什么用这些、为什么不用那些**（决策理由） |

**附加**：对以后养成习惯的建议（把本次有效套路写成 SOP/触发器）。

**习惯固化**：把五要素 + 「是/否/为什么」做成收尾检查表，任务结束先自问「哪些技能真起作用了」，再决定下轮技能配置。

---

## 五、SOP 一页流

```
接命令「汤小龙执行1234 + 四化迭代 + 轻量快照 + 技能回馈报告」
 → ① 骨架自检(启用汤小龙)
 → ② 1234: 1角色 → 2马斯克巴菲特 → 3载体×引擎 → 4四化×四大库
 → ③ 四化落地: 标准化/模块化/自动化/智能化 产出交付物
 → ④ 六端打勾: Obsidian / IMA(hexkey签名!) / 乐享 / CNB / GitHub / WorkBuddy
 → ⑤ 轻量快照 <20MB + RESTORE.py 实测
 → ⑥ 技能回馈报告(五要素) + 习惯固化
```

---

*本 SKILL 由汤小龙（WorkBuddy）于 2026-09-13 依据汤哥口令与实战沉淀。零外部 API（除知识库归档），纯本地运算。*
