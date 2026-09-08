# THIRD_PARTY.md · 第三方组件声明

本包融合了以下 **MIT 许可**开源项目的组件。按 MIT 许可要求，分发时必须保留本声明及各组件版权声明。

## 1. claude-skill-paper-writing（vendored 素材）

- 来源：https://github.com/Liuyuan999/claude-skill-paper-writing
- 许可：MIT License — Copyright (c) 2026 Liuyuan999
- 融入文件（`参考文献写作素材/`）：
  - `abstract-and-intro.md`、`rebuttals.md`、`checklists.md`、`general-principles.md`
  - `paper-types/journal-theoretical.md`、`conference-theoretical-10page.md`、
    `conference-experimental-10page.md`、`conference-short-5page.md`
- 注：其知识源为 Simon Peyton Jones / Jennifer Widom / Jacob Steinhardt 等公开写作建议的**转述提炼**（原作者 README 声明不含原文逐字复制）

## 2. paper-writing-skill（vendored 素材）

- 来源：https://github.com/SNL-UCSB/paper-writing-skill
- 许可：MIT License — Copyright (c) 2026 Arpit Gupta
- 融入文件（`参考文献写作素材/`）：
  - `brainstorming_guide.md`、`gate_mechanical.md`、`compression_patterns.md`、`rhetorical_moves.md`

## 3. academic-paper-skills（vendored 脚本）

- 来源：https://github.com/lishix520/academic-paper-skills
- 许可：MIT License — Copyright (c) 2025 Li Shixiong
- 融入文件（`质量门禁/`）：
  - `gap_analysis.py`、`evaluate_samples.py`、`final_evaluation.py`、`chapter_quality_check.py`

## 4. 参考过但未融入的仓库

- **kchemorion/academic-manuscript-skill**：README 自称 MIT 但仓库内**无 LICENSE 文件** → 按「先实测再采信」原则，未复制其任何代码，仅借鉴思路。

## 5. 明确排除

- **ARS（academic-research-skills 及其 ARS-Codex 发行版）**：LICENSE 实测为 **CC BY-NC 4.0**（Copyright 2026 Cheng-I Wu）——**非商用**。
  本包内**不含**其任何文件；其内容仅存放于内部参考目录（`学术科研技能套件ARS` 上游留档），不随本包分发、不用于商用交付。

## 自有版权部分（无第三方依赖）

- `scripts/lobster_lit_search.py`、`scripts/lobster_sql_query.py`、`scripts/lobster_citation_check.py`
- `subskills/` 全部 5 个 SKILL.md、根 `SKILL.md`、`README.md`
