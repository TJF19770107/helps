# 🦞 龙虾AI主控中心 — CF隧道全链路诊断报告
**生成时间**: 2026-05-13 18:56  
**隧道ID**: ff624654-b1af-431d-8c3a-f645b0b1e21b  
**域名**: doubao.tjf19770107.cn  
**执行团队**: 一键达 / 盾甲甲 / 稳如山 / 安迪 / 深网网

---

## 一、隧道状态报告（一键达）

### 1.1 当前运行状态

| 指标 | 状态 | 详情 |
|------|------|------|
| cloudflared进程 | ✅ 运行中 | PID 48716, 已运行40分钟 |
| 隧道连接 | ✅ 健康 | 1个活跃副本, 2条路由 |
| 路由1 (/) | ✅ 正常 | → localhost:18000 (doubao-free-api) |
| 路由2 (/qrcode) | ✅ 正常 | → localhost:18091 (ai-bridge-1) |
| 凭证文件 | ✅ 存在 | C:\Users\Administrator\.cloudflared\ff624654...json |
| 配置文件 | ✅ 已更新 | /qrcode 路由已指向18091 |

### 1.2 容器状态

| 容器 | 端口 | 状态 |
|------|------|------|
| ai-doubao2-1 | 127.0.0.1:18000→8000 | ✅ Up 50min |
| ai-bridge-1 | 0.0.0.0:18091→8091 | ✅ Up 50min |
| hermes-agent | 127.0.0.1:8642-8670 | ✅ Up ~1h |
| hermes-webui | 127.0.0.1:6060 | ✅ Up ~1h |
| doubao-proxy | 0.0.0.0:8000→8000 | ⚠️ 全网暴露 |

### 1.3 关键修复记录
- ✅ ai-bridge-1 容器已启动
- ✅ DOUBAO_QR_URL_PREFIX 已从IPv6改为 https://doubao.tjf19770107.cn
- ✅ CF隧道 /qrcode 路由已从18092改为18091
- ✅ cloudflared进程运行正常，配置已生效

---

## 二、安全审计结果（盾甲甲）

### 2.1 风险评级

| 风险项 | 等级 | 状态 | 说明 |
|--------|------|------|------|
| doubao-proxy 0.0.0.0:8000 | 🔴 P0 | 未修复 | 全网暴露doubao API，任何IP可访问 |
| CF隧道凭证文件 | 🟡 P1 | 已缓解 | 存储在用户目录，需确保权限600 |
| Docker容器特权模式 | 🟢 P2 | 正常 | 未检测到特权容器 |
| 明文Cookie环境变量 | 🟡 P1 | 待处理 | .env中DOUBAO_CLOUD_COOKIE未配置 |

### 2.2 安全加固建议

1. **立即修复**: 将 `doubao-proxy` 端口绑定改为 `127.0.0.1:8000:8000`
2. **凭证保护**: 确保 `C:\Users\Administrator\.cloudflared\*.json` 文件权限为仅当前用户可读写
3. **Cookie配置**: 在 `.env` 中配置 `DOUBAO_CLOUD_COOKIE` 后重启 `ai-doubao2-1`
4. **定期轮换**: 每90天在Cloudflare Dashboard刷新隧道令牌

---

## 三、端口健康报告（稳如山）

### 3.1 端口连通性测试

| 端口 | 监听状态 | TCP连通 | HTTP响应 | 响应时间 |
|------|----------|---------|----------|----------|
| 18000 | ✅ LISTENING | ✅ 连通 | 🟢 200 OK | 2503ms |
| 18091 | ✅ LISTENING | ✅ 连通 | 🟡 404 (正常) | 340ms |
| 6060 | ✅ LISTENING | — | — | — |
| 8642 | ✅ LISTENING | — | — | — |

> 注: 18091返回404是正常行为，因为桥接服务未配置根路径处理器。

### 3.2 故障自动恢复方案

```powershell
# 隧道健康检查脚本逻辑
$ports = @(18000, 18091)
foreach ($port in $ports) {
    $tcp = New-Object System.Net.Sockets.TcpClient
    try {
        $tcp.Connect("127.0.0.1", $port)
        Write-Host "端口 $port 正常"
        $tcp.Close()
    } catch {
        Write-Host "端口 $port 异常，触发重启..."
        docker compose -f E:\龙虾AI主控中心\docker-compose.lobster.yml restart
    }
}
```

---

## 四、性能优化建议（安迪）

### 4.1 当前延迟分析

| 指标 | 数值 | 评级 |
|------|------|------|
| 18000 HTTP响应 | 2503ms | 🔴 偏慢 |
| 18091 HTTP响应 | 340ms | 🟢 正常 |
| 隧道建立时间 | ~2s | 🟡 可优化 |

### 4.2 优化建议

1. **18000端口响应慢**: doubao-free-api容器可能需要预热，建议配置健康检查探针
2. **启用HTTP/2**: 在cloudflared配置中添加 `no-tls-verify: true` 和 `http2-origin: true`
3. **连接池优化**: 建议增加 `max-conns-per-ip: 50` 防止连接耗尽
4. **CDN缓存**: 对静态资源启用Cloudflare缓存规则

---

## 五、监控方案（深网网）

### 5.1 监控指标

| 指标 | 采集方式 | 告警阈值 |
|------|----------|----------|
| cloudflared进程存活 | PowerShell Get-Process | 进程不存在立即告警 |
| 端口18000/18091连通性 | TCP连接测试 | 连续3次失败告警 |
| HTTP响应码 | Invoke-WebRequest | 非200/404持续1分钟告警 |
| 隧道连接状态 | cloudflared metrics | 连接断开立即告警 |

### 5.2 告警通知方案

```powershell
# 简易监控脚本框架
function Send-Alert($message) {
    # 可接入飞书/钉钉/企业微信Webhook
    Write-Host "[ALERT] $message"
}

while ($true) {
    $cf = Get-Process -Name "cloudflared" -ErrorAction SilentlyContinue
    if (-not $cf) { Send-Alert "cloudflared进程已停止" }
    
    $tcp = New-Object System.Net.Sockets.TcpClient
    try { $tcp.Connect("127.0.0.1", 18000); $tcp.Close() } 
    catch { Send-Alert "18000端口不可达" }
    
    Start-Sleep -Seconds 60
}
```

---

## 六、一键启停PowerShell脚本

脚本已保存至: `E:\龙虾AI主控中心\lobster_tunnel_control.ps1`

```powershell
# ============================================
# 🦞 龙虾AI主控中心 — CF隧道一键启停脚本
# 隧道ID: ff624654-b1af-431d-8c3a-f645b0b1e21b
# 域名: doubao.tjf19770107.cn
# ============================================

param(
    [Parameter()]
    [ValidateSet("start", "stop", "restart", "status", "health")]
    [string]$Action = "status"
)

$TunnelId = "ff624654-b1af-431d-8c3a-f645b0b1e21b"
$CfPath = "C:\CloudflareTunnel\cloudflared.exe"
$ConfigPath = "C:\Users\Administrator\.cloudflared\config.yml"
$ComposePath = "E:\龙虾AI主控中心\docker-compose.lobster.yml"

function Test-Admin {
    $currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Get-TunnelStatus {
    $cf = Get-Process -Name "cloudflared" -ErrorAction SilentlyContinue
    if ($cf) {
        Write-Host "✅ cloudflared 运行中 (PID: $($cf.Id))" -ForegroundColor Green
    } else {
        Write-Host "❌ cloudflared 未运行" -ForegroundColor Red
    }
    
    $ports = @(18000, 18091, 6060, 8642)
    foreach ($p in $ports) {
        $conn = Test-NetConnection -ComputerName 127.0.0.1 -Port $p -WarningAction SilentlyContinue
        if ($conn.TcpTestSucceeded) {
            Write-Host "  ✅ 端口 $p 监听正常" -ForegroundColor Green
        } else {
            Write-Host "  ❌ 端口 $p 未监听" -ForegroundColor Red
        }
    }
}

function Start-Tunnel {
    Write-Host "🚀 启动隧道..." -ForegroundColor Cyan
    
    # 启动Docker容器
    docker compose -f $ComposePath up -d doubao2 doubao_bridge
    
    # 启动cloudflared
    $cf = Get-Process -Name "cloudflared" -ErrorAction SilentlyContinue
    if (-not $cf) {
        Start-Process -FilePath $CfPath -ArgumentList "tunnel","--config",$ConfigPath,"run",$TunnelId -WindowStyle Hidden
        Start-Sleep -Seconds 3
        Write-Host "✅ 隧道已启动" -ForegroundColor Green
    } else {
        Write-Host "⚠️ 隧道已在运行" -ForegroundColor Yellow
    }
}

function Stop-Tunnel {
    Write-Host "🛑 停止隧道..." -ForegroundColor Cyan
    
    $cf = Get-Process -Name "cloudflared" -ErrorAction SilentlyContinue
    if ($cf) {
        Stop-Process -Name "cloudflared" -Force
        Write-Host "✅ cloudflared 已停止" -ForegroundColor Green
    }
    
    # 可选: 停止容器
    # docker compose -f $ComposePath stop doubao2 doubao_bridge
}

function Test-Health {
    Write-Host "🏥 健康检查..." -ForegroundColor Cyan
    
    $allOk = $true
    
    # 检查cloudflared
    $cf = Get-Process -Name "cloudflared" -ErrorAction SilentlyContinue
    if (-not $cf) { $allOk = $false }
    
    # 检查端口
    $ports = @(18000, 18091)
    foreach ($p in $ports) {
        $tcp = New-Object System.Net.Sockets.TcpClient
        try { $tcp.Connect("127.0.0.1", $p); $tcp.Close() } 
        catch { $allOk = $false }
    }
    
    if ($allOk) {
        Write-Host "✅ 所有检查通过" -ForegroundColor Green
    } else {
        Write-Host "❌ 存在异常，建议执行 restart" -ForegroundColor Red
    }
}

# 主逻辑
switch ($Action) {
    "start"   { Start-Tunnel }
    "stop"    { Stop-Tunnel }
    "restart" { Stop-Tunnel; Start-Sleep -Seconds 2; Start-Tunnel }
    "status"  { Get-TunnelStatus }
    "health"  { Test-Health }
}
```

### 使用方法

```powershell
# 查看状态
.\lobster_tunnel_control.ps1 -Action status

# 启动隧道
.\lobster_tunnel_control.ps1 -Action start

# 停止隧道
.\lobster_tunnel_control.ps1 -Action stop

# 重启隧道
.\lobster_tunnel_control.ps1 -Action restart

# 健康检查
.\lobster_tunnel_control.ps1 -Action health
```

---

## 七、总结

| 模块 | 状态 | 关键结论 |
|------|------|----------|
| 隧道连通性 | ✅ 正常 | cloudflared运行中，2条路由生效 |
| 端口服务 | ✅ 正常 | 18000/18091均监听且可连通 |
| 安全风险 | ⚠️ 待修复 | doubao-proxy全网暴露需处理 |
| 性能表现 | 🟡 可优化 | 18000响应偏慢，建议预热 |
| 监控告警 | 🟡 待部署 | 脚本已提供，可接入Webhook |

**下一步行动**:
1. 修复 `doubao-proxy` 端口绑定为 `127.0.0.1:8000`
2. 配置 `.env` 中的 `DOUBAO_CLOUD_COOKIE`
3. 部署监控脚本并接入告警通道
