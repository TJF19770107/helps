"""口播样片 #3：AI分身·产品发布会风格（30秒，强音轨，0积分）"""
import subprocess, os, asyncio, edge_tts, random
from PIL import Image, ImageDraw, ImageFont

OUT = r"E:\龙虾AI主控中心\我的AI分身\豆包主会话全集\AI分身出片"
os.chdir(OUT)

# ============ 主题文案（8段，每段配独立画面） ============
# 这是"产品发布会"风的口播样片，对应接单群里要的1分钟里最常见的"产品介绍"
TITLE = "AI 分身·发布会"
SUB = "零积分出片·接单实测样片 #3"
SEGMENTS = [
    "各位老板、同事、合作伙伴们，大家好。我是AI分身汤小虾。",
    "今天发布我们的接单出片产品：零积分口播视频生产线。",
    "全程 edge-tts 免费配音，加 Pillow 高品质画面，再上 FFmpeg 推镜。",
    "一分钟内交付，立体声四万四千赫兹，蓝牙耳麦直接听。",
    "不烧积分，不烧云服务，不烧云端GPU，纯本地三件套。",
    "覆盖企业内训、产品介绍、数据盘点、营销矩阵全部场景。",
    "接单群里那一到两分钟的需求，咱们零积分就能交付。",
    "这是接单出片大技能库，第一条产品发布会样片演示。谢谢。",
]
TOTAL = 30  # 目标 30 秒（够 5–10 秒分段，也够接单样片用）

# ============ 文案→音频（edge-tts 免费） ============
async def make_audio():
    audios = []
    for i, text in enumerate(SEGMENTS):
        voice = "zh-CN-XiaoxiaoNeural"  # 中文女声，免费
        speed = "-15%"  # 略慢更专业
        path = f"audio_p{i}.mp3"
        comm = edge_tts.Communicate(text, voice, rate=speed)
        await comm.save(path)
        # 测时长
        r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1", path],
                           capture_output=True, text=True)
        d = float(r.stdout.strip())
        print(f"  P{i}: {d:.2f}s  {text[:18]}...")
        audios.append((path, d))
    return audios

# ============ 静态帧（Pillow·深蓝科技风） ============
def make_frame(idx, text, out_path):
    W, H = 1920, 1080
    img = Image.new("RGB",(W,H),(8,12,28))
    draw = ImageDraw.Draw(img)

    # 深蓝径向渐变（蓝→黑）
    for y in range(H):
        t = y/H
        r = int(8*(1-t) + 3*t)
        g = int(16*(1-t) + 8*t)
        b = int(48*(1-t) + 22*t)
        draw.line([(0,y),(W,y)], fill=(r,g,b))

    # 随机粒子光点
    random.seed(idx*73+11)
    for _ in range(180):
        x = random.randint(0,W); y = random.randint(0,H)
        r = random.randint(1,3); a = random.randint(60,180)
        draw.ellipse([x-r,y-r,x+r,y+r], fill=(0,180+a//2,255-a//3))

    # 顶部装饰条
    draw.rectangle([0,0,W,10], fill=(0,200,255))
    # 标题
    try:
        font_title = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 84)
        font_sub = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 38)
        font_main = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 58)
        font_seg = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 32)
    except Exception:
        font_title = ImageFont.load_default(); font_sub=font_title; font_main=font_title; font_seg=font_title

    draw.text((80, 90), TITLE, fill=(255,255,255), font=font_title)
    draw.text((84, 198), SUB, fill=(140,200,240), font=font_sub)

    # 段号块
    draw.rounded_rectangle([80,280,260,360], radius=12, fill=(0,140,200))
    draw.text((130,295), f"P{idx+1:02d}", fill=(255,255,255), font=font_seg)

    # 主文案（自动换行）
    text = text.strip()
    lines, cur = [], ""
    for ch in text:
        cur += ch
        if len(cur) >= 18:
            lines.append(cur); cur=""
    if cur: lines.append(cur)
    y = 420
    for line in lines:
        draw.text((80, y), line, fill=(245,250,255), font=font_main)
        y += 90

    # 字幕条
    draw.rounded_rectangle([60, H-150, W-60, H-90], radius=16,
                            fill=(20,40,80))
    draw.text((90, H-130), f"AI 分身 · 接单出片 · 段 {idx+1}/{len(SEGMENTS)}",
              fill=(180,220,255), font=font_seg)

    img.save(out_path, "PNG", optimize=True)
    return out_path

# ============ 合成（FFmpeg：画面 + 音频，+faststart，立体声） ============
def synth(audios, total_sec):
    n = len(audios)
    # 每段按音频时长+0.3s间隔分配，但总时长目标 total_sec
    per = total_sec / n
    parts = []
    for i,(apath,_) in enumerate(audios):
        fpath = f"frame_p{i}.png"
        make_frame(i, SEGMENTS[i], fpath)
        seg_dur = max(per - 0.4, 3.0)
        out = f"seg_p{i}.mp4"
        cmd = [
            "ffmpeg","-y","-loop","1","-i",fpath,"-i",apath,
            "-t", f"{seg_dur:.3f}",
            "-vf", f"zoompan=z='min(zoom+0.0005,1.08)':d=25:s=1920x1080:fps=24",
            "-c:v","libx264","-preset","medium","-crf","22","-tune","stillimage",
            "-c:a","aac","-b:a","192k","-ar","44100","-ac","2",
            "-shortest","-pix_fmt","yuv420p", out
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode!=0:
            print("SEG ERR:", r.stderr[-500:]); return None
        parts.append(out)
    # concat
    listf = "_concat_p.txt"
    with open(listf,"w",encoding="utf-8") as f:
        for p in parts: f.write(f"file '{p}'\n")
    final = "agent_video_koubo_sample3_20260826.mp4"
    cmd = ["ffmpeg","-y","-f","concat","-safe","0","-i",listf,
           "-c:v","libx264","-preset","medium","-crf","22",
           "-c:a","aac","-b:a","192k","-ar","44100","-ac","2",
           "-movflags","+faststart", final]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode!=0:
        print("FINAL ERR:", r.stderr[-500:]); return None
    return final

# ============ 主流程 ============
async def main():
    print("=== 1) 出 8 段口播音频 ===")
    audios = asyncio.run(make_audio()) if False else await make_audio()
    print("=== 2) 出 8 段画面 + 合成 ===")
    final = synth(audios, TOTAL)
    if final:
        # 强封一次（保险音轨）
        strong = "agent_video_koubo_sample3_20260826_有声强封.mp4"
        cmd = ["ffmpeg","-y","-i",final,
               "-c:v","libx264","-preset","medium","-crf","22",
               "-c:a","aac","-b:a","192k","-ar","44100","-ac","2",
               "-movflags","+faststart","-shortest", strong]
        subprocess.run(cmd, capture_output=True)
        print(">>> 最终产物:", strong)
        # 抽帧
        for t in [3,12,22]:
            subprocess.run(["ffmpeg","-y","-v","error","-ss",str(t),"-i",strong,
                            "-frames:v","1", f"qc_p{t}.png"], capture_output=True)
    else:
        print("合成失败")

if __name__ == "__main__":
    asyncio.run(main())
