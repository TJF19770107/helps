---
name: opc-customized-deployment
description: 定制化部署：把 OPC 庄家团与产出物适配到龙虾本地路径、CNB 云原生格式与企业微信接单群。
triggers:
  - 同步 CNB
  - 同步企业微信
  - 定制路径
  - 云原生格式
---

# OPC 定制化部署技能

## 适配清单

| 目标环境 | 本地路径/格式 | 同步方式 |
|----------|---------------|----------|
| 本地技能库 | `技能库/agency-agents/one-person-company/` | 写入 Markdown |
| OPC 庄家团 | `opc-doc/orchestrator/team/` | 写入 experts/skills/connectors |
| CNB 云端 | `企业微信群定制接单项目/.cnb/` | 写入 YAML + 更新 settings.yml |
| 企微接单 | `企业微信群定制接单项目/scripts/` | 提供调用接口文档 |
| Obsidian | `技能库/lobster_task_standard_workflow_v3.0/opc-skills/` | Markdown 索引 |

## 安全约束
- CNB AI Credits > 80% 时仅做本地文件准备，不触发云端构建。
- 不修改 `.git/config`，不提交密钥。
- `Obsidian知识库/` 目录沙箱禁区，只写授权的技能库目录。

## 输出
- 同步状态报告
- 受影响的文件列表
