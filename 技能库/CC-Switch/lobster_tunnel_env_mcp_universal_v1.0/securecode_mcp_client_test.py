import argparse
import json
import os
import ssl
import sys
import urllib.request
from typing import Any, Dict, Optional, Tuple


def _post_json(url: str, payload: Dict[str, Any], bearer: str, timeout_s: float) -> Tuple[int, Dict[str, Any]]:
    """Posts a JSON payload to url and returns (status, json_response)."""
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url=url, data=data, method="POST")
    req.add_header("Content-Type", "application/json; charset=utf-8")
    if bearer:
        req.add_header("Authorization", f"Bearer {bearer}")

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    if hasattr(ssl, "TLSVersion"):
        ctx.minimum_version = ssl.TLSVersion.TLSv1_3

    with urllib.request.urlopen(req, context=ctx, timeout=timeout_s) as resp:
        body = resp.read()
        return resp.status, json.loads(body.decode("utf-8") if body else "{}")


def _rpc(url: str, method: str, params: Optional[Dict[str, Any]], rpc_id: Any, bearer: str, timeout_s: float) -> Dict[str, Any]:
    """Executes a single JSON-RPC request."""
    payload: Dict[str, Any] = {"jsonrpc": "2.0", "id": rpc_id, "method": method}
    if params is not None:
        payload["params"] = params
    status, res = _post_json(url, payload, bearer, timeout_s)
    if status < 200 or status >= 300:
        raise RuntimeError(f"HTTP {status}")
    return res


def main() -> int:
    """Runs an MCP handshake and basic tool calls for verification."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="https://127.0.0.1:19090/mcp")
    parser.add_argument("--bearer", default="")
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args()

    bearer = args.bearer.strip() or os.environ.get("SECURECODE_MCP_BEARER_TOKEN", "").strip()
    init = _rpc(args.url, "initialize", {}, 1, bearer, args.timeout)
    if "error" in init:
        raise RuntimeError(f"initialize error: {init['error']}")

    tools = _rpc(args.url, "tools/list", {}, 2, bearer, args.timeout)
    if "error" in tools:
        raise RuntimeError(f"tools/list error: {tools['error']}")

    echo = _rpc(
        args.url,
        "tools/call",
        {"name": "securecode.echo", "arguments": {"text": "ping"}},
        3,
        bearer,
        args.timeout,
    )
    if "error" in echo:
        raise RuntimeError(f"tools/call error: {echo['error']}")

    print(json.dumps({"ok": True, "initialize": True, "tools": True, "call": True}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
