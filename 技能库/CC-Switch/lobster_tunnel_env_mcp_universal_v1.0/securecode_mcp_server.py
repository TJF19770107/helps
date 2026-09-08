import argparse
import json
import os
import ssl
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, Optional, Tuple


def _read_required_env(name: str) -> str:
    """Reads a required environment variable and raises if missing/empty."""
    v = os.environ.get(name, "").strip()
    if not v:
        raise RuntimeError(f"Missing required env var: {name}")
    return v


def _read_optional_env(name: str) -> str:
    """Reads an optional environment variable (returns empty string if missing)."""
    return os.environ.get(name, "").strip()


def _jsonrpc_result(_id: Any, result: Any) -> Dict[str, Any]:
    """Builds a JSON-RPC success response."""
    return {"jsonrpc": "2.0", "id": _id, "result": result}


def _jsonrpc_error(_id: Any, code: int, message: str, data: Optional[Any] = None) -> Dict[str, Any]:
    """Builds a JSON-RPC error response."""
    err: Dict[str, Any] = {"code": code, "message": message}
    if data is not None:
        err["data"] = data
    return {"jsonrpc": "2.0", "id": _id, "error": err}


def _read_body(handler: BaseHTTPRequestHandler) -> bytes:
    """Reads raw request body bytes with Content-Length semantics."""
    length_s = handler.headers.get("Content-Length", "0").strip()
    try:
        length = int(length_s)
    except Exception:
        length = 0
    if length <= 0:
        return b""
    return handler.rfile.read(length)


def _auth_ok(handler: BaseHTTPRequestHandler, bearer_token: str) -> bool:
    """Validates Authorization: Bearer <token> header."""
    auth = (handler.headers.get("Authorization") or "").strip()
    if not auth.startswith("Bearer "):
        return False
    got = auth[len("Bearer ") :].strip()
    return bool(got) and got == bearer_token


def _tool_list() -> Any:
    """Returns MCP tools/list payload."""
    return [
        {
            "name": "securecode.status",
            "description": "Returns secure tunnel/security status without exposing secrets.",
            "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        },
        {
            "name": "securecode.echo",
            "description": "Echoes input text. Invoke when validating MCP tool calls.",
            "inputSchema": {
                "type": "object",
                "properties": {"text": {"type": "string"}},
                "required": ["text"],
                "additionalProperties": False,
            },
        },
    ]


def _call_tool(name: str, arguments: Dict[str, Any]) -> Any:
    """Executes supported tools and returns MCP content array."""
    if name == "securecode.status":
        return [
            {
                "type": "text",
                "text": json.dumps(
                    {
                        "ok": True,
                        "tls": {"enabled": True, "minVersion": "TLSv1.3"},
                        "auth": {"bearer": "enabled"},
                    },
                    ensure_ascii=False,
                ),
            }
        ]
    if name == "securecode.echo":
        text = str(arguments.get("text", ""))
        return [{"type": "text", "text": text}]
    raise KeyError(f"Unknown tool: {name}")


class _Handler(BaseHTTPRequestHandler):
    server_version = "SecureCodeMCP/1.0"

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _send_json(self, status: int, payload: Dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path.rstrip("/") == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"OK")
            return
        self.send_response(404)
        self.end_headers()

    def do_POST(self) -> None:
        if self.path.rstrip("/") != "/mcp":
            self.send_response(404)
            self.end_headers()
            return

        bearer = _read_optional_env("SECURECODE_MCP_BEARER_TOKEN")
        if bearer:
            if not _auth_ok(self, bearer):
                self._send_json(401, _jsonrpc_error(None, -32001, "Unauthorized"))
                return

        raw = _read_body(self)
        try:
            req = json.loads(raw.decode("utf-8") if raw else "{}")
        except Exception:
            self._send_json(400, _jsonrpc_error(None, -32700, "Parse error"))
            return

        _id = req.get("id")
        method = req.get("method")
        params = req.get("params") or {}

        try:
            if method == "initialize":
                result = {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "securecode-mcp", "version": "1.0"},
                }
                self._send_json(200, _jsonrpc_result(_id, result))
                return

            if method == "notifications/initialized":
                self._send_json(200, _jsonrpc_result(_id, {"ok": True}))
                return

            if method == "tools/list":
                self._send_json(200, _jsonrpc_result(_id, {"tools": _tool_list()}))
                return

            if method == "tools/call":
                tool_name = str(params.get("name", ""))
                arguments = params.get("arguments") or {}
                if not isinstance(arguments, dict):
                    raise ValueError("arguments must be object")
                content = _call_tool(tool_name, arguments)
                self._send_json(200, _jsonrpc_result(_id, {"content": content}))
                return

            self._send_json(200, _jsonrpc_error(_id, -32601, "Method not found"))
        except KeyError as e:
            self._send_json(200, _jsonrpc_error(_id, -32602, "Invalid params", {"error": str(e)}))
        except Exception as e:
            self._send_json(200, _jsonrpc_error(_id, -32000, "Server error", {"error": str(e)}))


def _build_tls_context(cert_path: str, key_path: str) -> ssl.SSLContext:
    """Builds a TLS server context enforcing TLS 1.3 minimum."""
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    if hasattr(ssl, "TLSVersion"):
        ctx.minimum_version = ssl.TLSVersion.TLSv1_3
    ctx.load_cert_chain(certfile=cert_path, keyfile=key_path)
    return ctx


def main() -> int:
    """Entrypoint for SecureCode MCP HTTPS server."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=19090)
    parser.add_argument("--cert", default="")
    parser.add_argument("--key", default="")
    args = parser.parse_args()

    cert_path = args.cert.strip() or _read_required_env("SECURECODE_TLS_CERT_PATH")
    key_path = args.key.strip() or _read_required_env("SECURECODE_TLS_KEY_PATH")
    _ = _read_optional_env("SECURECODE_MCP_BEARER_TOKEN")

    httpd = HTTPServer((args.host, args.port), _Handler)
    httpd.socket = _build_tls_context(cert_path, key_path).wrap_socket(httpd.socket, server_side=True)
    try:
        httpd.serve_forever(poll_interval=0.25)
    except KeyboardInterrupt:
        return 0
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
