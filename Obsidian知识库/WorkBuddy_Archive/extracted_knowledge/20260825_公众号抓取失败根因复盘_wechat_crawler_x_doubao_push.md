---
title: 公众号抓取失败根因复盘（wechat_crawler × doubao/push）
summary: 2026-04-19 同一公众号 5 次抓取全部失败/零收益的根因链与修复 SOP
tags: [故障复盘, 爬虫, doubao-push, bs4, 运维知识]
source_files:
  - raw_original/20260824_174004_豆包学习材料_公众号文章汇总_20260419_023748.md
  - raw_original/20260824_174339_豆包学习材料_公众号文章汇总_20260419_025128.md
  - raw_original/20260824_174652_豆包学习材料_公众号文章汇总_20260419_025319.md
  - raw_original/20260824_175149_豆包学习材料_公众号文章汇总_20260419_025715.md
  - raw_original/20260824_175523_豆包学习材料_wechat_c_awle__v1.1 执行结果_20260419_030835.md
distilled_by: 龙虾五步法 V3.6 + 仓颉蒸馏(RIA-TV++) + 赛博书屋 v1.5
distilled_at: 2026-08-25
---

# 公众号抓取失败根因复盘（wechat_crawler × doubao/push）

> 萃取自 `raw_original` 下 5 份「豆包学习材料_公众号文章汇总 / wechat_crawler_v1.1 执行结果」归档（内容时间戳 2026-04-19 02:37–03:08，落盘于 2026-08-24）。
> 仓颉蒸馏定位：本批无新知识本体，**唯一可复用资产 = 抓取链路故障根因 + 修复 SOP**（反例/原则提取器产出）。

## 一、一句话摘要

同一篇公众号文章在 30 分钟内被反复抓取 5 次，**全部失败或零收益**；根因是三层叠加（Python 缺 `bs4` 依赖 → 本地 `doubao/push` 推送服务 500 → Hermes 本地连接中断），最终**没有任何文章内容进入知识库**。

## 二、事件时间线（原始归档）

| # | 内容时间 | 抓取阶段 | 结果 | 关键错误 |
|---|----------|----------|------|----------|
| 1 | 02:37:48 | 推送 | 失败 | `500 Server Error: INTERNAL SERVER ERROR for url: http://127.0.0.1:8080/doubao/push` |
| 2 | 02:51:28 | 抓取 | 失败 | `技能执行失败: No module named 'bs4'` |
| 3 | 02:53:19 | 抓取 | 失败 | `技能执行失败: No module named 'bs4'` |
| 4 | 02:57:15 | 抓取+总结 | 失败 | `bs4` 缺失 + AI总结 `('Connection aborted.', RemoteDisconnected(...))` |
| 5 | 03:08:35 | 爬虫 | success 但零收益 | `发现文章数: 1 / 新增落盘数: 0 / 知识库同步 成功: 0` |

目标 URL 始终为：`https://mp.weixin.qq.com/s/EFPs3rokogR5WqUECt9D5g`

## 三、根因链（三层，缺一即复发）

| 层 | 根因 | 现象 | 影响 |
|----|------|------|------|
| L1 依赖层 | 爬虫 Python 环境缺 `beautifulsoup4`（`bs4`） | `No module named 'bs4'` | 抓取阶段直接崩溃，拿不到正文 |
| L2 服务层 | `127.0.0.1:8080` 是 Hermes/Doubao 桌面端本地 HTTP 服务（`HERMES_BASE_URL` 默认 `http://127.0.0.1:8080`，实际推送路由 `/hermes/learn/file`，旧版为 `/doubao/push`），当时返回 500 | `500 INTERNAL SERVER ERROR` | 即便抓到也推不进豆包队列 |
| L3 模型层 | Hermes 本地推理连接被对端中断 | `Connection aborted / RemoteDisconnected` | AI 总结失败，无摘要产出 |

> 第 5 次虽报表 success，但「新增落盘 0 / 同步 0」说明：爬虫跑通了外壳，下游推送与落盘仍为空——**整条链路在当时实质是断的**，只是错误被吞成了 success。

## 四、修复 SOP（可复用）

### 4.1 依赖修复（L1）
```bash
# 用隔离的 WorkBuddy 托管 Python 安装 bs4，避免污染系统/损坏的 VNPY 环境
PY=C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe
$PY -m pip install beautifulsoup4 lxml
# 验证
$PY -c "import bs4; print('bs4 OK', bs4.__version__)"
```

### 4.2 推送服务修复（L2）【已实测定案 2026-08-25】
- **端口归属已确认**：`127.0.0.1:8080` 不是独立服务，而是 **Hermes/Doubao 桌面端本地 HTTP 服务**（`wechat_crawler_v1.1/main.py` L26：`DEFAULT_HERMES_URL = os.environ.get("HERMES_BASE_URL", "http://127.0.0.1:8080")`），实际推送路由为 **`/hermes/learn/file`**（L469），旧版才是 `/doubao/push`。
- **当前实测健康**：netstat 显示 127.0.0.1:8080 **无本地监听**（唯一 8080 是到远程 42.81.250.66 的出站连接）；`Doubao.exe` 在跑但未暴露该端点；上游 13460 模型代理 **DOWN（HTTP=000）**。
- **重抓前置**：必须先启动 Hermes/Doubao 桌面端使其在 127.0.0.1:8080 监听，并恢复 13460 代理，否则重抓必再失败。
- 存活检查命令：`curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/hermes/learn/file`（新版路由）。
- 端口角色对照（来自端口矩阵）：`15731=HY3混元代理`、`18808=Marvis`、`13460=AtomCode 模型代理`；`8080=Hermes/Doubao 桌面端本地服务`。

### 4.3 模型连接修复（L3）
- Hermes 本地推理连接中断多为上游代理（13460 AtomCode）超时/并发互斥；先跑健康检查 `curl -s http://127.0.0.1:13460/health`，确认 `lock_free==true` 再发起总结。

### 4.4 重抓验证清单
1. `bs4` 可导入 ✅
2. `doubao/push` 返回 200 ✅
3. Hermes 健康检查通过 ✅
4. 重抓同一 URL → 新增落盘数 > 0、知识库同步 > 0 才算闭环 ✅

## 五、原则 / 反例（仓颉蒸馏产出）

- **原则 P1**：爬虫依赖必须随技能包固化进隔离 venv，禁止依赖系统/共享 Python（VNPY 环境已损坏先例）。
- **原则 P2**：`success` 状态码不可信，必须校验「新增落盘数 / 同步数 > 0」才是真成功。
- **反例 C1**：5 次失败仍反复抓同一 URL，未做熔断/告警，浪费 30 分钟与本地算力——应「首次失败即告警 + 暂停重试」。
- **反例 C2**：错误被吞成 success（第 5 次），掩盖真实断链，延误根因定位。

## 六、四化迭代落点

- **智能化**：后续同类抓取任务，启动前自动校验 `bs4` 依赖 + `doubao/push` 存活，不通过不抓。
- **定制化**：归档命名已带 `raw_original/wechat_push_log/20260419/` 子目录隔离，避免与真正豆包聊天会话混淆（见 B 步骤）。
- **全自动化**：校验脚本纳入 `cangjie_bridge.py` 前置检查；失败自动记入 `temp/.ima_pending.log` 待重试。
- **自我净化**：5 份原始失败日志已迁至 `wechat_push_log/` 子目录，根因知识沉淀本卡，避免仓库根目录噪音（见 B/C 步骤）。

## 七、C 排查实测结论（2026-08-25 定案）

| 检查项 | 命令 | 实测结果 |
|--------|------|----------|
| 8080 监听 | `netstat -ano \| grep :8080` | ❌ 无本地监听；唯一 8080 为出站连接（pid 21348 → 42.81.250.66） |
| doubao 进程 | `tasklist \| grep -i doubao` | Doubao.exe 在跑，但未在 127.0.0.1:8080 暴露端点 |
| 上游模型代理 | `curl http://127.0.0.1:13460/health` | ❌ HTTP=000（DOWN）→ 印证 L3 Connection aborted |

**结论**：归档里的 500/断连 = 当时 Hermes/Doubao 桌面端根本没在 8080 提供 `/doubao/push`（旧路由）或 `/hermes/learn/file`（新路由）。**当前状态仍不满足重抓条件**（8080 无监听 + 13460 DOWN），需先恢复两条链路。爬虫本体定位：`技能库/CC-Switch/wechat_crawler_v1.1/`。

---

*本文由龙虾五步法 V3.6（成本优先 / 中文铁律）萃取，配套赛博书屋 v1.5 落盘规范、仓颉 RIA-TV++ 反例提取。C 步骤已实测定案（8080=Hermes 桌面端 / 13460=AtomCode 代理 / 双链路待恢复）。零外部 API，纯本地运算。*
