---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_d56c045c79b611f1b3d35254007bceed
    ReservedCode1: Iq/zVefj0LzVOeoB/fdGDZyiV3+p8K2Ol3q5IQ4llRX55OdFs/bGiR6LjTJJFaJZJdbgct02yPr43LiZAUCMFjJ4MW4JUee0RpKwoeJTzvF6wTNphJe9H81OhThWn8oTbtVrL3fAs8ww6jpGluI4pgNTOfH6aHp/S3fkyc8103mAS7s+NHrAnrBMMwI=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_d56c045c79b611f1b3d35254007bceed
    ReservedCode2: Iq/zVefj0LzVOeoB/fdGDZyiV3+p8K2Ol3q5IQ4llRX55OdFs/bGiR6LjTJJFaJZJdbgct02yPr43LiZAUCMFjJ4MW4JUee0RpKwoeJTzvF6wTNphJe9H81OhThWn8oTbtVrL3fAs8ww6jpGluI4pgNTOfH6aHp/S3fkyc8103mAS7s+NHrAnrBMMwI=
---



# MT5量化策略开发标准化模板

> **技能ID**: skill-mt5-quant-template-v1.0  
> **创建日期**: 2026-07-07  
> **适用领域**: MetaTrader 5 自动化交易策略开发  
> **来源项目**: 黄金黑马策略V1.7（头肩底形态量化EA）  
> **状态**: 正式版，可复用

---

## 一、技能概述

本技能沉淀了MT5量化策略从源码编写→编译部署→参数联动→文档归档→版本回滚的**全链路标准化流程**。适用于所有基于MQL5语言的MT5 Expert Advisor（EA）开发项目。

### 核心能力清单

| 编号 | 能力 | 说明 |
|------|------|------|
| 1 | 一键生成MQL5源码 | 按策略需求生成完整的`.mq5`源码，内置参数面板、入场/止盈/止损逻辑 |
| 2 | 编译生成EX5 | 通过MetaEditor64编译为可直接运行的`.ex5`文件，零警告零错误 |
| 3 | `.set`配置全场景联动 | 参数在F7面板/策略测试器/实盘Comment/回测可视化四大场景同步生效 |
| 4 | E/C双目录同步 | E盘主仓库←→C盘MT5部署目录双向同步，时间戳/MD5/体积三项校验 |
| 5 | 结构化README | 自动生成含参数说明、回测指南、迭代规范、排查清单的完整文档 |
| 6 | ≤10MB轻量快照 | 每次迭代打包源码+EX5+.set+README，支持一键回滚 |

---

## 二、标准项目结构

```
E:\龙虾AI主控中心\我的AI分身\CODEX量化策略{YYYYMMDD}\{券商}\{策略名}\
├── ea_{策略名}_v{major}.{minor}.mq5          # MQL5源码（主仓库）
├── ea_{策略名}_v{major}.{minor}.ex5          # 编译产物
├── ea_{策略名}_v{major}.{minor}_{param}.set   # 参数配置文件
├── README_{策略名}_v{major}.{minor}.md        # 结构化文档
└── ea_{策略名}_v{major}.{minor}_snapshot_{YYYYMMDD}.zip  # 轻量快照
```

### 双目录映射

| 角色 | 路径 |
|------|------|
| **E盘主仓库** | `E:\龙虾AI主控中心\我的AI分身\CODEX量化策略{YYYYMMDD}\{券商}\{策略名}\` |
| **C盘MT5部署目录** | `C:\Users\{用户名}\AppData\Roaming\MetaQuotes\Terminal\{实例ID}\MQL5\Experts\` |

> MT5实例ID通过 `C:\Users\{用户名}\AppData\Roaming\MetaQuotes\Terminal\` 下查找，格式为32位十六进制字符串。

---

## 三、全链路开发流程（龙虾五步法适配版）

### 步骤1：源码编写

**输入**：策略需求描述（形态识别、入场条件、风控参数）

**执行**：
1. 生成完整 `.mq5` 源码，包含：
   - `#property` 元信息声明
   - 输入参数面板（`input` 变量，覆盖形态点位/均线/手数/止损止盈/点差上限等）
   - Comment 实时校验（图表左上角显示运行参数）
   - Print 日志输出（专家日志记录每次入场决策依据）
   - 入场逻辑（形态识别 → 条件确认 → 开仓）
   - 分批止盈 / 移动止损 / 固定止损
2. 参数默认值使用当前`.set`文件中的值，不硬编码历史参数

**核验**：
- Comment 和 Print 双通道输出，确保参数面板值与内存实际运行值一致
- 参数命名规范：`Inp{分组}{含义}`，如 `InpPatternHighPrice`、`InpStopLossPips`

### 步骤2：编译部署

**工具**：MetaEditor64（MT5自带编译器）

**执行**：
```powershell
# Windows典型路径
& "C:\Program Files\MT5 by {券商}\MetaEditor64.exe" /compile:"{源码路径}\ea_xxx.mq5" /log
```

**验收标准**：0 errors, 0 warnings

**部署**：将编译生成的 `.ex5` 拷贝至C盘MT5部署目录，确保MD5与E盘编译产物一致：
```powershell
(Get-FileHash "{C盘路径}\ea_xxx.ex5" -Algorithm MD5).Hash
(Get-FileHash "{E盘路径}\ea_xxx.ex5" -Algorithm MD5).Hash
```

### 步骤3：参数联动配置

**核心原则**：`.set` 文件是唯一持久化参数标准。四大场景必须同步：

| 场景 | 载体 | 生效方式 |
|------|------|----------|
| F7原生面板 | MT5图表 → 右键 → EA属性 | 加载.set后参数填入面板 |
| 策略测试器 | Ctrl+R → 输入标签页 | 加载.set后参数同步至输入框 |
| 实盘图表 | 图表左上角 Comment | EA运行时读取内存参数实时显示 |
| 回测可视化 | 回测图表Comment + 交易表格 | EA运行时读取参数，回测后展示 |

**关键约束**：
- 策略测试器手动改值仅临时生效，重启MT5后回弹为.set原始值
- 任何参数变更必须更新.set并双向同步到E/C双目录
- `.set` 文件命名格式：`ea_{策略名}_v{major}.{minor}_{核心参数}.set`

### 步骤4：文档生成

**README 标准结构**：

| 章节 | 内容 |
|------|------|
| 一、策略概述 | 策略名、版本、适用品种/周期、核心思想 |
| 二、入场规则 | 形态识别条件、五重确认逻辑、参数说明 |
| 三、参数面板 | 核心参数对照表（参数名/默认值/含义/联动说明） |
| 四、交易执行 | 手数计算、分批止盈、止损、交易表格校验标准 |
| 五、部署指南 | 安装路径、.set加载教程、回测步骤 |
| 六、迭代规范 | 版本号规则、变更记录、.set覆盖三场景 |
| 七、注意事项与排查 | 不开仓排查清单、策略测试器风险警告 |
| 八、双目录归档 | E/C双路径、双向同步规则、轻量快照约束 |

**不可回退约束**：已被验收通过的修订项（四大场景联动、策略测试器说明、排查清单）在后续文档更新中禁止删除或缩水。

### 步骤5：版本快照与回滚

**快照内容**：源码(.mq5) + 编译产物(.ex5) + 参数配置(.set) + 文档(README.md)

**体积约束**：≤10MB（MQL5项目天然满足，文本文件压缩率极高）

**命令**：
```powershell
Compress-Archive -Path "*.mq5", "*.ex5", "*.set", "README*.md" -DestinationPath "ea_xxx_snapshot_{YYYYMMDD}.zip"
```

**回滚流程**：
1. 解压快照包到临时目录
2. 覆盖E盘主仓库对应文件
3. 拷贝ex5到C盘MT5部署目录
4. 在MT5中重新加载EA验证

---

## 四、QA验收清单

以下检查项必须在每次迭代交付前逐条验证：

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 源码编译 | 0 errors, 0 warnings |
| 2 | Comment校验 | 图表左上角显示的参数与.set一致 |
| 3 | Print校验 | 专家日志输出参数与.set一致 |
| 4 | EX5 MD5一致 | E盘和C盘EX5的MD5哈希完全相同 |
| 5 | .set同步 | E/C双目录.set文件内容一致 |
| 6 | 文档版本 | README中参数默认值、路径、版本号与实际一致 |
| 7 | 排查清单 | 不开仓排查清单覆盖当前版本所有入场条件 |
| 8 | 快照可用 | 最新快照.zip存在且≤10MB |

---

## 五、复用指南

### 新项目启动

1. 复制本模板到新策略目录
2. 修改策略名称、入场逻辑、参数定义
3. 按步骤1→5顺序执行完整流程
4. 首次迭代即生成快照作为基线

### 迭代开发

1. 修改 `.mq5` 源码
2. 编译 → 验证MD5 → 部署EX5
3. 更新 `.set`（如有参数变更）
4. 同步更新 README 相关章节
5. 生成新快照，保留上一版本快照作为备份

### 故障恢复

1. 解压最近一次有效快照
2. 覆盖E盘仓库 → 重新部署C盘EX5
3. 在策略测试器中加载.set验证

---

## 六、已沉淀项目经验

| 经验编号 | 来源 | 类型 | 要点 |
|----------|------|------|------|
| EXP-001 | V1.7 | 参数管理 | 全局统一唯一目标值，废弃历史默认值；禁止硬编码参数 |
| EXP-002 | V1.7 | 文档同步 | 删除"永久锁定"等过时措辞，改为"动态可配置" |
| EXP-003 | V1.7 | 参数联动 | 四大场景必须同步：F7面板/策略测试器/实盘Comment/回测可视化 |
| EXP-004 | V1.7 | 测试风险 | 策略测试器手动改值仅临时生效，重启回弹 |
| EXP-005 | V1.7 | 双目录 | E/C双路径归档+三项校验，防止版本分叉 |
| EXP-006 | V1.7 | 快照 | 每次迭代打包≤10MB快照，支持一键回滚 |
| EXP-007 | V1.7 | Comment/Print | 永久保留双通道校验代码，作为可视化核验手段 |

---

> **归档位置**: `E:\龙虾AI主控中心\我的AI分身\技能库\MT5量化策略标准化开发技能包\`  
> **适用范围**: 所有MQL5 EA策略开发项目  
> **路径变更记录**: 2026-07-07 由 `skill_knowledge\编程开发\` 迁移至 `我的AI分身\技能库\MT5量化策略标准化开发技能包\`（量化资源独立分区）  
> **最后更新**: 2026-07-07
*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*
