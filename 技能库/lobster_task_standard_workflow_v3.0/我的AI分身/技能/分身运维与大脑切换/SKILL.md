---
title: 分身运维与大脑切换技能
summary: 免费大脑(NVIDIA/GLM)配置、重启防失忆、香港VPS代理、网络诊断、Firecrawl vs Playwright
tags: [分身运维, 免费大脑, NVIDIA, GLM, 重启恢复, VPS, 代理, 四化]
version: v1.0
distilled_at: 2026-08-27
distilled_from: 汤哥 2026-08-27 多轮对话迭代
home: 技能库\lobster_task_standard_workflow_v3.0\我的AI分身\技能\分身运维与大脑切换
---

# 分身运维与大脑切换 v1.0

## 一、免费大脑（零成本）
- NVIDIA 免费：`meta/llama-3.2-11b-vision-instruct`，端点 `https://integrate.api.nvidia.com/v1`（chat），key 读 `NVIDIA_API_KEY`。
- 智谱 GLM：`glm-5.3-flash`，端点 `https://open.bigmodel.cn/api/paas/v4`，key 读 `GLM_API_KEY`。注意是推理模型，输出在 `reasoning_content`，需给足 max_tokens。
- 测试命令：直接 POST 该端点，显式注入 key（用户级注册表不一定进运行时，需 set 或从恢复脚本注入）。

## 二、重启防失忆（关键）
- 改 model_provider + 重启会断对话，但**持久化文件保记忆**：
  1. `HANDOFF_恢复文档.md`（当前任务/配置/待办全量）。
  2. `scripts\重启恢复.cmd`（注入双 key + 打开恢复文档 + 提示 resume）。
  3. Codex `resume` 本线程 或 新会话读恢复文档。

## 三、香港 VPS 代理
- 方案包：`香港VPS\`（README / server_setup.sh / client_singbox.yaml / migrate_checklist.md）。
- 本机无通用代理（mihomo 空壳、无二进制）；GitHub 直连时好时坏；TeamoRouter 51427 是 AI 专用非通用代理。
- 走 VPS = 走代理，可连 GitHub/Firecrawl/Google；需用户提供 SSH 后一键部署。

## 四、网络/代理诊断顺序
1. 分层测：DNS(Resolve-DnsName) → HTTP(Invoke-WebRequest) → TCP。
2. 查系统代理残留：`HKCU\...\Internet Settings` ProxyServer/ProxyEnable。
3. 查监听端口：`netstat -ano | findstr LISTENING`。
4. 查代理二进制/进程：clash/v2ray/xray/sing-box/frpc。

## 五、Firecrawl vs Playwright
- Firecrawl：高层清洗→Markdown，MCP原生，反爬，适合知识萃取/资讯采集，需 key。
- Playwright：底层完整浏览器控制，可登录/交互/JS，零成本，需自写逻辑。
- 互补：萃取用 Firecrawl，定制抓取用 Playwright。

## 六、分身当前工具
- !web(联网抓取) / !edit(改文件+备份) / !render_video / !note / !search_kb
- 大脑顺序：GLM → NVIDIA → MiMo → Ollama