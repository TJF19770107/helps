import asyncio, os, subprocess, random
import edge_tts
from PIL import Image, ImageDraw, ImageFont

WORK = r"E:\龙虾AI主控中心\我的AI分身\豆包主会话全集\AI分身出片"
os.makedirs(WORK, exist_ok=True)
FONT_BD = "C:/Windows/Fonts/msyhbd.ttc"
FONT_RG = "C:/Windows/Fonts/msyh.ttc"
W, H = 1920, 1080
FPS = 25

VOICE = "zh-CN-XiaoxiaoNeural"
RATE  = "-15%"
TEXT  = "我是汤哥的AI分身，心理画像加技能库，零成本也能出片。"

def font(sz, bold=True):
    return ImageFont.truetype(FONT_BD if bold else FONT_RG, sz)

def vgrad(top, bot):
    img = Image.new("RGB", (W, H))
    for y in range(H):
        t = y / H
        img.putpixel((0, y), tuple(int(a + (b - a) * t) for a, b in zip(top, bot)))
    return img

def particles(img, n=64, seed=11):
    rnd = random.Random(seed)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for _ in range(n):
        x, y = rnd.randint(0, W), rnd.randint(0, H)
        r = rnd.uniform(0.8, 2.8)
        a = rnd.randint(30, 120)
        col = (120, 200, 255, a) if rnd.random() < 0.7 else (255, 215, 130, a)
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    return Image.alpha_composite(img.convert("RGBA"), ov)

def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for ch in text:
        if d.textlength(cur + ch, font=f) > maxw:
            lines.append(cur); cur = ch
        else:
            cur += ch
    lines.append(cur)
    return lines

def build_frame():
    img = vgrad((8, 16, 42), (2, 6, 20)).convert("RGBA")
    img = particles(img)
    d = ImageDraw.Draw(img)
    cx, cy = W // 2, 520

    # 头像光环
    for rr in range(170, 140, -2):
        al = int(40 + (170 - rr) * 3)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  outline=(90, 170, 255, al), width=2)
    # 头像内圆
    d.ellipse([cx - 130, cy - 130, cx + 130, cy + 130],
              fill=(10, 22, 54, 230), outline=(180, 220, 255, 220), width=4)
    f_av = font(78)
    av = "龙虾AI"
    tw = d.textlength(av, font=f_av)
    d.text((cx - tw / 2, cy - 50), av, font=f_av, fill=(255, 255, 255, 245))

    # 顶部标题
    f_t = font(76)
    title = "我是汤哥的AI分身"
    tw = d.textlength(title, font=f_t)
    d.text((cx - tw / 2, 150), title, font=f_t, fill=(255, 255, 255, 248))
    f_s = font(36, bold=False)
    sub = "AI DIVISION · 龙虾AI主控中心"
    tw = d.textlength(sub, font=f_s)
    d.text((cx - tw / 2, 250), sub, font=f_s, fill=(150, 200, 255, 220))

    # 底部字幕条
    f_c = font(48)
    lines = wrap(d, TEXT, f_c, 1500)
    th = len(lines) * 64 + 40
    y0 = H - 200 - th // 2
    d.rounded_rectangle([cx - 820, y0, cx + 820, y0 + th], 22, fill=(8, 12, 30, 175))
    yy = y0 + 28
    for ln in lines:
        tw = d.textlength(ln, font=f_c)
        d.text((cx - tw / 2, yy), ln, font=f_c, fill=(255, 255, 255, 240))
        yy += 64

    out = os.path.join(WORK, "frame.png")
    img.convert("RGB").save(out)
    return out

async def gen_audio():
    out = os.path.join(WORK, "audio.mp3")
    c = edge_tts.Communicate(TEXT, VOICE, rate=RATE)
    with open(out, "wb") as fd:
        async for ch in c.stream():
            if ch["type"] == "audio":
                fd.write(ch["data"])
    return out

def dur(path):
    s = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "default=noprint_wrappers=1",
                        path], capture_output=True, text=True).stdout.strip()
    return float(s.split("=")[-1])

def render(frame, audio):
    adur = dur(audio)
    n = max(int(adur * FPS), 1)
    out = os.path.join(WORK, "agent_video.mp4")
    vf = (f"zoompan=z='min(1.0+0.0006*on,1.12)':d={n}:"
          f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},"
          f"fade=t=in:st=0:d=0.5,fade=t=out:st={adur-1:.2f}:d=1.0")
    cmd = ["ffmpeg", "-y", "-loop", "1", "-i", frame, "-i", audio,
           "-vf", vf, "-shortest",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
           "-ar", "44100", "-ac", "2", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    return out, adur

if __name__ == "__main__":
    fr = build_frame()
    print("frame:", fr)
    au = asyncio.run(gen_audio())
    print("audio:", au)
    out, adur = render(fr, au)
    print("VIDEO:", out, "dur=%.2fs" % adur)
