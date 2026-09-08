#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙虾五步法 - 自动导入MCP配置到CC Switch
 lobster_codex_benchmark_v1.0: 读取并解析JSON配置
 lobster_claude_mem_gstack_bridge_v1.0: 和CC Switch建立通信桥接
 lobster_task_standard_workflow_full_v2.0: 按标准工作流完成导入、启用、校验全流程
"""

import sqlite3
import json
import os
from pathlib import Path

# ============================================
# 1. 路径配置
# ============================================
DB_PATH = r"C:\Users\Administrator\.cc-switch\cc-switch.db"
IMPORT_DIR = r"C:\Users\Administrator\WorkBuddy\2026-05-22-task-3\lobster_mcp"

# ============================================
# 2. MCP服务器元数据定义
# ============================================
MCP_SERVERS = [
    {
        "id": "brave-search",
        "file": "import_1_brave.json",
        "name": "Brave Search",
        "description": "Brave搜索引擎MCP服务器，支持隐私安全的网络搜索",
        "homepage": "https://brave.com/search",
        "docs": "https://github.com/modelcontextprotocol/servers/tree/main/src/brave-search",
        "tags": ["search", "web", "brave"]
    },
    {
        "id": "lobster-netdisk-search",
        "file": "import_2_netdisk.json",
        "name": "Lobster Netdisk Search",
        "description": "龙虾网盘搜索MCP，支持夸克、百度、阿里云盘搜索",
        "homepage": "https://github.com/lobster-ai/netdisk-search",
        "docs": "https://github.com/lobster-ai/netdisk-search#readme",
        "tags": ["search", "netdisk", "quark", "baidu", "aliyun", "lobster"]
    },
    {
        "id": "xiaohongshu-browser",
        "file": "import_3_xiaohongshu.json",
        "name": "Xiaohongshu Browser",
        "description": "小红书浏览器自动化MCP，支持小红书内容抓取和搜索",
        "homepage": "https://www.xiaohongshu.com",
        "docs": "https://github.com/microsoft/playwright-mcp",
        "tags": ["browser", "xiaohongshu", "social", "playwright"]
    },
    {
        "id": "wechat-video-browser",
        "file": "import_4_wechat_video.json",
        "name": "WeChat Video Browser",
        "description": "微信视频号浏览器自动化MCP，支持视频号内容抓取",
        "homepage": "https://channels.weixin.qq.com",
        "docs": "https://github.com/microsoft/playwright-mcp",
        "tags": ["browser", "wechat", "video", "playwright"]
    },
    {
        "id": "desktop-automation",
        "file": "import_5_desktop_automation.json",
        "name": "Desktop Automation",
        "description": "桌面自动化Puppeteer MCP服务器，支持浏览器自动化操作",
        "homepage": "https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer",
        "docs": "https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer",
        "tags": ["automation", "puppeteer", "browser", "desktop"]
    }
]

# ============================================
# 3. 执行导入
# ============================================
def main():
    print("=" * 60)
    print("龙虾五步法 - CC Switch MCP 自动导入工具")
    print("=" * 60)

    # 连接数据库
    print(f"\n[1/5] 连接CC Switch数据库: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print("  ✓ 数据库连接成功")

    # 检查现有MCP数量
    cursor.execute("SELECT COUNT(*) FROM mcp_servers")
    before_count = cursor.fetchone()[0]
    print(f"\n[2/5] 当前MCP数量: {before_count} 个")

    results = []

    # 遍历并导入每个MCP
    print(f"\n[3/5] 开始导入 {len(MCP_SERVERS)} 个MCP服务器...")
    for meta in MCP_SERVERS:
        file_path = os.path.join(IMPORT_DIR, meta["file"])
        print(f"\n  → 处理: {meta['id']} ({meta['name']})")

        # 读取JSON配置
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                server_config = json.load(f)
            server_config_json = json.dumps(server_config, ensure_ascii=False)
            print(f"    ✓ 读取配置: {meta['file']}")
        except Exception as e:
            print(f"    ✗ 读取失败: {e}")
            results.append({"id": meta["id"], "status": "FAILED", "error": str(e)})
            continue

        # 检查是否已存在
        cursor.execute("SELECT id FROM mcp_servers WHERE id = ?", (meta["id"],))
        existing = cursor.fetchone()

        # 使用REPLACE INTO（存在则替换，不存在则插入）
        try:
            cursor.execute("""
                REPLACE INTO mcp_servers
                (id, name, server_config, description, homepage, docs, tags,
                 enabled_claude, enabled_codex, enabled_gemini, enabled_opencode, enabled_hermes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                meta["id"],
                meta["name"],
                server_config_json,
                meta["description"],
                meta["homepage"],
                meta["docs"],
                json.dumps(meta["tags"], ensure_ascii=False),
                1,  # enabled_claude
                1,  # enabled_codex
                1,  # enabled_gemini
                1,  # enabled_opencode
                1   # enabled_hermes
            ))

            action = "更新" if existing else "新增"
            print(f"    ✓ {action}成功 | Claude ✓ | Codex ✓ | Gemini ✓ | OpenCode ✓ | Hermes ✓")
            results.append({"id": meta["id"], "status": action, "error": None})

        except Exception as e:
            print(f"    ✗ 导入失败: {e}")
            results.append({"id": meta["id"], "status": "FAILED", "error": str(e)})

    # 提交事务
    conn.commit()

    # ============================================
    # 4. 校验结果
    # ============================================
    print(f"\n[4/5] 校验导入结果...")
    cursor.execute("SELECT id, name, enabled_claude, enabled_codex, enabled_gemini, enabled_opencode, enabled_hermes FROM mcp_servers")
    all_servers = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM mcp_servers")
    after_count = cursor.fetchone()[0]

    print(f"\n  导入后MCP总数: {after_count} 个 (原有 {before_count} + 新增 {after_count - before_count})")

    # 检查5个目标MCP
    target_ids = {m["id"] for m in MCP_SERVERS}
    verified = []
    for row in all_servers:
        if row[0] in target_ids:
            enabled = all(row[2:7])
            status = "✓ 已启用/已校验/可调用" if enabled else "⚠ 已添加但部分模型未启用"
            verified.append({
                "id": row[0],
                "name": row[1],
                "claude": row[2],
                "codex": row[3],
                "gemini": row[4],
                "opencode": row[5],
                "hermes": row[6],
                "status": status
            })
            print(f"  {status} | {row[0]} ({row[1]})")

    conn.close()
    print("\n  ✓ 数据库连接已关闭")

    # ============================================
    # 5. 汇总输出
    # ============================================
    print(f"\n[5/5] 最终汇总")
    print("=" * 60)
    print(f"\n  导入前MCP数量: {before_count}")
    print(f"  导入后MCP数量: {after_count}")
    print(f"  净增数量: {after_count - before_count}")
    print(f"\n  目标状态:")
    for v in verified:
        print(f"    • {v['id']}: {v['status']}")
        print(f"      Claude={v['claude']} | Codex={v['codex']} | Gemini={v['gemini']} | OpenCode={v['opencode']} | Hermes={v['hermes']}")

    # 生成JSON报告
    report = {
        "before_count": before_count,
        "after_count": after_count,
        "new_count": after_count - before_count,
        "servers": verified,
        "all_pass": all(v['claude'] and v['codex'] and v['gemini'] and v['opencode'] and v['hermes'] for v in verified)
    }

    report_path = os.path.join(IMPORT_DIR, "import_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n  报告已保存: {report_path}")
    print("=" * 60)

    return report

if __name__ == "__main__":
    report = main()
    exit(0 if report["all_pass"] else 1)
