# -*- coding: utf-8 -*-
"""
MCP桥接层通用模板 v1.1
用途：在Marvis环境中通过shell_executor调用MCP命令行工具
通信模式：stdio（标准输入输出）
"""

import subprocess
import json
import sys
import argparse
import os
import time

# ============================================================
# 配置区域
# ============================================================

# MCP服务器NPM包名（子类覆盖）
MCP_PACKAGE_NAME = "@modelcontextprotocol/server-xxx"

# MCP服务器启动命令
MCP_START_COMMAND = ["npx", "-y", MCP_PACKAGE_NAME]

# 超时时间（秒）
MCP_TIMEOUT = 30

# 编码
ENCODING = "utf-8"


# ============================================================
# MCP stdio 协议处理
# ============================================================

def send_mcp_request(process, request_dict):
    """向MCP进程发送JSON-RPC请求"""
    request_json = json.dumps(request_dict, ensure_ascii=False) + "\n"
    process.stdin.write(request_json)
    process.stdin.flush()


def read_mcp_response(process):
    """从MCP进程读取JSON-RPC响应"""
    line = process.stdout.readline()
    if not line:
        return None
    return json.loads(line)


def mcp_call_tool(tool_name, arguments):
    """
    通用MCP工具调用
    参数：
        tool_name: MCP工具名称
        arguments: 参数字典
    返回：
        dict: 工具执行结果
    """
    process = None
    try:
        # 启动MCP服务器进程
        process = subprocess.Popen(
            MCP_START_COMMAND,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding=ENCODING,
            bufsize=1
        )

        # 发送initialize请求
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "0.1.0",
                "capabilities": {},
                "clientInfo": {"name": "marvis-mcp-bridge", "version": "1.1"}
            }
        }
        send_mcp_request(process, init_request)
        init_response = read_mcp_response(process)

        if not init_response:
            return {"error": "MCP服务器初始化无响应"}

        # 发送tools/call请求
        call_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        send_mcp_request(process, call_request)

        # 读取响应
        result = read_mcp_response(process)

        if result is None:
            return {"error": "MCP工具调用无响应"}

        if "error" in result:
            return {"error": result["error"]}

        return {"result": result.get("result", {})}

    except subprocess.TimeoutExpired:
        return {"error": f"MCP调用超时（{MCP_TIMEOUT}秒）"}
    except Exception as e:
        return {"error": f"MCP调用异常: {str(e)}"}
    finally:
        if process:
            try:
                process.stdin.close()
                process.wait(timeout=5)
            except:
                process.kill()


# ============================================================
# 命令行接口
# ============================================================

def build_parser(tools_description):
    """构建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description=f"MCP桥接脚本 - {MCP_PACKAGE_NAME}",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("tool", type=str, help="MCP工具名称")
    parser.add_argument("--args", type=str, default="{}",
                        help="JSON格式的参数字符串，如 '{\"key\":\"value\"}'")
    return parser


def main():
    parser = argparse.ArgumentParser(description="MCP桥接通用模板")
    parser.add_argument("tool", type=str, help="MCP工具名称")
    parser.add_argument("--args", type=str, default="{}",
                        help="JSON格式的参数字符串")

    args = parser.parse_args()

    try:
        arguments = json.loads(args.args)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"参数JSON解析失败: {str(e)}"}, ensure_ascii=False))
        sys.exit(1)

    result = mcp_call_tool(args.tool, arguments)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
