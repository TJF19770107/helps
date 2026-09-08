#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_avatar_snapshot.py · AI分身 轻量快照 + 回滚说明（<20MB）
==================================================
打包分身实体核心 + 看图技能 + 关键配置，时间戳命名，供故障后一键回滚。
用法：python make_avatar_snapshot.py
"""
import os
import sys
import zipfile
from datetime import datetime

ENT = r"E:\龙虾AI主控中心\我的AI分身\AI分身实体"
SCRIPTS = os.path.dirname(os.path.abspath(__file__))
SKILL = r"E:\龙虾AI主控中心\我的AI分身\技能库\lobster_see_screen\SKILL.md"
CFG = r"C:\Users\Administrator\.codex\config.toml"

ITEMS = [
    os.path.join(ENT, "SOUL.md"),
    os.path.join(ENT, "avatar.py"),
    os.path.join(ENT, "nvidia_avatar.py"),
    os.path.join(ENT, "CLAUDE.md"),
    os.path.join(ENT, "README.md"),
    os.path.join(ENT, "启动AI分身.bat"),
    os.path.join(ENT, "启动AI分身_NVIDIA.bat"),
    os.path.join(SCRIPTS, "vision_read.py"),
    os.path.join(SCRIPTS, "capture_and_read.py"),
    os.path.join(SCRIPTS, "make_avatar_snapshot.py"),
    SKILL,
    CFG,
]

OUT = r"E:\龙虾AI主控中心\我的AI分身\AI分身实体\snapshots"
os.makedirs(OUT, exist_ok=True)
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
zip_path = os.path.join(OUT, "avatar_snapshot_%s.zip" % ts)

packed, missing = [], []
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for p in ITEMS:
        if os.path.exists(p):
            zf.write(p, os.path.basename(p))
            packed.append(os.path.basename(p))
        else:
            missing.append(p)

size_mb = os.path.getsize(zip_path) / 1024 / 1024
print("快照:", zip_path)
print("大小: %.2f MB (限制 20MB)" % size_mb)
print("打包 %d 个文件:" % len(packed))
for p in packed:
    print("  -", p)
if missing:
    print("缺失 %d (跳过):" % len(missing))
    for m in missing:
        print("  -", m)
print("符合<20MB:" , "是" if size_mb <= 20 else "否")

restore = os.path.join(OUT, "RESTORE_%s.md" % ts)
with open(restore, "w", encoding="utf-8") as f:
    f.write("# 回滚说明 - %s\n\n" % ts)
    f.write("快照: %s\n\n" % zip_path)
    f.write("## 回滚步骤（PowerShell）\n\n")
    f.write("```powershell\n")
    f.write("# 1. 解压快照到临时目录\n")
    f.write("Expand-Archive -Path '%s' -DestinationPath 'C:\\tmp\\avatar_restore' -Force\n\n" % zip_path)
    f.write("# 2. 按需覆盖对应路径（先备份现状再覆盖，可逆）\n")
    f.write("Copy-Item 'C:\\tmp\\avatar_restore\\*' 'E:\\龙虾AI主控中心\\我的AI分身\\AI分身实体\\' -Recurse -Force\n")
    f.write("Copy-Item 'C:\\tmp\\avatar_restore\\vision_read.py','C:\\tmp\\avatar_restore\\capture_and_read.py','C:\\tmp\\avatar_restore\\make_avatar_snapshot.py' 'E:\\龙虾AI主控中心\\我的AI分身\\企业微信群定制接单项目\\scripts\\' -Force\n")
    f.write("```\n\n")
    f.write("> 原则：回滚前先备份现状；本快照只含轻量配置/脚本，不含日志/数据库/缓存。\n")
print("回滚说明:", restore)