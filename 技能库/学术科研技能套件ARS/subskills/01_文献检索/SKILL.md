---
name: ARS文献检索
description: 用免费学术 API（arXiv/CrossRef/OpenAlex/Semantic Scholar）做系统性文献检索、文献矩阵、综述素材收集与来源可信度分级。零积分本地脚本执行，禁止凭空编造文献。
version: 1.0
parent: 学术科研技能套件ARS
lobster:
  cost_mode: zero-credit
  触发词: [文献检索, 找文献, 文献综述, 系统性回顾, 文献矩阵, 查文献, 事实核查, 研究方向]
  上游入口: ars/deep-research/WORKFLOW.md
  零积分脚本: scripts/ars_lit_search.py
allowed-tools: Read, Grep, Bash(G:/g_venv_ars/Scripts/python.exe *)
---

# 1. 文献检索

## 用途
以零积分方式获取真实存在的学术文献，产出可核验的文献清单 / 文献矩阵，支撑综述与选题。
**本技能不写论文正文**，只负责「找到并核实文献」。

## 触发指令
```
文献检索：大模型在高等教育质量保障中的应用
找文献：social media addiction adolescents
文献矩阵：近五年 元分析 在线学习成效
```

## 执行步骤（按顺序，不得跳步）
1. **先跑脚本拿真实数据**（零积分，必做）
   ```bash
   G:/g_venv_ars/Scripts/python.exe scripts/ars_lit_search.py \
     --source all --q "英文关键词" --limit 20 --out refs.json --cache .cache
   ```
   中文课题：中英双语各跑一次；必要时读 `chinese_literature_api_protocol.md`（⚠ 10.7k tokens，需报备）
2. **粗筛**：按年份（默认近 5–10 年）、来源层级、是否同行评审过滤
3. **定级**：读 `source_quality_hierarchy.md`，给每条文献标注证据等级
4. **成表**：套 `literature_matrix_template.md` 产出文献矩阵（作者/年份/方法/样本/结论/局限）
5. **核验**：抽查 ≥20% 条目，人工打开 DOI/URL 确认标题作者一致

## 零积分脚本参数
| 参数 | 说明 |
|------|------|
| `--source` | `arxiv` / `crossref` / `openalex` / `s2` / `all` |
| `--q` | 关键词（**英文命中率显著更高**） |
| `--limit` | 每源条数 |
| `--out` | 结果存 JSON |
| `--cache` | 缓存目录，同课题不重复联网 |
| `--abstract` | 带摘要输出 |

**连通性已实测**：三个 API 均直连可达（200），无需代理、无需密钥。

## 按需加载白名单（禁止越界读取）
| 文件 | 体量 | 何时读 |
|------|------|--------|
| `references/arxiv_api_protocol.md` | ~2.1k tok | 需调arXiv细节 |
| `references/openalex_api_protocol.md` | ~2.0k tok | 需调OpenAlex细节 |
| `references/source_quality_hierarchy.md` | ~3.1k tok | 证据定级 |
| `templates/literature_matrix_template.md` | ~1.2k tok | 成表 |
| `WORKFLOW.md` | ~11.3k tok | 系统性回顾/PRISMA 流程 |
| `agents/source_verification_agent.md` | ~3.2k tok | 来源真实性核查 |
| ⚠ `agents/bibliography_agent.md` | ~10.2k tok | **需报备** |
| ⚠ `agents/socratic_mentor_agent.md` | ~16.6k tok | **需报备**（选题迷茫时用） |

## token 消耗预估
| 模式 | 加载内容 | 预估 |
|------|----------|------|
| **轻量检索**（默认） | 本 SKILL + 2 个 API 协议 + 脚本 | **≈ 3–5k** |
| 标准综述 | + 质量层级 + 文献矩阵模板 + WORKFLOW | **≈ 16–19k** |
| 深度系统性回顾 | + bibliography/source_verification agent | **≈ 30k（需报备）** |

> 脚本执行本身 **0 积分**（本地 HTTP 请求免费学术 API）。

## 人工核验点（强制，不可省略）
- [ ] 每条文献的 **标题、作者、年份** 与原文一致（不得凭模型记忆补全）
- [ ] DOI 能真实解析（打不开的一律剔除）
- [ ] 综述结论不得超出已核验文献的支持范围
- [ ] 标注「AI 未核实」的条目禁止进入正式稿件
