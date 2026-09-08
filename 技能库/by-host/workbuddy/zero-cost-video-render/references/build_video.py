# -*- coding: utf-8 -*-
"""
零积分短视频渲染：PIL 绘制 6 分镜画面 + FFmpeg zoompan/xfade/amix 合成
输出: agent_video_20260819.mp4
"""
import math
import os
import random
import subprocess
import sys

import edge_tts  # noqa
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE)
W, H = 1920, 1080
FPS = 25
FONT_BD = "C:/Windows/Fonts/msyhbd.ttc"
FONT_RG = "C:/Windows/Fonts/msyh.ttc"
FONT_EL = "C:/Windows/Fonts/msyhl.ttc" if os.path.exists("C:/Windows/Fonts/msyhl.ttc") else FONT_RG

NARR = open("narration.txt", encoding="utf-8").read().strip().split("\n")
AUD_DUR = []  # 各段音频时长
for i in range(6):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1", f"audio/seg{i}.mp3"],
        capture_output=True, text=True)
    AUD_DUR.append(float(out.stdout.strip().split("=")[-1]))
print("音频时长:", AUD_DUR)


def font(sz, bold=True):
    return ImageFont.truetype(FONT_BD if bold else FONT_RG, sz)


def vgrad(rgb_top, rgb_bot):
    """垂直渐变背景"""
    top = Image.new("RGB", (1, H), rgb_top)
    bot = Image.new("RGB", (1, H), rgb_bot)
    grad = Image.blend(top, bot, 0.55)
    for y in range(H):
        t = y / H
        r = int(rgb_top[0] + (rgb_bot[0] - rgb_top[0]) * t)
        g = int(rgb_top[1] + (rgb_bot[1] - rgb_top[1]) * t)
        b = int(rgb_top[2] + (rgb_bot[2] - rgb_top[2]) * t)
        grad.putpixel((0, y), (r, g, b))
    return grad.resize((W, H))


def particles(img, n=46, seed=7):
    """漂浮粒子"""
    rnd = random.Random(seed)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for _ in range(n):
        x, y = rnd.randint(0, W), rnd.randint(0, H)
        r = rnd.uniform(0.8, 2.6)
        a = rnd.randint(30, 110)
        col = (120, 200, 255, a) if rnd.random() < 0.7 else (255, 215, 130, a)
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    img = img.convert("RGBA")
    img.alpha_composite(ov)
    return img


def neon_line(img, x0, y0, x1, y1, color=(80, 160, 255, 120), w=2):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ov).line([x0, y0, x1, y1], fill=color, width=w)
    img.alpha_composite(ov)


def caption(img, text, y=H - 180):
    """底部字幕条"""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    f = font(46)
    # 分两行
    lines = []
    cur = ""
    for ch in text:
        if d.textlength(cur + ch, font=f) > 1500:
            lines.append(cur)
            cur = ch
        else:
            cur += ch
    lines.append(cur)
    th = len(lines) * 62 + 36
    y0 = y - th // 2
    d.rounded_rectangle([W // 2 - 810, y0, W // 2 + 810, y0 + th], 22,
                        fill=(8, 12, 30, 168))
    yy = y0 + 30
    for ln in lines:
        tw = d.textlength(ln, font=f)
        d.text(((W - tw) / 2, yy), ln, font=f, fill=(255, 255, 255, 235))
        yy += 62
    img.alpha_composite(ov)


def card(img, x0, y0, x1, y1, title, sub, fill=(20, 40, 90, 215), tc=(255, 255, 255)):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rounded_rectangle([x0, y0, x1, y1], 28, fill=fill,
                        outline=(255, 255, 255, 60), width=2)
    d.text((x0 + 50, y0 + 46), title, font=font(52), fill=tc)
    d.text((x0 + 50, y0 + 132), sub, font=font(40), fill=(200, 215, 255, 220))
    img.alpha_composite(ov)


def text_on(img, xy, s, f, fill=(255, 255, 255)):
    ImageDraw.Draw(img).text(xy, s, font=f, fill=fill)


def seg0():
    img = vgrad((10, 15, 30), (26, 5, 51))
    img = particles(img, seed=11)
    d = ImageDraw.Draw(img)
    neon_line(img, 120, 260, W - 120, 260)
    neon_line(img, 120, 300, W - 120, 300, color=(255, 200, 90, 90))
    # 大模型(灰小) vs AI Agent(金大)
    text_on(img, (W - 900, 210), "大模型火了三年……", font(44))
    t1 = "AI Agent"
    f1 = font(150)
    tw = d.textlength(t1, font=f1)
    text_on(img, ((W - tw) / 2, 400), t1, f1, fill=(255, 210, 90))
    text_on(img, ((W - d.textlength("它凭什么？", font(72))) / 2, 620),
            "它凭什么？", font(72), fill=(255, 255, 255))
    text_on(img, ((W - d.textlength("—— 60 秒讲懂 AI Agent ——", font(40))) / 2, 760),
            "—— 60 秒讲懂 AI Agent ——", font(40), fill=(150, 180, 230))
    caption(img, NARR[0])
    return img


def seg1():
    img = vgrad((8, 16, 38), (20, 8, 60))
    img = particles(img, seed=23)
    d = ImageDraw.Draw(img)
    text_on(img, (W // 2 - 330, 90), "Agent 是怎么搭出来的？", font(58))
    cx = W // 2
    # 底层: 砖块
    d.rounded_rectangle([cx - 280, 780, cx + 280, 900], 12, fill=(96, 104, 120, 255))
    d.rectangle([cx - 280, 830, cx + 280, 900], fill=(80, 88, 104, 255))
    for bx in range(cx - 250, cx + 260, 90):
        d.rectangle([bx, 788, bx + 60, 826], outline=(130, 138, 155, 255), width=2)
    d.text((cx - 130, 802), "MCP · 砖", font=font(42), fill=(235, 240, 250))
    # 中层: 预制件
    d.rounded_rectangle([cx - 330, 560, cx + 330, 700], 16, fill=(58, 120, 220, 255))
    d.text((cx - 120, 595), "Skill · 预制件", font=font(46), fill=(255, 255, 255))
    # 顶层: 精装房
    d.polygon([(cx - 210, 430), (cx, 330), (cx + 210, 430)], fill=(255, 170, 60, 255))
    d.rectangle([cx - 170, 430, cx + 170, 560], fill=(120, 90, 210, 255))
    d.rectangle([cx - 40, 470, cx + 40, 560], fill=(40, 30, 80, 255))
    d.text((cx - 105, 478), "Agent", font=font(40), fill=(255, 240, 200))
    # 左侧竖箭头
    for yy in range(760, 620, -26):
        d.line([(cx - 460, yy), (cx - 460, yy - 20)], fill=(255, 210, 90, 255), width=5)
    d.polygon([(cx - 460, 600), (cx - 478, 630), (cx - 442, 630)], fill=(255, 210, 90, 255))
    d.text((cx - 560, 640), "层层搭建", font=font(36), fill=(255, 210, 90))
    caption(img, NARR[1])
    return img


def seg2():
    img = vgrad((10, 18, 34), (16, 10, 60))
    img = particles(img, seed=31)
    d = ImageDraw.Draw(img)
    text_on(img, (90, 80), "本周 GitHub · AI Agent 霸主", font(50))
    # 左: 星标
    fbig = font(150)
    d.text((150, 260), "★", font=font(190), fill=(255, 200, 60))
    text_on(img, (360, 290), "380,000", fbig, fill=(255, 255, 255))
    text_on(img, (360, 500), "OpenClaw 登顶 GitHub", font(56), fill=(255, 200, 60))
    text_on(img, (150, 640), "多智能体舰队，成最热赛道", font(44), fill=(200, 215, 255))
    # 右: 舰队编队节点
    nx, ny = 1350, 420
    pts = [(nx, ny), (nx + 210, ny - 130), (nx + 430, ny), (nx + 210, ny + 140),
           (nx + 105, ny + 60), (nx + 320, ny + 60)]
    for i, p in enumerate(pts[:4]):
        x, y = p
        d.ellipse([x - 26, y - 26, x + 26, y + 26], fill=(70, 140, 255, 255))
        d.text((x - 12, y - 20), str(i + 1), font=font(34), fill=(255, 255, 255))
    for a, b in [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (0, 4), (1, 5)]:
        d.line([pts[a], pts[b]], fill=(120, 180, 255, 150), width=3)
    d.text((nx + 40, ny + 200), "舰队编队", font=font(44), fill=(150, 200, 255))
    caption(img, NARR[2])
    return img


def seg3():
    img = vgrad((8, 18, 40), (24, 8, 52))
    img = particles(img, seed=41)
    d = ImageDraw.Draw(img)
    text_on(img, (W // 2 - 320, 80), "本周两大动作", font(56))
    # 左卡片: 支付宝 AHA
    card(img, 130, 240, 930, 800, "支付宝 AHA", "跨端互联 · 手机 → 汽车")
    d.rounded_rectangle([220, 430, 400, 660], 18, outline=(120, 200, 255, 220), width=4)
    d.line([400, 545, 620, 545], fill=(120, 200, 255, 255), width=5)
    d.rounded_rectangle([620, 430, 800, 660], 24, outline=(120, 200, 255, 220), width=4)
    d.ellipse([700, 600, 740, 640], fill=(255, 255, 255, 180))
    d.ellipse([660, 600, 700, 640], fill=(255, 255, 255, 180))
    d.text((300, 690), "手机", font=font(38), fill=(170, 210, 255))
    d.text((660, 690), "汽车", font=font(38), fill=(170, 210, 255))
    # 右卡片: Grok Bot
    card(img, 990, 240, 1790, 800, "Grok Bot", "自带云电脑的 AI 员工",
         fill=(70, 40, 130, 215), tc=(255, 225, 140))
    d.rounded_rectangle([1130, 420, 1560, 620], 14, fill=(18, 24, 50, 255),
                        outline=(180, 150, 255, 220), width=3)
    d.rectangle([1130, 620, 1560, 650], fill=(120, 100, 200, 255))
    d.text((1150, 460), "AI 员工", font=font(52), fill=(255, 255, 255))
    d.text((1150, 545), "Gmail · CRM · 网页", font=font(34), fill=(160, 180, 230))
    text_on(img, (850, 440), "VS", font(70), fill=(255, 210, 90))
    caption(img, NARR[3])
    return img


def seg4():
    img = vgrad((10, 20, 36), (30, 8, 40))
    img = particles(img, seed=51)
    d = ImageDraw.Draw(img)
    text_on(img, (W // 2 - 220, 80), "差距在哪？", font(58))
    # 左: 只会聊
    d.rounded_rectangle([180, 320, 820, 700], 30, fill=(70, 84, 110, 220))
    d.ellipse([240, 380, 440, 580], outline=(200, 215, 240, 255), width=6)
    d.rounded_rectangle([480, 380, 740, 500], 22, fill=(200, 215, 240, 255))
    d.text((500, 415), "只会聊", font=font(48), fill=(30, 40, 70))
    d.text((250, 760), "大模型", font=font(52), fill=(200, 215, 240))
    # 右: 能干活
    x0, y0 = 1010, 330
    items = [("干活", (255, 120, 90)), ("跨端", (120, 200, 255)), ("组队", (160, 255, 170))]
    for k, (lab, col) in enumerate(items):
        xx = x0 + k * 250
        d.ellipse([xx, y0, xx + 120, y0 + 120], fill=(col[0], col[1], col[2], 200))
        d.text((xx + 22, y0 + 34), lab, font=font(38), fill=(20, 25, 45))
    # 火苗
    fy = 620
    d.ellipse([x0 + 260, fy, x0 + 420, fy + 190], fill=(255, 120, 40, 255))
    d.ellipse([x0 + 300, fy - 70, x0 + 400, fy + 60], fill=(255, 190, 60, 255))
    d.text((x0 + 270, fy + 205), "更火", font=font(52), fill=(255, 210, 90))
    caption(img, NARR[4])
    return img


def seg5():
    img = vgrad((14, 22, 44), (30, 10, 56))
    img = particles(img, seed=61)
    d = ImageDraw.Draw(img)
    # Logo 圆环
    d.ellipse([W // 2 - 90, 150, W // 2 + 90, 330], outline=(255, 210, 90, 255), width=6)
    d.text((W // 2 - 46, 205), "凌导", font=font(56), fill=(255, 210, 90))
    text_on(img, ((W - d.textlength("关注我", font(130))) / 2, 420),
            "关注我", font(130), fill=(255, 255, 255))
    text_on(img, ((W - d.textlength("下期：手把手教你搭第一个 Agent", font(56))) / 2, 620),
            "下期：手把手教你搭第一个 Agent", font(56), fill=(200, 215, 255))
    d.text((W // 2 - 240, 780), "· 看懂 AI ·", font=font(40), fill=(150, 180, 230))
    caption(img, NARR[5])
    return img


def zoom_filter(idx, dur):
    """zoompan: 偶段 zoom-in，奇段 zoom-out，末段静止"""
    n = int(dur * FPS)
    if idx == 5:
        z = "1.0"
        x = "iw/2-(iw/zoom/2)"
        y = "ih/2-(ih/zoom/2)"
    elif idx % 2 == 0:
        z = f"min(1.0+0.00065*on,1.12)"
        x = "iw/2-(iw/zoom/2)"
        y = "ih/2-(ih/zoom/2)"
    else:
        z = f"max(1.12-0.00065*on,1.0)"
        x = "iw/2-(iw/zoom/2)"
        y = "ih/2-(ih/zoom/2)"
    return (f"zoompan=z='{z}':d={n}:x='{x}':y='{y}':s={W}x{H}:fps={FPS}")


def build():
    # 1) 画帧
    frames = [seg0(), seg1(), seg2(), seg3(), seg4(), seg5()]
    os.makedirs("frames", exist_ok=True)
    for i, fr in enumerate(frames):
        fr.convert("RGB").save(f"frames/seg{i}.png")
        print(f"frame seg{i}.png saved")

    # 2) 时长规划: 画面 = 音频 + 1.2s 缓冲
    BUF = 1.2
    XF = 0.5
    durs = [a + BUF for a in AUD_DUR]
    total = sum(durs) - XF * 5
    print("各段画面时长:", [round(x, 2) for x in durs], "总长:", round(total, 2))

    # 3) ffmpeg filter_complex
    inputs = []
    for i in range(6):
        inputs += ["-i", f"frames/seg{i}.png"]
    for i in range(6):
        inputs += ["-i", f"audio/seg{i}.mp3"]

    fc = []
    for i in range(6):
        fc.append(f"[{i}:v]{zoom_filter(i, durs[i])}[v{i}];")
    # xfade 链
    offs = []
    acc = 0
    for i in range(5):
        acc += durs[i]
        offs.append(acc - XF * (i + 1))
    cur = "v0"
    for i in range(5):
        fc.append(f"[{cur}][v{i + 1}]xfade=transition=fade:duration={XF}:offset={offs[i]:.3f}[x{i + 1}];")
        cur = f"x{i + 1}"
    fc.append(f"[{cur}]fade=t=out:st={total - 1.5:.3f}:duration=1.5[vout];")
    # 音频延迟+混音
    ast = []
    for i in range(6):
        start = (sum(durs[:i]) - XF * i) + 0.15
        ms = int(start * 1000)
        fc.append(f"[{6 + i}:a]adelay={ms}|{ms}[a{i}];")
        ast.append(f"[a{i}]")
    # 四化·自我净化+兼容性: 单声道TTS -> 立体声 + 44.1k + 响度归一化(避免部分蓝牙耳麦无声)
    fc.append(f"{''.join(ast)}amix=inputs=6:normalize=0,pan=stereo|c0=c0|c1=c0,loudnorm=I=-16:TP=-2.0,aresample=44100[aout]")

    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", "".join(fc),
        "-map", "[vout]", "-map", "[aout]",
        "-t", f"{total:.3f}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        "-movflags", "+faststart",
        "agent_video_20260819.mp4",
    ]
    print(">>> ffmpeg 渲染中（预计 1-3 分钟）...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG FAIL:", r.stderr[-3000:])
        sys.exit(1)
    print("FFMPEG OK")
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration,size:stream=codec_name,width,height",
         "-of", "json", "agent_video_20260819.mp4"],
        capture_output=True, text=True)
    print(out.stdout)


if __name__ == "__main__":
    build()
