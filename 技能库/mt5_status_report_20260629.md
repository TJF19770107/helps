---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_28845c9d736311f1aabe5254007bceed
    ReservedCode1: zxzU9x5uogdQFsP4e0+EsvRrdxRmSR6sgZE9IxLNrdMsPRHkG77p3QEWfWeKGuGVarUgSaxqivc1G+xMpE2VQywy4GtBkxdi0+xVzCFBXPD/2wicDUEixUtMNPOvMFK8ZwF33RSfQnEdTJGieDLf6NoiU0AxZ1UBO67mTYs7RfqIe5753qYIxBY5ZXQ=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_28845c9d736311f1aabe5254007bceed
    ReservedCode2: zxzU9x5uogdQFsP4e0+EsvRrdxRmSR6sgZE9IxLNrdMsPRHkG77p3QEWfWeKGuGVarUgSaxqivc1G+xMpE2VQywy4GtBkxdi0+xVzCFBXPD/2wicDUEixUtMNPOvMFK8ZwF33RSfQnEdTJGieDLf6NoiU0AxZ1UBO67mTYs7RfqIe5753qYIxBY5ZXQ=
---

﻿# MT5 客户端完整状态报告

**生成时间**: 2026-06-29 08:10  
**操作系统**: Windows 10 Build 19045  
**检查范围**: 快捷方式、安装完整性、进程、端口、服务/计划任务

---

## 1. 桌面快捷方式检查

| 搜索位置 | 结果 |
|----------|------|
| 桌面 (User + Public) | **未找到** MT5/MetaTrader/terminal64 相关快捷方式 |
| 开始菜单 | **未找到** MT5/MetaTrader/terminal64 相关快捷方式 |

> 快捷方式可能已被删除或安装时未创建。MT5 主程序在安装目录中直接运行。

---

## 2. 安装完整性检查

### 2.1 安装目录

`
C:\Program Files\MT5 by FOREX.com Global CN\
`

| 子目录 | 状态 |
|--------|------|
| Bases | ✅ 存在 |
| Config | ✅ 存在 |
| MQL5 | ⚠️ 存在但结构不完整 |
| Profiles | ✅ 存在 |
| Sounds | ✅ 存在 |

### 2.2 核心可执行文件

| 文件 | 路径 | 大小 | 修改时间 | 状态 |
|------|------|------|----------|------|
| terminal64.exe | C:\Program Files\MT5 by FOREX.com Global CN\terminal64.exe | 85.3 MB | 2026-02-16 | ✅ 存在 |
| metatester64.exe | C:\Program Files\MT5 by FOREX.com Global CN\metatester64.exe | - | - | ✅ 存在 |

### 2.3 MQL5 目录完整性

`
C:\Program Files\MT5 by FOREX.com Global CN\MQL5\
└── profiles\
    └── charts\
        └── default\
`

| 标准子目录 | 预期 | 实际 |
|-----------|------|------|
| Experts | 存放EA交易 | ❌ 缺失 |
| Scripts | 存放脚本 | ❌ 缺失 |
| Include | 存放头文件 | ❌ 缺失 |
| Images | 存放图片资源 | ❌ 缺失 |
| Shared Projects | 共享项目 | ❌ 缺失 |

> ⚠️ MQL5 目录严重不完整，缺少5个核心子目录。这可能是首次安装后从未运行导致未初始化，或者目录被手动删除。

### 2.4 Config 目录

| 文件 | 说明 |
|------|------|
| Config\terminal.ini | 终端界面配置文件，ProgramBuild=2085 |
| Config\servers.dat | 交易服务器配置文件 |
| Config\terminal.lic | 许可证文件 |

> terminal.ini 中未发现 MCP/Python API 端口配置项。

---

## 3. 进程检查

| 进程名称 | PID | CPU | 内存 | 启动时间 | 状态 |
|----------|-----|-----|------|----------|------|
| terminal64.exe | - | - | - | - | ❌ 未运行 |
| metatester64.exe | - | - | - | - | ❌ 未运行 |
| metatrader-http-server | 49780 | 0.016s | 3.6 MB | 2026-06-29 08:03 | ⚠️ 运行中，仅1线程 |

> metatrader-http-server 进程存在但处于挂起等待状态（仅1线程），未绑定任何端口，说明正在等待 MT5 终端登录验证。

---

## 4. MCP 服务端口检查

| 端口 | 用途 | 状态 |
|------|------|------|
| 8000 | metatrader-http-server 默认 | ❌ 未监听 |
| 18888 | MT5 Python API 常用 | ❌ 未监听 |
| 55555 | MCP 桥接常用 | ❌ 未监听 |
| 8888 | 备用端口 | ❌ 未监听 |

> UDP 50001 端口由 PID 5544 占用（非MT5相关）。

### metatrader-http-server 进程端口

PID 49780 (metatrader-http-server) 当前未绑定任何 TCP 端口。根据历史经验，该程序需要先通过 MT5 终端登录验证（600秒超时）才会启动 HTTP 服务器。

---

## 5. 后台运行状态

| 检查项 | 结果 |
|--------|------|
| Windows 服务 | ❌ 未发现 MT5 相关服务 |
| 计划任务 | ❌ 未发现 MT5 相关计划任务 |

---

## 6. 异常项汇总

| 序号 | 严重度 | 异常项 | 详情 |
|------|--------|--------|------|
| 1 | ⚠️ 中 | terminal64.exe 未运行 | MT5 终端客户端未启动 |
| 2 | ⚠️ 中 | MQL5 目录不完整 | 缺少 Experts/Scripts/Include/Images/Shared Projects |
| 3 | ⚠️ 中 | MCP 端口全部未监听 | 18888/55555/8000 均未监听 |
| 4 | ⚠️ 中 | metatrader-http-server 挂起 | 等待 MT5 登录，600s 超时后可能退出 |
| 5 | 🟡 低 | 无桌面快捷方式 | 需手动到安装目录启动 |

---

## 7. 修复建议

1. **启动 MT5 终端**: 手动运行 C:\Program Files\MT5 by FOREX.com Global CN\terminal64.exe，登录账号后 MQL5 目录会自动初始化。
2. **重启 metatrader-http-server**: MT5 登录成功后，重新启动 metatrader-http-server 使其绑定端口 8000。
3. **创建桌面快捷方式**: 右键 	erminal64.exe → 发送到桌面快捷方式。
4. **若需 MCP 桥接**: MT5 登录后，确认 Python API 已启用（工具→选项→智能交易系统→允许WebRequest）。
*（内容由AI生成，仅供参考）*
