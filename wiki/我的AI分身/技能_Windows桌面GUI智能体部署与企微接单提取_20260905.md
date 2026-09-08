---
title: 技能_Windows桌面GUI智能体UFO部署_企微接单信息提取
tags: [UFO, GUI-Agent, 企业微信, 接单自动化, 四化迭代, 汤小龙]
distilled_at: 2026-09-05
---

# Windows 桌面 GUI 智能体（UFO）部署与企微接单提取

## 硬件侦察结论（2026-09-05 实测）

- 本机无独立显卡（仅 Intel UHD 730 核显），nvidia-smi 不存在。
- UI-TARS/Qwen-GUI 本地量化模型需要 6-8G 显存，本机不可行。
- 结论：**微软 UFO + 云端视觉模型**（TeamoRouter 0.01折 glm 系列）是本机最优解。UFO 的控件树识别纯 CPU 可跑，视觉理解走 API。

## UFO 已落地

- 源码位置：`E:\龙虾AI主控中心\我的AI分身\tools\UFO`（官方 microsoft/UFO，depth=1 克隆）
- 网络要点：git clone 走 `git -c http.proxy=socks5h://127.0.0.1:1081`（本机直连 GitHub 被墙）
- 待办：创建 `config/gpt_config.yaml`，host 填 TeamoRouter 兼容端点，模型填 glm-5.3-flash-free 系列；API Key 从环境变量 `TEAMOROUTER_API_KEY` 读，零硬编码。

## 企业微信数据两条路（已验证的事实）

1. **历史库直读：不可行（已实测）**
   - `message.db` 是 SQLCipher 加密 SQLite，裸 sqlite3 连接报 `file is not a database`。
   - 库位置：`G:\DiskMigration\D_WXWork\1688857769689155\Data\message.db`（813MB，另有 800MB 备份副本）。
   - 解密密钥在运行中的企微进程内存里，需密钥提取工具或内存 dump。
2. **视觉读取：可行，是主路线**
   - 用 UFO/Orca computer-use 操作正在运行的企微界面，逐群读取接单信息。
   - 优点：读到的是最新消息，不需要管理员审批机器人，绕开权限麻烦。
   - 边界：长链路任务要拆短（打开群→滚屏→截图→提取→退出），单段成功率才高。

## 接单信息提取流程（标准作业）

1. UFO/Orca 打开企微 → 定位接单群 → 滚动加载新消息。
2. 截图发给视觉模型，提取结构化字段：客户/需求/价格/时间/联系人。
3. 写入 ` Obsidian wiki/Projects/企微接单流水/`，按日期归档。
4. 定价参考历史 `message.db` 解密数据（未来解锁后回灌）。

## 经验沉淀

- 遇到"读不了数据库"先测是不是 SQLCipher 加密，别在裸 SQLite 上浪费时间。
- 无独显机器选 GUI Agent：优先控件树方案（UFO），视觉部分用云端便宜模型。
- git/GitHub 被墙统一走 socks5h://127.0.0.1:1081 代理。
