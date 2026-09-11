#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ARS 实证SQL数据分析（零积分）v1.0 — 龙虾AI主控中心适配层

三级降级，保证本机一定能跑：
  1) duckdb（推荐）：直接 read_csv_auto / read_parquet 查 CSV/Parquet，无需建库
  2) pandas：读表后 DataFrame 执行（次选，本套件未安装）
  3) stdlib sqlite3 + csv：最后兜底，纯标准库零依赖

用法：
  python ars_sql_query.py --table main=data/raw.csv --sql "SELECT year, AVG(score) s FROM main GROUP BY 1 ORDER BY 1"
  python ars_sql_query.py --table a=a.csv --table b=b.csv --sql "SELECT * FROM a JOIN b ON a.id=b.id" --out out.csv
  python ars_sql_query.py --table main=data.xlsx --sql "SELECT COUNT(*) FROM main"   # xlsx 需 duckdb 之外额外支持，见提示

铁律：脚本只产出「实际算出来的数」。任何未在输出中的数字都是不存在的数字，
禁止在论文中书写本脚本未产出的统计量（见 ../风险提示与合规红线.md）。
"""
import argparse
import os
import sqlite3
import sys
import csv

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def run_duckdb(tables, sql, out):
    import duckdb
    con = duckdb.connect(":memory:")
    try:
        for name, path in tables.items():
            p = os.path.abspath(path)
            low = p.lower()
            if low.endswith((".parquet", ".pq")):
                con.execute("CREATE VIEW \"%s\" AS SELECT * FROM read_parquet_auto('%s')" % (name, p.replace("'", "''")))
            elif low.endswith((".csv", ".tsv", ".txt")):
                con.execute("CREATE VIEW \"%s\" AS SELECT * FROM read_csv_auto('%s')" % (name, p.replace("'", "''")))
            elif low.endswith((".db", ".sqlite", ".sqlite3")):
                con.execute("ATTACH '%s' AS _att" % p.replace("'", "''"))
                con.execute("CREATE VIEW \"%s\" AS SELECT * FROM _att.sqlite_master LIMIT 0" % name)
                raise RuntimeError("SQLite 文件请改用 --engine sqlite 并指定表名")
            else:
                con.execute("CREATE VIEW \"%s\" AS SELECT * FROM read_csv_auto('%s')" % (name, p.replace("'", "''")))
        cur = con.execute(sql)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
        return cols, rows
    finally:
        con.close()


def run_sqlite(tables, sql, out):
    """stdlib 兜底：CSV 载入内存 SQLite 后执行（仅支持 CSV）。"""
    con = sqlite3.connect(":memory:")
    for name, path in tables.items():
        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            r = csv.reader(f)
            header = next(r)
            data = [tuple(x for x in row) for row in r]
        cols = ",".join('"%s"' % h.replace('"', '""') for h in header)
        con.execute('CREATE TABLE "%s" (%s)' % (name, cols))
        con.executemany('INSERT INTO "%s" VALUES (%s)' % (name, ",".join("?" * len(header))), data)
    cur = con.execute(sql)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    con.close()
    return cols, rows


def main():
    ap = argparse.ArgumentParser(description="ARS 零积分 SQL 实证分析")
    ap.add_argument("--table", action="append", default=[], required=True,
                    help="表名=文件路径，可重复，如 main=data/raw.csv")
    ap.add_argument("--sql", required=True, help="要执行的 SQL（只读查询）")
    ap.add_argument("--engine", default="auto", choices=["auto", "duckdb", "sqlite"])
    ap.add_argument("--out", default="", help="结果另存为 CSV")
    ap.add_argument("--show", type=int, default=30, help="终端打印行数，默认 30")
    a = ap.parse_args()

    tables = {}
    for t in a.table:
        if "=" not in t:
            print("参数错误：--table 必须形如 表名=文件路径 -> %s" % t)
            sys.exit(2)
        k, v = t.split("=", 1)
        if not os.path.exists(v):
            print("文件不存在：%s" % os.path.abspath(v))
            sys.exit(2)
        tables[k.strip()] = v.strip()

    head = a.sql.strip().lower()
    if not (head.startswith("select") or head.startswith("with") or head.startswith("describe")):
        print("安全拦截：本脚本只允许只读查询（SELECT / WITH / DESCRIBE）。")
        sys.exit(2)

    engine = a.engine
    cols = rows = None
    if engine in ("auto", "duckdb"):
        try:
            cols, rows = run_duckdb(tables, a.sql, a.out)
            engine = "duckdb"
        except Exception as e:  # noqa: BLE001
            if engine == "duckdb":
                print("duckdb 执行失败：%s" % e)
                sys.exit(1)
            print("[duckdb 不可用，降级 stdlib] %s" % str(e)[:120])
            engine = "sqlite"
    if cols is None:
        cols, rows = run_sqlite(tables, a.sql, a.out)
        engine = "sqlite(stdlib)"

    print("引擎: %s | 行数: %d" % (engine, len(rows)))
    w = [max(len(str(c)), *(len(str(r[i])) for r in rows[:a.show])) if rows else len(str(c))
         for i, c in enumerate(cols)]
    print(" | ".join(str(c).ljust(w[i]) for i, c in enumerate(cols)))
    print("-+-".join("-" * x for x in w))
    for r in rows[:a.show]:
        print(" | ".join(str(v).ljust(w[i]) for i, v in enumerate(r)))
    if len(rows) > a.show:
        print("... 其余 %d 行已省略（--show 调整）" % (len(rows) - a.show))

    if a.out:
        with open(a.out, "w", encoding="utf-8-sig", newline="") as f:
            wr = csv.writer(f)
            wr.writerow(cols)
            wr.writerows(rows)
        print("已保存: %s" % os.path.abspath(a.out))

    print("\n⚠ 只可引用上表实际输出的数值；缺失值处理、样本量口径需人工确认后再写入论文。")


if __name__ == "__main__":
    main()
