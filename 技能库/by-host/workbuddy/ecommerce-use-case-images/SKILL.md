---
name: ecommerce-use-case-images
description: 'Generate ecommerce use-case images from product photos and confirmed usage scenarios. Use when the user asks to create product usage, lifestyle application, target audience, gift, travel, commuting, home, outdoor, storage, or scenario-based ecommerce images with GPT Image 2.'
compatibility: "Requires the oo CLI."
metadata:
  icon: "\U0001F3AF"
  title: Ecommerce Use Case Images
  companionSkill: gpt-image-2
  packageName: '@zjxuyunshi/ecommerce-use-case-images'
  version: 0.0.1
---

# Ecommerce Use Case Images

## When to Use

Use this skill when the user wants ecommerce images that explain where, when, why, or for whom a product is used. Typical outputs include commuting, travel, office, home storage, gift giving, parent-child use, outdoor use, beauty routine, pet use, cleaning workflow, kitchen use, or holiday scenario graphics.

Use this when the image should communicate a use case, not merely a pretty scene. Use `ecommerce-scene-images` for broad lifestyle scenes and `ecommerce-selling-point-images` for abstract benefit callouts.

## Inputs

- Required: one or more product images. Preserve product identity and visible details.
- Optional but recommended: target use case, target audience, occasion, setting, or workflow. If absent, infer only a low-risk visible category use case.
- Optional: reference images for scenario mood, user environment, layout, or props.
- Optional: target language and text policy. Use concise labels only when requested or useful for domestic ecommerce.
- Optional: platform, size, format, quality, and count.

Do not imply medical, safety, slimming, waterproof, load-bearing, child-safety, food-contact, electrical, or regulated claims unless supplied.

## Execution

Use `$gpt-image-2` image editing mode via `fusion-api.openai_image_edit_async_submit`. Upload local images with `oo file upload`; pass the product first, then references.

Prompt structure:

```text
Create a marketplace-ready ecommerce use-case image.
Primary product: preserve image 1 accurately, including product shape, color, logos, packaging, and distinctive details.
Use case: <confirmed or conservative scenario>.
Target audience/occasion: <if supplied>.
Reference usage: use images 2+ only for scenario mood, environment, props, and layout inspiration.
Composition: show the product clearly in the use context, product remains prominent, realistic scale and interaction, clean ecommerce visual hierarchy.
Text policy: <none or concise factual Chinese/English labels>.
Avoid: unsupported claims, fake effects, fake before/after, extra included items, competitor marks, QR codes, phone numbers, watermarks, platform badges, distorted product.
```

Run:

```bash
oo connector run "fusion-api" --action "openai_image_edit_async_submit" --data @payload.json --json
```

Use exact `$gpt-image-2` payload fields.

## Result Handling

Read URLs from `.data.data[].url`. Download to `/Users/yunshi/Downloads/ecommerce-use-case-images/<short-product-name>-<timestamp>/` with names like `use-case-image-01.png`. Preview when practical and mention the use case used.

## Failure Handling

- Missing product image: ask for one.
- Missing use case: infer a conservative category-safe scenario or ask if multiple outcomes are plausible.
- Regulated or proof-dependent scenario: ask for confirmation or omit the claim.
- Too many references: select the most relevant scenario references.
- Connector handle, timeout, auth, billing, upload, or schema failure: follow `$gpt-image-2` guidance and report the exact blocker.
