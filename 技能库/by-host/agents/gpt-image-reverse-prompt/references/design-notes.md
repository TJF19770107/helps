# Design Notes: GPT Image Reverse Prompt

These notes capture the reusable design reasoning behind this skill. They are not required for normal execution; use them when improving the skill, explaining the workflow, or comparing it with other image-to-prompt tools.

## Source Pattern Worth Keeping

The `Pandas886/reverse-image-prompt-skill` repo is small but useful because it treats image-to-prompt as a staged agent workflow rather than a one-shot captioning task:

1. Build a seed: title, aspect ratio, keywords, Chinese prompt, notes.
2. Build secondary outputs: English prompt and structured JSON.
3. Merge by field instead of concatenating intermediate text.

This pattern stabilizes the visual understanding before writing the final prompt and reduces prompt drift.

## What Needed Upgrading for GPT Image

The source pattern was closer to general image generation and still carried some Stable Diffusion-era assumptions. For GPT Image-style models, prefer:

- natural-language visual briefs instead of tag soup;
- explicit generate/edit/style/layout/product modes;
- `preserve_elements`, `change_elements`, and `avoid` instead of only `negative_prompt`;
- first-class `text_elements` with readability confidence;
- target-use awareness: poster, thumbnail, ecommerce, UI mockup, portrait, infographic, etc.;
- a clear note that this reconstructs a usable visual brief, not the exact original prompt.

## Durable Strategy

For future improvements, keep the skill focused on this contract:

```text
reference image
→ stable visual seed
→ GPT Image-ready English brief
→ structured JSON schema
→ concise final delivery
```

Do not let it collapse into plain captioning, OCR, or Stable Diffusion keyword extraction.

## Good Test Cases

Use real images from these categories when validating updates:

- portrait/photo with lighting and pose details;
- poster or thumbnail with readable and unreadable text;
- ecommerce/product image where product identity must be preserved;
- layout-heavy infographic or UI mockup;
- multi-image request where one image is source and another is style/layout reference.

Check that the output:

- chooses the correct `mode`;
- marks estimated aspect ratios;
- does not invent unreadable text;
- uses natural English prompt prose;
- includes preserve/change/avoid constraints when relevant;
- returns valid JSON in `jsonPrompt`.
