---
name: deerflow-g-deploy
description: DeerFlow项目G盘部署技能V2.0。覆盖Docker Compose部署、Marvis联动配置、调研速查验证、迁移验证与回滚。触发词：DeerFlow部署、G盘部署DeerFlow、deerflow compose、迁移DeerFlow、DeerFlow验证、G盘项目迁移。
version: 2.0
agent_created: true
updated: 2026-07-24
reconstructed: true
reconstruction_fidelity: 80
---

# DeerFlow G盘部署技能 V2.0

> 定位：将DeerFlow项目完整部署到G盘（外置/数据盘），实现"E盘存程序、G盘存数据"的动静分离架构
> 核心目标：一键Compose拉起、Marvis自动联动、调研能力可验证、迁移前后可对比

## 一、何时激活本技能

- 用户说"把DeerFlow部署到G盘""DeerFlow迁移到G盘"
- E盘空间不足，需要将DeerFlow数据目录迁出
- 新环境首次部署DeerFlow
- DeerFlow升级后需要重新验证调研/搜索能力
- 需要检查Marvis与DeerFlow的联动状态

## 二、前置条件与检查

### 2.1 磁盘与路径检查

```bash
# ① G盘可用空间（建议≥20GB）
df -h /g

# ② G盘是否可写
touch /g/_write_test_ && rm /g/_write_test_ && echo "G盘可写"

# ③ 目标目录规划
G_PROJECT="G:/龙虾AI主控中心/数据迁移/DeerFlow"
G_DATA="G:/龙虾AI主控中心/数据迁移/DeerFlow_data"
```

**磁盘熔断规则**：
| 盘符 | 剩余空间 | 动作 |
|------|---------|------|
| G盘 | <20GB | 🔴 暂停部署，先清理或扩容 |
| E盘 | <5GB | 🟡 优先将数据目录迁往G盘 |

### 2.2 依赖检查

```bash
# Docker
docker --version
docker compose version

# Git（用于拉取/更新代码）
git --version

# Marvis客户端（用于联动）
ls "E:/龙虾AI主控中心/Marvis" 2>/dev/null || echo "Marvis路径待确认"
```

## 三、核心执行流程

### Step 1 · 备份原环境

```bash
# 若E盘已有DeerFlow，先压缩备份到G盘
SRC_E="E:/龙虾AI主控中心/DeerFlow"
BACKUP_G="G:/Marvis修复备份_$(date +%Y%m%d)/DeerFlow_backup"

if [ -d "$SRC_E" ]; then
  mkdir -p "$BACKUP_G"
  # 使用robocopy避免中文路径bug
  robocopy "$SRC_E" "$BACKUP_G" /E /COPY:DAT /R:2 /W:1
  echo "✅ 备份完成: $BACKUP_G"
fi
```

### Step 2 · 目录迁移（动静分离）

```bash
# 创建G盘目录结构
mkdir -p "$G_PROJECT"
mkdir -p "$G_DATA"/{logs,cache,db,uploads,models}

# 迁移策略：程序文件保留在E盘或整体迁到G_PROJECT
# 数据目录通过volume挂载到G_DATA
```

### Step 3 · Docker Compose部署

```yaml
# docker-compose.yml 示例（G盘部署版）
version: "3.8"
services:
  deerflow:
    image: deerflow:latest
    container_name: deerflow-g
    ports:
      - "18080:8080"
    volumes:
      - "G:/龙虾AI主控中心/数据迁移/DeerFlow_data/logs:/app/logs"
      - "G:/龙虾AI主控中心/数据迁移/DeerFlow_data/cache:/app/cache"
      - "G:/龙虾AI主控中心/数据迁移/DeerFlow_data/db:/app/db"
      - "G:/龙虾AI主控中心/数据迁移/DeerFlow_data/uploads:/app/uploads"
    environment:
      - DEERFLOW_DATA_DIR=/app/data
      - LOG_LEVEL=info
      - MARVIS_API_URL=http://host.docker.internal:18808
    restart: unless-stopped
```

```bash
# 拉起服务
cd "$G_PROJECT"
docker compose pull
docker compose up -d

# 查看状态
docker compose ps
docker compose logs -f --tail 50
```

### Step 4 · Marvis联动配置

```bash
# 在Marvis中添加DeerFlow服务入口
# 配置项：
# - 服务名: DeerFlow-G
# - URL: http://127.0.0.1:18080
# - 类型: research / search
# - Token路由: 本地优先，必要时走MiMO
```

**Marvis配置检查清单**：
- [ ] DeerFlow服务地址可达
- [ ] Token统计能识别DeerFlow调用
- [ ] 定时任务能触发DeerFlow调研

### Step 5 · 调研速查验证

```bash
# ① 服务根接口
curl -s http://127.0.0.1:18080/health

# ② 搜索能力验证
curl -s -X POST http://127.0.0.1:18080/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"DeerFlow 项目介绍","top_k":3}'

# ③ 调研能力验证（长链路）
curl -s -X POST http://127.0.0.1:18080/api/research \
  -H "Content-Type: application/json" \
  -d '{"topic":"AI Agent 编排架构","depth":"medium"}'
```

**验证标准**：
| 检查项 | 通过标准 |
|--------|---------|
| /health | 返回200 + {"status":"ok"} |
| /api/search | 5秒内返回结果，无空值 |
| /api/research | 30秒内返回结构化报告 |
| 日志 | 无ERROR级异常 |

### Step 6 · 迁移验证（前后对比）

```bash
# 对比项：
# - 服务端口是否一致
# - 历史数据是否完整
# - 环境变量是否生效
# - Marvis调用统计是否正常

# 数据完整性校验（示例）
diff -rq "$BACKUP_G/db" "$G_DATA/db" 2>/dev/null || echo "需手动核对数据库"
```

## 四、参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `deploy_path` | string | `G:/龙虾AI主控中心/数据迁移/DeerFlow` | 程序部署目录 |
| `data_path` | string | `G:/龙虾AI主控中心/数据迁移/DeerFlow_data` | 数据挂载目录 |
| `port` | int | `18080` | 对外暴露端口 |
| `mode` | string | `fresh` | 部署模式：fresh（全新）/migrate（迁移）/verify（仅验证） |
| `backup_first` | bool | true | 迁移前是否自动备份 |

## 五、输出格式

```markdown
## DeerFlow G盘部署报告

- **部署模式**: {mode}
- **程序目录**: {deploy_path}
- **数据目录**: {data_path}
- **服务端口**: {port}
- **G盘剩余**: {x}GB
- **容器状态**: {running/exited}
- **健康检查**: {PASS/FAIL}
- **调研速查**: {PASS/FAIL}
- **迁移验证**: {PASS/FAIL}
- **回滚备份**: {backup_path}
```

## 六、使用示例

### 示例1：全新部署到G盘
```
用户：在G盘全新部署一套DeerFlow
→ mode=fresh
→ 检查G盘空间→创建目录→docker compose up -d
→ 健康检查→调研速查→输出报告
```

### 示例2：从E盘迁移到G盘
```
用户：E盘满了，把DeerFlow迁到G盘
→ mode=migrate
→ 备份E盘原环境→迁移程序+数据→挂载G_DATA→启动→验证
```

### 示例3：仅验证现有G盘部署
```
用户：看看DeerFlow G盘部署是否正常
→ mode=verify
→ docker compose ps→/health→/api/search→/api/research
```

## 七、联动Skill表

| 联动技能 | 方向 | 联动内容 |
|---------|------|---------|
| `fleet-devops-orchestrator` | 单向→出 | 纳入舰队6维度体检"项目部署健康"项 |
| `local-llm-integration-fix` | 单向→入 | DeerFlow调用LLM失败时联动排查 |
| `tat-adhoc-exec` | 单向→入 | 远程服务器上执行DeerFlow部署命令 |
| `skill-ecosystem-steward` | 单向→出 | 部署完成后更新项目矩阵 |

## 八、错误处理

| 现象 | 原因 | 解决方案 |
|------|------|---------|
| G盘不可写 | 移动硬盘未挂载/只读 | 重新插拔或换USB口 |
| docker compose pull失败 | 网络/镜像不存在 | 检查Docker镜像源或本地build |
| 端口18080被占用 | 其他服务占用 | 修改port参数 |
| /api/search超时 | 搜索引擎API未配置 | 检查环境变量和API key |
| 数据目录权限不足 | Windows挂载权限 | 以管理员运行Docker Desktop |
| Marvis无法识别 | URL配置错误 | 确认host.docker.internal或127.0.0.1 |

## 九、回滚方案

```bash
# 若迁移后验证失败，执行回滚
cd "$G_PROJECT"
docker compose down

# 恢复E盘原环境（若是迁移模式）
robocopy "$BACKUP_G" "$SRC_E" /E /COPY:DAT /R:2 /W:1

# 重新启动原环境
cd "$SRC_E"
docker compose up -d
```

## 十、健康度自评

| 维度 | 得分 | 说明 |
|------|------|------|
| 时效性 | 25/25 | 2026-07-24重建 |
| 完整性 | 22/25 | 10节完整，部分DeerFlow专有配置需按实际项目调整 |
| 联动度 | 20/25 | 4个联动 |
| 内容质量 | 22/25 | 含流程+参数+示例+错误处理+回滚 |
| **总分** | **89/100** | 🟢优秀 |

## 十一、版本日志

- V1.0 (2026-06-23)：首次创建，基础G盘部署流程
- V1.0→V2.0 (2026-06-27)：新增Compose部署、Marvis联动、调研速查、迁移验证
- V2.0 (2026-07-24)：从工作记忆重建，强化动静分离架构、磁盘熔断规则、回滚方案

---

> 本技能解决DeerFlow项目"往哪放、怎么放、放完怎么验"的问题。部署前务必确认G盘空间与可写性；迁移前务必自动备份。
