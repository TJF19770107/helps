from __future__ import annotations

import base64
import json
import os
import posixpath
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin
from xml.etree import ElementTree as ET


def _env(name: str, default: str = "") -> str:
    """读取环境变量（不回显敏感值）。"""

    return os.environ.get(name, default)


def _require_env(name: str) -> str:
    """读取必需环境变量。"""

    v = _env(name, "")
    if not v:
        raise RuntimeError(f"缺少环境变量：{name}")
    return v


def _has_env(name: str) -> bool:
    """判断环境变量是否已设置。"""

    return bool(_env(name, "").strip())


def _build_base_url() -> str:
    """构建 WebDAV 根 URL。"""

    base = _require_env("LOBSTER_WEBDAV_URL").strip().rstrip("/") + "/"
    return base


def _auth_tuple() -> Tuple[str, str]:
    """读取 WebDAV 基本认证用户名/密码。"""

    user = _require_env("LOBSTER_WEBDAV_USER")
    pwd = _require_env("LOBSTER_WEBDAV_PASS")
    return user, pwd


def _requests():
    """延迟导入 requests。"""

    try:
        import requests  # type: ignore

        return requests
    except Exception as e:
        raise RuntimeError("缺少依赖 requests；请先安装后再使用本技能。") from e


def _normalize_remote_path(remote_path: str) -> str:
    """规范化 remote_path。"""

    p = (remote_path or "/").strip()
    if not p.startswith("/"):
        p = "/" + p
    p = re.sub(r"/{2,}", "/", p)
    return p


def _remote_url(remote_path: str) -> str:
    """拼接远端完整 URL。"""

    base = _build_base_url()
    rp = _normalize_remote_path(remote_path)
    return urljoin(base, rp.lstrip("/"))


def _propfind_list(url: str, auth: Tuple[str, str]) -> List[Dict[str, Any]]:
    """用 PROPFIND 列目录。"""

    requests = _requests()
    headers = {"Depth": "1", "Content-Type": "application/xml"}
    body = """<?xml version="1.0" encoding="utf-8" ?>
<d:propfind xmlns:d="DAV:">
  <d:prop>
    <d:displayname />
    <d:resourcetype />
    <d:getcontentlength />
    <d:getlastmodified />
  </d:prop>
</d:propfind>
"""
    resp = requests.request("PROPFIND", url, headers=headers, data=body.encode("utf-8"), auth=auth, timeout=30)
    if resp.status_code not in (200, 207):
        raise RuntimeError(f"PROPFIND 失败：HTTP {resp.status_code}")

    ns = {"d": "DAV:"}
    root = ET.fromstring(resp.content)
    out: List[Dict[str, Any]] = []
    for r in root.findall("d:response", ns):
        href = r.findtext("d:href", default="", namespaces=ns)
        prop = r.find("d:propstat/d:prop", ns)
        if prop is None:
            continue
        display = prop.findtext("d:displayname", default="", namespaces=ns)
        size = prop.findtext("d:getcontentlength", default="", namespaces=ns)
        lastmod = prop.findtext("d:getlastmodified", default="", namespaces=ns)
        rtype = prop.find("d:resourcetype", ns)
        is_dir = bool(rtype is not None and rtype.find("d:collection", ns) is not None)
        out.append(
            {
                "href": href,
                "name": display,
                "is_dir": is_dir,
                "size": int(size) if str(size).isdigit() else None,
                "last_modified": lastmod,
            }
        )
    return out


def webdav_list(remote_path: str = "/") -> Dict[str, Any]:
    """列出 remote_path 下的子项。"""

    auth = _auth_tuple()
    url = _remote_url(remote_path)
    items = _propfind_list(url, auth=auth)
    return {
        "ok": True,
        "remote_path": _normalize_remote_path(remote_path),
        "items": items,
        "env": {
            "LOBSTER_WEBDAV_URL": "SET" if _has_env("LOBSTER_WEBDAV_URL") else "EMPTY",
            "LOBSTER_WEBDAV_USER": "SET" if _has_env("LOBSTER_WEBDAV_USER") else "EMPTY",
            "LOBSTER_WEBDAV_PASS": "SET" if _has_env("LOBSTER_WEBDAV_PASS") else "EMPTY",
        },
    }


def webdav_download(remote_path: str, local_path: str) -> Dict[str, Any]:
    """下载 remote_path 到 local_path。"""

    requests = _requests()
    auth = _auth_tuple()
    url = _remote_url(remote_path)
    lp = Path(local_path).expanduser().resolve()
    lp.parent.mkdir(parents=True, exist_ok=True)

    with requests.get(url, auth=auth, stream=True, timeout=60) as resp:
        if resp.status_code != 200:
            raise RuntimeError(f"GET 失败：HTTP {resp.status_code}")
        with lp.open("wb") as f:
            for chunk in resp.iter_content(chunk_size=1024 * 128):
                if chunk:
                    f.write(chunk)

    return {"ok": True, "remote_path": _normalize_remote_path(remote_path), "local_path": str(lp)}


def webdav_upload(local_path: str, remote_path: str) -> Dict[str, Any]:
    """上传 local_path 到 remote_path（PUT）。"""

    requests = _requests()
    auth = _auth_tuple()
    url = _remote_url(remote_path)
    lp = Path(local_path).expanduser().resolve()
    if not lp.exists() or not lp.is_file():
        raise RuntimeError("local_path 不存在或不是文件。")

    with lp.open("rb") as f:
        resp = requests.put(url, data=f, auth=auth, timeout=60)
    if resp.status_code not in (200, 201, 204):
        raise RuntimeError(f"PUT 失败：HTTP {resp.status_code}")

    return {"ok": True, "remote_path": _normalize_remote_path(remote_path), "local_path": str(lp)}


def webdav_mkdir(remote_path: str) -> Dict[str, Any]:
    """创建远端目录（MKCOL）。"""

    requests = _requests()
    auth = _auth_tuple()
    url = _remote_url(remote_path)
    resp = requests.request("MKCOL", url, auth=auth, timeout=30)
    if resp.status_code not in (201, 204, 405):
        raise RuntimeError(f"MKCOL 失败：HTTP {resp.status_code}")
    return {"ok": True, "remote_path": _normalize_remote_path(remote_path), "http": resp.status_code}


def run_json(payload: Dict[str, Any]) -> Dict[str, Any]:
    """JSON 统一入口。"""

    action = str(payload.get("action") or "").strip()
    if action == "list":
        return webdav_list(remote_path=str(payload.get("remote_path") or "/"))
    if action == "download":
        return webdav_download(remote_path=str(payload.get("remote_path") or ""), local_path=str(payload.get("local_path") or ""))
    if action == "upload":
        return webdav_upload(local_path=str(payload.get("local_path") or ""), remote_path=str(payload.get("remote_path") or ""))
    if action == "mkdir":
        return webdav_mkdir(remote_path=str(payload.get("remote_path") or ""))
    raise ValueError("未知 action：支持 list/download/upload/mkdir")


def main() -> int:
    """命令行主入口。"""

    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        print(json.dumps(run_json(payload), ensure_ascii=False))
        return 0
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
