# Workflow Notes for GPT Image Reverse Prompt

This reference is for agents that need a compact recipe while using the `gpt-image-reverse-prompt` skill.

## Core Principle

Do not try to recover the exact original prompt. Convert the reference image into an executable visual brief for GPT Image-style generation or editing.

## Compact Recipe

1. Choose mode: `generate`, `edit`, `style_reference`, `layout_reference`, or `product_recreation`.
2. Build a Chinese seed: title, aspect ratio, target use, keywords, Chinese prompt, notes.
3. Rewrite an English prompt as natural GPT Image-ready prose.
4. Build structured JSON with subject, scene, style, composition, lighting, colors, camera, mood, materials, text elements, preserve/change/avoid arrays, and keywords.
5. Merge by field. Do not show intermediate seed unless requested.

## GPT Image Prompt Patterns

### Generate

```text
Create a <ratio/use> image featuring <subject> in <scene>. Use <composition>, <lighting>, <palette>, and <style>. Emphasize <materials/mood>. Avoid <constraints>.
```

### Edit

```text
Use the uploaded image as the source reference. Preserve <identity/product/layout>. Change <requested changes>. Keep <style/lighting/composition constraints>. Avoid <unwanted artifacts>.
```

### Layout Reference

```text
Create a new image using the reference layout: <hierarchy>, <negative space>, <text zones>, <subject placement>. Replace the content with <new content> while keeping the same visual balance.
```

### Product Recreation

```text
Use the uploaded product image as the main reference. Preserve the product identity, silhouette, material, label placement, proportions, and key details. Place it in <scene> with <lighting> and <background>. Avoid changing the logo, label text, or product shape unless requested.
```

## Text Confidence

- High: fully readable text; quote exactly.
- Medium: mostly readable; quote only visible parts and explain uncertainty.
- Low: text block visible but unreadable; describe position and style only.
