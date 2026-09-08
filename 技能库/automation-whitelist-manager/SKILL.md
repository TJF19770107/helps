---
name: "automation-whitelist-manager"
description: "程序自动化白名单管理技能 v1.0：管理app-agent对Windows桌面EXE应用的自动化操作权限白名单，支持截图/进程启停/配置修复/接口连通校验权限的增删改查。触发词：白名单、自动化权限、加入白名单、移除白名单、白名单查询。"
version: "1.0"
merged_from: ["WorkBuddy自动化白名单配置实战"]
date: "2026-06-29"
primary_path: "E:\龙虾AI主控中心\我的AI分身\技能库\automation-whitelist-manager\SKILL.md"
---

# 程序自动化白名单管理技能 v1.0

技能名称：程序自动化白名单管理（Automation Whitelist Manager）
技能标识：automation-whitelist-manager
适用范围：app-agent对所有需要自动化操作的Windows桌面EXE应用的权限管理
版本号：v1.0
更新时间：2026-06-29

---

## 1) 背景与问题

app-agent在执行Windows桌面应用（EXE）的自动化操作时，需要该应用在白名单中获得授权。未在白名单中的应用将被拦截，导致以下操作无法执行：

- 截图（窗口截图、区域截图）
- 进程启停（优雅关闭、强制终止、重启）
- 配置修复（读写应用配置文件）
- 接口连通校验（网络连通性诊断）

WorkBuddy 因不在自动化白名单中，app-agent无法对其执行全自动修复流程（截图诊断、进程启停、配置修复、接口连通校验），迫使每次修复需手动切换PowerShell脚本操作。

---

## 2) 白名单配置结构

配置文件路径（正式版本）：`E:\龙虾AI主控中心\我的AI分身\技能库\automation-whitelist-manager\automation_whitelist.json`

> 注意：C盘 `{Marvis-User-Data}\skills\automation_whitelist.json` 仅为 app-agent 执行期缓存副本，修改时需同步更新E盘正式版本。

```json
{
  "_meta": {
    "version": "1.0.0",
    "description": "App-Agent EXE Automation Whitelist",
    "lastUpdated": "YYYY-MM-DDTHH:mm:ss+08:00"
  },
  "whitelist": {
    "应用名": {
      "executable_path": "绝对路径\\应用.exe",
      "package_name": "com.example.app",
      "permissions": {
        "screenshot": true,
        "process_control": true,
        "config_repair": true,
        "interface_connectivity_check": true,
        "full_automation": true
      },
      "granted_at": "YYYY-MM-DDTHH:mm:ss+08:00",
      "status": "active"
    }
  }
}
```

### 权限字段说明

| 权限字段 | 类型 | 说明 |
|----------|------|------|
| screenshot | boolean | 允许截图（窗口/区域） |
| process_control | boolean | 允许进程启停（关闭/启动/重启） |
| config_repair | boolean | 允许读写修改应用配置文件 |
| interface_connectivity_check | boolean | 允许执行网络连通性诊断 |
| full_automation | boolean | 全自动化超级权限（包含以上全部） |

### 状态字段

| 状态值 | 说明 |
|--------|------|
| active | 白名单生效中 |
| suspended | 白名单暂时挂起 |
| revoked | 白名单已撤销 |

---

## 3) 操作流程

### 3.1 查询白名单

```
1. 读取 automation_whitelist.json
2. 遍历 whitelist 对象的所有 key
3. 输出应用名 + 权限状态表格
```

### 3.2 新增应用

```
1. 确认应用可执行文件绝对路径
2. 确认需要授权的权限项（默认全开）
3. 构造权限对象，加入 whitelist
4. 更新 _meta.lastUpdated 时间戳
5. 写回 JSON 文件
```

### 3.3 移除应用

```
1. 从 whitelist 对象中 delete 对应 key
2. 更新 _meta.lastUpdated
3. 写回 JSON
```

### 3.4 修改权限

```
1. 读取目标应用的 permissions 对象
2. 按需翻转权限开关
3. 更新 _meta.lastUpdated
4. 写回 JSON
```

### 3.5 备份与恢复

```
备份：复制 `E:\龙虾AI主控中心\我的AI分身\技能库\automation-whitelist-manager\automation_whitelist.json` → `G:\龙虾AI主控中心\我的AI分身\技能库\backup\automation_whitelist.json.bak.{YYYYMMDD}`
恢复：用 .bak 文件覆盖原文件
```

---

## 4) 加入白名单后验证清单

每次将应用加入白名单后，必须执行以下验证（自动化验证闭环）：

| 序号 | 验证项 | 方法 | 通过标准 |
|------|--------|------|----------|
| 1 | 截图权限 | 截取应用主窗口 | 截图文件生成，界面正常渲染 |
| 2 | 进程启停 | 先关闭再启动应用 | 关闭成功 + 启动成功 + 进程数恢复 |
| 3 | 日志健康 | 读取应用日志最后500行 | 无ECONNRESET/fetch failed致命错误 |
| 4 | 子进程存活 | 检查所有子进程 | 全部存活，主窗口可聚焦 |

---

## 5) 已录入白名单的应用

| 应用 | 可执行路径 | 权限 | 状态 |
|------|-----------|------|------|
| WorkBuddy | F:\Program\WorkBuddy.exe | 全权限 | active |

---

## 6) 故障排查

### 配置文件读取失败
- 检查文件是否存在：`{Marvis-User-Data}\skills\automation_whitelist.json`
- 检查 JSON 格式合法性

### 应用加入白名单后仍无法操作
- 确认 executable_path 与实际安装路径一致
- 确认 permissions 中对应字段为 true
- 确认 status 为 active

### 权限被意外重置
- 从 .bak 备份文件恢复
- 检查是否有其他进程写入冲突

---

## 7) 关联技能

- lobster_task_standard_workflow_full_v2.3（龙虾五步法，含软件服务故障诊断子流程）
- workbuddy-recovery-rollback v1.0（WorkBuddy网络故障诊断与修复）
- direct-network-recovery-rollback v1.0（直连网络一键恢复+回滚）
