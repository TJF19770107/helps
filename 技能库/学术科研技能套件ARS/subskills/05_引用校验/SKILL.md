---
name: ARS引用校验
description: 三层引用校验——结构层（正文引用↔参考文献比对）、格式层（APA7 等）、存在性层（联网核对文献是否真实存在，专治 AI 幻觉编造文献）。零积分脚本为主。
version: 1.0
parent: 学术科研技能套件ARS
lobster:
  cost_mode: zero-credit
  触发词: [引用校验, 查引用, 参考文献核对, 引文检查, APA7校验, 文献真伪, 幻觉检查]
  上游入口: ars/academic-paper/agents/citation_compliance_agent.md
  零积分脚本: scripts/ars_citation_check.py
  可选上游脚本: ars/scripts/check_v3_7_3_three_layer_citation.py
allowed-tools: Read, Grep, Bash(G:/g_venv_ars/Scripts/python.exe *)
---

# 5. 引用校验（防 AI 幻觉最后一关）

## 用途
在稿件定稿前拦截三类问题：漏引/漏列、格式错误、**文献根本不存在（幻觉）**。
**存在性层是本套件防幻觉的核心，强烈建议每次定稿必跑。**

## 触发指令
```
引用校验：draft.md
查引用：核对正文与参考文献是否一一对应
文献真伪：这批参考文献有没有编造的
```

## 执行步骤
1. **跑脚本（零积分，必做）**：
   ```bash
   G:/g_venv_ars/Scripts/python.exe scripts/ars_citation_check.py draft.md --verify --upstream
   ```
   - `--verify`：联网核对每条文献是否真实存在（每条间隔 1s 防限流，最多核对 40 条）
   - `--upstream`：追加调用上游 ARS 三层 lint（需 `G:\g_venv_ars` 的 yaml/markdown）
2. **看 L1 结构层**：`✗ 正文引用了但参考文献表查无对应` → 必须补齐或删除
3. **看 L2 格式层**：年份、DOI 链接、句号
4. **看 L3 存在性层**：`✗ 未命中` 的条目 → **人工逐条打开原文确认**
   > 未命中 ≠ 一定造假（可能是题名截断、中文文献、预印本），但**必须人工确认后才能保留**
5. **人工复核**：抽查比例不低于 20%

## 已实测（2026-09-09）
- 结构层：正确识别出「Brown (2019) 未被正文引用」；已引用条目匹配通过
- 上游 `check_v3_7_3_three_layer_citation.py` 在 `G:\g_venv_ars` 下运行返回 `PASSED`
- 存在性层依赖 CrossRef + OpenAlex，两者均直连可达

## 按需加载白名单
| 文件 | 体量 | 何时读 |
|------|------|--------|
| `agents/citation_compliance_agent.md` | ~6.1k tok | 需要人工级深度校对 |
| `references/apa7_chinese_citation_guide.md` | ~3.9k tok | 中英文 APA7 细节 |
| `references/citation_format_switcher.md` | — | 切换引用格式（MLA/Chicago等） |

## token 消耗预估
| 模式 | 加载内容 | 预估 |
|------|----------|------|
| **纯脚本校验**（默认，推荐） | 本 SKILL + 脚本输出回读 | **≈ 1–2k** |
| 脚本 + 格式精校 | + APA7 中文指南 | **≈ 5–6k** |
| 深度合规审查 | + citation_compliance agent | **≈ 11–13k** |

## 人工核验点（强制，本技能为最后防线）
- [ ] 每一条 `✗ 未命中` 都已人工打开原文或数据库确认
- [ ] 正文引用与参考文献表**双向**一一对应
- [ ] DOI 可解析、卷期页完整
- [ ] **任何 AI 新增的文献，未经人工核验一律不得保留在稿件中**
