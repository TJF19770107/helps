# -*- coding: utf-8 -*-
"""Binance kline incremental updater.

Public market data only; no API key required.
Timestamps on disk are UTC+8 strings matching the existing CSVs.
"""

import argparse
import json
import csv
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

TZ8 = timezone(timedelta(hours=8))
HEADERS = ["timestamp", "open", "high", "low", "close", "volume",
           "close_time", "quote_volume", "trades", "taker_buy_volume",
           "taker_buy_quote_volume"]
BASE_URLS = {
    "spot": "https://api.binance.com/api/v3/klines",
    "futures": "https://fapi.binance.com/fapi/v1/klines",
}
INTERVAL_MS = {"1m": 60_000, "5m": 300_000, "15m": 900_000, "1h": 3_600_000,
               "4h": 14_400_000, "1d": 86_400_000}
# 数据目录历史命名用 15min/1h 这类标签，和币安 interval 参数解耦
INTERVAL_LABEL = {"1m": "1min", "5m": "5min", "15m": "15min", "1h": "1h",
                  "4h": "4h", "1d": "1d"}


def fetch(symbol: str, interval: str, market: str, start_ms: int, proxy: str = "", retries: int = 3):
    url = (f"{BASE_URLS[market]}?symbol={symbol}&interval={interval}"
           f"&startTime={start_ms}&limit=1000")
    cmd = ["curl.exe", "-s", "-m", "30", url]
    if proxy:
        cmd[2:2] = ["-x", proxy]
    for attempt in range(retries):
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=40)
            if proc.returncode == 0 and proc.stdout.strip():
                return proc.stdout
            raise RuntimeError(f"curl exit {proc.returncode} {proc.stderr.strip()}")
        except Exception as exc:
            if attempt == retries - 1:
                raise
            print(f"  重试 {attempt + 1}: {exc}")
            time.sleep(2 ** attempt)


def fetch_json(symbol, interval, market, start_ms, proxy):
    """空响应在代理链路上偶发，必须重试而不是当成无数据。"""
    for attempt in range(3):
        raw = fetch(symbol, interval, market, start_ms, proxy)
        batch = json.loads(raw) if raw.strip() else []
        if batch:
            return batch
        time.sleep(1 + attempt)
    raise RuntimeError("连续空响应，代理链路不稳定")


def fmt_row(k):
    open_dt = datetime.fromtimestamp(k[0] / 1000, TZ8)
    close_dt = datetime.fromtimestamp(k[6] / 1000, TZ8).replace(second=59)
    return [open_dt.strftime("%Y-%m-%d %H:%M:%S"), k[1], k[2], k[3], k[4], k[5],
            close_dt.strftime("%Y-%m-%d %H:%M:%S"), k[7], k[8], k[9], k[10]]


def last_ts(path: Path):
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    if len(rows) < 2:
        return 0
    return int(datetime.strptime(rows[-1][0], "%Y-%m-%d %H:%M:%S").replace(tzinfo=TZ8).timestamp() * 1000)


def update(symbol: str, path: Path, interval: str, market: str, proxy: str = ""):
    step = INTERVAL_MS.get(interval, 900_000)
    start = last_ts(path) + step
    if start >= time.time() * 1000:
        print(f"{symbol}: 已是最新（下一根未开盘）")
        return
    total = 0
    rows_out = []
    while True:
        batch = fetch_json(symbol, interval, market, start, proxy)
        if not batch:
            break
        rows_out.extend(fmt_row(k) for k in batch)
        start = batch[-1][0] + step
        total += len(batch)
        if len(batch) < 1000:
            break
        time.sleep(0.2)
    if not rows_out:
        print(f"{symbol}: 已是最新")
        return
    seen = set()
    if path.exists():
        with path.open("r", encoding="utf-8", newline="") as f:
            seen = {r[0] for r in csv.reader(f)}
    new_rows = [r for r in rows_out if r[0] not in seen]
    mode = "a" if path.exists() else "w"
    with path.open(mode, encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if mode == "w":
            w.writerow(HEADERS)
        w.writerows(new_rows)
    print(f"{symbol}: 新增 {len(new_rows)} 根 K 线")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--symbols", default="")
    ap.add_argument("--market", choices=["spot", "futures"], default="futures")
    ap.add_argument("--interval", default="15m")
    ap.add_argument("--proxy", default="socks5h://127.0.0.1:1081",
                    help="代理；传 none 走直连")
    args = ap.parse_args()
    root = Path(args.dir)
    proxy = "" if args.proxy.lower() == "none" else args.proxy
    tag = "永续" if args.market == "futures" else "现货"
    label = INTERVAL_LABEL.get(args.interval, args.interval)
    files = sorted(root.glob(f"*_{tag}_{label}_全历史.csv"))
    targets = []
    if args.symbols:
        for sym in [s.strip().upper() for s in args.symbols.split(",") if s.strip()]:
            targets.append((sym, root / f"{sym}_{tag}_{label}_全历史.csv"))
    else:
        for f in files:
            targets.append((f.name.split("_")[0], f))
    if not targets:
        print("目录里没有匹配的数据文件，先用 --symbols 指定币种建全量。")
        sys.exit(1)
    for sym, path in targets:
        try:
            update(sym, path, args.interval, args.market, proxy)
        except Exception as exc:
            print(f"{sym}: 失败 {exc}")


if __name__ == "__main__":
    main()
