# -*- coding: utf-8 -*-
"""
MCP桥接脚本 - mcp-server-time v1.1
功能：时间/时区服务封装
"""

import subprocess
import json
import sys
import argparse

MCP_PACKAGE_NAME = "@modelcontextprotocol/server-time"
MCP_START_COMMAND = ["npx", "-y", MCP_PACKAGE_NAME]
ENCODING = "utf-8"
TIMEOUT = 30


def mcp_call(tool_name, arguments):
    process = None
    try:
        process = subprocess.Popen(
            MCP_START_COMMAND,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, encoding=ENCODING, bufsize=1
        )
        # Initialize
        init = json.dumps({"jsonrpc":"2.0","id":1,"method":"initialize",
                           "params":{"protocolVersion":"0.1.0","capabilities":{},
                           "clientInfo":{"name":"marvis-bridge","version":"1.1"}}}) + "\n"
        process.stdin.write(init); process.stdin.flush()
        process.stdout.readline()

        # Tool call
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
    parser = argparse.ArgumentParser(description="MCP桥接 - 时间服务")
    parser.add_argument("tool", choices=["get_current_time","convert_time","list_timezones"], help="工具名")
    parser.add_argument("--timezone", default="Asia/Shanghai", help="时区")
    parser.add_argument("--timestamp", default="", help="时间戳")
    parser.add_argument("--source_fmt", default="ISO", help="源格式")
    parser.add_argument("--target_fmt", default="Unix", help="目标格式")

    args = parser.parse_args()
    arguments = {}

    if args.tool == "get_current_time":
        arguments["timezone"] = args.timezone
    elif args.tool == "convert_time":
        arguments["timestamp"] = args.timestamp
        arguments["source_format"] = args.source_fmt
        arguments["target_format"] = args.target_fmt

    result = mcp_call(args.tool, arguments)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
