---
name: "lobster_tunnel_env_mcp_universal_v1.0"
description: "三合一固化：FRP 隧道 + SecureCode兼容密钥管理 + MCP(TLS)认证流转，一键建立云端Agent↔本地容器安全链路并输出验收报告。Invoke when 需要自动连通与自检固化。"
---

# 龙虾永续固化 · 云端Agent↔本地容器 一键安全连通（三合一 v1.0）

技能名称：云端Agent↔本地容器 一键安全连通（三合一）  
技能标识：lobster_tunnel_env_mcp_universal_v1.0  
版本号：v1.0  
更新时间：2026-05-01  
技能定位：实现「云端 Agent ↔ 本地容器」一键全自动连通的通用固化技能（网络隧道 + 密钥管理 + MCP 认证流转）。  

## 硬性边界（与全局规则对齐）

- 不在任何仓库文件/日志中明文落盘密钥；密钥仅以“加密形态”落盘，运行时通过环境变量/受保护存储注入。
- 脚本输出仅包含状态与路径，不回显任何密钥/令牌/证书私钥内容。
- 无需交互输入（默认全自动）；如缺少必要环境变量则进入“只读自检”并输出缺口提示。

## 三合一模块（缺一不可）

1) **内网穿透模块（FRP）**
   - 自动生成 FRP 配置并启动 frps/frpc（Docker 方式默认本地自测；生产模式支持把 frps 部署到公网 VPS）
   - 支持断线自动重连（frpc 设置 loginFailExit=false 等）
   - 支持把本地 MCP HTTPS 端口映射到“远端可访问端口”

2) **密钥管理模块（SecureCode MCP 兼容实现）**
   - 自动生成 AES-256 与 RSA-4096（以及 TLS 证书材料）
   - 以受保护存储（DPAPI 加密文件）落盘，并写入“非敏感”的 .env.example 变量名与路径指针
   - 密钥不向 AI 明文暴露：脚本与报告只回传路径/是否已设置

3) **MCP 认证流转模块（SecureCode MCP 兼容实现）**
   - 启动本地 SecureCode MCP HTTPS 服务（TLS 1.3 优先，最小 TLS 版本强制为 1.3）
   - 从受保护存储加载认证材料，对 MCP 请求执行 Bearer 校验
   - 提供 MCP 工具：status / rotate / echo（用于验收与排障）

## 固化流程（固定顺序，串行执行）

1) 启动 FRP 隧道（自测模式：本机 frps+frpc；生产模式：仅启动 frpc，frps 由公网侧提供）  
2) 生成安全密钥并写入受保护存储（同时只更新 .env.example 的变量名/路径指针）  
3) 启动 SecureCode MCP（HTTPS）服务，加载受保护存储中的密钥配置  
4) 通过 MCP 初始化与工具调用完成认证校验，并验证“通过 FRP 映射端口也可访问”  
5) 输出连通状态报告（JSON，脱敏）  

## 一键用法（Windows 推荐）

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\.trae\skills\lobster_tunnel_env_mcp_universal_v1.0\run.ps1
```

## 产物与落盘（默认）

- 运行日志与报告：`.trae/skills/lobster_tunnel_env_mcp_universal_v1.0/.lobster_state/`
- 受保护密钥存储：`.trae/skills/lobster_tunnel_env_mcp_universal_v1.0/.lobster_state/securecode/secrets.dpapi`
- TLS 证书材料（PEM，私钥文件仅本机 ACL 可读）：`%LOCALAPPDATA%\LobsterSecureCode\tls\`
- FRP 配置与 compose：`.trae/skills/lobster_tunnel_env_mcp_universal_v1.0/`（docker-compose.frp.local.yml + frps.toml + frpc.toml）

## 验收标准（硬门禁）

- 调用一次脚本，全流程无交互、无报错，且同时满足：
  - HTTPS MCP 直连可用（initialize + tools/list + tools/call）
  - FRP 映射端口可用（同样可完成 MCP 调用）
  - 报告中显示 PASS，且不包含任何敏感值
