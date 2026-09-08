---
name: ecommerce-image-system
description: 电商生图系统（4技能聚合）：gpt-image-2(主生图)+ecommerce-image-studio(详情页/卖点图)+ecommerce-use-case-images(使用场景图)+gpt-image-reverse-prompt(参考图反推提示词)。触发词：电商图、商品图、详情页、卖点图、产品拆解、电商生图、淘宝图、产品图、listing图。
version: 1.0
agent_created: true
updated: 2026-08-26
cost_mode: strict
protocol: 全域模板#326
---

# 电商生图系统（4 技能聚合）

> 一个文件夹管电商图：说"生成电商图"，自动路由到本系统对应技能。
> 位置：`E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v3.0\我的AI分身\电商配套\`

## 一、4 技能分工

| 技能 | 本地路径(WorkBuddy) | 能力 | 场景 |
|------|---------------------|------|------|
| **gpt-image-2** | `~\.workbuddy\skills\gpt-image-2` | 文生图/改图（GPT Image 2） | 产品爆炸拆解图、主图、任意生图 |
| **ecommerce-image-studio** | `~\.workbuddy\skills\ecommerce-image-studio` | 商品图套装（listing/生活方式/广告首帧/卖点图/详情图/平台规格图） | Amazon/Shopify/TikTok/小红书/淘宝/虾皮/Temu/DTC |
| **ecommerce-use-case-images** | `~\.workbuddy\skills\ecommerce-use-case-images` | 使用场景图（送礼/通勤/居家/户外/存储等） | 场景化营销图 |
| **gpt-image-reverse-prompt** | `~\.workbuddy\skills\gpt-image-reverse-prompt` | 参考图反推 GPT Image 提示词 | 模仿竞品/复刻风格 |

## 二、路由规则（自动匹配）

```
"生成电商图" → 判需求：
  ├─ 产品拆解/爆炸图/标注卖点 → gpt-image-2
  ├─ 详情页/卖点图/平台规格图 → ecommerce-image-studio
  ├─ 使用场景/生活方式图 → ecommerce-use-case-images
  ├─ 给参考图要同款风格 → gpt-image-reverse-prompt → 再 gpt-image-2
  └─ 任意商品主图 → gpt-image-2
```

## 三、调用链（OOMOL oo-cli）

```
oo connector run fusion-api -a openai_image_async_submit -d '{"prompt":"...","model":"gpt-image-2","size":"1536x1152","output_format":"png","quality":"high"}' --wait-result
```
- 提交→轮询→返回图片 URL→下载到 `Obsidian\wiki\我的AI分身\产物\`
- 依赖：oo-cli（E:\oo\oo.exe）+ 已登录（OOMOLer_4lxY_team）

## 四、接单建议（企业微信接单群）

- 商品主图/详情页图/拆解图：单张可报价 ¥20-100，一套详情页 ¥100-300
- 参考图反推+改图：¥50-150/张
- 交付标准：1024×1024/1536×1152 PNG 高清，可加标注文案

## 五、验证记录（2026-08-26）

- ✅ gpt-image-2 实测出图成功（无线蓝牙耳机爆炸拆解图）
- ✅ 3 个配套技能安装成功（7 agents）
- ⏳ ecommerce-image-studio 等配套实测（下次接单前各测 1 张）

---

*v1.0 | 全域模板 #326 | 电商接单能力闭环*
