---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 58152cf0aacf686f4558d7a7c43bec24_49cbf1c161a611f18f065254007bceed
    ReservedCode1: TmvkFrLjDTZzyNuE0sR/K+S9bGVCY+tdSxdW1vhovVI/lBG5g8z5RHdXfQEEqrR7iGcjyaJCrOYgupLXPhM8k7luhN8NiH93MYYoNf5vqt1vjkzfmFGoVncAWYadkbcW1Emmob9MeuUETZZMUo2tISe4V2ABn8BuUslKCL5NyKn4mmAhtWkGnOfohAo=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 58152cf0aacf686f4558d7a7c43bec24_49cbf1c161a611f18f065254007bceed
    ReservedCode2: TmvkFrLjDTZzyNuE0sR/K+S9bGVCY+tdSxdW1vhovVI/lBG5g8z5RHdXfQEEqrR7iGcjyaJCrOYgupLXPhM8k7luhN8NiH93MYYoNf5vqt1vjkzfmFGoVncAWYadkbcW1Emmob9MeuUETZZMUo2tISe4V2ABn8BuUslKCL5NyKn4mmAhtWkGnOfohAo=
---

# AI分身蒸馏_R26

**版本**: 3.0

AI分身全自动六步蒸馏流程的MCP工具定义集，含蒸馏专用工具、质量门控校验、状态锁管理。R26新增Goal模式持久化执行和执行可验证性。

## 质量门控
- **G1 (实事求是)**: verify_output_traceability
- **G2 (MD5去重)**: md5_dedup_check
- **G3 (路径合规)**: output_path_validation
- **G4 (对标校验)**: benchmark_matrix_validation
- **G5 (全局一致性)**: cross_file_consistency_verification

## 工具定义

### 1. distill_personality

步骤1：分析自己 — 基于角色总说明书/SOUL/USER/AGENTS及历史迭代记录生成用户人格画像

#### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| config_paths | array | 是 | 核心配置文件的绝对路径列表：角色总说明书/SOUL/USER/AGENTS |
| round_number | string | 是 | 蒸馏轮次编号 |
| previous_portrait | string | 否 | 上轮用户人格画像文件路径（可选，用于对比） |
| output_path | string | 是 | 产出文件目标路径 |

#### 输出

| 字段 | 类型 | 说明 |
|------|------|------|
| file_path | string | 生成的人格画像文件路径 |
| file_size_bytes | integer |  |
| quality_gate | string |  |
| sections_count | integer | 文档章节数 |
| new_findings | array | 本轮新发现摘要列表 |

#### 执行约束
- **requires_lock**: True
- **max_retries**: 3
- **timeout_seconds**: 300
- **permission_level**: auto

### 2. distill_plan

步骤2：制定计划 — 对齐双轨工作流，生成R26进化规划

#### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| portrait_path | string | 是 | 步骤1产出的人格画像文件路径 |
| config_paths | array | 是 | 角色总说明书/当前SOUL/USER/AGENTS路径 |
| round_number | string | 是 |  |
| benchmark_target | object | 否 | 对标矩阵目标设定 |
| candidate_protocols | array | 否 | 候选技能协议编号列表 |
| output_path | string | 是 |  |

#### 输出

| 字段 | 类型 | 说明 |
|------|------|------|
| file_path | string |  |
| sections_count | integer |  |
| short_term_goals | array |  |
| mid_term_goals | array |  |
| quality_gate | string |  |

#### 执行约束
- **requires_lock**: True
- **max_retries**: 3
- **timeout_seconds**: 300
- **permission_level**: auto

### 3. distill_convert_files

步骤3：文件转换 — 扫描全目录非MD文件，转换为MD格式并MD5去重

#### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| root_path | string | 是 | 扫描根目录 |
| target_formats | array | 否 | 需要转换的源文件格式列表 |
| exclude_patterns | array | 否 | 排除模式 |
| output_log_path | string | 是 |  |
| round_number | string | 是 |  |

#### 输出

| 字段 | 类型 | 说明 |
|------|------|------|
| log_path | string |  |
| total_scanned | integer |  |
| converted_count | integer |  |
| skipped_count | integer |  |
| failed_count | integer |  |
| quality_gate | string |  |

#### 执行约束
- **requires_lock**: True
- **max_retries**: 2
- **timeout_seconds**: 600
- **permission_level**: confirm_for_large_batch
- **agent**: OpenClaw龙虾Agent

### 4. distill_knowledge_base

步骤4：构建知识库 — 遍历全目录文件统计+提取概念词条+生成知识图谱索引

#### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| root_path | string | 是 |  |
| previous_index | string | 否 | 上轮知识库索引文件路径（用于增量对比） |
| min_concept_count | integer | 否 | 最少提取概念词条数 |
| output_path | string | 是 |  |
| round_number | string | 是 |  |

#### 输出

| 字段 | 类型 | 说明 |
|------|------|------|
| file_path | string |  |
| total_files | integer |  |
| file_type_distribution | object |  |
| concept_count | integer |  |
| new_concepts | array |  |
| knowledge_domains | array |  |
| quality_gate | string |  |

#### 执行约束
- **requires_lock**: True
- **max_retries**: 2
- **timeout_seconds**: 300
- **permission_level**: auto

### 5. distill_create_self_skill

步骤5：创建self-skill — 基于步骤1-4产出和参考版本，生成技能定义三件套

#### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| portrait_path | string | 是 | 步骤1产出路径 |
| plan_path | string | 是 | 步骤2产出路径 |
| index_path | string | 是 | 步骤4产出路径 |
| previous_skill_path | string | 是 | 上轮self-skill文件路径（作为模板参考） |
| previous_mcp_path | string | 是 | 上轮mcp-tools文件路径 |
| previous_capabilities_path | string | 是 | 上轮agent-capabilities文件路径 |
| round_number | string | 是 |  |
| new_protocols | array | 否 | 本轮新增/升级的技能协议编号 |
| output_dir | string | 是 |  |

#### 输出

| 字段 | 类型 | 说明 |
|------|------|------|
| skill_file | string | self-skill .md文件路径 |
| mcp_file | string | mcp-tools .json文件路径 |
| capabilities_file | string | agent-capabilities .md文件路径 |
| quality_gate | string |  |

#### 执行约束
- **requires_lock**: True
- **max_retries**: 3
- **timeout_seconds**: 480
- **permission_level**: auto

### 6. distill_update_core_config

步骤6：更新核心配置 — SOUL/USER/AGENTS版本升级 + 角色总说明书更新

#### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| soul_path | string | 是 | SOUL.md当前路径 |
| user_path | string | 是 | USER.md当前路径 |
| agents_path | string | 是 | AGENTS.md当前路径 |
| master_doc_path | string | 是 | 角色总说明书当前路径 |
| soul_new_version | string | 否 |  |
| user_new_version | string | 否 |  |
| agents_new_version | string | 否 |  |
| master_doc_new_version | string | 否 |  |
| plan_path | string | 否 | 步骤2进化规划路径（提取升级内容） |
| portrait_path | string | 否 | 步骤1人格画像路径 |
| round_number | string | 是 |  |
| r26_intelligence_summary | object | 否 | R26情报摘要（角色总说明书新章节内容） |

#### 输出

| 字段 | 类型 | 说明 |
|------|------|------|
| soul_new_path | string |  |
| user_new_path | string |  |
| agents_new_path | string |  |
| master_doc_new_path | string |  |
| version_changes | array |  |
| quality_gate | string |  |

#### 执行约束
- **requires_lock**: True
- **max_retries**: 2
- **timeout_seconds**: 300
- **permission_level**: confirm
- **agent**: Hermes Agent

### 7. distill_sync_sub_agents

全域同步 — 将核心配置三元组同步到豆包Agent/Hermes Agent/OpenClaw的config目录

#### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| soul_path | string | 是 | 最新SOUL.md路径 |
| user_path | string | 是 | 最新USER.md路径 |
| agents_path | string | 是 | 最新AGENTS.md路径 |
| target_agents | array | 是 |  |
| verify_keywords | array | 否 | 抽查验证关键词列表（确认同步完整性） |
| round_number | string | 是 |  |

#### 输出

| 字段 | 类型 | 说明 |
|------|------|------|
| sync_log_path | string |  |
| synced_agents | array |  |
| md5_checksums | object | 各副本MD5哈希 |
| spot_check_passed | boolean | 抽查验证是否通过 |
| quality_gate | string |  |

#### 执行约束
- **requires_lock**: True
- **max_retries**: 2
- **timeout_seconds**: 120
- **permission_level**: auto
- **agent**: Hermes Agent

### 8. distill_r26_goal_mode_execute

R26新增 — Goal模式持久化执行：心跳检测+退出拦截+幻觉拦截+重试预算。在六步全流程中持续监控执行状态。

#### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| steps | array | 是 | 待执行的步骤编号列表 |
| heartbeat_interval_seconds | integer | 否 |  |
| max_retry_budget | integer | 否 | 每步骤最大重试次数 |
| verify_output_real_check | boolean | 否 | 是否执行IO级产出验证（非缓存） |
| log_path | string | 是 | 执行日志输出路径 |

#### 输出

| 字段 | 类型 | 说明 |
|------|------|------|
| completed_steps | array |  |
| failed_steps | array |  |
| degraded_steps | array |  |
| heartbeat_log | array |  |
| execution_time_seconds | number |  |
| goal_mode_verdict | string |  |

#### 执行约束
- **requires_lock**: True
- **max_retries**: 3
- **timeout_seconds**: 1800
- **permission_level**: auto
- **r26_only**: True

## 状态锁
- **Lock File**: .distillation_lock
- **Lock Path**: E:\龙虾AI主控中心\我的AI分身\定时任务\.distillation_lock
- **Timeout Seconds**: 1800
- **Heartbeat Interval Seconds**: 15
- **Auto Release On Timeout**: True
- **Force Unlock Command**: Remove-Item .distillation_lock

## 对标矩阵
- 当前版本: v3.18
- 当前评分: 98.3
- 目标版本: v3.19
- 目标评分: 98.6

## 协议清单
- 已建立: 87
- R26 正式化协议:
  - #88 Goal模式Agent持久化执行
  - #90 AI视频创作商业闭环分析

## R26 Goal 模式特性

### Heartbeat Detection
- **Source**: Claude Code Stop Hook
- **Interval Seconds**: 15
- **Action On Miss**: auto_release_lock + alert

### Exit Interception
- **Source**: Codex goal模式
- **Check Method**: verify_output_file_exists_on_disk
- **Prevent Premature Exit**: True

### Hallucination Interception
- **Source**: Hermes五层防烂尾
- **Gate**: G1
- **Method**: IO-level_disk_verification_not_cache

### Retry Budget
- **Max Per Step**: 3
- **Backoff Strategy**: incremental_5s
- **On Budget Exhausted**: degrade_step + log

## Agent 版本矩阵
- **豆包Agent**: v10.3_R26
- **Hermes Agent**: v3.8_R26
- **OpenClaw龙虾Agent**: v3.8_R26
*（内容由AI生成，仅供参考）*
