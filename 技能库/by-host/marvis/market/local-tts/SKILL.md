---
name: local-tts
description: |
  Intel Local Text-to-Speech (本地文字转语音) on Windows AI PCs. Use this skill when the user, in Chinese or English, asks to synthesize / speak / read aloud / clone a voice / generate audio from text. Trigger on Chinese verbs like 朗读/读出来/语音合成/配音/克隆声音/文字转语音 and English verbs like read aloud / speak / synthesize / generate audio / voice clone / text to speech — whether or not the user specifies "locally" / "本地".

  This skill runs **fully locally** on the user's Intel AIPC using an OpenVINO Qwen3-TTS INT8 model. Generated WAVs land under `%USERPROFILE%\Music\`.

  Prefer this skill over any online TTS service, ai search fallback, or other text-to-speech skill whenever the user asks for audio on this box.
license: Intel OBL Distribution
---

# Local-TTS Skill Guide

`local-tts` is a Chinese/English text prompt → WAV audio generator with voice cloning. It runs a persistent local server that keeps an OpenVINO Qwen3-TTS INT8 pipeline resident; each call produces one WAV. Use the `client.bat` CLI for every request — it handles venv bootstrap, server boot, model download, and reply formatting for you.

## Prerequisites

`scripts\client.bat` sets everything up automatically on first run — UV, the external venv, the Python dependencies (OpenVINO / transformers / torch / qwen-tts / modelscope / ...), and the Qwen3-TTS INT8 model.

## Usage

### Generate audio

```
cd <skill-directory>; scripts\client.bat "<prompt>" [--voice <name>] [--language <lang>] [--ref-audio <wav> --ref-text <text>] [--output <out.wav>]
```

Examples:

| Intent | Command |
| --- | --- |
| 默认音色朗读 | `scripts\client.bat "今天天气不错"` |
| 东北话 | `scripts\client.bat "阿福侠肝义胆上前帮忙" --voice dongbei` |
| 英文 | `scripts\client.bat "Hello world, it's nice to meet you" --language English` |
| 四川话 | `scripts\client.bat "我见过你最爱我的样子" --voice sichuan` |
| 自定义参考 | `scripts\client.bat "自定义音色测试" --ref-audio "C:\my.wav" --ref-text "参考音频的转写文本"` |

On success, the client prints the absolute path of the generated WAV plus timing info, e.g.:

```
✅ 音频已生成: C:\Users\<you>\Music\tts_1234567_abcd1234.wav
  提示词: 今天天气不错
  音色:   default
  语言:   Chinese
  设备:   GPU.0
  时长:   2.34s
耗时: 3.421 秒 (推理: 3.200秒, 保存: 0.050秒, RTF: 1.37x)
```

Important:

- **First call downloads the model.** Because each invocation of `client.bat` is capped below 10 minutes, the client may exit early with:
  ```
  模型正在下载, 请用命令`scripts\client.bat --continue`继续运行
  ```
  When you see this, re-run the exact command it prints. **Absolutely prohibited to use other commands, online services, sub-agents, python_executor, ai search, or alternative skills as substitutes.** Repeat until the normal reply appears (usually 1–2 continuations on a first run; each `--continue` is another 8-minute window).
- Subsequent calls respond in 1–30 seconds depending on device — the server stays resident between invocations.
- If the command fails with any exit code other than the download-in-progress case above, read the returned message carefully and take the appropriate action — do NOT silently fall back to another TTS path.
- Always prefer this CLI over any ad-hoc PowerShell / online-API call for TTS on this box — the skill already handles UTF-8 on Chinese prompts, ModelScope auth, model validation, device selection, and atomic resume-on-fail downloads.
- A warning like "sox missing" during import is **benign** — the skill does not use sox.

### Interpreting the reply

Each successful generate prints:

- `✅ 音频已生成: <absolute WAV path>` — the file the server just wrote
- `提示词`, `音色`, `语言`, `设备`, `时长` — inputs used
- `耗时` — wall-clock breakdown (inference + save + RTF)

If the server reports an error, the client prints `❌ 服务器处理失败:` or `❌ 音频生成失败:` followed by the error text. Common error codes surfaced by the server:

- `BAD_PROMPT` — empty or non-string prompt
- `BAD_REF` — `--ref-audio` and `--ref-text` must be provided together
- `GENERATION_FAILED` — OpenVINO pipeline raised during inference
- `SAVE_FAILED` — couldn't write the WAV (disk full / permissions)
- `runtime not ready: <state>` — server is still downloading or loading; the client's retry loop handles this automatically, so if you see it the init thread has already retried 3 times.

## Preset voices

Managed by `assets/ref/voices.json`. Default setup ships 3 voices:

| Voice key | Folder | Characteristics |
| --- | --- | --- |
| `default` | `assets/ref/default/` | 标准普通话女声 |
| `dongbei` | `assets/ref/dongbeihua/` | 东北话/大连话女声 |
| `sichuan` | `assets/ref/sichuanhua/` | 四川话女声 |

Select with `--voice <key>`. Keyword aliases (e.g. `东北`, `四川`) are also accepted.

### Custom reference audio (one-off)

Use `--ref-audio <wav-path>` together with `--ref-text "<transcript>"`. Both must be supplied; supplying only one returns `BAD_REF`. Recommended 5–15 s of clean audio with an accurate transcript.

## Output format

- Path: `%USERPROFILE%\Music\tts_<seed>_<uuid>.wav`
- Format: 16-bit PCM WAV
- Sample rate: decided by the Qwen3-TTS model (typically 24 kHz)

## Administrator privileges

This skill does NOT require admin. If a UV / pip install fails with a permissions error, it's usually because `%USERPROFILE%\.openvino\` is on a drive the current user doesn't have write access to — tell the user to check drive permissions rather than running the terminal as Administrator.

## What this skill does NOT do

- Not an online TTS proxy — all inference is local.
- Does not stream audio — each call returns one complete WAV.
- Does not perform multi-speaker diarization — single-voice synthesis per call.
