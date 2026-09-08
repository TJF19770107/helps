---
name: ai-video-production-pipeline
description: 完整AI视频生产流水线（6技能融合）：口播线(Video-Use+剪映自动化)+动画漫剧线(HyperFrames+Seedance2+Remotion)+封面(ImageGen)双模编排，一站式出片。触发词：视频流水线、AI视频生产、口播剪辑、动画漫剧、批量视频、视频技能融合。
version: 1.0
agent_created: true
updated: 2026-08-26
cost_mode: strict
---

# 完整AI视频生产流水线（6 技能融合）

> 把 6 个 GitHub 视频 Skill 融合为一条可路由的双模流水线。
> 定位分析结论：**口播线和动画漫剧线都覆盖**，按需求路由。

## 一、6 技能拆解（素材分析）

| 技能 | 仓库 | 能力 | 定位 |
|------|------|------|------|
| Video-Use | `browser-use/video-use` | 口播素材自动剪辑 | 🎙️ 口播线核心 |
| HyperFrames | `heygen-com/hyperframes` | 图文转动画视频 | 🎨 动画线核心 |
| Remotion | `remotion-dev/remotion` | 模板化批量生成 | 📊 批量线（榜单/盘点/混剪） |
| Jianying-Editor | `luoluo22/jianying-editor-skill` | 剪映流程自动化 | ✂️ 后期统一出口 |
| Seedance2 | `dexhunter/seedance2-skill` | AI视频提示词生成 | 💡 创意入口（短剧/广告/分镜） |
| ImageGen | Image-Generation-Skill | 封面配图生成 | 🖼️ 全链路共用 |

## 二、双模路由（回答"口播还是动画漫剧"）

```
用户需求
 ├─ 真人出镜/口播/采访/教程 → 🎙️ 口播线
 │    Video-Use(剪辑口播) → Jianying(后期) → ImageGen(封面)
 ├─ 动画/漫剧/短剧/广告 → 🎨 动画漫剧线
 │    Seedance2(分镜提示词) → HyperFrames(图文转动画) / Remotion(批量模板)
 │    → Jianying(后期) → ImageGen(封面)
 └─ 数据盘点/榜单/混剪 → 📊 批量线
      Remotion(模板批量) → Jianying(切片) → ImageGen(封面)
```

**定位结论**：不是单一用途——**口播剪辑和动画漫剧两条线都被覆盖**，靠 Seedance2 提示词入口 + HyperFrames/Remotion 生成 + 剪映后期统一收口。

## 三、流水线五步

```
Step1 需求路由：判定口播/动画/批量 → 选线
Step2 创意脚本：Seedance2 生成分镜/脚本提示词（短剧/广告/科普）
Step3 素材生成：HyperFrames(图文转动画) / Remotion(模板批量) / Video-Use(口播素材)
Step4 后期合成：Jianying-Editor 剪映自动化（混剪/切片/字幕/配乐）
Step5 封面交付：ImageGen 封面配图 + 成片输出
```

## 四、调用方式

- 每步可独立调用（按需取用），也可整链跑（Step1-5）
- 依赖安装：各技能按仓库 README 安装（Remotion 需 Node；Jianying 需剪映桌面版；Video-Use 需浏览器自动化）
- 零积分优先：本地模型/免费 API 兜底，云端能力（OOMOL oo-cli）可选增强

## 五、与 OOMOL 协同

- gpt-image-2（电商生图）同属 OOMOL 托管能力，经 oo-cli 调用
- 本流水线的 ImageGen 步骤可升级为 gpt-image-2（电商级配图）或保留本地 ImageGen（零成本）

## 六、验收标准

1. 口播需求 → 出片（口播剪辑+字幕+封面）✅
2. 漫剧需求 → 出片（分镜→动画→后期→封面）✅
3. 批量需求 → 出片（模板批量+切片）✅
4. 每步产物可复用（脚本/模板/封面入四库）

---

*v1.0 | 2026-08-26 | 融入龙虾五步法 §18 + 全域模板 #323*
