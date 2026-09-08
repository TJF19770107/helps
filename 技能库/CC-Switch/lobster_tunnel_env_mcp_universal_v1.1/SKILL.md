---
name: "lobster_tunnel_env_mcp_universal_v1.1"
description: "三合一固化升级版：FRP 隧道 + DPAPI密钥存储 + Windows证书存储(零私钥文件)的 SecureCode MCP(HTTPS/TLS1.3)；输出仅含SHA256证书指纹的验收报告。Invoke when 需云端↔本地安全连通落地。"
---

# 龙虾永续固化 · 云端Agent↔本地容器 一键安全连通（三合一 v1.1）

技能标识：lobster_tunnel_env_mcp_universal_v1.1  
版本号：v1.1  
更新时间：2026-05-01  
技能定位：在 v1.0 基础上补齐两项硬门禁：  
- TLS 私钥不再以文件形式落盘（改为 Windows CurrentUser 证书存储加载）  
- 验收报告仅输出自签证书的 SHA256 指纹（不输出证书明文/私钥/任何密钥材料）  

## 端口铁律（硬门禁）

- 严禁占用：8000 / 18000 / 18091（豆包专属）  
- Hermes 固定：6060（WebUI）、8642（主网关），不改不占  
- 本技能默认使用：本地 `19090`（SecureCode MCP HTTPS），本地 FRP 映射端口 `19100`（仅自测）  

## 三合一模块（缺一不可）

1) **内网穿透模块（FRP）**
   - 目标：将本地 `19090` 的 MCP HTTPS 安全服务暴露到公网 frps 的映射端口（允许范围：8001-8100）
   - 生产：公网 frps 部署到 CNB 实例（Ubuntu 22.04），绑定 `7000`，放行 `8001-8100`

2) **密钥管理模块（DPAPI 加密存储）**
   - 生成：AES-256、RSA-4096、Bearer Token（仅用于 MCP 认证）
   - 存储：DPAPI(CurrentUser) 加密落盘（不在日志/报告输出明文）

3) **MCP 认证流转模块（SecureCode MCP 兼容服务）**
   - 协议：MCP over HTTPS（JSON-RPC），强制 TLS 1.3 最小版本
   - 证书：自签证书写入 Windows CurrentUser 证书存储（私钥非导出，不产生私钥文件）
   - 客户端：按 SHA256 指纹钉扎校验，跳过域名/CA 校验

## 一键用法（本地前置基础验收）

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\.trae\skills\lobster_tunnel_env_mcp_universal_v1.1\run.ps1
```

## 产物（不含敏感值）

- 验收报告：`.trae/skills/lobster_tunnel_env_mcp_universal_v1.1/.lobster_state/reports/`（仅含证书 SHA256 指纹与状态）
- DPAPI 密钥存储：`.trae/skills/lobster_tunnel_env_mcp_universal_v1.1/.lobster_state/securecode/secrets.dpapi`
- Windows 证书存储：`Cert:\CurrentUser\My`（FriendlyName 前缀 `LobsterSecureCodeMcp`）
