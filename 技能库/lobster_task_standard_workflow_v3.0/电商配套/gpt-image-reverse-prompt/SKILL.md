---
name: gpt-image-reverse-prompt
description: 'Reverse engineer a reference image into GPT Image-ready prompts, from quick Style DNA plus dense prompt output to advanced Chinese, English, and JSON prompt schemas. Use when the user asks to turn an image into a prompt, reverse a visual reference, extract a GPT Image 2 prompt, or adapt an image style for generation, editing, article illustrations, covers, or creative variations.'
compatibility: "Requires the oo CLI."
metadata:
  icon: "\U0001F5BC️"
  title: GPT Image Reverse Prompt
  packageName: '@zjxuyunshi/gpt-image-reverse-prompt'
  version: 0.0.1
---

# GPT Image Reverse Prompt

## Overview

Use this skill to turn one or more reference images into prompts that work well with GPT Image-style image generation and editing models. The goal is not to recover the exact original prompt. The goal is to translate the visible image into an executable visual brief: what to create, what to preserve, what to change, and what constraints matter.

The workflow is intentionally multi-stage internally but concise externally. First stabilize visual understanding in a seed object, then rewrite the prompt for GPT Image, then merge the result into a fixed schema. Do not expose intermediate reasoning unless the user explicitly asks for the process.

For the design rationale behind this schema and the reusable lessons extracted from comparing image-to-prompt skills, see `references/design-notes.md`.

## When to Use

Use this skill when the user asks to:

- reverse engineer an image prompt;
- convert an image into a generation prompt;
- analyze a reference image for GPT Image, GPT Image 2, gpt-image, GPT-4o Image, or similar multimodal image generation;
- produce Chinese and English prompts from an uploaded image;
- output structured JSON prompt data from an image;
- recreate the style, layout, composition, or visual brief of a reference image;
- write an image-edit prompt that preserves some elements of the uploaded image.

Do not use this skill when the user only wants a caption, OCR, object detection, aesthetic critique, or a general explanation of the image. Use it only when the requested output is a reusable image-generation or image-editing prompt.

## Language Policy

Follow the user's current message language for conversational output and the default quick reverse prompt. Do not rely on stored language preferences when they conflict with the user's actual message.

- If the user writes in Chinese, the quick reverse prompt should be Chinese.
- If the user writes in English, the quick reverse prompt should be English.
- If the user writes in another language, follow that language when practical.
- If the user mixes languages, use the majority language.

Advanced mode may still include both `zhPrompt` and `enPrompt` because that schema is meant for cross-tool reuse. If the user explicitly says "all Chinese", "all English", or asks for only one language, respect that request and omit the other language from the displayed result.

## Input Handling

Only run the reverse-prompt workflow when the user is actually asking to reverse, generate, edit, adapt, or extend image prompts. If the user is reviewing a prompt, comparing instructions, or asking how this skill behaves, answer that meta request instead of demanding an image.

When the user asks for image reverse engineering:

- No image: ask for one image in the user's language. Keep it short.
- One image: continue with the workflow.
- Multiple images: ask whether to reverse one image, compare them, or combine them into one style/brief, unless the user's intent is already clear.
- Image plus article/text: do not assume cover art. Route through the article mode below.

## Article, Cover, and Illustration Routing

If the user provides an article or substantial text together with an image style reference, distinguish the target before generating prompts:

- If they say "illustration", "article image", "in-article image", or equivalent, use article-illustration mode. Extract 3-5 visually strong concepts/scenes from the article, list candidates, and ask the user to choose unless they already specified one.
- If they say "cover" or "封面", use cover mode. Extract the core theme and mood, then propose 2-3 cover directions in the reference style.
- If wording is ambiguous, ask whether they want one cover or several article illustrations.

Do not default article requests to covers. This is a common failure mode.

## Output Contract

There are two display modes. Choose the lightest output that satisfies the user.

### Quick Output Mode

Use quick mode by default when the user asks casually to reverse an image, asks for "just the prompt", asks for a concise result, or does not request JSON/structured output.

Default quick response format:

```markdown
🧬 Style DNA
<A × B × C>

🔍 Reverse Prompt
<one dense prompt in the user's current language>

Next step: <1-3 short conversational suggestions>
```

Quick prompt rules:

- Target length: 40-120 words for English, or the comparable compact length in the user's language. For complex images, allow up to about 180 words only when needed to preserve essential visual information.
- Every phrase must carry non-redundant visual information. Delete empty praise such as "beautiful", "stunning", "high quality", "ultra detailed", and generic "best quality" unless the user explicitly wants that style.
- Use the order: subject and action, scene/background, composition/viewpoint, rendering/style, color/light, mood.
- The prompt language follows the user's current message language.
- The prompt should be a high-density reconstruction, not a caption and not a reusable vague style template.

### Advanced Structured Mode

Use advanced mode when the user asks for GPT Image 2, GPT Image Tool, JSON, structured output, English prompt, Chinese + English prompts, editing constraints, product preservation, layout reference, or automation-ready fields.

Return these fields in this order:

1. `title`
2. `mode`
3. `aspectRatio`
4. `targetUse`
5. `keywords`
6. `zhPrompt`
7. `enPrompt`
8. `jsonPrompt`
9. `notes`

Advanced response format:

````markdown
**Title**
<title>

**Mode**
<generate | edit | style_reference | layout_reference | product_recreation | article_illustration | cover>

**Aspect Ratio**
<aspectRatio>

**Target Use**
<targetUse>

**Keywords**
<keyword 1> | <keyword 2> | <keyword 3>

**Chinese Prompt**
<zhPrompt>

**English GPT Image Prompt**
<enPrompt>

**Structured Prompt**
```json
{ ... }
```

**Notes**
<notes>
````

If the user asks for raw block format, use:

```text
[TITLE]...[/TITLE]
[MODE]...[/MODE]
[ASPECT_RATIO]...[/ASPECT_RATIO]
[TARGET_USE]...[/TARGET_USE]
[KEYWORDS]...[/KEYWORDS]
[ZH_PROMPT]...[/ZH_PROMPT]
[EN_PROMPT]...[/EN_PROMPT]
[JSON_PROMPT]{...}[/JSON_PROMPT]
[NOTES]...[/NOTES]
```

If the user asks for only one field, internally follow the full workflow but display only the requested field.

## Mode Selection

Choose one mode before writing the final prompt:

- `generate`: create a new image from scratch using the reference as visual guidance.
- `edit`: use the uploaded image as the source image and preserve specified elements while changing others.
- `style_reference`: recreate the visual style, lighting, palette, or medium, without preserving exact subject identity.
- `layout_reference`: reproduce layout, composition, hierarchy, or information architecture, especially for posters, ads, UI mockups, thumbnails, and infographics.
- `product_recreation`: create or improve a product/ecommerce image while preserving product identity, shape, material, label, and key selling context.
- `article_illustration`: apply the reference style to one or more concepts/scenes from an article.
- `cover`: apply the reference style to a single cover image for an article, video, post, or presentation.

When the user does not specify a mode, infer the safest default:

- If the user says “use this image”, “keep”, “change”, “replace”, “edit”, or the image contains a real person/product that likely must remain identifiable, choose `edit` or `product_recreation`.
- If the user says “make something like this”, “reverse this style”, “learn this composition”, or “reference”, choose `style_reference` or `layout_reference`.
- If article text is present, distinguish `article_illustration` from `cover` before writing prompts.
- Otherwise choose `generate`.

## Internal Workflow

### 1. Build the Seed

Inspect the image and build a private seed object with:

- `title`
- `mode`
- `aspectRatio`
- `targetUse`
- `keywords`
- `zhPrompt`
- `notes`

Seed rules:

- `keywords` should be 5-10 short terms, not long sentences.
- `zhPrompt` must be a complete Chinese image-generation prompt, not a tag list.
- Cover subject, scene, composition, lighting, colors, atmosphere, style, camera, material, and output purpose when visible or inferable.
- If information is uncertain, mark uncertainty in `notes`; do not invent precise details.
- If the image contains text, separate readable text from unreadable text in the seed.

Use common generation ratios when exact dimensions are unknown:

- `1:1`
- `4:5`
- `3:4`
- `2:3`
- `3:2`
- `16:9`
- `9:16`
- `21:9`

If the ratio is estimated, say so in `notes`.

### 2. Build the Quick Reverse Prompt

For quick mode, write one dense reverse prompt in the user's current message language. It should aim to reproduce the main subject, composition, style, colors, light, and mood as closely as possible, while staying concise. Do not promise exact recovery of the original prompt or seed.

Use professional image-generation vocabulary, but avoid empty quality modifiers. If a word can be removed without changing the visual reconstruction, remove it.

### 3. Build the GPT Image Prompt

Write `enPrompt` as a natural English visual brief for GPT Image-style models.

Rules for `enPrompt`:

- Do not mechanically translate `zhPrompt`.
- Do not use Stable Diffusion tag soup such as `masterpiece, best quality, 8k, ultra detailed, trending on artstation` unless the user explicitly asks for that style.
- Prefer clear prose with concrete visual instructions.
- Include output purpose, composition, lighting, material, style, subject relationship, and constraints.
- For image editing, explicitly say what to preserve and what to change.
- For layout references, explicitly describe hierarchy, negative space, typography zones, and visual balance.
- For product images, explicitly preserve product identity, shape, material, label, logo placement, and scale if visible.
- If the image has readable text that must be reproduced, quote it exactly and specify its location and typography style.
- If text is unreadable, describe it as unreadable small text or placeholder text; do not hallucinate its content.

Good GPT Image-style prompt shape:

```text
Create a vertical editorial poster featuring ... Use ... lighting and ... composition. Place ... in the upper third, leave clean negative space around ..., and keep the palette ... Preserve ... Avoid adding extra text, logos, distorted hands, or cluttered background.
```

For edit mode, use this shape:

```text
Use the uploaded image as the source reference. Preserve ... Change ... Keep ... Avoid ...
```

### 4. Build the Structured JSON

Return `jsonPrompt` as a JSON object. Include these fields:

```json
{
  "mode": "generate | edit | style_reference | layout_reference | product_recreation | article_illustration | cover",
  "target_use": "...",
  "aspect_ratio": "...",
  "subject": "...",
  "scene": "...",
  "style": "...",
  "composition": "...",
  "lighting": "...",
  "colors": ["..."],
  "camera": "...",
  "mood": "...",
  "materials": ["..."],
  "text_elements": [
    {
      "content": "...",
      "position": "...",
      "style": "...",
      "confidence": "high | medium | low"
    }
  ],
  "preserve_elements": ["..."],
  "change_elements": ["..."],
  "avoid": ["..."],
  "keywords": ["..."]
}
```

Field guidance:

- `text_elements`: use an empty array when there is no visible text. If text is partly unreadable, set `confidence` to `low` and do not guess missing words.
- `preserve_elements`: especially important in `edit` and `product_recreation` modes.
- `change_elements`: use an empty array for pure generation unless the user gives edit instructions.
- `avoid`: write natural GPT Image constraints, not Stable Diffusion negative prompt tags.
- `colors` and `materials` should be arrays for easier reuse.

### 5. Merge by Field

The final answer is not seed text plus secondary text. Merge by field:

- Seed provides: `title`, `mode`, `aspectRatio`, `targetUse`, `keywords`, `zhPrompt`, `notes`.
- GPT Image rewrite provides: `enPrompt`.
- Structured pass provides: `jsonPrompt`.

If `enPrompt` conflicts with the image, the user instruction, or the seed, revise it conservatively. Do not include analysis prose, numbered steps, or `Prompt:` labels inside `enPrompt`.

## Multi-Image Handling

If the user sends multiple images:

- If they ask to compare or combine them, produce one combined prompt and explain what each image contributes.
- If they do not ask to combine, analyze each image separately using the full output contract.
- If one image is a source and another is a style/layout reference, set `mode` to `edit`, `style_reference`, or `layout_reference` and clearly separate `preserve_elements` from style/layout guidance.

## Text and Typography Rules

For posters, UI, thumbnails, ads, ecommerce images, packaging, and infographics, typography is part of the prompt:

- Capture visible text exactly only when readable.
- Describe position, hierarchy, font personality, alignment, scale, and spacing.
- If text must be editable or replaced, put the desired copy in `text_elements` and mention it in `enPrompt`.
- Do not invent brand names, product claims, prices, legal labels, dates, or small-print text.
- If the image has a logo but the user did not provide rights or source files, describe it generically unless the brand is clearly visible and user intent requires it.

## Generation Follow-Through

If the user asks to generate an image after receiving the reverse prompt:

- Use the generated reverse prompt directly, adapted only for the selected image tool's syntax and supported aspect ratios.
- Do not add unrelated text, logos, watermarks, signatures, UI marks, or brand labels.
- If the reference image or user request intentionally contains text, preserve or replace that text exactly as requested instead of applying a blanket no-text rule.
- Prefer the original/reference aspect ratio. Only default to common landscape ratios such as `16:9`, `3:2`, or `2:1` when the user has not specified a ratio and the reference ratio is unavailable or unsuitable.
- After generation, give only a brief next-step suggestion: regenerate closer, change one element, or extend into a series.

## Safety and Uncertainty Rules

- Never claim to recover the original prompt exactly. Say it is an estimated reconstruction or usable visual brief when relevant.
- Do not identify private persons or infer sensitive attributes from faces.
- Do not hallucinate small text, labels, logos, medical/legal claims, or exact product specs.
- Do not include copyrighted character names unless the user explicitly asks and the image clearly depicts that character; prefer generic visual descriptions when possible.
- If the image is too blurry, cropped, low-resolution, or visually ambiguous, still provide a best-effort prompt but mark limitations in `notes`.

## Common Pitfalls

1. **Outputting Stable Diffusion tag soup.** GPT Image-style prompts should be natural, direct visual briefs.
2. **Only captioning the image.** A caption says what is present; a reverse prompt says how to generate or edit it.
3. **Mechanical translation.** The English prompt should be rewritten for the image model, not translated line by line from Chinese.
4. **Losing edit intent.** If the user wants to preserve identity, product shape, or layout, state that explicitly.
5. **Guessing unreadable text.** Preserve only readable text; describe unreadable text as such.
6. **Forgetting output purpose.** Posters, thumbnails, ads, ecommerce images, icons, and portraits need different prompt wording.
7. **Exposing internal stages unnecessarily.** Do the staged reasoning internally; show only the final deliverable unless asked.
8. **Using advanced JSON output for every casual request.** Default to quick Style DNA plus Reverse Prompt unless the user asks for structured fields.
9. **Defaulting article requests to covers.** Ask or route based on the user's wording. Article illustrations and covers are different deliverables.

## Verification Checklist

Before responding, check:

- [ ] The selected `mode` matches the user’s intent.
- [ ] `aspectRatio` is either visible or marked as estimated in `notes`.
- [ ] The display mode is appropriate: quick for casual use, advanced for structured/GPT Image/JSON/editing requests.
- [ ] In quick mode, the reverse prompt follows the user's current message language and stays dense, specific, and concise.
- [ ] In advanced mode, `zhPrompt` is a complete Chinese prompt, not keywords.
- [ ] In advanced mode, `enPrompt` is natural GPT Image-ready prose, not SD tags or a mechanical translation.
- [ ] In advanced mode, `jsonPrompt` is valid JSON and contains all required fields.
- [ ] Readable text is quoted exactly; unreadable text is not invented.
- [ ] Preserve/change/avoid constraints are explicit when editing, recreating products, adapting layouts, or generating article/cover variants.
- [ ] The final answer contains only the requested fields if the user asked for a partial output.
