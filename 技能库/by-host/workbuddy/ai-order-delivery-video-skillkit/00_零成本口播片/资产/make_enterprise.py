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

# 企业培训/口播样片脚本（8段，约90秒，0积分）
SEG = [
    ("01 · 企业AI分身 · 第一课",
     ["不是聊天机器人", "是带心理画像的数字员工"],
     "欢迎来到企业AI分身第一课，我是你的数字员工，替你干活的分身。"),
    ("02 · 它有什么",
     ["大脑：大模型推理", "手脚：自动化执行", "技能库：200+ 角色能力"],
     "它由大脑、手脚和技能库三部分组成，既能思考也能自动执行。"),
    ("03 · 第二大脑 · 四库",
     ["Obsidian 知识库", "IMA 即时检索", "乐享 团队共享"],
     "它还连着四库作为第二大脑，Obsidian、IMA、乐享，记忆永不丢失。"),
    ("04 · 怎么干活",
     ["接单→拆解→执行→交付", "龙虾五步法闭环", "全程零手动干预"],
     "按下龙虾五步法，从接单、拆解、执行到交付，全自动闭环。"),
    ("05 · 成本优势",
     ["口播课件：零积分", "真生成视频：按量计费", "成本前置进报价"],
     "口播课件零成本，真生成视频按量计费，每一分成本都前置到报价里。"),
    ("06 · 能接什么单",
     ["企业培训 / 科普", "产品介绍 / 口播", "数据盘点 / 批量混剪"],
     "企业培训、产品介绍、数据盘点、批量混剪，这些单我们都能接。"),
    ("07 · 交付标准",
     ["1080P 立体声", "字幕 + 封面", "源文件入知识库"],
     "交付标准统一：1080P立体声、带字幕封面、源文件全部进知识库。"),
    ("08 · 现在开始",
     ["把需求发给我", "我出脚本 + 报价", "确认即开干"],
     "把需求发过来，我出脚本和报价单，你确认，我立刻开干。"),
]

def font(sz, bold=True):
    return ImageFont.truetype(FONT_BD if bold else FONT_RG, sz)

def vgrad(top, bot):
    img = Image.new("RGB", (W, H))
    for y in range(H):
        t = y / H
        img.putpixel((0, y), tuple(int(a + (b - a) * t) for a, b in zip(top, bot)))
    return img

def particles(img, n=60, seed=11):
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

def build_frame(i, title, bullets, caption):
    img = vgrad((8, 16, 42), (2, 6, 20)).convert("RGBA")
    img = particles(img, seed=11 + i)
    d = ImageDraw.Draw(img)
    cx = W // 2

    # 左侧编号大色块
    d.rounded_rectangle([120, 150, 320, 350], 24, fill=(20, 40, 90, 200),
                        outline=(120, 180, 255, 200), width=3)
    fnum = font(120)
    d.text((150, 165), title.split(" · ")[0], font=fnum, fill=(180, 220, 255, 240))

    # 标题
    f_t = font(70)
    tt = title.split(" · ")[-1]
    tw = d.textlength(tt, font=f_t)
    d.text((360, 195), tt, font=f_t, fill=(255, 255, 255, 248))

    # 分隔线
    d.line([120, 400, W - 120, 400], fill=(90, 150, 255, 160), width=3)

    # 要点
    f_b = font(52)
    y = 470
    for b in bullets:
        d.ellipse([140, y + 14, 160, y + 34], fill=(255, 215, 130, 230))
        bw = d.textlength(b, font=f_b)
        d.text((190, y), b, font=f_b, fill=(225, 238, 255, 240))
        y += 90

    # 底部字幕条
    f_c = font(44)
    lines = wrap(d, caption, f_c, 1500)
    th = len(lines) * 60 + 40
    y0 = H - 170 - th // 2
    d.rounded_rectangle([cx - 830, y0, cx + 830, y0 + th], 22, fill=(8, 12, 30, 178))
    yy = y0 + 26
    for ln in lines:
        tw = d.textlength(ln, font=f_c)
        d.text((cx - tw / 2, yy), ln, font=f_c, fill=(255, 255, 255, 240))
        yy += 60

    out = os.path.join(WORK, f"frame_{i:02d}.png")
    img.convert("RGB").save(out)
    return out

async def gen_audio(i, text):
    out = os.path.join(WORK, f"audio_{i:02d}.mp3")
    c = edge_tts.Communicate(text, VOICE, rate=RATE)
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

def render(frames, audios):
    N = len(frames)
    adur = [dur(a) for a in audios]
    BUF, XF = 1.0, 0.5
    durs = [a + BUF for a in adur]
    total = sum(durs) - XF * (N - 1)

    fc = []
    for i in range(N):
        n = int(durs[i] * FPS)
        z = f"min(1.0+0.0006*on,1.10)" if i % 2 == 0 else f"max(1.10-0.0006*on,1.0)"
        fc.append(f"[{i}:v]zoompan=z='{z}':d={n}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS}[v{i}];")
    offs = []
    for i in range(N - 1):
        offs.append(sum(durs[:i + 1]) - XF * (i + 1))
    cur = "v0"
    for i in range(N - 1):
        fc.append(f"[{cur}][v{i+1}]xfade=transition=fade:duration={XF}:offset={offs[i]:.3f}[x{i+1}];")
        cur = f"x{i+1}"
    fc.append(f"[{cur}]fade=t=out:st={total-1.5:.3f}:duration=1.5[vout];")
    for i in range(N):
        start = sum(durs[:i]) - XF * i + 0.15
        ms = int(start * 1000)
        fc.append(f"[{N+i}:a]adelay={ms}|{ms}[a{i}];")
    fc.append(f"{''.join(f'[a{i}]' for i in range(N))}amix=inputs={N}:normalize=0,pan=stereo|c0=c0|c1=c0,loudnorm=I=-16:TP=-2.0,aresample=44100[aout]")

    cmd = (["ffmpeg", "-y"]
           + [x for i in range(N) for x in ("-i", frames[i])]
           + [x for i in range(N) for x in ("-i", audios[i])]
           + ["-filter_complex", "".join(fc),
              "-map", "[vout]", "-map", "[aout]",
              "-t", f"{total:.3f}",
              "-c:v", "libx264", "-preset", "medium", "-crf", "20",
              "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
              "-ar", "44100", "-ac", "2", "-movflags", "+faststart",
              os.path.join(WORK, "agent_video_enterprise_sample.mp4")])
    subprocess.run(cmd, check=True)
    return total

if __name__ == "__main__":
    frames, audios = [], []
    for i, (t, b, c) in enumerate(SEG):
        frames.append(build_frame(i, t, b, c))
        audios.append(asyncio.run(gen_audio(i, c)))
        print(f"[{i}] {t} -> {c}")
    total = render(frames, audios)
    print("ENTERPRISE SAMPLE:", os.path.join(WORK, "agent_video_enterprise_sample.mp4"), "dur=%.2fs" % total)
