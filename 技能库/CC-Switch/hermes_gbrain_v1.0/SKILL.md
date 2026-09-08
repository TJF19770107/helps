---
name: "hermes_gbrain_v1.0"
description: "代码智能分析、架构理解、全仓库搜索、依赖图谱、重构建议。Invoke when 需要理解陌生代码库结构、做跨文件语义搜索、生成架构图、识别技术债务或评估重构风险。"
tags: ["code-analysis", "architecture", "search", "refactor", "dependency", "brain", "hermes", "gstack"]
---

# Hermes G Brain v1.0 — 代码分析与架构理解

## 核心能力

| 能力域 | 具体功能 |
|--------|---------|
| 仓库扫描 | 目录树生成、文件统计、技术栈识别 |
| 语义搜索 | 跨文件函数/类/变量定位，支持正则与模糊匹配 |
| 架构图谱 | 模块依赖关系图、调用链路图、循环依赖检测 |
| 技术债识别 | 重复代码、长函数、高耦合模块、TODO/FIXME 统计 |
| 重构建议 | 提取函数/类、解耦模块、接口抽象方案 |
| 文档生成 | 自动生成 README、API 文档、函数注释 |

## 触发条件

- 接手陌生代码库，需要快速建立全局认知
- 需要跨文件搜索某个功能点的全部实现
- 需要检查模块间耦合度、识别循环依赖
- 需要为重构/迁移提供风险评估和方案
- 需要自动补全缺失的文档或注释

## 标准工作流

### Phase 1：快速定向（<2 分钟）

```bash
# 1. 目录树（只看结构，不看内容）
find . -type f -name "*.py" | head -50
# 或 Windows：
Get-ChildItem -Recurse -Filter "*.py" | Select-Object FullName | Select-Object -First 50

# 2. 技术栈识别
# 检查 package.json / pyproject.toml / Cargo.toml / pom.xml / go.mod
# 确定：语言 / 框架 / 主要依赖

# 3. 入口文件定位
# main.py / index.ts / App.tsx / cmd/ / src/main.*
```

### Phase 2：架构摘要

```markdown
## 架构速览模板

- **项目名称**：<name>
- **技术栈**：<lang> + <framework>
- **核心模块**：
  - `<module_a>/`：<一句话描述>
  - `<module_b>/`：<一句话描述>
- **数据流向**：<入口> → <处理层> → <存储/输出>
- **外部依赖**：<数据库 / API / 消息队列>
- **技术债热点**：<文件名>（<问题描述>）
```

### Phase 3：语义搜索 SOP

```bash
# 查找所有实现某功能的函数（以 Python 为例）
grep -rn "def.*<keyword>" --include="*.py" .

# 查找特定类的所有引用
grep -rn "<ClassName>" --include="*.py" . | grep -v "^.*#"

# 查找 TODO / FIXME / HACK
grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.py" . | wc -l
```

### Phase 4：依赖图谱生成

```bash
# Python 项目
pip install pydeps && pydeps <package_dir> --max-bacon=3 --cluster

# Node.js 项目
npx madge --image graph.svg ./src

# 通用（AST 分析）
# 输出 mermaid 格式的依赖图，供 Hermes WebUI 渲染
```

### Phase 5：重构风险矩阵

| 指标 | 阈值 | 说明 |
|------|------|------|
| 函数行数 | > 50 行 | 建议拆分 |
| 圈复杂度 | > 10 | 建议简化分支 |
| 模块耦合度 | > 5 直接依赖 | 考虑抽象接口 |
| 重复代码率 | > 15% | 提取公共函数 |
| 无测试覆盖率 | > 40% | 重构前先补测试 |

## 与 Hermes / Trae 联动

- Hermes 侧：通过 `/gbrain analyze <path>` 触发分析；结果输出到 `gstack-brain-context`。
- Trae 侧：分析结果自动注入当前会话上下文，增强后续代码生成的准确性。
- 输出格式：优先 Markdown 表格 + Mermaid 图（可被 WebUI 渲染）。
- 全局共享路径：`C:\Users\Administrator\.claude\skills\hermes_gbrain_v1.0\SKILL.md`

## 验收口径

- 目录树和技术栈识别完成，输出≥3条架构洞察
- 语义搜索结果精确（无大量误报）
- 技术债统计有数字依据（文件数/行数）
- 重构建议可操作（指定具体文件和行号）

## 安全边界

- 只读分析，不自动修改任何源文件
- 不上传代码到外部服务
- 敏感文件（.env / secrets / private key）自动跳过，不输出内容
