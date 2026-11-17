# -*- coding: utf-8 -*-
"""
obsidian_rest.py —— Obsidian local-rest-api 客户端库（v1.0.0）

解决三个真实坑：
  1. 端口有两个：27124=HTTPS、27123=HTTP(insecure)。默认只开 27124，且需自签证书。
     → 本库优先试 27123(HTTP)，失败再试 27124(HTTPS+跳过校验)
  2. PATCH 是「局部指令代数」(targetType/target/operation)，裸文本 PATCH 会 400。
     → 整文件写入走 PUT(text/markdown)；局部改写走 PATCH，且 target 必须逐字符等于
       document-map 里的可寻址键（标题带时间戳/重复标题会带不可见后缀）
  3. 成功状态码不止 200：新建返回 204(无 body)、更新返回 200、删除返回 204。
     → 统一按 {200,201,204} 判成功

零外部依赖，只用标准库。
"""
import os, sys, json, ssl, time, urllib.request, urllib.error, urllib.parse, hashlib, datetime

__version__ = "1.0.0"

DEFAULT_VAULT = r"E:\龙虾AI主控中心\我的AI分身\Obsidian知识库"
ENVF = r"E:\博主学习库\_tools\obsidian_rest.env"


def _read_key(envf=ENVF):
    """从 env 文件读 API key（不打印明文）"""
    if not os.path.exists(envf):
        raise RuntimeError(f"凭据文件不存在: {envf}")
    key = None
    for line in open(envf, encoding="utf-8"):
        line = line.strip()
        if line.startswith("OBSIDIAN_API_KEY="):
            key = line.split("=", 1)[1].strip()
    if not key:
        raise RuntimeError(f"凭据文件缺 OBSIDIAN_API_KEY: {envf}")
    return key


class ObsidianRest:
    def __init__(self, key=None, base=None, vault=DEFAULT_VAULT, timeout=25):
        self.key = key or _read_key()
        self.vault = vault
        self.timeout = timeout
        self.base = base or self._autodetect()
        self._ctx = ssl.create_default_context()
        self._ctx.check_hostname = False
        self._ctx.verify_mode = ssl.CERT_NONE

    # ---------- 连接探测 ----------
    def _autodetect(self):
        """优先 HTTP 27123（免证书），失败退 HTTPS 27124"""
        for scheme, port in [("http", 27123), ("https", 27124)]:
            try:
                st, _ = self._raw(scheme, port, "/vault/")
                if st == 200:
                    return f"{scheme}://127.0.0.1:{port}"
            except Exception:
                continue
        raise RuntimeError(
            "Obsidian REST 通道不可达。请确认：\n"
            "  1) Obsidian 已启动（双击桌面「Obsidian知识库」）\n"
            "  2) 插件 obsidian-local-rest-api 已启用（主库 community-plugins.json 已含）\n"
            "  3) data.json 里 enableInsecureServer=true（否则只开 27124 HTTPS）"
        )

    def _raw(self, scheme, port, path, method="GET", body=None, ctype=None, headers=None):
        url = f"{scheme}://127.0.0.1:{port}{path}"
        req = urllib.request.Request(url, method=method)
        if self.key:
            req.add_header("Authorization", f"Bearer {self.key}")
        if ctype:
            req.add_header("Content-Type", ctype)
        for k, v in (headers or {}).items():
            req.add_header(k, v)
        data = None
        if body is not None:
            data = body.encode("utf-8") if isinstance(body, str) else json.dumps(body).encode("utf-8")
        opener = urllib.request.build_opener(
            urllib.request.HTTPSHandler(context=self._ctx) if scheme == "https"
            else urllib.request.HTTPHandler())
        try:
            with opener.open(req, data=data, timeout=self.timeout) as r:
                return r.status, r.read().decode("utf-8", "ignore")
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8", "ignore")

    def call(self, path, method="GET", body=None, ctype=None, headers=None):
        p = urllib.parse.urlsplit(self.base)
        return self._raw(p.scheme, p.port, path, method, body, ctype, headers)

    # ---------- 读 ----------
    def list_dir(self, rel=""):
        """列目录（rel 为 vault 内相对路径，如 'P07_xxx/02_产物归档/'）"""
        st, raw = self.call("/vault/" + urllib.parse.quote(rel))
        if st != 200:
            raise RuntimeError(f"list_dir {rel} -> HTTP {st}: {raw[:200]}")
        d = json.loads(raw)
        items = d.get("files", []) if isinstance(d, dict) else d
        return [x if isinstance(x, str) else x.get("path", "") for x in items]

    def read(self, rel):
        st, raw = self.call("/vault/" + urllib.parse.quote(rel))
        if st != 200:
            raise RuntimeError(f"read {rel} -> HTTP {st}: {raw[:200]}")
        return raw

    def read_json(self, rel):
        st, raw = self.call("/vault/" + urllib.parse.quote(rel),
                             headers={"Accept": "application/vnd.olrapi.note+json"})
        if st != 200:
            raise RuntimeError(f"read_json {rel} -> HTTP {st}: {raw[:200]}")
        return json.loads(raw)

    def document_map(self, rel):
        st, raw = self.call("/vault/" + urllib.parse.quote(rel),
                             headers={"Accept": "application/vnd.olrapi.document-map+json"})
        if st != 200:
            raise RuntimeError(f"document_map {rel} -> HTTP {st}: {raw[:200]}")
        return json.loads(raw)

    # ---------- 写 ----------
    def write(self, rel, content, create_dirs=True):
        """整文件写入（新建或覆盖）。返回 (status, disk_path)"""
        if create_dirs:
            self._mkdirs(rel)
        st, raw = self.call("/vault/" + urllib.parse.quote(rel), method="PUT",
                            body=content, ctype="text/markdown")
        ok = st in (200, 201, 204)
        if not ok:
            raise RuntimeError(f"write {rel} -> HTTP {st}: {raw[:300]}")
        return st, self.abs_path(rel)

    def append(self, rel, text):
        """追加到文件末尾（读改写）"""
        old = ""
        try:
            old = self.read(rel)
        except Exception:
            pass
        return self.write(rel, old.rstrip("\n") + "\n\n" + text.strip() + "\n")

    def patch(self, rel, target_type, target, operation, content=None, **kw):
        """局部指令改写。target 必须逐字符等于 document-map 里的可寻址键"""
        body = {"targetType": target_type, "target": target, "operation": operation}
        if content is not None:
            body["content"] = content
        body.update(kw)
        st, raw = self.call("/vault/" + urllib.parse.quote(rel), method="PATCH", body=body)
        if st not in (200, 201, 204):
            raise RuntimeError(f"patch {rel} -> HTTP {st}: {raw[:300]}")
        return st

    def delete(self, rel):
        st, raw = self.call("/vault/" + urllib.parse.quote(rel), method="DELETE")
        if st not in (200, 202, 204):
            raise RuntimeError(f"delete {rel} -> HTTP {st}: {raw[:300]}")
        return st

    # ---------- 本地 ----------
    def abs_path(self, rel):
        return os.path.join(self.vault, rel.replace("/", os.sep))

    def _mkdirs(self, rel):
        """确保目录存在（Obsidian PUT 会自动建目录，但显式建更稳）"""
        d = os.path.dirname(self.abs_path(rel))
        if d and not os.path.isdir(d):
            os.makedirs(d, exist_ok=True)

    def disk_sha(self, rel):
        p = self.abs_path(rel)
        if not os.path.exists(p):
            return None
        return hashlib.sha256(open(p, "rb").read()).hexdigest()

    # ---------- 便利方法 ----------
    def note(self, rel, title, body, tags=None, extra_frontmatter=None):
        """写一篇带 frontmatter 的笔记"""
        fm = []
        if tags:
            fm.append("tags: [" + ", ".join(tags) + "]")
        fm.append("created: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        for k, v in (extra_frontmatter or {}).items():
            fm.append(f"{k}: {v}")
        content = "---\n" + "\n".join(fm) + "\n---\n\n# " + title + "\n\n" + body.rstrip() + "\n"
        return self.write(rel, content)

    def search_files(self, keyword, limit=50):
        """按文件名递归找（走目录遍历）"""
        out = []
        stack = [""]
        while stack and len(out) < limit:
            cur = stack.pop()
            try:
                items = self.list_dir(cur)
            except Exception:
                continue
            for it in items:
                p = (cur + it) if cur else it
                if it.endswith("/"):
                    stack.append(p)
                elif keyword.lower() in it.lower():
                    out.append(p)
        return out


if __name__ == "__main__":
    ob = ObsidianRest()
    print(f"ObsidianRest v{__version__}  base={ob.base}  vault={ob.vault}")
    print(f"顶层 {len(ob.list_dir())} 项")
    for x in ob.list_dir()[:10]:
        print("  ", x)
