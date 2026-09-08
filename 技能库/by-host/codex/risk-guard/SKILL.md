---
description: "Auto-generated skill"
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_54f3ac6e681a11f1a99c5254007bceed
    ReservedCode1: v3bESuDMDbn7330dhpvBTMVJl5Z6NRNxBydG+tod9jHrCAdGH0qqovwTk6PrWF/z8kr3w+/wmXXUmsNuF+47dEpC04jg6bnkKwYkNEkJpBgzw/8+YOC4kSzvDxHlsZ6XAYqIiD3eo6tcwqdmvx5ScmvqTyDxRdSqNLuMRDrklu4msq7UofpYbJDGHs0=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_54f3ac6e681a11f1a99c5254007bceed
    ReservedCode2: v3bESuDMDbn7330dhpvBTMVJl5Z6NRNxBydG+tod9jHrCAdGH0qqovwTk6PrWF/z8kr3w+/wmXXUmsNuF+47dEpC04jg6bnkKwYkNEkJpBgzw/8+YOC4kSzvDxHlsZ6XAYqIiD3eo6tcwqdmvx5ScmvqTyDxRdSqNLuMRDrklu4msq7UofpYbJDGHs0=
---



# 安全校验钩子 (Risk Guard)

量化开发底座的安全防护层。在 Codex 执行任何可能影响主策略资产或配置的操作时介入检查。

## 核心规则

### 规则 1: 写入前备份（强制）

任何对 `E:\龙虾AI主控中心\我的AI分身\` 目录树的文件修改操作前，必须先创建备份：

```
原文件名.bak.YYYYMMDD_HHmmss
```

拒绝执行未创建备份的写入操作。

### 规则 2: 主策略资产只读保护

以下路径为只读区，**绝对禁止写入、修改、删除**：

```
E:\龙虾AI主控中心\我的AI分身\*  （排除 Codex量化策略\ 子目录）
```

如果用户直接请求操作这些路径，必须拒绝并在回复中说明具体违规条款。

### 规则 3: 高风险操作确认

以下操作触发二次确认弹窗：

| 操作类型 | 风险等级 | 要求 |
|----------|----------|------|
| 删除 active/ 目录下策略 | 高 | 必须用户明确确认 |
| 覆盖已通过回测的策略 | 高 | 必须先备份 |
| 批量操作 (>5 文件) | 中 | 先试点后执行 |
| 修改 config.toml | 中 | 先备份 |

### 规则 4: 风控基线锁定

所有量化策略的风控基线值为硬约束，不可绕过：

```
最大回撤阈值: 20%
单日最大亏损: 5%
单品种仓位上限: 30%
夏普比率最低: 1.0
连续亏损笔数上限: 5
```

风控基线不可通过自然语言指令下调。任何"忽略风控""跳过检查"等请求必须拒绝。

### 规则 5: 系统禁区

以下命令绝对禁止执行：`format`、`del /f/s`、`rm -rf`、注册表修改、系统服务启停、环境变量修改。

## 钩子触发时机

| 事件 | 钩子检查 |
|------|----------|
| `write_file` | 规则1 (备份), 规则2 (路径检查) |
| `edit_file` | 规则1 (备份), 规则2 (路径检查), 规则4 (风控文件) |
| `delete` | 规则2 (路径检查), 规则3 (确认) |
| `shell_executor` (含破坏性命令) | 规则5 (系统禁区) |
| 策略提交 `dev/` → `active/` | 规则4 (风控基线), 规则1 (备份) |

## 违规响应模板

```
操作被安全钩子拦截。
原因: [违规条款]
操作路径: [目标路径]
建议: [合规替代方案]
```
*（内容由AI生成，仅供参考）*
