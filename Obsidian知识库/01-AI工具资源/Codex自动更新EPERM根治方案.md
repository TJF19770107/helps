# Codex CLI 自动更新 EPERM 根治方案

**日期**：2026-07-31
**状态**：已修复
**影响范围**：所有 Orca 项目中的 Codex CLI

## 问题现象

每次在 Orca 终端启动 Codex，都会自动执行：
```
Updating Codex via 'npm install -g @openai/codex'...
```
然后报错：
```
npm error code EPERM
npm error errno -4048
npm error syscall unlink
npm error path I:\npm\node_modules\@openai\codex-XXXXX\...\codex.exe
```

## 根因分析

1. Codex CLI 默认启用 **启动时更新检查**
2. 检测到新版本后自动执行 `npm install -g @openai/codex`
3. Windows 下 `codex.exe` 被运行中的进程或杀毒软件锁定
4. npm 无法 unlink 旧文件 → EPERM 失败
5. 每次启动都重复此流程，永远失败

## 根治方案

在 `~/.codex/config.toml` **顶部**（顶级键）添加：

```toml
check_for_update_on_startup = false
```

### 关键注意点

- **必须是顶级键**，不能放在任何 `[section]` 内（如 `[plugins]`、`[features]`）
- 放在 section 内时配置不报错但**不生效**
- 必须同步到 Orca runtime config：`~/AppData/Roaming/Orca/codex-runtime-home/home/config.toml`

### 涉及文件

| 文件 | 作用 |
|------|------|
| `~/.codex/config.toml` | 主配置 |
| `~/AppData/Roaming/Orca/codex-runtime-home/home/config.toml` | Orca runtime 配置 |

## 来源

- GitHub issue [#14336](https://github.com/openai/codex/issues/14336)
- OpenAI 工程师 `etraut-openai` 确认的官方配置项

## 相关坑点

- **P9**：Codex 自更新 EPERM（临时修复：先杀进程再 npm install）
- **P13**：本次根治方案（禁用启动时更新检查）

## 验证方法

```bash
# 在 Orca 新标签页中启动 Codex
codex
# 应该直接进入交互界面，不再出现 "Updating Codex..." 消息
```
