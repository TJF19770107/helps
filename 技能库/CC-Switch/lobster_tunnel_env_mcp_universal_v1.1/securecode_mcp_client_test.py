import argparse
import hashlib
import json
import socket
import ssl
import sys
from typing import Any, Dict, Optional, Tuple


def _sha256_hex(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def _https_jsonrpc(url_host: str, url_port: int, path: str, payload: Dict[str, Any], bearer: str, expected_cert_sha256: str, timeout_s: float) -> Dict[str, Any]:
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    if hasattr(ssl, "TLSVersion"):
        ctx.minimum_version = ssl.TLSVersion.TLSv1_3

    raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = (
        f"POST {path} HTTP/1.1\r\n"
        f"Host: {url_host}:{url_port}\r\n"
        f"Content-Type: application/json\r\n"
        f"Content-Length: {len(raw)}\r\n"
        f"Connection: close\r\n"
    ).encode("utf-8")
    if bearer:
        req += f"Authorization: Bearer {bearer}\r\n".encode("utf-8")
    req += b"\r\n" + raw

    with socket.create_connection((url_host, url_port), timeout=timeout_s) as sock:
        with ctx.wrap_socket(sock, server_hostname=url_host) as ssock:
            cert_bin = ssock.getpeercert(binary_form=True)
            got = _sha256_hex(cert_bin)
            if expected_cert_sha256 and got.lower() != expected_cert_sha256.lower():
                raise RuntimeError("CERT_FINGERPRINT_MISMATCH")
            ssock.sendall(req)
            resp = b""
            while True:
                chunk = ssock.recv(65536)
                if not chunk:
                    break
                resp += chunk

    header, _, body = resp.partition(b"\r\n\r\n")
    if b" 200 " not in header.split(b"\r\n", 1)[0]:
        raise RuntimeError("HTTP_NOT_200")
    return json.loads(body.decode("utf-8") if body else "{}")


def _rpc(host: str, port: int, path: str, method: str, params: Optional[Dict[str, Any]], rpc_id: Any, bearer: str, expected_cert_sha256: str, timeout_s: float) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"jsonrpc": "2.0", "id": rpc_id, "method": method}
    if params is not None:
        payload["params"] = params
    return _https_jsonrpc(host, port, path, payload, bearer, expected_cert_sha256, timeout_s)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=19090)
    parser.add_argument("--path", default="/mcp")
    parser.add_argument("--bearer", default="")
    parser.add_argument("--cert-sha256", default="")
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args()

    init = _rpc(args.host, args.port, args.path, "initialize", {}, 1, args.bearer, args.cert_sha256, args.timeout)
    if "error" in init:
        raise RuntimeError("initialize_error")

    tools = _rpc(args.host, args.port, args.path, "tools/list", {}, 2, args.bearer, args.cert_sha256, args.timeout)
    if "error" in tools:
        raise RuntimeError("tools_list_error")

    echo = _rpc(
        args.host,
        args.port,
        args.path,
        "tools/call",
        {"name": "securecode.echo", "arguments": {"text": "ping"}},
        3,
        args.bearer,
        args.cert_sha256,
        args.timeout,
    )
    if "error" in echo:
        raise RuntimeError("tools_call_error")

    print(json.dumps({"ok": True, "initialize": True, "tools": True, "call": True}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

