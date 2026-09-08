# lobster_ai_local_deploy_v1.0
# 本地 AI 集群部署运维技能

---
name: lobster_ai_local_deploy_v1.0
version: "1.0"
description: |
  龙虾本地AI集群完整部署运维技能。覆盖 Ollama + CC Switch + Hermes
  + Cloudflared + Bridge 在 Windows 环境的完整部署、配置、健康检查、
  故障排查树。内嵌本机自动探测参数（Node v25.2.1, Edge浏览器,
  gemma4:latest模型）。适用于初始化部署、故障恢复、版本升级等场景。
tags:
  - lobster
  - deploy
  - ollama
  - windows
  - local-ai
  - devops
agent_created: true
---

## 本地 AI 集群部署运维技能 — lobster_ai_local_deploy_v1.0

---

### 0. 本机环境参数（自动探测，已确认）

```yaml
os: Windows (win32)
node: v25.2.1 (C:\Program Files\nodejs\)
npm: 11.14.1
python: 3.13.8 (E:\VNPY\python.exe)
browser: Microsoft Edge
browser_path: C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
ollama_status: ONLINE
ollama_port: 11434
ollama_models:
  primary: gemma4:latest (8B, Q4_K_M, 9.6GB)
  backup:  gemma4:e4b   (8B, Q4_K_M, 9.6GB)
ssh_keys: C:\Users\Administrator\.ssh\ (known_hosts, 无id_rsa私钥)
```

---

### 1. 部署架构全貌

```
┌─────────────────────────────────────────────────────────────┐
│                   龙虾本地AI集群架构 v1.0                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐    │
│  │              外网访问层                               │    │
│  │  域名: doubao.tjf19770107.cn                         │    │
│  │  Cloudflared v2026.5.0 (C:\Program Files\cloudflared\) │ │
│  │  备用版本: v2026.3.0 (C:\CloudflareTunnel\)           │    │
│  │    / ──────────────→ localhost:18000 (公共网关)        │    │
│  │    /qrcode ─────────→ localhost:18091 (Bridge二维码)  │    │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              服务层                                   │    │
│  │  Gateway     port: 18000  ⚙️ 按需启动                 │    │
│  │  Bridge QR   port: 18091  ⚙️ 按需启动 (bridge_server) │    │
│  │  Hermes      port: 8642   ⚙️ 按需启动 (hermes.py)     │    │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              本地模型层                               │    │
│  │  Ollama      port: 11434  ✅ 常驻在线                  │    │
│  │    gemma4:latest (主力, Q4_K_M, 需 ~10GB 内存)        │    │
│  │    gemma4:e4b    (备用, 同规格)                       │    │
│  │  [已关闭] Ollama Docker port: 11435                   │    │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              AI工具层                                 │    │
│  │  CC Switch v3.15.0  (MCP管理中心)                     │    │
│  │  WorkBuddy (道道)   (迭代员主控)                      │    │
│  │  OpenCode           (代码工具)                        │    │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

### 2. Ollama 部署与管理（核心服务）

#### 2.1 服务状态验证

```bash
# 1. 验证 Ollama API 在线
curl http://localhost:11434/api/tags

# 2. 确认模型可用（gemma4:latest 已确认存在）
ollama list

# 3. 快速推理测试
ollama run gemma4:latest "测试：返回当前时间" --verbose
```

#### 2.2 Ollama 管理命令（Windows）

```powershell
# 查看 Ollama 服务状态
Get-Service ollama | Select-Object Name, Status

# 启动 Ollama
Start-Service ollama

# 停止 Ollama（慎用，影响所有AI工具）
Stop-Service ollama

# 查看 Ollama 进程内存占用
Get-Process -Name "ollama" -ErrorAction SilentlyContinue | `
  Select-Object Name, @{N='Memory(MB)';E={[Math]::Round($_.WorkingSet/1MB)}}

# 查看当前加载的模型
ollama ps
```

#### 2.3 内存管理（gemma4 需约10GB）

```powershell
# 查看可用内存
(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1024 / 1024
# 返回值单位: GB

# 内存不足时：关闭占用大内存的应用后重试
# 注意: gemma4:latest 和 gemma4:e4b 共用同一权重文件，同时加载不额外占用空间
```

---

### 3. Cloudflared 管理（双版本）

#### 3.1 版本说明与路径

```yaml
主版本:
  version: v2026.5.0
  path: C:\Program Files\cloudflared\cloudflared.exe
  用途: 生产环境首选

备用版本:
  version: v2026.3.0
  path: C:\CloudflareTunnel\cloudflared.exe
  用途: 主版本故障时切换
```

#### 3.2 启动与管理

```bash
# 使用主版本启动隧道
"C:\Program Files\cloudflared\cloudflared.exe" tunnel run

# 切换至备用版本
C:\CloudflareTunnel\cloudflared.exe tunnel run

# 查看隧道状态
"C:\Program Files\cloudflared\cloudflared.exe" tunnel info

# 验证路由（/ → 18000）
curl -I http://localhost:18000/health

# 验证路由（/qrcode → 18091）
curl -I http://localhost:18091/health
```

#### 3.3 Cloudflared 版本切换决策

```
主版本不可用？
├── 检查主版本进程是否已退出
│   → tasklist | findstr cloudflared
├── 查看主版本日志
│   → "C:\Program Files\cloudflared\cloudflared.exe" tunnel run --loglevel debug
└── 启动备用版本（v2026.3.0）
    → C:\CloudflareTunnel\cloudflared.exe tunnel run
```

---

### 4. Hermes 代理层管理

```bash
# 服务文件路径（预设）
HERMES_DIR=C:\Users\Administrator\hermes_service\
HERMES_SCRIPT=hermes.py

# 启动 Hermes（使用 VNPY Python）
E:\VNPY\python.exe C:\Users\Administrator\hermes_service\hermes.py

# 健康检查
curl http://localhost:8642/health

# 关键配置注意（已知问题）：
# Hermes 内的 ZhipuAI 配置会覆盖 OLLAMA_HOST 环境变量
# 解决方案：在 hermes.py 中显式设置 OLLAMA_HOST，隔离变量作用域
```

---

### 5. Bridge 服务管理

```bash
# 服务路径（预设）
BRIDGE_DIR=C:\Users\Administrator\bridge_service\

# 启动 Bridge Server
E:\VNPY\python.exe C:\Users\Administrator\bridge_service\bridge_server.py

# 验证二维码页面
start http://localhost:18091/welcome.html

# 健康检查
curl http://localhost:18091/health

# 常见问题：
# 问题：QRCode.js 白屏
# 解决：确认 CDN 换为内联模式（已修复）
```

---

### 6. CC Switch 配置（Ollama 接入）

CC Switch v3.15.0 Ollama 供应商配置（适配本机）：

```json
{
  "providers": {
    "ollama-local-lobster": {
      "type": "ollama",
      "baseUrl": "http://localhost:11434",
      "models": [
        "gemma4:latest",
        "gemma4:e4b"
      ],
      "defaultModel": "gemma4:latest"
    }
  }
}
```

**已知问题与解决**：

| 问题 | 根因 | 解决方案 |
|------|------|---------|
| CC Claude扩展找不到Ollama模型 | VS Code扩展宿主进程隔离，env变量不传递 | 在CC Switch中直接配置baseUrl，不依赖OLLAMA_HOST |
| Hermes ZhipuAI变量覆盖Ollama | hermes.py配置优先级问题 | 在hermes.py中显式设置OLLAMA_HOST=http://localhost:11434 |
| Docker Ollama端口11435冲突 | Docker实例残留 | 已关闭，确认仅11434活跃 |

---

### 7. MCP 服务器管理

MCP 服务器目录：`C:\Users\Administrator\.workbuddy\mcp-servers\`

#### 已部署的 MCP Server

```
lobster-netdisk-search/
  ├── index.js          (MCP Server 主程序，已生成)
  ├── package.json      (依赖声明)
  └── node_modules/     (已安装: @mcp/sdk, axios等)
```

#### 验证 MCP Server 可启动

```bash
# 测试网盘 MCP Server 启动（不挂 stdio，只验证语法）
node --check C:\Users\Administrator\.workbuddy\mcp-servers\lobster-netdisk-search\index.js

# 或直接运行（会进入stdio等待，Ctrl+C退出）
node C:\Users\Administrator\.workbuddy\mcp-servers\lobster-netdisk-search\index.js
```

---

### 8. 全系统健康检查脚本

```bash
#!/bin/bash
# lobster_health_check.sh — 全系统健康检查
# 使用: bash lobster_health_check.sh

echo "======================================="
echo " 龙虾AI主控中心 全系统健康检查"
echo " $(date '+%Y-%m-%d %H:%M:%S')"
echo "======================================="

check_port() {
  local name=$1 port=$2
  if curl -s --max-time 3 "http://localhost:$port" > /dev/null 2>&1 || \
     curl -s --max-time 3 "http://localhost:$port/health" > /dev/null 2>&1 || \
     netstat -ano 2>/dev/null | grep -q ":$port "; then
    echo "  ✅ $name (port $port): 在线"
  else
    echo "  ❌ $name (port $port): 离线/未启动"
  fi
}

echo ""
echo "【核心服务】"
check_port "Ollama (必须)" 11434
check_port "Hermes" 8642
check_port "Gateway" 18000
check_port "Bridge QR" 18091

echo ""
echo "【数据库（按需）】"
check_port "PostgreSQL" 5432
check_port "MySQL" 3306

echo ""
echo "【Ollama 模型状态】"
models=$(curl -s http://localhost:11434/api/tags 2>/dev/null | node -e "
  let d='';process.stdin.on('data',c=>d+=c);
  process.stdin.on('end',()=>{
    try{const m=JSON.parse(d).models||[];
    m.forEach(x=>console.log('  ✅ '+x.name+' ('+x.details.parameter_size+')'))
    }catch(e){console.log('  ❌ 无法获取模型列表')}
  })")
echo "$models"

echo ""
echo "【环境信息】"
echo "  Node: $(node --version 2>/dev/null || echo 未安装)"
echo "  Python: $(E:/VNPY/python.exe --version 2>/dev/null || echo 未找到)"

echo ""
echo "======================================="
echo " 检查完成"
echo "======================================="
```

---

### 9. 部署清单（全新部署或重装）

```
阶段一：基础环境
□ 1.  确认 Node.js >= 18.0 已安装
□ 2.  确认 Python 3.x 已安装（VNPY: E:\VNPY\python.exe）
□ 3.  确认 Microsoft Edge 已安装（替代Chrome）

阶段二：Ollama 本地模型
□ 4.  安装/启动 Ollama 服务（验证 localhost:11434）
□ 5.  拉取 gemma4:latest: ollama pull gemma4:latest
□ 6.  验证 API: curl http://localhost:11434/api/tags

阶段三：服务层
□ 7.  配置并启动 Hermes 服务（8642）
□ 8.  启动 Bridge QR Server（18091）
□ 9.  启动 Gateway（18000）
□ 10. 验证三个服务健康检查均通过

阶段四：外网访问
□ 11. 安装 Cloudflared v2026.5.0 到 C:\Program Files\cloudflared\
□ 12. 备份旧版本至 C:\CloudflareTunnel\
□ 13. 配置隧道路由：/ → 18000, /qrcode → 18091
□ 14. 启动 Cloudflared 隧道
□ 15. 验证域名 doubao.tjf19770107.cn 可访问

阶段五：AI工具链
□ 16. 在 CC Switch 中配置 Ollama 供应商（localhost:11434）
□ 17. 安装 MCP 服务器（网盘搜索等）
□ 18. 导入 cc_switch_import.json 配置
□ 19. 运行全系统健康检查脚本
□ 20. 验证一次完整的五步法任务执行
```

---

### 10. 完整故障排查树

```
=== 故障排查决策树 ===

Ollama 不可用？
├── API 超时（curl 无响应）
│   ├── 检查进程: tasklist | findstr ollama
│   ├── 服务未启动 → Start-Service ollama
│   └── 进程在但API无响应 → 重启: Stop-Service ollama; Start-Service ollama
├── 模型加载失败
│   ├── 内存不足 → 检查可用内存 → 关闭大内存应用
│   ├── 模型文件损坏 → ollama rm gemma4:latest && ollama pull gemma4:latest
│   └── 磁盘空间不足 → 检查模型存储盘剩余空间
└── 端口冲突
    └── netstat -ano | findstr :11434 → 终止冲突进程（仅保留Ollama桌面版）

Cloudflared 隧道断开？
├── 主版本崩溃
│   ├── 切换备用版本: C:\CloudflareTunnel\cloudflared.exe tunnel run
│   └── 查看主版本日志定位根因
├── Token 过期
│   └── cloudflared tunnel info → 重新登录: cloudflared tunnel login
├── 网络问题
│   └── ping 1.1.1.1 → 检查本机网络连接
└── 路由配置错误
    └── cloudflared tunnel route dns ... → 重新配置DNS路由

CC Switch 找不到 Ollama 模型？
├── 环境变量未传递（扩展进程隔离）
│   └── 在 CC Switch 配置中直接写入 baseUrl: http://localhost:11434
├── Hermes ZhipuAI 变量覆盖
│   └── 修改 hermes.py，在启动时显式 os.environ["OLLAMA_HOST"] = "http://localhost:11434"
└── 模型名称错误
    → 正确: gemma4:latest 或 gemma4:e4b
    → 错误: gemma4:e4b（单独存在时路径相同，建议用 gemma4:latest）

MCP Server 无法启动？
├── Node 版本不兼容
│   └── node --version → 确认 >= 18.0
├── 依赖缺失
│   └── cd <server-dir> && npm install
├── 脚本语法错误
│   └── node --check <script.js>
└── 端口被占用（非stdio类型）
    └── netstat -ano | findstr :<port>
```
