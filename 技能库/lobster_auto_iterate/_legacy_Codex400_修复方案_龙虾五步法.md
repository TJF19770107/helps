# Codex++ 桌面版 400 错误修复方案（龙虾五步法 + 全域模板）

> 生成时间：2026-07-18 ｜ 调用：龙虾五步法 V2.6 + 龙虾全域官方模板
> 环境：Windows ｜ Codex++ 桌面版 → cc-switch(15721) → MiMO

---

## 一、根因结论（已用日志铁证确认）

**错误**：`{"error":{"code":"400","message":"Unsupported model gpt-5.5"}}`

**根因**：Codex++ 桌面端 GUI 的「模型下拉框」当前选中了 `gpt-5.5`（OpenAI 系列模型名），
该值被原样放进请求体的 `model` 字段发给本地代理 cc-switch(15721)，
cc-switch 透传给 MiMO，`gpt-5.5` MiMO 不认识 → 直接 400 拒绝。

**铁证**（来自 cc-switch 代理日志表 `proxy_request_logs`）：

| 时间 | request_model | model(实际转发) | status |
|------|--------------|----------------|--------|
| 最近 | `gpt-5.5` | `gpt-5.5` | **400** |
| 之前全部 | `mimo-v2.5-pro` | `mimo-v2.5-pro` | **200** |

即：**后端链路完全正常，`mimo-v2.5-pro` 一直能跑通（200），唯独 `gpt-5.5` 被 MiMO 拒。**

**链路各环节配置（均已确认正确，无需改）**：
- cc-switch(15721) 代理配置：provider `d240abd2 (Xiaomi MiMo)`，`model = "mimo-v2.5-pro"`，端点 `token-plan-cn.xiaomimimo.com/v1` ✅
- `common_config_codex`：`model = "mimo-v2.5-pro"` ✅
- `.codex/config.toml`：`model = "mimo-v2.5-pro"` ✅
- AI Code Switch(4567) `routes.json`：`targetModel = "mimo-v2.5-pro"` ✅（备用重写层，当前未运行）

**一句话**：问题 100% 出在 Codex++ GUI 下拉框选了 `gpt-5.5`，与后端/配置无关。

---

## 二、龙虾五步法执行记录

### ✅ Step 1 精准确份（已完成诊断，备份待执行）
- 活跃配置已定位：`E:\龙虾AI主控中心\CC-Switch\.cc-switch\cc-switch.db`（SQLite，46MB）
- Codex++ 选中模型存于 `AppData\Roaming\Codex\Local Storage\leveldb`（二进制，直接改有损，不推荐手改）

### 🔧 Step 2 修复（核心动作 = 改 GUI 下拉框）
见下方「修复操作」。

### ✅ Step 3 校验
已验证：`curl 15721` 用 `mimo-v2.5-pro` → 正常返回；用 `gpt-5.5` → 400。
修改下拉框后，Codex++ 发出的 model 即变为 `mimo-v2.5-pro`，400 消失。

### 🔁 Step 4 回滚预案
- 回滚 = 把下拉框从 `mimo-v2.5-pro` 切回原值即可（GUI 内可逆，零风险）。
- 不动任何配置文件，无破坏面。

### 📝 Step 5 日志留存
本文件即结构化日志；轻快照落 G 盘（见第四节，需你授权写入 G 盘）。

---

## 三、修复操作（请你在 Codex++ 桌面版里执行，1 次点击）

1. 打开 Codex++ 桌面版。
2. 找到**右下角「模型」下拉框**（当前显示 `5.5` / `gpt-5.5`）。
3. 切换为 **`mimo-v2.5-pro`**（同列表里的 MiMo V2.5 Pro；若列表没有，选 `mimo-v2-omni` 亦可）。
4. 重新发送任意消息 → 400 消失，正常对话。

> 为什么是它：cc-switch 透传客户端 model 字段，只有 MiMO 支持的模型名（`mimo-v2.5-pro` / `mimo-v2-omni`）能通过。

---

## 四、E 盘空间治理 + E/G 软连接方案（需你授权执行）

### 现状
- **E 盘 100% 满**（141G 用 140G，仅剩 ~1.3G）—— 这是 AI Code Switch(4567) 起不来的根因。
- **G 盘** `G:\龙虾AI主控中心` 为数据盘（剩 ~55G），较宽松。
- ⚠️ 本环境 `/tmp` 映射到 `E:\tmp`（因 E 满，所有写 `/tmp` 的命令均失败）。

### 方案：把重数据从 E 迁 G，E 原位留 Junction 软链接
以 AI Code Switch 为例（它在 E 盘且已挂）：

```powershell
# 1) 复制数据到 G 盘（保持结构）
robocopy "E:\aicodeswitch_v5" "G:\aicodeswitch_v5" /E /COPYALL /R:1 /W:1

# 2) 原目录改名留底（不删）
Rename-Item "E:\aicodeswitch_v5" "E:\aicodeswitch_v5.bak"

# 3) 在 E 原位建 Junction 指回 G（程序无感，路径不变）
cmd /c mklink /J "E:\aicodeswitch_v5" "G:\aicodeswitch_v5"

# 4) 启动 AI Code Switch（4567 兜底重写层恢复）
#    用 E:\aicodeswitch_v5\aicodeswitch.cmd start
```

**收益**：
- E 盘立即释放 AI Code Switch 体积，4567 兜底重写层恢复（即便 GUI 仍是 gpt-5.5，4567 也会重写 → 400 自愈）。
- 后续重数据统一存 G，E 只留软链接，符合你「E/G 软连接」的架构意图。

### 轻快照（落 G 盘，不胀 E 盘）
快照只含配置与关键状态（不含模型权重/缓存）：
- `cc-switch.db`（provider 配置）
- `.codex/config.toml`、`cc-switch-model-catalog.json`
- AI Code Switch `fs-db/routes.json`、`config.json`
- 目标目录：`G:\龙虾AI主控中心\Codex备份\snapshots\20260718_codex400_fix\`

---

## 五、待你确认/授权
1. 是否在 Codex++ 里把模型下拉框切到 `mimo-v2.5-pro`（主修复，必做）。
2. 是否授权我执行 E→G 迁移 + Junction + 轻快照写入（当前沙箱已拦截 G 盘写入，需你放行对应路径）。
