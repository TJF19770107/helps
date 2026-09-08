---
name: pan-auto-learn
description: 网盘课程资源自动化学习闭环：分享链接→自动转存→编目→下载→仓颉蒸馏→IMA/乐享知识库沉淀。触发词：网盘转存、网盘学习、百度网盘、自动转存、课程转存、网盘抓取、playwright pan、pan auto learn。
version: 1.0
agent_created: true
updated: 2026-08-21
cost_mode: strict
---

# 网盘课程资源自动化学习闭环

> 全程零积分（Playwright 本地 RPA + 百度网盘 MCP + 仓颉规则蒸馏 + IMA/乐享 MCP）。
> 实测：8 门课程全部自动转存到本人网盘，1 个工作日内编目+蒸馏+双库同步完成。

## 一、核心能力

1. **批量转存**：百度网盘分享链接（带提取码）→ 自动登录 → 逐个转存到本人账号
2. **结构化编目**：转存后用 MCP `file_list/file_doc_list` 拿到真实目录树（无需 DOM 解析）
3. **本地下载**：浏览器自动化把文档类（PDF/Word/PPT/Excel）下载到 `E:/龙虾AI主控中心/课程资料库`
4. **零成本蒸馏**：规则化提取课程名/标签/模块/接单锚点 → 仓颉 RIA-TV++ 卡片
5. **双库同步**：乐享（权威源）+ IMA（镜像）通过 MCP `add_knowledge` / `block_update_page` 推送

## 二、关键脚本（已实测）

| 脚本 | 路径 | 功能 |
|------|------|------|
| 转存器 | `jiedan_pipeline/tools/baidu_pan_transfer_bot.js` | 8 门课 Playwright 自动转存 |
| 登录器 | `jiedan_pipeline/tools/baidu_pan_login_only.js` | 仅登录扫码，30 分钟等待 |
| 转存结果 | `jiedan_pipeline/outputs/pan_transfer_result.json` | 8 个 success |
| 蒸馏器 | `jiedan_pipeline/tools/cangjie_distill.py` | 规则化蒸馏为 RIA-TV++ 卡片 |

## 三、核心坑（一次性记住）

| 坑 | 解决方案 |
|----|---------|
| 百度网盘 MCP 只能管本人网盘，他人分享链接需"转存" | 先用 Playwright RPA 转存到本人账号 |
| 分享链接里含 U+2011 等非标准连字符 | `url.replace(/[\u2010-\u2015]/g, '-')` 清洗 |
| 第 4 课程后弹窗未关闭导致 `ERR_ABORTED` | 每课程用 `context.newPage()` 独立标签 |
| config.yaml 缩进错 | 全部用 2 空格对齐 |
| Playwright 找不到模块 | `export NODE_PATH="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules"` |
| 登录超时 | 拆出 `baidu_pan_login_only.js`，先扫码再跑转存 |
| 百度 MCP 429 限流 | 等待重置（错误信息会给具体时间） |
| 精准搜课程用专属关键词 | 广搜返回 1.5TB 存量噪声 |

## 四、四化落地

- **智能化**：Playwright RPA 自动登录/转存 + 关键词自动匹配 + 错误自动重试
- **定制化**：适配汤哥环境（百度网盘账号 133*****380 / E盘归档目录 / 8 门课标签化）
- **全自动化**：转存结果落 JSON、编目落 JSON、蒸馏卡片落 MD、双库同步落 MCP
- **自我进化**：仓颉 RIA-TV++ 蒸馏 + 课程萃取卡片迭代 + 月度巡检 automation

## 五、与企微自动接单的衔接

转存+蒸馏后的课程标签/锚点直接喂给 `wecom_ws_bot.py`：
- 关键词"电商"→ 命中课程《AIGC+电商实战课》→ 推送详情页话术
- 关键词"AI Agent"→ 命中课程《微软AI Agent零基础入门实战课》→ 推送架构话术
- 关键词"短视频"→ 命中课程《视频号分成计划懒人玩法》→ 推送爆款脚本话术

## 六、零积分说明

- Playwright 本地浏览器自动化：0 积分
- 百度网盘 MCP：免费接口
- 仓颉规则蒸馏：本地 Python 脚本，0 积分
- IMA/乐享 MCP：免费
- 唯一人工点：首次登录扫码（10秒），之后全自动

## 七、版本日志

- V1.0 (2026-08-21)：基于 8 门网盘课程实测转存+编目+蒸馏流程沉淀
