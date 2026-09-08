# -*- coding: utf-8 -*-
"""
MCP桥接脚本 - mcp-server-github v1.1
功能：GitHub API操作封装
前置条件：GITHUB_PERSONAL_ACCESS_TOKEN 环境变量已设置
"""

import subprocess
import json
import sys
import argparse
import os

MCP_PACKAGE_NAME = "@modelcontextprotocol/server-github"
MCP_START_COMMAND = ["npx", "-y", MCP_PACKAGE_NAME]
ENCODING = "utf-8"
TIMEOUT = 60


def mcp_call(tool_name, arguments):
    token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN", "")
    env = os.environ.copy()
    env["GITHUB_PERSONAL_ACCESS_TOKEN"] = token

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
    parser = argparse.ArgumentParser(description="MCP桥接 - GitHub服务")
    parser.add_argument("tool", choices=[
        "search_repositories","get_file_contents","create_or_update_file",
        "push_files","create_repository","get_issue","create_issue",
        "create_pull_request","fork_repository","create_branch",
        "list_commits","list_issues","update_issue","add_issue_comment",
        "search_code","search_issues","search_users","get_me"
    ], help="工具名")
    parser.add_argument("--query", default="", help="搜索关键词")
    parser.add_argument("--owner", default="", help="仓库所有者")
    parser.add_argument("--repo", default="", help="仓库名")
    parser.add_argument("--file_path", default="", help="文件路径")
    parser.add_argument("--title", default="", help="标题")
    parser.add_argument("--body", default="", help="正文")
    parser.add_argument("--branch", default="main", help="分支名")
    parser.add_argument("--base_branch", default="main", help="基础分支")
    parser.add_argument("--head_branch", default="", help="头部分支")
    parser.add_argument("--state", default="open", help="状态")
    parser.add_argument("--limit", type=int, default=10, help="每页数量")

    args = parser.parse_args()
    arguments = {}

    if args.tool in ("search_repositories","search_code","search_issues","search_users"):
        arguments["query"] = args.query
        arguments["per_page"] = args.limit
    elif args.tool in ("get_file_contents","create_or_update_file"):
        arguments["owner"] = args.owner
        arguments["repo"] = args.repo
        arguments["path"] = args.file_path
    elif args.tool in ("create_issue","list_issues","update_issue"):
        arguments["owner"] = args.owner
        arguments["repo"] = args.repo
        if args.title:
            arguments["title"] = args.title
        if args.body:
            arguments["body"] = args.body
        arguments["state"] = args.state
    elif args.tool == "create_pull_request":
        arguments["owner"] = args.owner
        arguments["repo"] = args.repo
        arguments["title"] = args.title
        arguments["body"] = args.body
        arguments["base"] = args.base_branch
        arguments["head"] = args.head_branch
    elif args.tool in ("create_branch","list_commits"):
        arguments["owner"] = args.owner
        arguments["repo"] = args.repo
        arguments["branch"] = args.branch

    result = mcp_call(args.tool, arguments)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
