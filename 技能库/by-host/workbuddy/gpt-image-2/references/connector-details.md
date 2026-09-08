# GPT Image 2 Connector Details

Use this reference only when debugging the runner, manually recovering a
session, or validating connector schemas.

## Actions

- Text-to-image submit: `fusion-api.openai_image_async_submit`
- Text-to-image result: `fusion-api.openai_image_async_result`
- Image edit submit: `fusion-api.openai_image_edit_async_submit`
- Image edit result: `fusion-api.openai_image_edit_async_result`

Do not use `--wait-result` for normal execution. Submit once, keep the
`sessionId`, then poll the matching result action with `sessionID`.

## Manual Text-To-Image

```bash
oo connector run "fusion-api" \
  --action "openai_image_async_submit" \
  --data '{"model":"gpt-image-2","prompt":"A minimalist product photo of a ceramic mug on a walnut table","output_format":"png","quality":"high","size":"1024x1024"}' \
  --json
```

```bash
oo connector run "fusion-api" \
  --action "openai_image_async_result" \
  --data '{"sessionID":"<sessionId>"}' \
  --json
```

## Manual Image Edit

```bash
oo connector run "fusion-api" \
  --action "openai_image_edit_async_submit" \
  --data '{"model":"gpt-image-2","prompt":"Replace the sweater with a well-fitted dark navy business suit. Preserve the same person, pose, lighting, camera angle, and background.","images":[{"image_url":"https://example.com/source.png"}],"output_format":"png","quality":"high","size":"1024x1536"}' \
  --json
```

```bash
oo connector run "fusion-api" \
  --action "openai_image_edit_async_result" \
  --data '{"sessionID":"<sessionId>"}' \
  --json
```

## Result Shapes

Completed result actions usually wrap the image payload:

- State: `.data.state == "completed"`
- Image URLs: `.data.data.data[].url`
- Revised prompts: `.data.data.data[].revised_prompt`
- Metadata: `.data.data.model`, `.data.data.size`, `.data.data.quality`,
  `.data.data.output_format`, `.data.data.usage`

Some connector modes may return the image payload directly under `.data`.
Handle both shapes.

If a result action returns `processing`, wait and poll the same `sessionID`
again. If it returns `not_found`, stop and report the session blocker.
