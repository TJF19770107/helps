# -*- coding: utf-8 -*-
"""
MCP桥接脚本 - mcp-server-filesystem v1.1
功能：安全文件系统操作封装
"""

import subprocess
import json
import sys
import argparse
import os

MCP_PACKAGE_NAME = "@modelcontextprotocol/server-filesystem"
# 固定允许目录（从环境变量或默认值读取）
ALLOWED_DIR = os.environ.get("MCP_FS_ALLOWED_DIR", os.getcwd())
MCP_START_COMMAND = ["npx", "-y", MCP_PACKAGE_NAME, ALLOWED_DIR]
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
    parser = argparse.ArgumentParser(description="MCP桥接 - 文件系统服务")
    parser.add_argument("tool", choices=[
        "read_file","write_file","list_directory","create_directory",
        "move_file","search_files","get_file_info","list_allowed_directories"
    ], help="工具名")
    parser.add_argument("--file_path", default="", help="文件或目录路径")
    parser.add_argument("--content", default="", help="文件内容")
    parser.add_argument("--pattern", default="*", help="搜索模式")
    parser.add_argument("--recursive", default="false", help="是否递归")

    args = parser.parse_args()
    arguments = {"path": args.file_path}

    if args.tool == "write_file":
        arguments["content"] = args.content
    elif args.tool == "search_files":
        arguments["pattern"] = args.pattern
        arguments["recursive"] = args.recursive.lower() == "true"

    result = mcp_call(args.tool, arguments)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
