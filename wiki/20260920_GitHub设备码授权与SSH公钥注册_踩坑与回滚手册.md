# GitHub SSH 公钥注册与设备码授权 · 踩坑与回滚手册 20260920

> 版本 v1.0 · 2026-09-20 12:10 CST · 汤小龙 · 龙虾五步法（检查→分析→修复→迭代→沉淀）
> 适用：GitHub SSH 通道打通 / 设备码授权 / 代理链路故障分流 / 回滚备份

## 一、目标与背景

汤哥要求：①GitHub 注册 SSH 公钥，打通 git SSH 通道；②不续费香港云服务器后 GitHub 能否直连；③全程零手动干预。本手册记录全过程踩坑、判定法与回滚路径。

## 二、链路依赖矩阵（先看这张表，别再猜）

| 链路 | 依赖香港服务器？ | 判定依据 |
|---|---|---|
| GitHub HTTPS git push/pull | ❌ | 09-20 直连 ls-remote 带 token 认证成功 |
| GitHub SSH（ssh.github.com:443 / github.com:22） | ❌ | 直连握手成功（公钥未注册时报 Permission denied=传输层已通） |
| GitHub REST API（api.github.com） | ❌ | 直连持续可用 |
| gh-proxy.com（只读兜底） | ❌ | 公共镜像站 |
| 7897 → Google/穿墙 | ✅ | 7897 是本机自建中转器，后端=自家香港服务器（SSH 隘道 1081），不续费即死 |
| Chrome 访问 github.com | ❌（但需关系统代理） | 直连可达；挂着死代理反而 ERR_PROXY_CONNECTION_FAILED |

**结论：GitHub 四条通道全部不依赖香港服务器；真正不可替代的是通用穿墙。**

## 三、假成功形态 #13：设备码过期但轮询器不报错

- 实证：设备码 `EXPIRES_IN=899`（15 分钟），超时后轮询器仍输出 `PENDING` 不退出——看起来"在等授权"，实际码已死。
- 判定法：**对比任务 Duration 与 EXPIRES_IN**。Duration > 900 秒仍在 PENDING = 码已过期，直接重新生成，别等。
- 修复：杀旧轮询器 → 重新生成新码（旧码不可复用）。

## 四、设备码授权三连坑（完整路径）

1. **令牌缺 scope → 404 伪装**（形态 #12）：`POST /user/keys` 用只有 `repo, user, workflow, write:packages` 的 token 返回 404（非 403）。判定：`GET /user` 200 + 响应头 `X-OAuth-Scopes`。注册 SSH 公钥必须补 `admin:public_key` scope → 走 OAuth 设备流（gh CLI 公开 client_id `178c6fc778ccc68e1d6a`）。
2. **脚本代理路由**：设备流脚本默认走系统代理（7897），撞上链路瞬断 502；强制直连又撞 10060（github.com:443 直连窗口时通时断）。**正解：显式 ProxyHandler 指定 7897 香港链路**（HTTPError 404/401 说明传输层是通的，只是接口语义报错）。
3. **登录墙**：`github.com/login/device` 强制要求 GitHub 登录态，自动化浏览器（全新 profile）必被重定向 `/login`。**登录这一步无法也不应绕过（密码属用户资产）**。正解=「人工登录 + 脚本接管」：有头浏览器弹窗人工输密码，脚本轮询 URL 检测回到 `/login/device` 后自动填码+点 Authorize。profile 用 `launchPersistentContext` 持久化，登录一次后续全自动。

## 五、代理链路故障分流表（Chrome/Edge 报错速查）

| 报错 | 含义 | 处置 |
|---|---|---|
| `ERR_PROXY_CONNECTION_FAILED` | 系统代理端口没监听（7897 死） | 拉起 `http2socks_7897.py`；或临时关系统代理走直连 |
| `ERR_CONNECTION_TIMED_OUT`（挂着代理时） | 走了死代理 | 同上；先 `netstat` 查 7897/1081 LISTENING |
| `ERR_TUNNEL_CONNECTION_FAILED` | 代理端口活着但数据面不通 | SSH 隘道（1081）僵死，杀 ssh 进程等 5 秒自动重连 |
| 直连超时、挂代理反而通 | 直连窗口关闭 | GitHub 换 7897 链路；国内直连时通时断属常态 |

**第三态陷阱（反复踩）**：`cmd start //min xxx.bat` 拉起常驻脚本无回执不验证=假成功（窗口闪退无人知）。正解：拉起后必须 `netstat` 查 LISTENING + 数据面探针（走代理 GET 一次真 URL）。

## 六、本机 SSH 配置（已固化，可直接抄）

`C:\Users\Administrator\.ssh\config`：

```
Host github.com
    HostName ssh.github.com
    Port 443
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

公钥注册成功后验证：`ssh -T git@github.com` → 预期 `Hi TJF19770107!`。

## 七、回滚路径

| 场景 | 回滚操作 |
|---|---|
| 设备码过期/输错 | 重新运行 `G:\WorkBuddy_Data\tmp\gh_device_flow_register.py` 生成新码（旧码自动作废，无副作用） |
| 公钥注册后发现是错误密钥 | GitHub → Settings → SSH keys 删除；或 `DELETE /user/keys/{id}`（需 admin:public_key scope） |
| ~/.ssh/config 改坏 | 删除该文件即恢复默认（22 端口），不影响 HTTPS 通道 |
| 7897 链路故障 | 杀 ssh+python 进程 → 重拉 `http2socks_7897.py` + `hk_proxy_tunnel.bat` → 数据面复测 |
| GitHub 通道全挂（极端） | 顺序回退：HTTPS 直连 → SSH 443 → `gh_api_push.py`（REST API 旁路）→ gh-proxy.com（只读） |
| 自动化浏览器残留 | 关 Edge 窗口；profile 在 `G:\WorkBuddy_Data\tmp\gh_edge_profile`，删目录即清会话 |

## 八、关键脚本清单

| 脚本 | 用途 |
|---|---|
| `G:\WorkBuddy_Data\tmp\gh_device_flow_register.py` | 设备流生成码+轮询+自动注册公钥（走 7897） |
| `G:\WorkBuddy_Data\tmp\gh_device_browser_fill.js` | 有头 Edge 人工登录+自动填码授权（playwright） |
| `E:\龙虾AI主控中心\我的AI分身\企业微信群定制接单项目\scripts\five_lib_dispatch.py` v2.2 | 六端分发（CNB 回查修复+GitHub 令牌内存注入） |
| `E:\龙虾AI主控中心\我的AI分身\企业微信群定制接单项目\scripts\gh_api_push.py` | GitHub REST API 旁路推送（git 层全挂时兜底） |

## 九、复用指令

- 重新生成设备码：`"C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe" -u "G:/WorkBuddy_Data/tmp/gh_device_flow_register.py"`（后台跑，取 USER_CODE）
- 浏览器填码：`NODE_PATH="I:/npm/node_modules" node gh_device_browser_fill.js <新码>`
- 全链路探针：直连 socket+TLS HEAD github.com/api.github.com；走 7897 GET google generate_204 + github.com
