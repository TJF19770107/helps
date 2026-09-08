# -*- coding: utf-8 -*-
"""gen_little_dragon_video.py · 生成「汤小龙·潜龙铭」有声视频（带文字）"""
import asyncio, os, subprocess
import edge_tts
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "voice")
os.makedirs(WORK, exist_ok=True)
FONT_BD = "C:/Windows/Fonts/msyhbd.ttc"
FONT_RG = "C:/Windows/Fonts/msyh.ttc"
W, H = 1280, 720
FPS = 25
VOICE = "zh-CN-YunxiNeural"   # 男声，更配「潜龙」
RATE = "-5%"
TITLE = "汤小龙 · 潜龙铭"
LINES = [
    "十年潜龙困深渊，一朝乘风上九天。",
    "天不生无用之人，地不长无名之草。",
    "黄河尚有澄清日，岂可人无得运时。",
    "雪压寒梅头不低，卧薪尝胆待佳期。",
    "终有一日同风起，扶摇直上九万里。",
]
TEXT = "。".join(LINES) + "。"

def font(sz, bold=True):
    return ImageFont.truetype(FONT_BD if bold else FONT_RG, sz)

def vgrad(top, bot):
    img = Image.new("RGB", (W, H))
    for y in range(H):
        t = y / H
        img.putpixel((0, y), tuple(int(a + (b - a) * t) for a, b in zip(top, bot)))
    return img

def build_frame():
    img = vgrad((12, 22, 50), (4, 8, 24))
    d = ImageDraw.Draw(img)
    # 潜龙意象：淡金色光环
    cx, cy = W // 2, H // 2
    for rr in range(220, 150, -2):
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  outline=(180, 160, 90, 60), width=2)
    d.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], outline=(210, 190, 120, 200), width=5)
    d.text((cx - d.textlength("龙", font=font(90))/2, cy - 60), "龙", font=font(90), fill=(235, 215, 130, 255))
    # 标题
    f_t = font(64)
    d.text((cx - d.textlength(TITLE, font=f_t)/2, 70), TITLE, font=f_t, fill=(255, 255, 255, 250))
    f_s = font(30, bold=False)
    sub = "十年潜龙 · 一朝乘风 · 扶摇直上九万里"
    d.text((cx - d.textlength(sub, font=f_s)/2, 150), sub, font=f_s, fill=(150, 200, 255, 210))
    # 诗句字幕区
    f_c = font(46)
    yy = 240
    for ln in LINES:
        tw = d.textlength(ln, font=f_c)
        d.text((cx - tw/2, yy), ln, font=f_c, fill=(255, 255, 255, 245))
        yy += 74
    out = os.path.join(WORK, "dragon_frame.png")
    img.convert("RGB").save(out)
    return out

async def gen_audio():
    out = os.path.join(WORK, "dragon_audio.mp3")
    c = edge_tts.Communicate(TEXT, VOICE, rate=RATE)
    with open(out, "wb") as f:
        async for ch in c.stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
    return out

def dur(path):
    s = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1", path], capture_output=True, text=True).stdout.strip()
    return float(s.split("=")[-1])

def render(frame, audio):
    adur = dur(audio)
    n = max(int(adur * FPS), 1)
    out = os.path.join(WORK, "汤小龙_潜龙铭_20260827.mp4")
    vf = (f"zoompan=z='min(1.0+0.0005*on,1.10)':d={n}:"
          f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},"
          f"fade=t=in:st=0:d=0.5,fade=t=out:st={max(adur-1,0.5):.2f}:d=0.8")
    cmd = ["ffmpeg", "-y", "-loop", "1", "-i", frame, "-i", audio, "-vf", vf, "-shortest",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
           "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    return out, adur

if __name__ == "__main__":
    fr = build_frame(); print("frame:", fr)
    au = asyncio.run(gen_audio()); print("audio:", au)
    out, adur = render(fr, au)
    print("VIDEO:", out, "dur=%.2fs" % adur)