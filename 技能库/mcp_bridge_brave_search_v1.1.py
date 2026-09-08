# -*- coding: utf-8 -*-
"""
MCP桥接脚本 - mcp-server-brave-search v1.1
功能：Brave搜索引擎封装
前置条件：BRAVE_API_KEY 环境变量已设置
"""

import subprocess
import json
import sys
import argparse
import os

MCP_PACKAGE_NAME = "@modelcontextprotocol/server-brave-search"
MCP_START_COMMAND = ["npx", "-y", MCP_PACKAGE_NAME]
ENCODING = "utf-8"
TIMEOUT = 30


def mcp_call(tool_name, arguments):
    api_key = os.environ.get("BRAVE_API_KEY", "")
    env = os.environ.copy()
    env["BRAVE_API_KEY"] = api_key

    process = None
    try:
        process = subprocess.Popen(
            MCP_START_COMMAND,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, encoding=ENCODING, bufsize=1,
            env=env
        )
        init = json.dumps({"jsonrpc":"2.0","id":1,"method":"initialize",
                           "params":{"protocolVersion":"0.1.0","capabilities":{},
                           "clientInfo":{"name":"marvis-bridge","version":"1.1"}}}) + "\n"
        process.stdin.write(init); process.stdin.flush()
        process.stdout.readline()

        call = json.dumps({"jsonrpc":"2.0","id":2,"method":"tools/call",
                           "params":{"name":tool_name,"arguments":arguments}}, ensure_ascii=False) + "\n"
        process.stdin.write(call); process.stdin.flush()

        resp = process.stdout.readline()
        if not resp:
            return {"error":"无响应"}
        result = json.loads(resp)
        if "error" in result:
            return {"error":result["error"]}
        return {"result":result.get("result",{})}
    except Exception as e:
        return {"error":str(e)}
    finally:
        if process:
            try:
                process.stdin.close()
                process.wait(timeout=5)
            except:
                process.kill()


def main():
    parser = argparse.ArgumentParser(description="MCP桥接 - Brave搜索")
    parser.add_argument("tool", choices=["brave_web_search","brave_local_search"], help="工具名")
    parser.add_argument("--query", required=True, help="搜索查询词")
    parser.add_argument("--limit", type=int, default=10, help="返回数量")

    args = parser.parse_args()
    arguments = {"query": args.query, "count": args.limit}

    result = mcp_call(args.tool, arguments)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
