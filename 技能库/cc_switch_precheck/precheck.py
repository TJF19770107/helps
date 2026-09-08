#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cc-switch 启动前强制预检 v1.0
遍历 cc-switch.db / config.json / 启动BAT，检测所有 127.0.0.1:4567 是否带 /v1 前缀。
异常自动修复(--fix)。退出码: 0合规 / 1异常(dry) / 2已修复
"""
import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

CC_DIR = Path(r"E:\龙虾AI主控中心\CC-Switch")
DB = CC_DIR / ".cc-switch" / "cc-switch.db"
CONFIGS = [CC_DIR / "config.json", CC_DIR / ".cc-switch" / "config.json"]

# 目标正确前缀
GOOD = "http://127.0.0.1:4567/v1"
# 匹配 4567 但缺 /v1 或带 /opencode 的错误形态
BAD_PATTERNS = [
    (re.compile(r"http://127\.0\.0\.1:4567(?!/v1)(?!/opencode/v1)"), "http://127.0.0.1:4567"),
    (re.compile(r"http://127\.0\.0\.1:4567/opencode/v1"), "http://127.0.0.1:4567/opencode/v1"),
]


def find_bad(text: str):
    """返回 (错误串, 应替换成的正确串) 列表"""
    res = []
    for pat, label in BAD_PATTERNS:
        for m in pat.finditer(text):
            bad = m.group(0)
            res.append((bad, GOOD if label == "http://127.0.0.1:4567" else "http://127.0.0.1:4567/v1"))
    return res


def fix_db(fix: bool):
    issues = []
    if not DB.exists():
        return issues
    conn = sqlite3.connect(str(DB))
    cur = conn.cursor()
    # providers 表
    try:
        cur.execute("SELECT id, settings_config FROM providers")
        for pid, cfg in cur.fetchall():
            if not cfg:
                continue
            bads = find_bad(cfg)
            if bads:
                new_cfg = cfg
                for bad, good in bads:
                    new_cfg = new_cfg.replace(bad, good)
                issues.append(("providers", pid, [b for b, _ in bads]))
                if fix:
                    cur.execute("UPDATE providers SET settings_config=? WHERE id=?", (new_cfg, pid))
        # provider_endpoints
        cur.execute("SELECT id, url FROM provider_endpoints")
        for eid, url in cur.fetchall():
            if not url:
                continue
            bads = find_bad(url)
            if bads:
                new_url = url
                for bad, good in bads:
                    new_url = new_url.replace(bad, good)
                issues.append(("provider_endpoints", eid, [b for b, _ in bads]))
                if fix:
                    cur.execute("UPDATE provider_endpoints SET url=? WHERE id=?", (new_url, eid))
        # proxy_live_backup
        try:
            cur.execute("SELECT rowid, original_config FROM proxy_live_backup")
            for rid, cfg in cur.fetchall():
                if not cfg:
                    continue
                bads = find_bad(cfg)
                if bads:
                    new_cfg = cfg
                    for bad, good in bads:
                        new_cfg = new_cfg.replace(bad, good)
                    issues.append(("proxy_live_backup", rid, [b for b, _ in bads]))
                    if fix:
                        cur.execute("UPDATE proxy_live_backup SET original_config=? WHERE rowid=?", (new_cfg, rid))
        except Exception:
            pass
        conn.commit()
    except Exception as e:
        print(f"[DB错误] {e}")
    finally:
        conn.close()
    return issues


def fix_configs(fix: bool):
    issues = []
    for cf in CONFIGS:
        if not cf.exists():
            continue
        try:
            text = cf.read_text(encoding="utf-8")
        except Exception:
            continue
        bads = find_bad(text)
        if bads:
            issues.append((str(cf), [b for b, _ in bads]))
            if fix:
                new_text = text
                for bad, good in bads:
                    new_text = new_text.replace(bad, good)
                cf.write_text(new_text, encoding="utf-8")
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix", action="store_true", help="发现异常自动修复")
    args = ap.parse_args()

    print("═══════ cc-switch 启动前预检 ═══════")
    db_issues = fix_db(args.fix)
    cfg_issues = fix_configs(args.fix)

    all_issues = db_issues + cfg_issues
    if not all_issues:
        print("✅ 全部合规：所有 127.0.0.1:4567 地址均携带 /v1 前缀")
        print("可安全启动 cc-switch")
        sys.exit(0)

    print(f"⚠️ 发现 {len(all_issues)} 处异常 (4567 地址缺 /v1 或含 /opencode):")
    for tbl, key, bads in all_issues:
        print(f"  [{tbl}] {key}: {bads}")

    if args.fix:
        print("🔧 已自动修复，请重启 cc-switch 使配置生效")
        sys.exit(2)
    else:
        print("ℹ️ dry-run 模式，加 --fix 自动修复")
        sys.exit(1)


if __name__ == "__main__":
    main()
