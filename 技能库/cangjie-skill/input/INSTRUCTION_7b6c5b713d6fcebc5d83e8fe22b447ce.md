# 仓颉蒸馏 Agent 指令

> 自动生成 | cangjie_bridge.py v1.1 | 2026-08-06T00:44:50.360774

## 蒸馏目标
- **来源**: 未知
- **作者**: 未知
- **原始链接**: 
- **字数**: 333
- **输入文件**: `E:\龙虾AI主控中心\我的AI分身\技能库\cangjie-skill\input\distill_7b6c5b713d6fcebc5d83e8fe22b447ce.json`

## 执行步骤（按仓颉SKILL.md RIA-TV++ 流水线）

### 阶段0: Adler整书理解
读取 `E:\龙虾AI主控中心\我的AI分身\技能库\cangjie-skill\input\distill_7b6c5b713d6fcebc5d83e8fe22b447ce.json` 中的 body 字段，生成 BOOK_OVERVIEW.md

### 阶段1: 并行提取（5个提取器）
调用仓颉 extractors/ 目录下的5个提取器prompt：
1. `framework-extractor.md` → 决策框架/思维模型
2. `principle-extractor.md` → 原则/清单/规则
3. `case-extractor.md` → 作者亲自使用过的实例
4. `counter-example-extractor.md` → 警告的失败模式
5. `glossary-extractor.md` → 关键概念词典

### 阶段1.5: 三重验证
- V1跨域: 原文中至少2处独立段落佐证
- V2预测力: 能回答原文未明说的新问题
- V3独特性: 不是常识性内容

### 阶段2: RIA++ 构造
将通过验证的单元构造为 SKILL.md（R/I/A1/A2/E/B 六段）

### 阶段3: Zettelkasten链接
生成 INDEX.md + GLOSSARY.md

### 阶段4: 压力测试
生成 test-prompts.json，不合格单元回炉

### 阶段5: 交付
生成 DIGEST.md，安装到 skills 目录

## 输出位置
```
cangjie-skill/output/7b6c5b713d6fcebc5d83e8fe22b447ce/
├── BOOK_OVERVIEW.md
├── SKILL.md
├── INDEX.md
├── GLOSSARY.md
├── DIGEST.md
└── test-prompts.json
```
