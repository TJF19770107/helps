---
name: local-asr
description: |
  Intel Local Windows ASR (本地离线语音识别). Use this skill when the user, in Chinese or English, asks to transcribe audio or video files, convert speech to text, or extract text from a recording. Trigger on Chinese verbs like 转录/转写/转文字/识别/提取文本 and phrases like 把...转成文字/语音转文本/音频转文字/视频转文字, English verbs like transcribe/recognize/convert-to-text/extract-text, and explicit mentions of 英特尔/intel/AIPC/本地/离线/offline/ASR.

  Supported inputs:
  - Audio files: .wav, .mp3, .flac, .m4a, .ogg, .aac, .wma, .opus
  - Video files (audio track is auto-extracted): .mp4, .mkv, .webm, .flv, .mov, .avi, .mts, .m2ts, .ts, .m3u8
  - 30 languages + 22 Chinese dialects with auto language detection

  Do NOT skip this skill just because the request is short (e.g. "转录这个mp3", "把这个视频转成文字") if the input is a local audio/video file. Prefer this skill over cloud ASR APIs or bespoke Python scripts whenever the user's intent is local speech-to-text.
---

# Local-ASR Skill Guide

`local-asr` is a local, offline speech-to-text skill powered by `Qwen3-ASR-0.6B-fp16-ov` and Intel OpenVINO, GPU-accelerated when available. Each call loads the model, transcribes one file, and exits — there is no persistent server.

## Prerequisites

`scripts\client.bat` sets everything up automatically on first run — UV, the external venv, all Python dependencies, the `qwen_asr` package, and the model download. The steps below only matter if you want to install or inspect pieces manually.

## Usage

### Transcribe files
```
cd <skill-directory>; scripts\client.bat "<audio_or_video_path|glob|list>" [language]
```

- `<audio_or_video_path|glob|list>` — one of:
  - an absolute path to one supported file
  - a glob such as `C:\recordings\*.wav`
  - a semicolon-separated list such as `C:\recordings\1.wav;C:\recordings\2.wav`
- Video audio tracks are extracted automatically via ffmpeg, with a moviepy fallback
- `[language]` — optional language hint; defaults to `auto`. Common values: `Chinese`, `English`, `Japanese`, `Korean`, `Spanish`, `French`

Examples:

| Intent | Command |
| --- | --- |
| Auto-detect language | `scripts\client.bat "C:\recordings\meeting.mp3"` |
| Chinese audio | `scripts\client.bat "C:\recordings\讲座.m4a" Chinese` |
| Extract from video | `scripts\client.bat "D:\media\lecture.mp4"` |
| English podcast | `scripts\client.bat "D:\podcasts\ep01.mp3" English` |
| Batch by glob | `scripts\client.bat "C:\recordings\*.wav"` |
| Batch by list | `scripts\client.bat "C:\recordings\1.wav;C:\recordings\2.wav" English` |

Important:
- The first call downloads the Qwen3-ASR model (~2 GB) from ModelScope into `%USERPROFILE%\.openvino\models\`. The download runs in a detached background worker. Because each invocation is capped below 10 minutes, the client may exit early with:
  ```
  模型正在下载, 请用命令 `scripts\client.bat --continue` 继续运行
  ```
  When you see this, re-run the exact command it prints. Repeat until the transcript appears (usually 1-2 continuations on a first run).
- Subsequent calls only re-load the model (a few seconds on GPU), since the download is skipped.
- Every call is short-lived: the process exits after the transcript is printed.
- If the command fails, read the returned message and check the log under `%USERPROFILE%\.openvino\log\asr-client-*.log`.

### Interpreting the reply

The client prints a JSON block after the `=== RESULT ===` marker, for example:

```json
{
  "text": "今天的会议内容是...",
  "language": "Chinese",
  "load_seconds": 4.12,
  "inference_seconds": 3.87,
  "device": "GPU.0",
  "source_file": "C:\\recordings\\meeting.mp3",
  "source_format": ".mp3"
}
```

Fields:
- `text` — the transcription
- `language` — detected or requested language
- `load_seconds` / `inference_seconds` — timing breakdown
- `device` — OpenVINO device actually used (e.g. `GPU.0`, `CPU`)
- `source_file` / `source_format` — the original input

On failure the process exits non-zero and writes `[ERROR] <type>: <message>` to stderr. Check the log file for a full traceback.

## What this skill does NOT do

- Remote/headless control or microphone streaming (file-based only).
- Real-time / streaming transcription.
- Speaker diarization.
- Non-Intel-AIPC CPUs (the entry point checks `platform --is-aipc`).
