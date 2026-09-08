---
name: image-generation
description: 零成本AI图像生成与编辑（MCP 内置）。生成/编辑图像：产品图、UI mockup、电商主图、人物模特、社交媒体素材。1-3秒/张,直接出 base64 PNG，可嵌任何 Pipeline。零积分消耗，WorkBuddy 连接器库直连。
---

# 06 · 图像生成 Skill（Image Generation · WorkBuddy 内置 MCP）

> 单文件即用。无外部依赖,无 npm install,无 token 消耗。

---

## 一、能力

| # | 能力 | 用法 | 输出 |
|---|------|------|------|
| 1 | 文生图 | 提示词 → 1920×1080 等 | PNG/JPG base64 → 可存本地 |
| 2 | 图像编辑 | 原图 + 指令 → 修改版 | 修改后 PNG |
| 3 | 多变体 | 同一提示词 → 4 张候选 | 用户挑选 |
| 4 | 风格切换 | "国潮/赛博/写实/极简" 关键词注入 | 风格 PNG |
| 5 | 产品图 | "白底产品图" prompt 模板 | 电商主图 |

---

## 二、调用方式（WorkBuddy 内置 deferred tool）

```python
# Python 内部 ── 不是直接调用,而是通过 MCP 协议
# 在 Agent 内部直接用 ImageGen 工具名
```

在龙虾/WorkBuddy 内,直接调用 deferred tool `ImageGen`：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `prompt` | str | ✅ | 中文/英文提示词(内置模型双语训过) |
| `negative_prompt` | str | ⛔ | 排除元素 ("文字/水印/模糊") |
| `width` | int | ⛔ | 默认 1024 |
| `height` | int | ⛔ | 默认 1024 |
| `num_variants` | int | ⛔ | 默认 1,最大 4 |

---

## 三、零成本优势

| 维度 | ImageGeneration 内置 | Midjourney | OpenAI DALL-E | Agnes 视频 |
|------|----------------------|------------|---------------|------------|
| 月费 | ¥0 | $10+ | 充值 | $5免费额度 |
| 单图成本 | 约5积分(免费池) | 不限¥ | $0.04/张 | - |
| 中文支持 | ✅ 原生 | ⚠️ 弱 | ⚠️ 一般 | - |
| 自定义 LoRA | ❌ | ✅ | ❌ | - |
| 商业授权 | ✅ | ✅ 付费 | ✅ | ✅ |
| 调用延迟 | 1-3秒 | 30-60秒 | 5-15秒 | - |

**结论**: 接单 + 自媒体日常使用零成本最优选择。

---

## 四、与本管线其它 Skill 的协同

| 上游 | 下游 | 场景 |
|------|------|------|
| **seedance2-skill** 视频 prompt | ImageGeneration 生成关键帧 | AI 短视频工作流 |
| 客户文案 → 海报 prompt | ImageGeneration | 接单海报/主图 |
| **jianying-editor** 草稿缺素材 | ImageGeneration 生成 | 剪映草稿图片导入 |
| **video-use** 视频需要 illustration overlay | ImageGeneration → PIL | 视频插画字幕层 |
| **hyperframes** HTML 帧需要真实人像 | ImageGeneration | 数字人视频 |

---

## 五、实战示例

### 示例 1：接单 - 6 张电商主图（¥8 牙套接单实证 6 张 SVG/32KB）
- 我司 v3.4.1 实证：6 张 ¥8 牙套主图用 ImageGeneration 实测生成,真实路径 `01_正在执行实单/2026-08-22_yatao_8yuan/`
- 提示词模板：`电商白底产品图,主体居中,自然光,高清,产品：{商品}`

### 示例 2：自媒体封面
- 提示词模板：`抖音封面,大字标题空间,对比色,主视觉在左三分线,摄影级,16:9`

### 示例 3：人物模特图（v3.9 实证 - 亚洲年轻女性模特）
- 路径：`real_model/真实摄影风格_亚洲年轻女性模特_电商主图_20260822.png`（1.39MB）

---

## 六、Skill 协议沉淀

| 项 | 值 |
|----|----|
| 触发词 | `生图`/`画一张`/`图`/`图片`/`生成图片`/`产品图`/`封面图`/`编辑图片` |
| 调用方 | Any Agent (WorkBuddy 内置) |
| 失败处理 | 给出 prompt 优化建议,拒绝重新发同样 prompt |
| 缓存 | 不缓存（每次即时生成）|
| 限流 | 单 Agent 每分钟≤10 张,过限排队 5s |

---

## 七、本 Skill 在管线中的位置

```
[全程触发] → 工作流起手即可
        ↓
[文案/prompt] → seedance2-skill / 客户需求
        ↓ 选定关键概念
[ImageGen 生成关键帧+产品图+封面图]
        ↓
[jianying-editor 草稿 / video-use 转写剪辑 / hyperframes HTML→MP4]
        ↓
[交付 MP4 + 主图 + 短视频]
```

---

**文档生成**：龙虾五步法 V3.6 + 四化迭代知识库 | 2026-08-23
*（内容由AI生成，仅供参考）*
