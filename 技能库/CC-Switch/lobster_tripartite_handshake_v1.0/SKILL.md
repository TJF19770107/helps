---
name: "lobster_tripartite_handshake_v1.0"
description: "三方握手：校验并固化 Hermes↔Trae↔豆包链路。Invoke when 任一方发起任务/复盘/同步/技能更新，或需要排查三方连通/版本/权限不一致。"
---

# 龙虾永续进化 · 三方共振通信握手（固化版 v1.0）

技能名称：三方共振通信握手（固化版）  
技能标识：lobster_tripartite_handshake_v1.0  
版本号：v1.0  
更新时间：2026-04-28  
核心目标：建立并维护「Hermes-Trae-豆包」三方通信链路，为分布式共振进化提供物理层、通信层、应用层的完整支持。  

## 触发条件（适用场景）

- 任意一方发起：任务执行 / 复盘 / 同步 / 技能更新
- 任意一方出现：链路不通、响应异常、版本不一致、权限令牌缺失或口径不统一

## 固化流程（固定顺序）

1) 物理层校验：检查三方节点 IP/端口连通性，输出连通状态报告  
2) 通信层握手：尝试心跳探测（HTTP 响应/状态码），确认在线状态与协议可达  
3) 应用层确认：校验技能版本、索引文件、权限令牌“是否已设置”，确保同步口径统一  
4) 链路固化：将成功节点写入链路配置（JSON），后续任务优先复用；离线节点自动标记并下次重试  

## 通信异常处理规则（硬口径）

- 单节点离线：跳过该节点，与在线两方继续；报告中标记离线节点与重试建议  
- 全链路异常：进入本地降级模式；生成待同步日志（不含敏感值），链路恢复后补发  
- 权限/版本不匹配：写入待同步日志并提示触发“增量同步”；完成版本对齐后再握手  

## 安全门禁（必须）

- 脚本不自动生成/写入任何密钥；仅检查环境变量是否已设置（SET/EMPTY），并按缺口提示由用户手动注入

## 产物与落盘（默认）

- 一键脚本（任意节点可运行）：
  - PowerShell：`handshake.ps1`
  - Shell：`handshake.sh`
- 链路固化文件：默认落盘到脚本同级的 `.lobster_state/tripartite_handshake_link.json`（可通过环境变量覆盖）
- 待同步日志：默认落盘到 `.lobster_state/tripartite_pending_sync.json`

## 脚本用法（推荐）

PowerShell（Windows）：

```powershell
pwsh -File .\.trae\skills\lobster_tripartite_handshake_v1.0\handshake.ps1 -Repair 0
```

Shell（Linux/macOS）：

```bash
bash ./.trae/skills/lobster_tripartite_handshake_v1.0/handshake.sh
```

## 完整技能文档（同源口径）

- 共享技能库（权威源）：`E:\龙虾AI主控中心\共享技能库\全局技能库\TRAE_20260428_lobster_tripartite_handshake_v1.0.md`
