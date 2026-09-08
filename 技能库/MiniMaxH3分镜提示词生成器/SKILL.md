---
title: "MiniMax H3 分镜提示词生成器"
summary: 一句中文需求 → 可直接粘贴海螺(MiniMax H3)的5秒分段专业分镜提示词；含四模块模板、角色一致性卡、海螺实操参数
tags: [MiniMax, H3, 海螺, 视频提示词, 分镜, 出片库]
trigger: ["H3提示词", "分镜提示词", "H3写提示词", "海螺提示词"]
source: MiniMax官方H3仓库README + ComfyUI官方教程 + 汤哥Y2K MV需求（2026-09-09 定型）
distilled_by: 汤小龙（WorkBuddy）· 1234快捷4
version: v1.0
date: 2026-09-09
---

# MiniMax H3 分镜提示词生成器 SKILL v1.0

> **用途**：接收一句中文需求，输出 N 段「5秒/段」的专业分镜提示词，每段可直接复制粘贴到海螺 WebApp 生成视频，最后剪映拼接成片。
> **前世今生**：短视频流传的 `h3-prompt-writing` skill 源头仓库 404 为假，本 SKILL 为汤小龙按官方文档重建的本地替代版，零依赖、零积分。

## 一、触发与输入

- **触发词**：H3提示词 / 分镜提示词 / H3写提示词 / 海螺提示词
- **输入格式**：`<题材/内容> + <风格> + <总时长> + <画幅>`
- **示例**：`H3提示词 一个Y2K风格45秒MV，赛博都市夜景，16:9`
- 汤哥没给全时按默认补：风格=写实电影感、时长=15秒、画幅=16:9，并在输出头部注明假设

## 二、生成规则（硬性）

1. **分段数 = 总时长 ÷ 5**（H3 单次输出 4-15 秒，5 秒/段最稳；45 秒 = seg01~seg09）
2. 每段必须包含**四模块**（缺一不可）：
   ```
   【整体场景】人物 + 地点 + 时间 + 光线 + 视觉风格
   【0-3秒】景别 + 人物动作 + 摄像机运动
   【3-5秒】切镜 + 表情/动作变化 + 场景变化
   【声音】环境声 + 动作音效 + (对白) + BGM 情绪
   ```
3. **角色一致性卡**（多段必用）：第 1 段前先输出一段「角色卡」——把主角外貌/服装/发色固化为一段固定描述文本，**后续每段原样复用**，跨段粘贴不改一字
4. **对白红线**：中文对白海螺本地生成易发音不准 → 画面交给 H3，对白走 edge-tts 单独生成再混音（对齐零成本口播片配方）；提示词内只写 `(无对白)` 或标注「对白后期TTS」
5. **每段输出格式**：中文版（给人看）+ 英文版（贴海螺，实测中英均可但英文更稳）
6. 段与段之间注明衔接点（尾帧=下段首帧，便于海螺首尾帧功能串联）

## 三、输出模板（照此产出）

```
═══ 角色卡（所有段落复用）═══
A young woman in her 20s with silver-dyed short hair, wearing a
translucent purple techwear jacket, chrome accessories, Y2K style...

═══ seg01 (0-5s) ═══
【中文】……
【EN】Golden hour on an elevated city highway, holographic billboards
flickering. 0-3s: medium shot, camera dolly-in as the woman leans on
a chrome railing, wind in her hair. 3-5s: cut to close-up, she turns
to camera and smirks. Sound: synthwave bass, distant traffic hum,
upbeat Y2K pop BGM. (No dialogue)

═══ seg02 (5-10s) ═══
（同结构；首帧衔接 seg01 尾帧……）
```

## 四、海螺实操（生成端）

| 项 | 值 |
|---|---|
| 入口 | https://hailuoai.com/tools/minimax-h3 （汤哥账号已注册：Hailuo UID 378569307197890566） |
| 单段 | 粘贴一段 EN 提示词 → 生成 5 秒 → 下载 |
| 串联 | 需要角色/构图严格衔接时用「首尾帧」：上段尾帧截图作下段首帧 |
| 额度 | 免费积分制（截图时余 60 积分），烧完再评估 API（$0.08/秒 量级，须过性价比协议） |
| 后期 | 全部段下载后 → 剪映拼接 + edge-tts 对白 + BGM 对齐 + 字幕 |
| 许可 | Community License 排除美欧英韩展示；接单商用前查最新条款 |

## 五、生成后动作（Agent 必做）

1. 输出的全部分镜写入 `01_正在执行实单/【日期_客户_H3视频】/需求确认文档/分镜提示词.md`（或临时单 `G:\tmp\`）
2. 生成结束问汤哥是否归档本案例 prompt → 效果好的回灌本 SKILL §六 案例库
3. 效果差的方向（如运镜词海螺不认）记录进 §六 踩坑

## 六、案例库与踩坑（持续回灌）

- （待首个实战案例回灌）

*v1.0 · 汤小龙 · 零积分本地技能 · 源头核验见《20260908_MiniMaxH3视频模型核验与接入路线_四化迭代.md》*
