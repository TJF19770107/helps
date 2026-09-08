# connector_launch.ps1 · P2 独立MCP启动器
# 用法: powershell -File connector_launch.ps1 -Name IMA
param([string]$Name)
$reg = Get-Content "E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v3.0\我的AI分身\MCP_插件\connectors.json" -Raw | ConvertFrom-Json
$c = $reg.connectors | Where-Object { $_.name -eq $Name }
if (-not $c) { "连接器不存在: $Name"; exit 1 }
"连接器: $($c.name) | 类型: $($c.type) | 状态: $($c.status)"
if ($c.status -eq "pending") { "该连接器待接入，未配置启动命令。" } else { "启动就绪（宿主层已连）。" }