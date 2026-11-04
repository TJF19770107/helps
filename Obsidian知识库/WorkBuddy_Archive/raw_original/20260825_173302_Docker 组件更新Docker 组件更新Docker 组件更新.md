# Docker 组件更新Docker 组件更新Docker 组件更新

> 会话ID: 12366857869096706 | 抓取时间: 2026-08-25T09:33:02.411Z | 消息数: 8 (用户4/助手4) | 图片数: 0
> 源URL: https://www.doubao.com/chat/12366857869096706

---

## **👤 用户**

Ready to be installed (No restart needed). Some components can be updated: Docker AI CLI, Docker Compose CLI, Docker MCP CLI, Docker Model Runner CLI Download size: 52 MB 翻译为中文

---

## **🤖 助手**

准备安装（无需重启）。部分组件可更新：Docker AI 命令行界面、Docker Compose 命令行界面、Docker MCP 命令行界面、Docker 模型运行器命令行界面 下载大小：52 MB

---

## **👤 用户**

Editor is now accessible via: 翻译为中文

---

## **🤖 助手**

现在可通过以下方式访问编辑器：

---

## **👤 用户**

configuration: - N8N_RUNNERS_ENABLED -> Running n8n without task runners is deprecated. Task runners will be turned on by default in a future version. Please set `N8N_RUNNERS_ENABLED=true` to enable task runners now and avoid potential issues in the future. Learn more 翻译为中文

---

## **🤖 助手**

配置： - N8N_RUNNERS_ENABLED -> 不使用任务运行器运行 n8n 已被弃用。未来版本中，任务运行器将默认开启。请设置 N8N_RUNNERS_ENABLED=true 以立即启用任务运行器，避免未来可能出现的问题。了解更多

---

## **👤 用户**

There is a deprecation related to your environment variables. Please take the recommended actions to update your configuration: - N8N_RUNNERS_ENABLED -> Running n8n without task runners is deprecated. Task runners will be turned on by default in a future version. Please set `N8N_RUNNERS_ENABLED=true` to enable task runners now and avoid potential issues in the future. Learn more 翻译为中文

---

## **🤖 助手**

ECONNRESET 错误通常表示网络连接被强行中断（如对方服务器关闭连接、网络中断等），结合日志中 “ Client network socket disconnected before secure TLS connection was established ” 的提示，问题可能与 TLS 握手失败 或 网络连接不稳定 相关。以下是具体解决步骤： 一、基础网络排查 检查网络稳定性 确认本地网络是否正常（如访问其他网站、 ping 目标服务器地址）。 若使用 Wi-Fi，尝试切换有线连接；若使用公司 / 校园网络，可能存在防火墙或代理限制，可尝试热点测试。 验证目标服务器状态 确认 Rudder 连接的服务器是否正常运行（可通过官网状态页、服务监控工具或联系服务提供商确认）。 若服务器临时维护，可能导致连接中断，等待恢复即可。 二、TLS 相关问题解决 检查系统时间和时区 TLS 握手依赖证书有效期，若本地系统时间与实际时间偏差较大（如超过证书有效期），会导致握手失败。 解决：同步系统时间（Windows 可通过 “设置→时间和语言→自动设置时间”；Linux 用 ntpdate 命令；Mac 用 “系统设置→通用→日期与时间”）。 更新 TLS 协议支持 旧版本的 TLS 协议（如 TLS 1.0/1.1）可能被服务器禁用，导致握手失败。 解决：确保客户端支持 TLS 1.2 及以上（如更新浏览器、操作系统或相关软件到最新版本）。 检查证书信任问题 若服务器使用自签名证书或未被本地信任的证书，可能被系统拦截。 解决： 手动导入并信任服务器证书（具体步骤因系统 / 软件而异）； 若为开发环境，可临时关闭证书验证（不建议生产环境，如 Node.js 可设置 process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0' ）。 三、代理或防火墙干扰 关闭代理或 VPN 代理或 VPN 可能修改网络路由，导致 TLS 握手过程中断。 解决：暂时关闭代理软件（如 Shadowsocks、VPN 客户端），或在软件中排除 Rudder 相关域名 / IP。 检查防火墙设置 本地防火墙（如 Windows Defender、Mac 防火墙）或网络防火墙可能拦截了 TLS 端口（默认 443）。 解决： 添加入站 / 出站规则，允许 Rudder 进程访问网络（尤其是 443 端口）； 若使用公司网络，联系 IT 部门确认是否放行目标服务器的 IP 和端口。 四、软件本身问题 更新 Rudder 或相关组件 旧版本软件可能存在 TLS 握手的 Bug，更新到最新版本通常能修复兼容性问题。 查看 Rudder 官方文档或更新日志，确认是否有针对 ECONNRESET 的修复。 重启相关服务 / 进程 临时的进程异常可能导致连接不稳定，重启 Rudder 或依赖的服务（如 Docker、Node.js 等），清除缓存后再试。 查看详细日志定位问题 若上述步骤无效，可开启更详细的日志（如 Rudder 的调试模式），查看 TLS 握手阶段的具体错误（如证书无效、协议不匹配等），进一步针对性解决。 五、其他可能场景 若使用 Docker 环境（结合之前的 Docker 配置记录），检查容器网络是否隔离、端口映射是否正确，或尝试重启 Docker 服务。 若为编程场景（如 Node.js 客户端），可能是代码中未正确处理连接超时，可增加超时时间或重试机制（如设置 retry 逻辑）。 如果以上步骤仍未解决，建议提供更多上下文（如 Rudder 的使用场景、连接的服务器地址、操作系统版本等），以便进一步排查。

---
