# -*- coding: utf-8 -*-
"""gen_dragon_anim.py · 免费逐帧动画：会动的龙 + 金字诗 + 音频 → mp4
零成本：Pillow(画帧) + edge-tts(声音) + ffmpeg(合成)。全本地。
"""
import asyncio, math, os, random, subprocess, tempfile, shutil
import edge_tts
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "voice")
os.makedirs(WORK, exist_ok=True)
FONT_BD = "C:/Windows/Fonts/msyhbd.ttc"
FONT_RG = "C:/Windows/Fonts/msyh.ttc"
W, H = 1280, 720
FPS = 24
VOICE = "zh-CN-YunxiNeural"
RATE = "-5%"
POEM = [
    "十年潜龙困深渊，一朝乘风上九天。",
    "天不生无用之人，地不长无名之草。",
    "黄河尚有澄清日，岂可人无得运时。",
    "雪压寒梅头不低，卧薪尝胆待佳期。",
    "终有一日同风起，扶摇直上九万里。",
]
TEXT = "。".join(POEM) + "。"
TITLE = "汤小龙 · 潜龙铭"

def font(sz, bold=True):
    return ImageFont.truetype(FONT_BD if bold else FONT_RG, sz)

def sky(t):
    top = (10 + int(6*math.sin(t*0.1)), 20, 52)
    bot = (3, 7, 22)
    img = Image.new("RGB", (W, H))
    for y in range(H):
        tt = y / H
        img.putpixel((0, y), tuple(int(a + (b - a) * tt) for a, b in zip(top, bot)))
    return img

def dragon_points(phase):
    pts = []
    n = 64
    for i in range(n):
        u = i / (n - 1)
        x = W * 0.10 + u * (W * 0.80) + math.sin(u * 3.0 + phase) * W * 0.02
        y = H * 0.60 + math.sin(u * 4.5 + phase) * H * 0.10 + math.sin(u * 9.0 + phase * 1.4) * H * 0.02
        thick = 30 * (1 - u * 0.55) + 4
        pts.append((x, y, thick))
    return pts

def draw_dragon(d, pts, t):
    rnd = random.Random(7)
    # 身体（粗线条 + 描边）
    for i in range(len(pts) - 1):
        (x1, y1, w1) = pts[i]; (x2, y2, w2) = pts[i+1]
        d.line([x1, y1, x2, y2], fill=(12, 14, 22), width=int(w1)+8)
        d.line([x1, y1, x2, y2], fill=(176, 152, 80), width=int(w1))
    # 鳞片
    for i in range(4, len(pts) - 2, 3):
        x, y, w = pts[i]
        d.arc([x-9, y-6, x+9, y+6], 200, 340, fill=(120, 200, 255), width=2)
    # 脊鳍
    for i in range(6, len(pts) - 4, 4):
        x, y, w = pts[i]
        for k in range(3):
            d.line([x - 8 + k*6, y - 8 - k, x - 2 + k*6, y - 4 + k], fill=(90, 160, 230), width=3)
    # 龙首
    hx, hy, hw = pts[-1]
    d.ellipse([hx - 34, hy - 26, hx + 34, hy + 26], fill=(200, 180, 110), outline=(20, 20, 30), width=3)
    # 眼睛
    d.ellipse([hx + 8, hy - 14, hx + 22, hy - 2], fill=(255, 240, 200), outline=(10, 10, 10), width=2)
    d.ellipse([hx + 13, hy - 10, hx + 18, hy - 5], fill=(20, 20, 40))
    # 眉
    d.line([hx + 2, hy - 24, hx + 26, hy - 18], fill=(40, 40, 50), width=4)
    # 鼻/角
    d.line([hx - 10, hy - 22, hx - 20, hy - 44], fill=(230, 215, 160), width=5)
    d.line([hx + 6, hy - 26, hx + 12, hy - 48], fill=(230, 215, 160), width=5)
    # 须（随 t 摆动）
    for s in (-1, 1):
        for k in range(24):
            bx = hx - 6 - k * 4
            by = hy + 10 + s * (6 + k * 2) + math.sin(t*0.15 + k*0.4) * 5
            d.ellipse([bx-2, by-2, bx+2, by+2], fill=(220, 220, 230))
    # 火球（从龙口喷出，闪烁）
    fx = hx + 26
    for k in range(3):
        fr = 18 - k * 5 + int(6 * math.sin(t * 0.9 + k))
        fy = hy + 4 - k * 3
        col = (255, 60 + k * 40, 30) if k < 2 else (255, 200, 60)
        d.ellipse([fx - fr, fy - fr, fx + fr, fy + fr], fill=col)

def draw_clouds(d, t):
    for i in range(3):
        cx = (140 + i * 380 - int(t * 18) % (W + 200)) 
        cy = 90 + i * 70
        for k in range(4):
            r = 34 - k * 5
            d.ellipse([cx - r, cy - r*0.6, cx + r, cy + r*0.6], fill=(210, 225, 245))

def draw_text(d, t):
    # 标题
    f_t = font(56)
    title = TITLE
    cx = W // 2
    d.text((cx - d.textlength(title, font=f_t)/2, 30), title, font=f_t, fill=(255, 255, 255, 250))
    # 诗句（金字，随 t 轻浮）
    f_c = font(42)
    yy = 150 + int(6 * math.sin(t*0.1))
    for ln in POEM:
        tw = d.textlength(ln, font=f_c)
        x = cx - tw/2
        d.text((x+2, yy+2), ln, font=f_c, fill=(120, 100, 40))   # 阴影/描边
        d.text((x, yy), ln, font=f_c, fill=(250, 210, 90))        # 金字
        yy += 56

def render_frame(t, frame_path):
    img = sky(t)
    d = ImageDraw.Draw(img)
    draw_clouds(d, t)
    phase = t * 0.05
    pts = dragon_points(phase)
    draw_dragon(d, pts, t)
    draw_text(d, t)
    img.convert("RGB").save(frame_path)

async def gen_audio():
    out = os.path.join(WORK, "dragon_anim_audio.mp3")
    c = edge_tts.Communicate(TEXT, VOICE, rate=RATE)
    with open(out, "wb") as f:
        async for ch in c.stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
    return out

def dur(path):
    s = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1",path],capture_output=True,text=True).stdout.strip()
    return float(s.split("=")[-1])

def render(adb, frame_dir):
    out = os.path.join(WORK, "汤小龙_会动的龙_20260827.mp4")
    adur = min(dur(adb), 20.0)
    total = int(adur * FPS)
    print("frames to render:", total, flush=True)
    for i in range(total):
        render_frame(i / FPS, os.path.join(frame_dir, f"f{i:05d}.png"))
        if i % 120 == 0: print("  frame", i, flush=True)
    cmd = ["ffmpeg","-y","-framerate",str(FPS),"-i",os.path.join(frame_dir,"f%05d.png"),
           "-i",adb,"-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p",
           "-c:a","aac","-b:a","192k","-ar","44100","-ac","2","-shortest",
           "-movflags","+faststart",out]
    subprocess.run(cmd, check=True)
    return out, adur

if __name__ == "__main__":
    adb = asyncio.run(gen_audio()); print("audio:", adb)
    fd = tempfile.mkdtemp(prefix="dragon_frames_")
    try:
        out, adur = render(adb, fd)
        print("VIDEO:", out, "dur=%.2fs" % adur)
    finally:
        shutil.rmtree(fd, ignore_errors=True)