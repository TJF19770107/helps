# references · 实战出处

| 文件 | 来源 | 用途 |
|------|------|------|
| `build_video.py` | 2026-08-20 凌晨 AI Agent 短视频 | PIL 画 6 分镜 + ffmpeg zoompan/xfade/amix 一次合成 |
| `generate_audio_v2.py` | 同上 | 按分镜逐段生成 edge-tts 配音 + SRT 词级字幕（7.x 兼容） |
| `narration.txt` | 同上，6 段科普旁白 | Step 1 输入，决定段数与节奏 |

最近实战工作区（含 ffmpeg 渲染日志、抽帧 QC 图）：`C:/Users/Administrator/WorkBuddy/2026-08-19-21-21-27/agent_video_build/`

下次用：
```bash
cd <your_project> && cp -r /g/WorkBuddy_Data/skills/zero-cost-video-render/references/ ./
python generate_audio_v2.py    # 配音
python build_video.py          # 画面+合成
```
