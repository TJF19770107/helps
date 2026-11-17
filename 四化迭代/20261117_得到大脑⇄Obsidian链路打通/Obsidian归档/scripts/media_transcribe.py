# -*- coding: utf-8 -*-
"""
media_transcribe.py —— 本机语音转文字链路（v1.0.0）

事实依据（不臆造）：
  - ffmpeg 已装: C:/ProgramData/chocolatey/bin/ffmpeg.exe
  · faster-whisper 1.2.1 已装（本地推理，零 API 费用）
  · 模型走 HF 镜像 HF_ENDPOINT=https://hf-mirror.com（直连 huggingface.co 被代理 502 拦）

流程：视频/音频 → ffmpeg 抽音轨(16k 单声道 wav) → faster-whisper 转写
      → 落盘 Obsidian「语音转写素材」→ 可选切「待回写得到大脑」

用法：
  python media_transcribe.py --model small --lang zh <媒体路径或URL>
  python media_transcribe.py --probe          # 体检：ffmpeg/whisper/模型缓存
"""
import os, sys, json, time, argparse, subprocess, tempfile, datetime, hashlib, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

sys.stdout.reconfigure(encoding="utf-8")

TRANSCRIPT_DIR = "P07_博主学习库（D盘+E盘）/02_产物归档/语音转写素材"
PENDING_DIR = "02_产物归档/待回写得到大脑"
FFMPEG = r"C:\ProgramData\chocolatey\bin\ffmpeg.exe"
HF_ENDPOINT = "https://hf-mirror.com"


def ffmpeg_bin():
    if os.path.exists(FFMPEG):
        return FFMPEG
    from shutil import which
    w = which("ffmpeg")
    if w:
        return w
    raise RuntimeError("找不到 ffmpeg。本机应在 C:\\ProgramData\\chocolatey\\bin\\ffmpeg.exe")


def probe():
    print("=== 语音转文字链路 · 体检 ===")
    ok = True
    try:
        b = ffmpeg_bin()
        r = subprocess.run([b, "-version"], capture_output=True, text=True, encoding="utf-8", errors="ignore")
        v = (r.stdout or "").splitlines()[0] if r.stdout else "?"
        print(f"  ✅ ffmpeg: {b}")
        print(f"     {v}")
    except Exception as e:
        print(f"  ❌ ffmpeg: {e}")
        ok = False

    try:
        import faster_whisper
        print(f"  ✅ faster-whisper {getattr(faster_whisper, '__version__', '?')}")
    except Exception as e:
        print(f"  ❌ faster-whisper 未装: {e}")
        ok = False

    cache = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub")
    print(f"  模型缓存: {cache}")
    if os.path.isdir(cache):
        for d in sorted(os.listdir(cache)):
            if "whisper" in d.lower():
                print(f"     📦 {d}")
    else:
        print("     （首次使用会自动下载，需 HF_ENDPOINT 镜像）")

    print(f"\n  结论: {'✅ 链路就绪' if ok else '❌ 有缺失项'}")
    return 0 if ok else 1


def extract_audio(src, workdir=None):
    """抽音轨 → 16k 单声道 wav"""
    tmpd = workdir or tempfile.mkdtemp(prefix="transcribe_")
    os.makedirs(tmpd, exist_ok=True)
    out = os.path.join(tmpd, "audio.wav")
    cmd = [ffmpeg_bin(), "-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000",
           "-acodec", "pcm_s16le", out]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    if not os.path.exists(out) or os.path.getsize(out) < 1000:
        raise RuntimeError(f"ffmpeg 抽音轨失败:\n{(r.stderr or '')[-800:]}")
    return out


def transcribe(src, model_size="small", lang="zh", compute="int8"):
    """转写，返回 (text, segments, elapsed)"""
    os.environ.setdefault("HF_ENDPOINT", HF_ENDPOINT)
    from faster_whisper import WhisperModel
    t0 = time.time()
    print(f"  加载模型 {model_size} (device=cpu, compute={compute}) ...")
    model = WhisperModel(model_size, device="cpu", compute_type=compute)
    print(f"  模型就绪 {time.time()-t0:.1f}s")
    print(f"  抽音轨 ...")
    wav = extract_audio(src)
    print(f"  音频: {os.path.getsize(wav)/1024/1024:.1f} MB")
    t1 = time.time()
    segments, info = model.transcribe(wav, language=lang, vad_filter=True,
                                      beam_size=5)
    segs = []
    print("  转写中 ...")
    for s in segments:
        segs.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()})
        print(f"    [{s.start:7.2f}s] {s.text.strip()[:80]}")
    text = "\n".join(s["text"] for s in segs)
    return text, segs, {"model": model_size, "lang": info.language,
                        "duration": round(info.duration, 2), "elapsed": round(time.time() - t1, 1)}


def save_to_obsidian(text, segs, meta, title=None):
    from obsidian_rest import ObsidianRest
    ob = ObsidianRest()
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fn = f"{ts}_{re.sub(r'[\\\\/:*?\"<>|]', '_', title or meta.get('source', 'transcript'))[:50]}.md"
    rel = TRANSCRIPT_DIR + "/" + fn
    body = []
    body.append(f"**来源**：{meta.get('source','')}")
    body.append(f"**转写时间**：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    body.append(f"**模型**：faster-whisper {meta.get('model')} / 语言 {meta.get('lang')} / 时长 {meta.get('duration')}s / 耗时 {meta.get('elapsed')}s")
    body.append("")
    body.append("## 全文")
    body.append("")
    body.append(text)
    body.append("")
    body.append("## 分段时间轴")
    body.append("")
    for s in segs:
        body.append(f"- `{s['start']:.2f}s → {s['end']:.2f}s` {s['text']}")
    body.append("")
    body.append("---")
    body.append("")
    body.append("## 四化拆解待办")
    body.append("- [ ] 提炼金句 / 钩子结构")
    body.append("- [ ] 转成可对标脚本模板")
    body.append("- [ ] 存入待回写队列推向得到大脑")
    content = "\n".join(body) + "\n"
    st, disk = ob.write(rel, content)
    ok = os.path.exists(disk) and len(text) > 0
    return ok, rel, disk, ob


def main():
    ap = argparse.ArgumentParser(description="本机语音转文字（faster-whisper）")
    ap.add_argument("media", nargs="?", help="本地音视频路径")
    ap.add_argument("--probe", action="store_true", help="体检")
    ap.add_argument("--model", default="small", help="tiny/base/small/medium/large-v3")
    ap.add_argument("--lang", default="zh")
    ap.add_argument("--title", default="")
    ap.add_argument("--no-save", action="store_true", help="只转写不落盘")
    args = ap.parse_args()

    if args.probe:
        return probe()
    if not args.media:
        ap.print_help()
        return 1

    src = args.media
    if not os.path.exists(src):
        print(f"❌ 文件不存在: {src}")
        return 1

    print(f"=== 语音转文字 ===\n源: {src}")
    text, segs, meta = transcribe(src, args.model, args.lang)
    meta["source"] = src
    print(f"\n  完成: {len(segs)} 段 / {len(text)} 字 / 耗时 {meta['elapsed']}s")

    if args.no_save:
        print("\n" + text[:2000])
        return 0

    ok, rel, disk, ob = save_to_obsidian(text, segs, meta, args.title)
    print(f"\n  {'✅' if ok else '❌'} 落盘: {rel}")
    print(f"     磁盘: {disk}")
    print(f"     字节 {os.path.getsize(disk)} B  sha {ob.disk_sha(rel)[:16]}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
