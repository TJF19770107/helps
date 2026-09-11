---
name: 龙虾论文写作与大纲
description: 选题头脑风暴→大纲→章节起草→风格审计→压缩的写作流水线。融合 MIT 素材（头脑风暴34问/修辞动作/风格门禁/论文类型模板），交付骨架与建议，禁全文代写。
version: 1.0
parent: 龙虾科研辅助技能包
lobster:
  cost_mode: low
  触发词: [论文写作, 论文大纲, 章节起草, 写作提纲, 润色压缩, 选题头脑风暴, 论文结构]
allowed-tools: Read, Glob, Bash(G:/g_venv_ars/Scripts/python.exe *)
---

# 3. 论文写作与大纲（自研流程 + MIT 素材）

## 用途
✅ 选题收敛、大纲、章节骨架、字数分配、修辞结构、风格审计、压缩
❌ 学位论文/课程论文全文或整章代写

## 触发指令
```
论文大纲：AI 对高教品保的影响（IMRaD，8000字）
选题头脑风暴：我对 AI 教育应用有兴趣但不确定方向
章节骨架：Introduction 段落级提纲
压缩：第4节超页 30%，帮我压
```

## 五阶段流水线
1. **选题头脑风暴**：读 `参考文献写作素材/brainstorming_guide.md`（34 问六阶段，MIT）；
   研究空白须有 **3–5 篇真实引用支撑**（先跑技能 1 拿到真实文献）
2. **架构**：按论文类型读模板（全部 MIT，本包内）：
   `journal-theoretical.md` / `conference-experimental-10page.md` / `conference-short-5page.md` / `conference-theoretical-10page.md`
3. **章节起草**：读 `参考文献写作素材/rhetorical_moves.md`（各节修辞动作）+ `abstract-and-intro.md`（摘要与引言模板）；
   **只出骨架与段落功能说明，正文由客户作者撰写**
4. **风格审计**：读 `参考文献写作素材/gate_mechanical.md`（M1–M18 机械门禁：破折号滥用/空洞词/被动语态/冗词）；
   需要跑质量门禁脚本时用 `质量门禁/gap_analysis.py`、`chapter_quality_check.py`、`final_evaluation.py`（MIT，实测可运行）
5. **压缩**：读 `参考文献写作素材/compression_patterns.md`，目标压缩 30–50%

## 加载纪律（单次只取 ≤3 个素材文件）
| 文件 | 体量级别 | 何时读 |
|------|----------|--------|
| `rhetorical_moves.md` / `abstract-and-intro.md` | 中 | 章节起草 |
| `brainstorming_guide.md` | 中 | 选题阶段 |
| `gate_mechanical.md` / `compression_patterns.md` | 中 | 审计/压缩 |
| `paper-types/*.md` | 小 | 定模板 |
| `checklists.md` | 小 | 投稿前自检 |

## token 预估
| 模式 | 预估 |
|------|------|
| 大纲+模板（默认） | **≈ 6–10k** |
| 全流程五阶段 | ≈ 18–25k（建议分多次会话） |

## 合规红线
- 骨架可交付，成文不行；学位论文整章/全文一律拒绝
- 大纲中的引用必须来自技能 1 已核验清单
- 交付时附：「本骨架为结构建议，全部论点与数据需作者自行补充核实」
