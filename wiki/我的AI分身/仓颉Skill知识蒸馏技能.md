---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_48124f848fa011f1b052525400826444
    ReservedCode1: BhhQZHq2nXojVdLP4WNssRvWGKliJi1mD7qfXwYPbTSThpHHY0I61UmxqaJP2bKU293Ap4YDV3vm5KLqnNEqdVMm4jQIgQzg0815Bknh4GtRYFVq97Rd4XQSm783bHgeA6bKZzn3OzfqZ6FXz7B7rlNlpGY0YPL2xOzLTx+IAiM+B8JFCyMWdxPHiyY=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_48124f848fa011f1b052525400826444
    ReservedCode2: BhhQZHq2nXojVdLP4WNssRvWGKliJi1mD7qfXwYPbTSThpHHY0I61UmxqaJP2bKU293Ap4YDV3vm5KLqnNEqdVMm4jQIgQzg0815Bknh4GtRYFVq97Rd4XQSm783bHgeA6bKZzn3OzfqZ6FXz7B7rlNlpGY0YPL2xOzLTx+IAiM+B8JFCyMWdxPHiyY=
---

# 仓颉Skill · 知识蒸馏技能 | 知识文档

> 归档日期：2026-08-04 | 版本：基于 GitHub main 分支完整克隆
> 适配体系：龙虾五步法 V3.0 · 全域官方模板 · ORCA 多智能体舰队

---

## 一、项目概述

**cangjie-skill** 是一个元技能（Meta-Skill），将书籍、长视频、播客、课程、访谈等高价值内容蒸馏成 Agent 可直接调用的标准化 Skill 工具包。配套 **RIA-TV++** 完整蒸馏流水线，支持断点续跑、并行提取、三重验证、压力测试。

| 属性 | 值 |
|------|-----|
| 仓库地址 | https://github.com/kangarooking/cangjie-skill |
| 许可证 | GNU AGPL v3 |
| 支持平台 | OpenClaw / Claude Code / Cursor |
| 核心方法论 | RIA-TV++（五阶段 + 并行提取 + 三重验证） |
| 生态定位 | nuwa-skill（蒸馏人）→ cangjie-skill（蒸馏书）→ darwin-skill（自动进化） |

---

## 二、核心能力

### 2.1 RIA-TV++ 蒸馏流水线

```
阶段 0: Adler 整书理解     → BOOK_OVERVIEW.md
阶段 1: 5 个 agent 并行提取 → 候选方法论单元池
阶段 1.5: 三重验证筛选       → 通过的单元（用户轻确认）
阶段 2: RIA++ 构造 skill     → SKILL.md（R/I/A1/A2/E/B 六段）
阶段 3: Zettelkasten 链接    → INDEX.md + GLOSSARY.md
阶段 4: 压力测试             → test-prompts.json + 回炉淘汰
阶段 5: 交付                 → DIGEST.md + 安装到 skills 目录
```

### 2.2 五个专项提取器

| 提取器 | 产出 |
|--------|------|
| 框架提取器（framework） | 决策框架 / 思维模型 |
| 原则提取器（principle） | 原则 / 清单 / 规则 |
| 案例提取器（case） | 作者亲自使用过的实例 |
| 反例提取器（counter-example） | 警告的失败模式 |
| 术语提取器（glossary） | 关键概念词典 |

### 2.3 三重验证

- **V1 跨域**：原文中至少 2 处独立段落佐证
- **V2 预测力**：能回答原文未明说的新问题
- **V3 独特性**：不是常识性内容

通过率通常 25-50%，保证产出的 skill 真正有独立价值。

---

## 三、目录结构

```
cangjie-skill/
├── SKILL.md                    # 元技能定义文件
├── README.md / README.en.md / README.ja.md
├── GITHUB_REPO.md
├── LICENSE
├── extractors/                 # 5个专项提取器 prompt
│   ├── framework-extractor.md
│   ├── principle-extractor.md
│   ├── case-extractor.md
│   ├── counter-example-extractor.md
│   └── glossary-extractor.md
├── methodology/                # 7篇方法论文档
│   ├── 00-overview.md
│   ├── 01-stage0-adler.md
│   ├── 02-stage1-parallel-extract.md
│   ├── 03-stage1.5-triple-verify.md
│   ├── 04-stage2-ria-plus.md
│   ├── 05-stage3-zettelkasten.md
│   ├── 06-stage4-pressure-test.md
│   └── 07-stage5-deliver.md
├── templates/                  # 4个模板文件
│   ├── BOOK_OVERVIEW.md.template
│   ├── SKILL.md.template
│   ├── INDEX.md.template
│   ├── DIGEST.md.template
│   └── test-prompts.json.template
├── scripts/
│   └── generate_star_history.py
└── assets/                     # 品牌资源
```

---

## 四、部署教程

### 4.1 环境依赖

无特殊依赖。cangjie-skill 是纯 Prompt Engineering 技能包，所有 extractor 和 methodology 均为 Markdown 格式的 Agent 指令。只需支持 Skill 调用的 Agent 平台即可。

### 4.2 安装方式

```bash
# 方式一：直接克隆
git clone https://github.com/kangarooking/cangjie-skill.git

# 方式二：镜像加速（国内）
git clone https://gh-proxy.com/https://github.com/kangarooking/cangjie-skill.git

# 方式三：通过 skills add（如 Claude Code / OpenClaw 环境）
npx skills add kangarooking/cangjie-skill
```

### 4.3 本地路径

```
E:\龙虾AI主控中心\我的AI分身\技能库\cangjie-skill\
```

已完整克隆，含全部 extractor、methodology、templates、scripts。

---

## 五、业务场景映射

### 5.1 ORCA 多智能体舰队
- **角色**：内容蒸馏前置处理器
- **用法**：ORCA 舰队从百度网盘获取课程视频 → cangjie-skill 蒸馏成可复用技能 → 注入 ORCA Agent 能力池
- **触发**：用户说「把这门课蒸馏成 skill」→ ORCA 调度 cangjie-skill 流水线

### 5.2 企业接单流水线
- **角色**：专业领域知识萃取工具
- **用法**：客户提供行业资料/培训视频 → cangjie-skill 蒸馏 → 生成可复用的行业知识技能包 → 融入接单交付体系

### 5.3 第二大脑自动化学习体系
- **角色**：知识→技能转化引擎
- **用法**：B站收藏视频 / 百度网盘课程 / 播客 → cangjie-skill 自动蒸馏 → Obsidian 知识库沉淀 → 可被任何 Agent 调用
- **配套**：video-downloader skill（下载视频+提取字幕）→ cangjie-skill（蒸馏技能）

---

## 六、已知限制

1. **需要完整文本输入**：不能凭记忆蒸馏，需要 PDF/字幕/转写稿等原始文本
2. **蒸馏质量依赖输入质量**：机器转写字幕可能影响提取效果
3. **大规模内容需分批**：超长内容需按分块策略处理
4. **部分平台依赖**：最佳体验依赖 OpenClaw/Claude Code 的 sub-agent 并行能力

---

## 七、ORCA 适配方案

### 7.1 接入方式
- cangjie-skill 作为 ORCA 的技能节点，注册于 `orca-worktree-ops` 技能目录
- 通过龙虾五步法 Step2「炼气化神·能力映射」自动发现并调用
- 蒸馏产出的技能自动归入 ORCA 能力池

### 7.2 调用链
```
用户输入 → 龙虾五步法 Step1 意图识别
  → Step2 识别需要内容蒸馏
  → 触发 cangjie-skill RIA-TV++ 流水线
  → Step5 蒸馏产出注入 Obsidian 知识库 + ORCA 技能池
```

### 7.3 与现有技能协同
- **忘语蒸馏模板**：功能重叠，cangjie-skill 更系统化，建议以 cangjie-skill 为标准升级
- **nuwa-skill**：蒸馏人的思维方式 → cangjie-skill 蒸馏方法论 → 两者互补
- **darwin-skill**：cangjie-skill 产出的 test-prompts.json 遵循 darwin 格式，可直接进化

---

## 八、四化执行记录

| 四化 | 状态 | 说明 |
|------|------|------|
| 智能化 | ✅ | Agent 自主识别蒸馏需求，无需用户指定参数 |
| 定制化 | ✅ | 适配龙虾生态路径（E盘技能库 + Obsidian 知识库） |
| 全自动化 | ✅ | Git clone → 文档生成 → 知识库录入 → 技能引用全自动 |
| 自我进化 | ✅ | 蒸馏技能产出可被 darwin-skill 自动进化 |

---

**文档生成**：Marvis Agent | 龙虾五步法 V3.0 | 2026-08-04
*（内容由AI生成，仅供参考）*
