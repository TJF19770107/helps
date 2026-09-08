---
name: 龙虾引用校验
description: 三层引用校验——结构/格式/存在性，联网核对文献真伪专治 AI 幻觉。自有版权脚本，零积分。
version: 1.0
parent: 龙虾科研辅助技能包
lobster:
  cost_mode: zero-credit
  触发词: [引用校验, 查引用, 参考文献核对, 引文检查, APA7校验, 文献真伪, 幻觉检查]
allowed-tools: Read, Grep, Bash(G:/g_venv_ars/Scripts/python.exe *)
---

# 5. 引用校验（自研，防幻觉最后一关）

## 用途
定稿前拦截：漏引/漏列、格式错误、**文献不存在（幻觉）**。存在性层为核心，定稿必跑。

## 触发指令
```
引用校验：draft.md
文献真伪：这批参考文献有没有编造的
```

## 执行步骤
1. **跑脚本（零积分，必做）**：
   ```bash
   G:/g_venv_ars/Scripts/python.exe scripts/lobster_citation_check.py draft.md --verify
   ```
   - L1 结构层：正文引用 ↔ 参考文献表双向比对
   - L2 格式层：年份/DOI 链接/句号
   - L3 存在性层：`--verify` 联网核对每条文献（CrossRef+OpenAlex，1s 间隔防限流，≤40 条）
2. `✗ 未命中` ≠ 一定造假（中文文献/预印本/题名截断都会未命中），**但保留前必须人工打开原文确认**
3. 抽查 ≥20% 人工复核

## token 预估
| 模式 | 预估 |
|------|------|
| 纯脚本校验（默认） | **≈ 1–2k** |
| + 写作原则参考 | ≈ 5–8k（读 `general-principles.md`，MIT） |

## 人工核验点（最后防线）
- [ ] 每条未命中已人工确认
- [ ] 双向一一对应，DOI 可解析、卷期页完整
- [ ] 任何 AI 新增文献未经核验不得保留
