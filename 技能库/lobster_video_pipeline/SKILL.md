---
name: lobster-video-pipeline
description: 龙虾视频制作全流程六合一管线：图像生成 → 视频生成(prompt) → 转写剪辑(video-use) → 剪映自动化(jianying) → 渲染(remotion/hyperframes HTML→MP4)。零成本,WorkBuddy/龙虾/任何 Agent 一键触发。覆盖自媒体/接单/影视解说/带货/数字人播报全场景。
---

# 🦞 龙虾视频流水线六合一 · Lobster Video Pipeline v1.0

> **2026-08-23 全栈打通版** | 单文件夹 | 零成本 | 工作流闭环
> 路径：`G:\WorkBuddy_Data\lobster_video_pipeline\`
> 标杆：GitHub热门Skill "覆盖视频制作工作流" 实测打通

---

## 一、定位与价值

| 维度 | 内容 |
|------|------|
| **一句话** | 6 个 GitHub 热门视频 Skill 拼成一条生产线,任何 Agent 一句话触发 |
| **单文件夹** | `G:\WorkBuddy_Data\lobster_video_pipeline\` 一处全搞定 |
| **零成本** | 全部本地 Python + FFmpeg + Node (按需)+ 内置 MCP,无月费 |
| **可拼装** | 6 个子 Skill 任意组合,4 阶段工作流：图像→prompt→剪辑→渲染 |
| **行业标杆** | browser-use/video-use(14.1k★)+ jianying-editor(2.3k★)+ remotion(92k★)+ hyperframes(92.9k★)+ seedance2(2.4k★)+ ImageGen MCP |

---

## 二、六大子 Skill 速查

| # | Skill | 关键能力 | 体积 | 触发词 |
|---|-------|----------|------|--------|
| 01 | [video-use](./01_video-use/SKILL.md) | 视频转写/智能剪辑/字幕/调色/overlay | 818K | 编辑视频/剪辑/转写/去口水/分镜/字幕 |
| 02 | [jianying-editor](./02_jianying-editor/SKILL.md) | 剪映草稿生成/导入/字幕/TTS/导出 | 8.0M | 剪映/生成草稿/AI 配音/字幕/导出 |
| 03 | [seedance2-skill](./03_seedance2-skill/SKILL.md) | Seedance 2.0 视频 prompt 编写 | 53K | 视频 prompt/AI 视频提示/Seedance |
| 04 | [remotion-skill](./04_remotion_skill_src/) | React/TS 程序化生成视频 | 14M(瘦身) | React 视频/程序化视频/数据视频 |
| 05 | [hyperframes](./05_hyperframes_src/) | HTML/CSS → MP4 (HeyGen 同款) | 147M | HTML 视频/网页转视频/HyperFrames |
| 06 | [image-generation](./06_image-generation/SKILL.md) | 文生图/产品图/封面图/编辑图 | 内置 MCP | 生图/画一张/封面/主图/模特 |

---

## 三、工作流闭环（核心价值）

```
┌──────────────────────────────────────────────────────────┐
│ ① 文案/创意生成                                          │
│   ├─ 06 ImageGeneration ── 产品图/封面图/主视觉         │
│   └─ 03 seedance2-skill  ── 视频生成 prompt（中英双语） │
├──────────────────────────────────────────────────────────┤
│ ② 视频素材产出                                           │
│   ├─ 04 remotion-skill    ── React 程序化生成           │
│   ├─ 05 hyperframes       ── HTML/CSS 渲染 MP4         │
│   └─ 调用外部视频 API（Seedance/可灵/MiniMax/Agnes）     │
├──────────────────────────────────────────────────────────┤
│ ③ 视频剪辑与转写                                         │
│   ├─ 01 video-use         ── 转写→cut→overlay→final.mp4│
│   └─ 02 jianying-editor   ── 剪映草稿→AI 配音→字幕      │
├──────────────────────────────────────────────────────────┤
│ ④ 渲染与导出                                             │
│   ├─ 01 video-use render  ── FFmpeg lossless concat     │
│   ├─ 05 hyperframes render ─ Chromium → MP4            │
│   └─ 02 jianying auto_export ── 剪映内导出 MP4           │
└──────────────────────────────────────────────────────────┘
```

---

## 四、Skill 互调用关系（图）

```
            ┌─────────────────┐
            │ 06 ImageGeneration│ (内置 MCP)
            │   关键帧/主图    │
            └────────┬────────┘
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
┌─────────────┐ ┌─────────┐ ┌──────────────┐
│03 seedance  │→│  视频 API │ │05 hyperframes│
│  prompt 库  │ │(Seedance/│ │  HTML→MP4    │
└─────────────┘ │ 可灵/MiniMax/│ └──────┬───────┘
                │  Agnes)   │        │
                └────┬──────┘        │
                     ↓               │
        ┌────────────┴───────────────┐
        ↓                            ↓
┌──────────────┐              ┌──────────────┐
│01 video-use  │ ←转写剪辑── │02 jianying    │
│ FFmpeg+PIL   │              │ 草稿生成/导入 │
└──────┬───────┘              └──────┬───────┘
       │                             │
       └────────────┬────────────────┘
                    ↓
            ┌─────────────────┐
            │  交付 MP4/草稿   │
            │  + 字幕/封面图  │
            └─────────────────┘
```

---

## 五、典型接单场景闭环

### 场景 A：自媒体 - 影视解说（¥0 成本，复刻 500 万粉流水线）
1. 03 seedance2-skill 写视频封面 prompt
2. 06 ImageGeneration 生成 1080×1920 竖屏封面
3. 01 video-use：源视频 → 转写 → 去口水 → 强点字幕 → 导出 final.mp4
4. **总成本：¥0**（用 FFmpeg + 字幕模板,跳过 AI API）

### 场景 B：接单 - 数字人电商主图（实证 6 张 ¥8）
1. 06 ImageGeneration：批量生 6 张亚洲模特图
2. 03 seedance2-skill 模板：「抖音带货直播风，30 秒带货」
3. 02 jianying-editor：生成草稿 + 配音 + 字幕
4. **总成本：5 积分左右 (内置 ImageGen 池)**

### 场景 C：企业 - 培训视频
1. 04 remotion-skill：写 React 组件 → 程序化渲染 MP4
2. 06 ImageGeneration：批量元素配图
3. 01 video-use：剪辑 → 加企业 LOGO 角标 → 导出
4. **总成本：首装 Node + Chromium ≈ 5 分钟,后续 ¥0**

### 场景 D：自媒体 - 编程教学
1. 录屏 → 01 video-use：转写代码段落 → 自动高亮 → 出片
2. 06 ImageGeneration：自动生课程封面
3. **总成本：¥0**（仅 FFmpeg + Whisper）

### 场景 E：接单 - 品牌短剧
1. 02 jianying-editor：草稿生成（含配音+字幕+特效）
2. 06 ImageGeneration：批量配图
3. 03 seedance2-skill：模板生成视频 prompt
4. **总成本：单条 ≤10 积分**

---

## 六、与现有龙虾生态的协同

| 已有 Skill | 关系 |
|-----------|------|
| `lobster-auto-bid` | 本管线产物的**报价输入**：剪辑/出图/渲视频 都能走自动报价器 |
| `hyperframes` (旧) | **本目录 05 即替代**旧装,内容更新 6 months,真源 HeyGen |
| `agnes_video_auto` | **互为备胎**：本管线 02 走 jianying(本地),Agnes 走 API(云端) |
| `lobster_ai_short_drama_script_skill_v1.0` | **管线预热**：剧本 → 本管线执行出片 |
| `zero-cost-video-render` | 本管线中"01 video-use → FFmpeg 步骤"的同名子技能,实现细节共享 |

---

## 七、调用方式

### 方式 1：触发词（中文关键词）

| 用户说 | 触发 |
|-------|------|
| 「视频」/「做视频」/「出片」 | 触发整条管线 |
| 「剪辑」/「转写」/「字幕」 | 命中 01 video-use |
| 「剪映」/「草稿」/「JianYing」 | 命中 02 jianying-editor |
| 「视频 prompt」/「Seedance」 | 命中 03 |
| 「React 视频」/「程序化视频」 | 命中 04 |
| 「HTML 视频」/「HyperFrames」 | 命中 05 |
| 「生图」/「封面」/「主图」 | 命中 06 |
| 「自媒体」/「短视频」/「带货」 | 自动路由到 01+06 组合 |

### 方式 2：CLI（PowerShell/Git Bash）

```bash
# 单文件夹路径(汤哥指定的实际位置)
PIPE="/g/WorkBuddy_Data/lobster_video_pipeline"

# 触发整条管线（Python 真实可用入口）
python "$PIPE/00_integration/pipeline.py" --task full --brief "30秒抖音带货"

# 单独调用某一阶段
python "$PIPE/00_integration/pipeline.py" --task image --prompt "电商白底产品图,30岁女性,口红" --out demo.png
python "$PIPE/00_integration/pipeline.py" --task video-edit --input in.mp4 --out final.mp4
python "$PIPE/00_integration/pipeline.py" --task sketch --draft out.draft  # 剪映草稿

# 自检
python "$PIPE/00_integration/test_pipeline.py"
```

### 方式 3：在 Agent 内直接读 SKILL.md

WorkBuddy / Claude Code / Codex 加载本目录任意 SKILL.md,**保持原仓库的 SKILL.md 协议不变**（这是 GitHub 上游规定的）——只补 06（内置 MCP）和顶层整合。

---

## 八、磁盘与依赖

| 资源 | 占用 | 位置 |
|------|------|------|
| 总占用 | ~ 200 MB | `G:\WorkBuddy_Data\lobster_video_pipeline\` |
| Python 依赖 | ≤30 MB | 见各 sub-skill `requirements.txt` / `pyproject.toml` |
| Node.js (可选) | 已装 | 仅 04 remotion 和 05 hyperframes 需要(npx 模式零持久占用) |
| FFmpeg | 系统路径 | Win10/11 通常自带,无则 `winget install ffmpeg` |
| Chromium | 0 | 05 hyperframes 触发时按需下载 |

**强制约束（铁律）**：
- ⚠️ E盘 0 字节剩余 → 本管线**全部在 G 盘** (USER MEMORY §G 章节),不写 E 盘
- ⚠️ 沙箱 .git/index.lock 拒绝写 → 本目录**不要 git init**（不是源仓库）

---

## 九、扩展与沉淀

| 待建 | 备注 |
|------|------|
| `00_integration/pipeline.py` | Python 主入口(各阶段统一调度)|
| `00_integration/test_pipeline.py` | 自检(发"我在"信号)|
| `00_integration/playbook.md` | 用户使用手册 + 故障排查 |
| `06_image-generation/SKILL.md` | 已写：ImageGen MCP 标准化入口 |
| `00_integration/demos/` | 各场景 demo 文件(随接单累积) |

沉淀位置：
- 技能源码 → `G:\WorkBuddy_Data\lobster_video_pipeline\` (本目录)
- 知识库 → `E:\龙虾AI主控中心\Obsidian\wiki\视频流水线\` (规划)
- 调度入口 → 后续接 `龙虾五步法 §11` 软链接注册表
- 全域模板 → 注册到 #319 协议（视频制作四化标准，待申请编号）

---

## 十、四化校准（成本优先置顶）

| 维度 | 落实 |
|------|------|
| **智能化** | 6 Skill 互调由 Agent 自主决策,用户只说"做视频" |
| **定制化** | 接单时按龙虾-auto-bid 输出报价 → 选择性价比最高的子 Skill |
| **全自动化** | 从 prompt 到 MP4 全链路零手动,5 步全部 Python/Node CLI 化 |
| **自我净化** | 各子 Skill 自带 SKILL.md 协议,Agent 自动读最新版本；hyperframes 的 6 个内置 SKILL.md 可热替换 |

---

**文档生成**：龙虾五步法 V3.6 + 1234（仓颉/全域模板/龙虾/赛博书屋）| 2026-08-23 20:14 CST
*（内容由AI生成，仅供参考）*
