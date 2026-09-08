---
name: zero-cost-video-render
description: 短视频/科普视频的零积分降级渲染。当视频生成子代理遇到 429 限流、API 限速、子代理失败、或用户明确要求"零积分出片"时，启用本方案：edge-tts（微软免费 TTS，零费用）+ Pillow（深蓝科技风静态帧）+ FFmpeg（zoompan/xfade/amix 一次合成）出 1920×1080 MP4。覆盖 30-90 秒科普/行业向短视频制作全流程，无需任何 AI 子代理、不消耗积分、不联网 API。
trigger:
  - 视频渲染失败
  - 429 限流
  - 视频降级
  - 零成本视频
  - 零积分视频
  - 零成本出片
  - 视频子代理失败
  - 视频生成降级
  - edge-tts
  - 本地渲染视频
version: 1.1
created: 2026-08-20
updated: 2026-08-22
author: 凌导（视频生成团队主理人）
---

# zero-cost-video-render · 零积分视频降级渲染

> 来源：2026-08-20 凌晨「AI Agent 智能体」60 秒短视频，因 WorkBuddy 用量 429 限流，灵映子代理 45 分钟失败后，主理人用纯本地工具链 8 分钟出片，**0 积分、0 API 费用、0 AI 子代理**。

---

## 0. 何时启用

满足以下任一条件，**放弃 AI 子代理**、启用本方案：

- ❌ WorkBuddy / 灵映 / HyperFrames 子代理报 `429 rate limit`
- ❌ 用户明确说「零积分 / 零成本 / 降级 / 本地出片」
- ❌ 视频生成需要立即出片，等不及子代理启动
- ❌ 已有灵枢产出的 JSON 制作包 + narration.txt，只需最后一步渲染

**不适用**：需要真人出镜、产品实拍、B-roll 实拍素材的视频（这种本方案做不了）。

---

## 1. 成本核算（启动前必跑，符合龙虾五步法 v4.0 置顶铁律）

```
【成本复盘模板】
- 预算积分：0
- 实际估算：0（edge-tts 微软免费 TTS，零费用；PIL/FFmpeg 系统级工具）
- 工具调用：4-6 次本地脚本执行（Bash + Python）
- 外部 API：edge-tts（WebSocket 走微软，免费、无 Key）
- 预计时长：5-10 分钟出片（60 秒视频）
```

性价比：高（用户要视频，本方案零成本可达，**不做就是 0**）。

---

## 2. 工具链预检（4 项必通过）

| 工具 | 检查命令 | 通过标准 |
|------|---------|---------|
| **edge_tts** | `"C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe" -c "import edge_tts; print('OK')"` | 输出 `OK`（已装在 managed Python） |
| **Pillow** | 同上 + `from PIL import Image, ImageDraw, ImageFont` | 已装或 `pip install pillow --quiet` 装到隔离环境 |
| **FFmpeg** | `ffmpeg -version` | 任意 6.0+ 版本，推荐 gyan.dev 8.x |
| **中文字体** | `ls C:/Windows/Fonts/msyh.ttc C:/Windows/Fonts/msyhbd.ttc` | 都存在（Windows 自带） |

零依赖 / 零联网检测脚本：

```bash
"C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe" -c "
import sys
ok = True
try:
    import edge_tts; print('[OK] edge_tts', edge_tts.__version__)
except ImportError: ok = False; print('[FAIL] edge_tts NOT installed')
try:
    from PIL import Image, ImageDraw, ImageFont; print('[OK] Pillow')
except ImportError: ok = False; print('[FAIL] Pillow NOT installed')
import subprocess
v = subprocess.run(['ffmpeg','-version'], capture_output=True, text=True).stdout.split('version ')[1].split(' ')[0]
print('[OK] ffmpeg', v)
import os
for f in ['msyh.ttc','msyhbd.ttc']:
    p = f'C:/Windows/Fonts/{f}'
    print('[OK]' if os.path.exists(p) else '[FAIL]', f)
sys.exit(0 if ok else 1)
"
```

任一 FAIL，先补：缺 Pillow → `pip install pillow --quiet`；其他基本都现成。

---

## 3. 标准工作流（4 步出片）

### Step 1 · 配音生成（按分镜逐段，零积分）

读取 `narration.txt`（每行一段，对应一个分镜），逐段调 edge-tts：

```python
# generate_audio_v2.py —— 完整脚本见本 skill 同目录 references/
import asyncio, os
import edge_tts

VOICE = "zh-CN-XiaoxiaoNeural"   # 中文女声，温柔科普感
RATE  = "-15%"                    # 慢速，让每段 8-9 秒，利于 60s 整体节奏
TEXT  = open("narration.txt", encoding="utf-8").read().strip().split("\n")

async def gen(i, text):
    # ★ edge_tts 7.x 关键：boundary="WordBoundary" 拿词级时间戳；feed(chunk) 传整个 chunk
    c = edge_tts.Communicate(text, VOICE, rate=RATE, boundary="WordBoundary")
    sm = edge_tts.SubMaker()
    with open(f"audio/seg{i}.mp3", "wb") as fd:
        async for ch in c.stream():
            if ch["type"] == "audio":
                fd.write(ch["data"])
            else:  # WordBoundary
                sm.feed(ch)
    with open(f"srt/seg{i}.srt", "w", encoding="utf-8") as fd:
        fd.write(sm.get_srt())

async def main():
    os.makedirs("audio", exist_ok=True)
    os.makedirs("srt", exist_ok=True)
    for i, t in enumerate(TEXT):
        print(f"[{i}] {t}")
        await gen(i, t)

asyncio.run(main())
```

**踩坑提示**：
- edge_tts 7.x 只有 `SentenceBoundary` 和 `audio` 两种 chunk；老脚本假设的 `WordBoundary` 已废弃 → 必须用 `boundary="WordBoundary"` 显式开启
- `SubMaker.feed(msg)` 接收整个 chunk 对象，不要拆 offset/duration/text 三个参数（那是旧版 API）
- `RATE=-15%` 是经验值：168 字 / 60s 视频最佳；太慢显得拖，太快对不齐画面

### Step 2 · 画面生成（PIL 静态帧 + 字幕条）

PIL 绘制 1920×1080 PNG，每分镜 1 帧。**所有分镜复用同一套模板**：

```python
from PIL import Image, ImageDraw, ImageFont
W, H = 1920, 1080
FONT_BD = "C:/Windows/Fonts/msyhbd.ttc"
FONT_RG = "C:/Windows/Fonts/msyh.ttc"

def font(sz, bold=True): return ImageFont.truetype(FONT_BD if bold else FONT_RG, sz)

def vgrad(top, bot):
    """垂直渐变背景"""
    img = Image.new("RGB", (W, H), top)
    for y in range(H):
        t = y / H
        img.putpixel((0, y), tuple(int(a + (b - a) * t) for a, b in zip(top, bot)))
    return img.resize((W, H))

def particles(img, n=46, seed=7):
    """漂浮粒子（科技感）"""
    import random
    rnd = random.Random(seed)
    ov = Image.new("RGBA", (W, H), (0,0,0,0))
    d = ImageDraw.Draw(ov)
    for _ in range(n):
        x, y = rnd.randint(0, W), rnd.randint(0, H)
        r = rnd.uniform(0.8, 2.6)
        a = rnd.randint(30, 110)
        col = (120,200,255,a) if rnd.random()<0.7 else (255,215,130,a)
        d.ellipse([x-r, y-r, x+r, y+r], fill=col)
    img = img.convert("RGBA"); img.alpha_composite(ov); return img

def caption(img, text, y=H - 180):
    """底部字幕条：圆角半透明黑底 + 白字"""
    ov = Image.new("RGBA", (W, H), (0,0,0,0))
    d = ImageDraw.Draw(ov)
    f = font(46)
    lines, cur = [], ""
    for ch in text:
        if d.textlength(cur + ch, font=f) > 1500:
            lines.append(cur); cur = ch
        else: cur += ch
    lines.append(cur)
    th = len(lines) * 62 + 36
    y0 = y - th // 2
    d.rounded_rectangle([W//2 - 810, y0, W//2 + 810, y0 + th], 22,
                        fill=(8,12,30,168))
    yy = y0 + 30
    for ln in lines:
        tw = d.textlength(ln, font=f)
        d.text(((W-tw)/2, yy), ln, font=f, fill=(255,255,255,235))
        yy += 62
    img.alpha_composite(ov)
```

每个分镜 1 张 PNG，保存到 `frames/segN.png`。

**踩坑提示**：
- Pillow `ImageDraw.text(xy, text, font, fill)` 的位置参数 fill 在 font **之前**！传 `font(52)` 当关键字 `font=font(52)` 才安全（直接用本 skill 的 `text_on` 辅助函数已封装）
- 字幕条 `y=H-180` 会与画在底部的图解文字（如本 skill 的"MCP·砖"在 y=780-900）碰撞 → **把图解上移或用两行字幕避开**，或接受碰撞（字幕条讲的内容正好盖住图解文字时，反而强化）
- 渐变背景 `putpixel` 1920×1080 一次性填很慢（约 2s），可接受；不要每帧重画，缓存或单次算

### Step 3 · FFmpeg 一次合成（zoompan + xfade + amix）

**所有 6 段拼接到一次 `filter_complex` 调用**——避免 6 次临时 mp4 中转：

```python
import subprocess
BUF = 1.2   # 画面比音频多 1.2s 缓冲
XF  = 0.5   # 段间交叉淡化 0.5s
# 1) 读音频时长
aud_dur = [float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
    "-of","default=noprint_wrappers=1",f"audio/seg{i}.mp3"],
    capture_output=True,text=True).stdout.strip().split("=")[-1]) for i in range(N)]
durs = [a + BUF for a in aud_dur]
total = sum(durs) - XF * (N - 1)

# 2) zoompan 滤镜（偶段 zoom-in / 奇段 zoom-out / 末段静止）
def zoom(i, dur):
    n = int(dur * 25)  # FPS=25
    if i == N - 1: z = "1.0"
    elif i % 2 == 0: z = f"min(1.0+0.00065*on,1.12)"
    else: z = f"max(1.12-0.00065*on,1.0)"
    return f"zoompan=z='{z}':d={n}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=25"

# 3) filter_complex
fc = []
for i in range(N):
    fc.append(f"[{i}:v]{zoom(i, durs[i])}[v{i}];")
offs = []
for i in range(N-1):
    offs.append(sum(durs[:i+1]) - XF * (i+1))
cur = "v0"
for i in range(N-1):
    fc.append(f"[{cur}][v{i+1}]xfade=transition=fade:duration={XF}:offset={offs[i]:.3f}[x{i+1}];")
    cur = f"x{i+1}"
fc.append(f"[{cur}]fade=t=out:st={total-1.5:.3f}:duration=1.5[vout];")
for i in range(N):
    start = sum(durs[:i]) - XF * i + 0.15
    ms = int(start * 1000)
    fc.append(f"[{N+i}:a]adelay={ms}|{ms}[a{i}];")
fc.append(f"{''.join(f'[a{i}]' for i in range(N))}amix=inputs={N}:normalize=0,pan=stereo|c0=c0|c1=c0,loudnorm=I=-16:TP=-2.0,aresample=44100[aout]")

cmd = ["ffmpeg","-y"] + [x for i in range(N) for x in ("-i",f"frames/seg{i}.png")] \
      + [x for i in range(N) for x in ("-i",f"audio/seg{i}.mp3")] + [
      "-filter_complex", "".join(fc),
      "-map","[vout]","-map","[aout]",
      "-t", f"{total:.3f}",
      "-c:v","libx264","-preset","medium","-crf","20",
      "-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-ar","44100",
      "-movflags","+faststart", "agent_video.mp4"]
subprocess.run(cmd, check=True)
```

**踩坑提示**：
- `zoompan` 对 `-i img.png`（非 loop）单帧输入也能输出多帧动画：`d=帧数` 直接控制
- xfade offset = 上一段累计时长 - 已重叠总时长，逐段递推
- `amix=normalize=0` 保持音量不衰减（默认 normalize=1 会按 1/N 缩放，音量会小）
- 末尾 `fade=t=out` 给个 1.5s 淡出，避免硬切
- `+faststart` 让 MP4 元数据前置，网页播放更顺

### Step 4 · 质检（5 项必查）

```bash
# 1) 文件存在
ls -la agent_video.mp4   # > 1MB
# 2) 时长
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 agent_video.mp4
# 3) 抽 4-5 帧画面人眼 QC（关键时间点）
for t in 4 15 30 42 50; do ffmpeg -y -v error -ss $t -i agent_video.mp4 -frames:v 1 qc_$t.png; done
# 4) 音视频同步
ffprobe -v error -show_entries stream=codec_name,channels,sample_rate -of default agent_video.mp4   # 必须 channels=2（立体声，避免蓝牙耳麦无声）
# 5) 移动到工作区根
mv agent_video.mp4 ../agent_video_<日期>.mp4
```

抽帧后用 Read 工具读 PNG 做肉眼看图质检：字幕不乱码、图解不重叠、配色统一、字体清晰。

---

## 4. 完整参考实现

工作脚本存放在本 skill 同目录 `references/`：

- `references/generate_audio_v2.py` —— Step 1 配音
- `references/build_video.py` —— Step 2 画面 + Step 3 合成（一站式）
- `references/narration.txt` 示例：6 段科普旁白样板
- `references/README.md` —— 历史实战经验（2026-08-20 AI Agent 智能体主题）

**实战出处**：`C:\Users\Administrator\WorkBuddy\2026-08-19-21-21-27\agent_video_build\`（即本次真实产出的工作区）

---

## 5. 与本机体系的联动

- **龙虾五步法 v4.0**：本 skill 是 Step4「自主执行」+ Step5「反思进化」的标准落地路径
- **零积分任务执行 skill**（`zero-cost-task-execution`）：本 skill 是该 skill 在"视频渲染"场景的具体实现
- **降级路径**：当 `video-gen-team/ling-producer` 失败时，本 skill 立即顶上
- **沉淀位置**：
  - 知识产出 → `E:\龙虾AI主控中心\Obsidian\wiki\视频生成\零积分降级渲染_20260820.md`
  - 工作脚本 → 本 skill `references/`

---

## 6. 已知限制

1. **画面是静态帧 + Ken Burns 动效**，不能做真人出镜、产品实拍、复杂转场
2. **edge-tts 不能定制音调/情感**，对语调要求高的解说场景需换 Azure TTS（要 Key）
3. **没有背景音乐**，全程靠配音 + 字幕；如需 BGM 可加 ffmpeg `amix` 一段版权免费音乐
4. **单语种最佳**（edge-tts 中文女声 Xiaoxiao 经验最稳）；多语种需逐段选 voice
5. **输出尺寸 1920×1080 横屏固定**；如需竖屏（抖音 9:16）需改 W/H + 重排布局
6. **v1.1 起音频默认立体声 44.1kHz**（已修单声道蓝牙耳麦无声问题）；若目标平台强制单声道，去掉 `pan=stereo` 即可

---

## 7. 快速启动（一行命令）

```bash
# 假设 narration.txt + frames/ + audio/ 都已就绪
cd agent_video_build && "C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe" build_video.py
```

完整流水线（从 0 旁白到出片）：

```bash
# 1) 配音
python generate_audio_v2.py
# 2) 画面 + 合成
python build_video.py
# 3) 质检抽帧
mkdir qc && for t in 4 15 30 42 50; do ffmpeg -y -v error -ss $t -i agent_video.mp4 -frames:v 1 qc/qc_$t.png; done
```

---

## 8. 四化迭代映射（自我进化标准）

| 四化 | 本 skill 落地 |
|------|--------------|
| **智能化** | edge-tts 7.x API 自动适配（`boundary=WordBoundary` + `feed(chunk)`）；`loudnorm` 自动响度归一化；zoompan 奇偶段自动正反推镜 |
| **定制化** | `narration.txt` 即改即渲；`VOICE/RATE/FPS/W/H` 均为顶部参数；分镜数 N 可变（4-6 段都行） |
| **全自动化** | 2 条命令出片（`generate_audio_v2.py` → `build_video.py`），无人工干预、无积分、无联网 API |
| **自我净化** | 渲染产物固定落 `agent_video_<日期>.mp4`；frames/audio/srt 为中间产物，定位明确可一键清理；v1.1 新增「单声道→立体声」自动校正，杜绝耳麦无声 |

**v1.1 修复记录（2026-08-22）**：原 v1.0 输出为**单声道 24kHz**，实测部分蓝牙耳麦/播放器不发声。已改为 `pan=stereo` + `aresample=44100` + `loudnorm`，输出 **立体声 44.1kHz**，全设备兼容。成片 `agent_video_20260819_v2.mp4` 已验证可播放。

## 9. 播放端耳麦无声排查清单（交付前自检）

片方已出立体声仍"耳麦没声音"，99% 是**播放端设备路由**问题，按序排查：

1. **设默认输出**：右键任务栏音量图标 → 声音设置 →「输出」选你的耳麦（非"扬声器"）；页尾「高级」里把耳麦也设为**默认通信设备**。
2. **换播放器**：WorkBuddy 内置预览面板有时不路由到蓝牙耳麦；用 **VLC / PotPlayer** 打开 MP4 最稳。
3. **查音量混音器**：播放时右键音量 → 打开音量混合器，确认该播放器通道没被静音/拉到 0。
4. **蓝牙耳麦**：确认已连接且电量充足；部分耳麦"听歌模式"和"通话模式"采样率不同，重连一次可解。
5. **有线耳麦**：拔插换前面板/后面板插孔，排除接触不良。

> 文件侧已用 `ffprobe` 验证音轨完好（非静音）后再交付；若上述都过仍无声，属硬件故障，非渲染问题。

---

**维护者**：凌导（视频生成团队主理人）
**首次实战**：2026-08-20 凌晨 02:00-02:14，「AI Agent 智能体」60s 短视频
**下次触发词**：「视频渲染失败」「零成本出片」「降级渲染」「429 限流」
