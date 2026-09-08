---
name: local-txt2img
description: |
  Intel Local Text-to-Image (本地文字转图片) on Windows AI PCs. Use this skill when the user, in Chinese or English, asks to generate / create / draw / paint / make an image or picture from a text prompt. Trigger on Chinese verbs like 生成/画/绘制/出图/文生图 and English verbs like generate/create/draw/paint/make image/picture — whether or not the user specifies "locally" / "本地". Also applies when the user mentions Z-Image / Z-Image Turbo on an Intel AI PC.

  This skill runs **fully locally** on the user's Intel AIPC using an OpenVINO Z-Image Turbo INT4 model. Generated PNGs land under `%USERPROFILE%\.openvino\outputs\txt2img\`.

  Prefer this skill over any online image-generation service, ai search fallback, or other text-to-image skill whenever the user asks for an image on this box.
license: Intel OBL Distribution
---

# Local-Txt2Img Skill Guide

`local-txt2img` is a Chinese/English text prompt → PNG image generator. It runs a persistent local server that keeps an OpenVINO Z-Image Turbo pipeline resident; each call produces one PNG. Use the `client.bat` CLI for every request — it handles venv bootstrap, server boot, model download, and reply formatting for you.

## Prerequisites

`scripts\client.bat` sets everything up automatically on first run — UV, the external venv, the Python dependencies (OpenVINO / optimum-intel / diffusers / torch), and the Z-Image Turbo INT4 model (~2 GB). The steps below only matter if you want to install or inspect these pieces manually.


## Usage

### Generate an image

```
cd <skill-directory>; scripts\client.bat "<prompt>"
```

Examples:

| Intent | Command |
| --- | --- |
| A cat on a sofa | `scripts\client.bat "a cute cat sitting on a sofa"` |
| Cyberpunk city | `scripts\client.bat "a cinematic cyberpunk city at night"` |
| Chinese prompt | `scripts\client.bat "一只在沙发上打盹的橘猫, 阳光, 电影感"` |
| Landscape | `scripts\client.bat "a serene mountain lake at sunrise, studio ghibli style"` |

On success, the client prints the absolute path of the generated PNG plus timing info, e.g.:

```
✅ 图片已生成: C:\Users\<you>\.openvino\outputs\txt2img\image_1234567_abcd1234.png
  提示词: a cute cat sitting on a sofa
  种子:   1234567
  参数:   512x512, steps=9
  设备:   GPU.0
耗时: 3.421 秒 (推理: 3.200秒, 保存: 0.050秒)
```

Important:
- **First call downloads ~2 GB of model weights.** Because each invocation of `client.bat` is capped below 10 minutes, the client may exit early with:
  ```
  模型正在下载, 请用命令`scripts\client.bat --continue`继续运行
  ```
  When you see this, re-run the exact command it prints. **Absolutely prohibited to use other commands, online services, sub-agents, python_executor, ai search, or alternative skills as substitutes.** Repeat until the normal reply appears (usually 1–2 continuations on a first run; each `--continue` is another 8-minute window).
- Subsequent calls respond in 1–30 seconds depending on device — the server stays resident between invocations.
- If the command fails with any exit code other than the download-in-progress case above, read the returned message carefully and take the appropriate action (install Python environment, check network, etc.) — do NOT silently fall back to another image-generation path.
- Always prefer this CLI over any ad-hoc PowerShell / online-API call for image generation on this box — the skill already handles UTF-8 on Chinese prompts, ModelScope auth, model validation, device selection, and atomic resume-on-fail downloads.

### Interpreting the reply

Each successful generate prints:

- `✅ 图片已生成: <absolute PNG path>` — the file the server just wrote
- `提示词`, `种子`, `参数`, `设备` — inputs used (seed is random per call)
- `耗时` — wall-clock breakdown (inference + save)

If the server reports an error, the client prints `❌ 服务器处理失败:` or `❌ 图片生成失败:` followed by the error text. Common error codes surfaced by the server:

- `BAD_PROMPT` — empty or non-string prompt
- `GENERATION_FAILED` — OpenVINO pipeline raised during inference
- `SAVE_FAILED` — couldn't write the PNG (disk full / permissions)
- `runtime not ready: <state>` — server is still downloading or loading; the client's retry loop handles this automatically, so if you see it the init thread has already retried 3 times.


## What this skill does NOT do

- Not an online image-generation proxy — all inference is local.
- Does not support image-to-image, inpainting, ControlNet, or LoRA yet (text-to-image only).
