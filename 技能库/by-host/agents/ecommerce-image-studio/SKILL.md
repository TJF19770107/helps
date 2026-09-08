---
name: ecommerce-image-studio
description: 'Generate market-ready ecommerce product image sets from product photos using oo-hosted AI image generation. Use when the user asks to create listing images, lifestyle scenes, ad first frames, selling-point graphics, detail images, or platform-specific visuals for Amazon, Shopify, TikTok Shop, Xiaohongshu, Taobao, Shopee, Temu, or DTC stores without writing prompts.'
compatibility: "Requires the oo CLI."
metadata:
  icon: "\U0001F6CD️"
  title: Ecommerce Image Studio
  companionSkill: gpt-image-2
  packageName: '@zjxuyunshi/ecommerce-image-studio'
  version: 0.0.4
---

# Ecommerce Image Studio

## When to Use

Use this skill when the user wants market-ready ecommerce visuals from product photos, especially when they do not want to write prompts or make detailed creative decisions.

Typical requests:

- Turn one product photo into a set of listing images, lifestyle images, ad first frames, selling-point graphics, or detail images.
- Create model, lookbook, wearing, carrying, or styled-on-person ecommerce images for apparel, accessories, bags, jewelry, beauty, and wearable products.
- Create ecommerce images for Amazon, Shopify, TikTok Shop, Xiaohongshu, Douyin, Taobao, Tmall, Shopee, Temu, Etsy, or DTC stores.
- Make a product image look more premium, more clickable, more platform-native, less AI-generated, or more suitable for a target market.
- Generate several creative directions for A/B testing from the same product photo.

This skill is the ecommerce strategy layer. Use `$gpt-image-2` for all actual image generation and editing execution.

## Inputs

- Required: at least one product image. Preserve the product's identity, shape, proportions, color, material, logo placement, packaging, labels, SKU details, and distinctive physical features.
- Optional: target platform. Default to general ecommerce if absent.
- Optional: target market or language. Default to the user's language and a broad international ecommerce style if absent.
- Optional: output goal. Default to a balanced 6-image set when the user asks for "a set" or gives no specific type.
- Optional: selling points. If absent, infer only visible, low-risk benefits and avoid proof-dependent claims.
- Optional: model preference for wearable products, such as gender presentation, age range, body type, ethnicity, pose, crop, market, styling mood, or "no model". If absent, choose a tasteful generic model direction suitable for the target market.
- Optional: reference images. Use them for composition, mood, lighting, scene, crop, or platform style only; do not copy unrelated products, brands, watermarks, or exact ad layouts.
- Optional: aspect ratio. Default to square `1024x1024`; use portrait `1024x1536` for social covers and vertical ads, and landscape `1536x1024` for website hero or banner-style images.
- Optional: count. Default to one image for a specific request or a 6-image set for a broad request.

Ask one concise follow-up only when there is no product image, when the output type is impossible to infer, when the user requests a specific real-person likeness or exact fit result without a model/reference image, or when a regulated/proof-dependent claim would materially change the image. Otherwise choose safe defaults and proceed.

## Execution

Use `$gpt-image-2` directly for the image operation. Do not run oo capability discovery during normal use. This skill should decide the ecommerce direction, build the creative brief and prompt, then hand execution to `$gpt-image-2` image editing mode.

### Submission Strategy

For a default full set of up to six ecommerce images, submit all independent
image jobs in one parallel batch by default. Keep one focused prompt, one
`$gpt-image-2` edit call, and one deterministic output name per asset; do not
collapse the set into one `n=6` request unless the user specifically wants
near-identical variations of the same concept.

For larger sets, text-heavy images, exacting model/try-on images, or unusually
high product-fidelity tasks, use a small concurrency limit of 3 to 4 jobs when
that is safer for reliability and review. If one asset fails with provider busy,
timeout, upload, or transient connector errors, retry only the failed asset once
after checking the result state. Do not resubmit successful assets.

### Default Set

When the user asks for a full set, generate these six assets unless they specify otherwise:

1. Clean listing image: product-dominant, platform-safe, minimal props.
2. Premium lifestyle scene: realistic use context with polished lighting.
3. Social ad first frame: thumb-stopping composition with clear text-safe space.
4. Selling-point graphic: one clear benefit or feature callout, mobile-readable.
5. Detail or texture image: material, structure, craftsmanship, packaging, or component close-up.
6. Market variant: a second creative direction for A/B testing, such as UGC-real-life, premium-studio, giftable-scene, or model-lookbook.

For apparel, accessories, jewelry, bags, beauty tools, or other wearable/use-on-body products, include at least one model, lookbook, wearing, carrying, or styled-on-person image in a full set unless the user asks for no model. If six outputs are requested, make the model image either asset 2 or asset 6 depending on which is more commercially useful.

### Platform Direction

- Amazon: clean, credible, product-first, no unsupported claims, no fake badges, no excessive text.
- Shopify or DTC: brand-forward, polished, editorial, strong product storytelling.
- TikTok Shop or Meta ads: authentic, fast-read, UGC or real-life energy, strong first-frame contrast.
- Xiaohongshu: lifestyle-led, tasteful, social-cover friendly, enough clean space for Chinese headline text when requested.
- Douyin, Taobao, Tmall, JD, Pinduoduo: higher conversion density is acceptable; keep text readable and claims factual.
- Shopee or Temu: high-contrast, simple benefit hierarchy, product very clear at small size.
- Etsy: handmade, giftable, warm, material-aware, avoid over-commercial styling unless requested.

### Creative Archetypes

Choose one or more archetypes instead of asking the user to invent a prompt:

- `clean-marketplace`: plain or lightly styled listing image.
- `premium-studio`: refined studio lighting, soft shadows, high-end product feel.
- `ugc-real-life`: believable phone-camera or casual user context.
- `social-first-frame`: high-click social ad image with clear focal point and text-safe area.
- `feature-callout`: product plus concise benefit callouts.
- `macro-texture`: close-up detail, material, structure, finish, or packaging quality.
- `giftable-scene`: seasonal, gifting, unboxing, or bundle presentation.
- `problem-solution`: visualizes the use case or pain point without fake before/after claims.
- `model-lookbook`: product styled on a tasteful AI model or partial-body crop, optimized for apparel, accessories, jewelry, bags, and wearable products.

### Model Imagery Policy

Model imagery is useful for wearable ecommerce products because it communicates scale, styling, drape, occasion, and aspiration. Do not omit it from apparel sets by default.

Use `$gpt-image-2` image editing mode with the product image first. If the user provides model, pose, or lifestyle references, pass those after the product image and use them only for pose, crop, lighting, body framing, and mood. Do not copy a real person's identity unless the user owns or supplied that identity reference and explicitly asks for preservation.

When no model preference is supplied, choose a generic market-appropriate model direction:

- Resortwear, dresses, kaftans, swim coverups: warm vacation lookbook, sunlit resort, relaxed standing or walking pose, full or three-quarter body crop.
- Jewelry, bags, watches, accessories: partial-body or hand/shoulder crop, product clearly visible, avoid face when not needed.
- Beauty and personal care: tasteful close-up or bathroom/vanity use scene, avoid medical claims or fake before/after proof.

Be honest in the prompt: create a commercial model/lifestyle image, not a guaranteed exact try-on. Preserve garment print, color, silhouette, and key details as much as possible, but do not claim exact fit, sizing, or manufacturing accuracy.

### Prompt Structure

Before calling `$gpt-image-2`, write a compact brief and convert it into one prompt per output image:

```text
Create a market-ready ecommerce image for <platform/market>.
Primary product: preserve the product from image 1 accurately, including shape, proportions, color, material appearance, packaging, labels, logo placement, SKU details, and distinctive physical features.
Image type: <listing/lifestyle/ad first frame/selling point/detail>.
Creative direction: <archetype and short rationale>.
Scene and composition: <specific scene, camera angle, product size, crop, text-safe space>.
Lighting and style: <realistic lighting, color palette, texture, finish, market tone>.
Visible text: <none or concise factual copy in target language>. Keep text mobile-readable and avoid tiny typography.
Reference usage: use images 2+ only for mood, scene, composition, lighting, crop, or layout inspiration; do not copy unrelated products, competitor branding, watermarks, badges, or exact layouts.
Avoid: distorted product, changed logo, changed packaging, fake certifications, fake platform badges, fake discounts, unsupported performance claims, QR codes, phone numbers, URLs, unreadable text, obvious AI gloss, plastic skin, warped hands.
```

For model-lookbook images, use this addition:

```text
Model direction: <generic target-market model, pose, crop, styling mood>. Show the product worn or styled naturally on the model, with the product clearly visible and commercially flattering.
Accuracy: preserve the garment/product color, print, silhouette, border details, scale impression, and styling intent from image 1. Do not make exact fit, sizing, or body-shaping claims.
Avoid: real-person likeness unless supplied and requested, distorted anatomy, warped hands, changed garment print, changed neckline/sleeves/hem, oversexualized posing, fake body results, plastic skin, hidden product.
```

For product-preserving workflows, call `$gpt-image-2` in image editing mode and keep the primary product image first. Use high quality and PNG by default. Use one `$gpt-image-2` call per requested asset when the set contains different image types, because each asset needs a focused prompt; for a default six-image set, run those asset-specific calls concurrently according to the submission strategy above.

## Result Handling

Follow `$gpt-image-2` result handling. Download or save generated images as that skill instructs, then preview or deliver the image artifacts to the user when practical.

Name outputs by role, for example:

- `listing-01.png`
- `lifestyle-01.png`
- `ad-first-frame-01.png`
- `selling-point-01.png`
- `detail-01.png`
- `variant-01.png`

After generation, briefly report:

- which platform/market direction was used
- which images were produced
- any important tradeoffs or safety adjustments
- one recommended next iteration, such as stronger UGC realism, cleaner marketplace compliance, or more premium styling

## Failure Handling

- Missing product image: ask for one product image and stop.
- Weak or ambiguous goal: default to the 6-image set unless the user explicitly wants a single image.
- Missing platform: default to general ecommerce, then mention that platform-specific variants can be generated next.
- Unsupported or risky claim: remove it or ask for evidence; do not invent certifications, medical claims, safety claims, performance numbers, awards, warranties, or absolute claims.
- Text-heavy request: keep generated on-image text short. For complex detail-page layouts, suggest generating a clean background image first and adding precise text/layout in a design tool afterward.
- Product fidelity risk: prefer fewer edits, cleaner backgrounds, and product-dominant compositions. If the model changes the product, rerun with a stricter preservation prompt.
- Model imagery risk: if the model image changes the garment too much, rerun with stronger preservation and a simpler pose/crop. If exact try-on, exact sizing, a specific person's likeness, or regulated body-result claims are required, ask for the needed reference image or clarify the limitation before generating.
- Reference image risk: use references as mood/layout only; never reproduce competitor packaging, trademarks, watermarks, or distinctive campaign layouts.
- `$gpt-image-2` failure, auth, billing, timeout, upload, or download issue: follow `$gpt-image-2` failure guidance and report the exact blocker. Do not start duplicate jobs just because a wait window ended.
