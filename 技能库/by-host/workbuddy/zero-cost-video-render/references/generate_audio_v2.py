# -*- coding: utf-8 -*-
"""按分镜逐段生成 edge-tts 配音 + SRT 字幕（edge-tts 7.x 兼容版）"""
import asyncio
import os
import edge_tts

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-15%"
TEXT = open("narration.txt", encoding="utf-8").read().strip().split("\n")
os.makedirs("audio", exist_ok=True)
os.makedirs("srt", exist_ok=True)


async def gen(i: int, text: str):
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
    for i, t in enumerate(TEXT):
        print(f"[{i}] {t}")
        await gen(i, t)
    print("DONE")


asyncio.run(main())
