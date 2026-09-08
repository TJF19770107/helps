---
title: Codex 看图能力 · 视觉适配器 Skill
summary: 让纯文本 Agent 也能「看图」：图片→结构化文本→理解，自动后端 gemini/ollama/tesseract
tags: [看图, 视觉, OCR, ModLens, gemini, tesseract, vision]
version: v1.0
distilled_at: 2026-08-25
---

# Codex 看图能力 · 视觉适配器 Skill v1.0

> 定位：模型本体（Codex / DeepSeek-V4-Flash）是纯文本基座，不能读像素。
> 本技能用视觉适配器把图片转成结构化文本，再基于文本理解，等效给 Agent「装上眼睛」。
> 后端自动探测：gemini（有 Key）→ ollama（本地视觉）→ tesseract（本地 OCR）。

## 一、何时用

- 用户发来报错截图 / 业务截图 / 账单截图 / 订单截图 / 设计稿
- 需要 OCR 提取图片里的文字
- 需要「看懂」图表、画面、设计元素（需 gemini 后端）

## 二、怎么用

```bash
# 看当前用哪个后端
python see_image.py --status

# 看图 / 提取文字
python see_image.py "图片路径.png" --prompt "识别这张截图里的文字和订单信息"
```

## 三、后端自动探测顺序

1. gemini：设了 GEMINI_API_KEY / GOOGLE_API_KEY 时启用，语义理解最强
2. ollama：本地 qwen2.5vl:7b / minicpm-v（需 Ollama 的 llama-server 正常）
3. tesseract：本地 OCR（chi_sim+eng），零密钥，提取文字

## 四、诚实边界

- tesseract：能「识字」（提取文字），零成本、已可用
- gemini：既识字又能「看懂」画面，需用户提供免费 Key
- 配好 Key 后无需改代码，ModLens 自动切到 gemini

## 五、触发词

看图 / 识别图片 / 读截图 / OCR / 报错截图 / 图片转文字 / 能不能看图 / 帮我看看这张图
