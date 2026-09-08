---
name: gpt-image-2
description: 'Generate new images or edit existing images with GPT Image 2. Use when the user asks for GPT Image 2, GPT text-to-image, 文生图, image generation, 改图, image-to-image editing, replacing objects, preserving a person/product, or turning local/reference images into edited PNG/JPEG/WebP outputs.'
compatibility: "Requires the oo CLI."
metadata:
  icon: ':simple-icons:openai:'
  title: GPT Image 2
  packageName: '@zjxuyunshi/gpt-image-2'
  version: 1.1.2
---

# GPT Image 2

Use this skill when the user wants GPT Image 2 to generate new images or edit
existing images.

The skill has two modes:

1. GPT text-to-image: create images from a prompt.
2. GPT image editing: modify one or more supplied images.

Do not use this skill when the user explicitly asks for local-only image
processing, SVG/CSS/canvas assets, or repo-native code instead of hosted image
generation.

Use `gpt-image-2-virtual-tryon` instead when the request centers on virtual
try-on, garment transfer, clothing replacement, fashion styling, apparel
ecommerce, catalog model imagery, or outfit variants.

## Implementation Actions

Use only these concrete connector actions. Treat the connector service as an
implementation detail; do not mention it to the user unless reporting a
technical failure.

- GPT text-to-image, async run:
  `fusion-api.openai_image_async_submit`
- GPT text-to-image, async result:
  `fusion-api.openai_image_async_result`
- GPT image editing, async submit:
  `fusion-api.openai_image_edit_async_submit`
- GPT image editing, async result:
  `fusion-api.openai_image_edit_async_result`

No Fusion API synchronous text-to-image action is selected for this skill. Do
not call `fusion-api.openai_image_generate`; if a user explicitly requires an
ordinary synchronous connector instead of the selected Fusion API path, use
`openai.create_image` only after confirming that the ordinary OpenAI service is
acceptable for their account, cost, and data-routing needs.

Do not run `oo search` or `oo connector search` during normal use. The
capabilities are already selected.

The submit actions return a `sessionId`. Do not use `--wait-result` for normal
execution. Submit once, record the `sessionId`, then poll the matching result
action with `{"sessionID":"..."}`. This keeps interrupted runs recoverable:
resume polling with the same `sessionId` instead of submitting a duplicate job.

Fusion API is the selected built-in provider path. Do not ask the user for an
OpenAI API key during normal execution unless the connector returns an auth or
billing failure that explicitly requires user action.

## Preferred Scripts

Prefer the bundled JS runner through `BUN_BE_BUN=1 oo <script.js>` for normal
execution. If that JavaScript runtime path is unavailable, run the same script
with local `node <script.js>`. The runner wraps the full flow and prints a
single JSON object that agents can parse. The script still shells out to the
`oo` CLI for connector calls, uploads, and downloads, so the `oo` CLI must be
available in both runtime modes:

- Text-to-image generation plus download:
  `BUN_BE_BUN=1 oo "<skill-dir>/scripts/run_image.js" --mode generate ...`
- Image editing plus optional local upload plus download:
  `BUN_BE_BUN=1 oo "<skill-dir>/scripts/run_image.js" --mode edit ...`

For runner usage details, run:

```bash
BUN_BE_BUN=1 oo "<skill-dir>/scripts/run_image.js" --help
```

Fallback when `BUN_BE_BUN=1 oo <script.js>` cannot execute JavaScript:

```bash
node "<skill-dir>/scripts/run_image.js" --mode generate ...
node "<skill-dir>/scripts/run_image.js" --mode edit ...
```

Use direct `oo connector run ...` commands only when debugging the scripts,
handling a script failure, or using a newly added connector field that the
scripts do not yet expose.

Script outputs include:

- `ok`: success boolean
- `session_id`: resumable Fusion API session ID
- `session_file`: local JSON file containing the session ID and resume details
- `local_paths`: downloaded result image paths
- `remote_urls`: generated result URLs
- `out_dir`: output directory
- `poll_count`: number of result polls performed
- `metadata`: model, usage, and connector metadata when returned
- `uploads`: uploaded local image metadata for edit runs

The scripts keep `stdout` machine-readable by printing only the final JSON
result there. Progress logs go to `stderr` by default, with messages such as
uploading, submitting, saved resumable session, polling, completed,
downloading, and saved. Pass `--quiet` to suppress progress logs when a caller
needs silent execution.

After submit, the runner writes `<name>.session.json` in `--out-dir` before it
starts polling, then waits 30 seconds before the first result poll by default.
If the process is interrupted after submit, read the `session_id` from that
file and resume with:

```bash
BUN_BE_BUN=1 oo "/Users/yunshi/.codex/skills/gpt-image-2/scripts/run_image.js" \
  --mode generate \
  --session-id "<sessionId>" \
  --out-dir "/Users/yunshi/Downloads/gpt-image-2/example" \
  --name "ceramic-mug" \
  --output-format "png"
```

Preferred resume command:

```bash
BUN_BE_BUN=1 oo "/Users/yunshi/.codex/skills/gpt-image-2/scripts/run_image.js" \
  --session-file "/Users/yunshi/Downloads/gpt-image-2/example/ceramic-mug.session.json"
```

Use `--mode edit` when resuming an edit session. `--prompt` and `--image` are
not required for resume runs because the task has already been submitted.
Resume runs poll immediately by default. Optional polling controls:
`--initial-poll-delay-ms 30000`, `--poll-interval-ms 5000`, and
`--poll-timeout-ms 1800000`; use `--initial-poll-delay-ms 0` to check
immediately after submit, or `--poll-timeout-ms 0` for no local timeout.

## Mode Selection

Choose GPT text-to-image when the user provides only a prompt or asks to create
a new image from text.

Choose GPT image editing when the user provides any source image, reference
image, mask, `file_id`, local image path, attached image, or asks to change an
existing image. This includes product edits, object replacement, restyling,
background changes, composition from references, and localized edits outside the
fashion try-on scope.

Ask one concise follow-up only when a required prompt, source image, or risky
creative choice is missing. Otherwise infer conservative defaults from the
request.

When asking, present a short choice prompt with a recommended option. Use a
free-form input option only when concrete choices cannot cover the decision.

## Shared Payload Rules

Use `gpt-image-2` unless the user names a different OpenAI image model.

Pass `output_format` as `png` by default. Use `jpeg` or `webp` only when the
user asks for it or when compression is specifically useful.

Do not pass `response_format` to Fusion API image actions; the connector schema
does not accept that field. Read completed image outputs from returned URLs.
Handle returned HTTP URLs as downloadable image URLs, and still handle returned
`data:image/...;base64,...` values as inline image data rather than as
downloadable HTTP URLs.

Pass `quality: "high"` when the user asks for a polished final image, identity
or product preservation, realistic edits, or a deliverable asset. Use
`quality: "auto"` for quick drafts unless the user requests speed or lower
cost.

Choose `size` from the source aspect ratio or the user's requested format.
For GPT Image 2, pass `auto` or any `WIDTHxHEIGHT` value that matches the
official size constraints:

- The largest dimension must be at most `3840`.
- Width and height must both be multiples of `16`.
- The longest side may be at most 3x the shortest side.
- Total pixels must be between `655360` and `8294400`, inclusive.

Popular sizes include:

- Square: `1024x1024`, `2048x2048`
- Landscape: `1536x1024`, `2048x1152`, `3840x2160`
- Portrait: `1024x1536`, `2160x3840`
- 4:3 landscape: `1024x768`, `1536x1152`, `2048x1536`
- Auto: `auto`

Do not use legacy small draft sizes such as `256x256` or `512x512` for GPT
Image 2, because they are below the official minimum total-pixel constraint.

Optional fields supported by both modes: `background`, `n`,
`output_compression`, `partial_images`, and `user`. `moderation` is supported
for text-to-image only. Include optional fields only when the user asks or they
materially improve the result.

For long prompts, nested image arrays, masks, or quote/newline-heavy values,
write the payload to a JSON file and run with `--data @payload.json` instead of
inline shell JSON.

For direct connector debugging, schema details, or manual result parsing, read
[references/connector-details.md](references/connector-details.md).

## Local Images

Edit input images must be one of these MIME types before they are sent to GPT
Image 2:

- `image/jpeg`
- `image/png`
- `image/gif`
- `image/webp`

For local file paths, detect the actual MIME type before upload. If the input is
not one of the supported MIME types, convert it to PNG first, then upload and
use the converted PNG as the edit input. The bundled runner does this
automatically for local files and unsupported inline `data:image/...` inputs.
On macOS, the runner tries `sips` first, then ImageMagick `magick`, legacy
ImageMagick `convert`, `ffmpeg`, and `python3` with Pillow. On other platforms,
the runner tries `magick`, `convert`, `ffmpeg`, `python3` with Pillow, and then
`sips` only if it happens to be available.
For remote HTTP(S) image URLs, pass only URLs that already resolve to one of the
supported image MIME types; if that is uncertain, download the image locally and
let the runner convert it before upload.

For local image inputs, upload the file with `oo file upload "<filePath>" --json`
first. Parse the returned JSON object's `downloadUrl` field and pass that signed
download URL as `images[].image_url` or `mask.image_url`. Do not pass raw local
file paths to Fusion API connector actions.

Example:

```bash
oo file upload "/path/to/source.png" --json
```

Expected JSON shape:

```json
{
  "downloadUrl": "https://...",
  "expiresAt": "2026-05-14T00:00:00.000Z",
  "fileName": "source.png",
  "fileSize": 12345,
  "id": "019...",
  "status": "active",
  "uploadedAt": "2026-05-07T00:00:00.000Z"
}
```

Each image reference must contain exactly one of:

- `image_url`: a public image URL
- `file_id`: an OpenAI file ID

For edit inputs, keep image order aligned with the user's wording. Put the main
source image first, then reference images.

When a remote HTTP result URL must be saved locally, use
`oo file download "<url>" "<outDir>" --name "<fileNameWithoutExtension>" --ext "<extension>"`
when you need a deterministic local filename. `oo file download` prints a
localized human-readable saved-path line on stdout and does not support
`--json`; the bundled runner accepts `Saved to`, `已保存到`, and `保存至` with
half-width or full-width colons. If a result unexpectedly contains a
`data:image/...;base64,...` value, decode the base64 content directly into a
local image file instead of downloading.
After saving, preview or deliver the saved artifact to the user.

## GPT Text-To-Image

Use this mode for pure prompt-based image creation.

Required input:

- `prompt`: 1 to 32000 characters

Preferred one-call generation and download:

```bash
BUN_BE_BUN=1 oo "/Users/yunshi/.codex/skills/gpt-image-2/scripts/run_image.js" \
  --mode generate \
  --prompt "A minimalist product photo of a ceramic mug on a walnut table" \
  --out-dir "/Users/yunshi/Downloads/gpt-image-2/example" \
  --name "ceramic-mug" \
  --output-format "png" \
  --quality "high" \
  --size "1024x1024"
```

The script submits the request, stores the returned `sessionId`, waits 30
seconds, polls `openai_image_async_result`, downloads each image, and returns
JSON containing `local_paths` and `remote_urls`.

## GPT Image Editing

Use this mode for image-to-image edits, reference-guided generation,
composition, masked edits, character or subject preservation, product edits,
and style transfer.

Required inputs:

- `prompt`: 1 to 32000 characters
- `images`: 1 to 16 image references

Prompt shape:

- Say exactly what should change.
- Say what must remain unchanged when preservation matters.
- For identity, product, layout, or style fidelity, explicitly request
  preservation in the prompt.
- For localized edits, include a `mask` image reference when the user provides
  one.

Run edits:

Preferred one-call upload, edit, and download:

```bash
BUN_BE_BUN=1 oo "/Users/yunshi/.codex/skills/gpt-image-2/scripts/run_image.js" \
  --mode edit \
  --prompt "Replace the sweater with a well-fitted dark navy business suit. Preserve the same person, face, pose, lighting, camera angle, and background." \
  --image "/path/to/source.png" \
  --out-dir "/Users/yunshi/Downloads/gpt-image-2/example" \
  --name "edited-result" \
  --output-format "png" \
  --quality "high" \
  --size "1024x1536"
```

Pass `--image` multiple times for source and reference images; keep the primary
source image first. The script uploads local images automatically, passes remote
URLs through unchanged, supports `file_id:<id>`, submits the edit, downloads
results, and returns JSON containing `local_paths`, `remote_urls`, `uploads`,
and connector metadata. It does not use oo wait mode; it stores the returned
`sessionId` and polls `openai_image_edit_async_result` itself.

## Results

The runner reads image URLs from the completed result action and handles both
wrapped and direct `.data` result shapes. If the result action returns
`processing`, poll the same `sessionId` again. For new submissions, wait 30
seconds before the first poll unless the user asks for faster feedback. If the
polling process is interrupted, resume with `--session-file`, `--session-id`, or
the matching result action manually. Do not submit a duplicate job unless the
user asks to retry.

When saving an HTTP URL, download it locally. When saving a returned
`data:image/...;base64,...` value, decode the base64 content directly into a
local image file. Use the requested output name if provided. Otherwise choose a
short descriptive name from the task and preserve the output format extension.
Do not print full data URIs in the final response.

On success, make the image visible to the user. When `local_paths` is non-empty,
use those saved files for inline previews in their returned order instead of
matching `remote_urls`; use a remote URL as the primary preview only when no
corresponding local file was saved. On Windows, preserve drive-letter paths as
`C:/...` or `C:\\...` and never add a leading slash such as `/C:/...` to a
Markdown image destination. Show or attach the local image artifact rather than
only reporting the path. A local path alone is not enough unless the environment
cannot preview or attach files.
Mention only materially important execution details such as model, returned
size, returned quality, returned format, poll count, or mask use.

On failure, report the exact connector state or error and the smallest next
action. Stop on missing prompt, missing required image, inaccessible image URL
or local path, unsupported option, schema rejection, auth, billing, permission,
timeout, or `not_found` session blockers. If the connector rejects a field,
remove or rename only the rejected field when the schema-supported equivalent is
known. If download fails after the image result is ready, use the returned
`session_id` and `remote_urls` from the error JSON to resume or manually
download. Do not switch models or connector actions silently.
