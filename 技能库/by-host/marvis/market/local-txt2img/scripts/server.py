"""Persistent local-txt2img server.

Listens on the Windows named pipe ``\\\\.\\pipe\\txt2img`` via
``multiprocessing.connection.Listener`` and dispatches text-to-image
requests from ``client.py``. Keeps an OpenVINO Z-Image Turbo pipeline
resident across invocations so each generate avoids cold-start cost.

State machine (same shape as ``skills/local-computer-use/src/scripts/server.py``):

    starting -> downloading -> loading -> running
                                        |-> error

Supported ops::

    status   -> {ok, state, pid, uptime_s, loaded_model_id, loaded_device}
    shutdown -> {ok, state: "shutting_down"}
    generate -> {ok, success, image_path, prompt, seed, steps,
                 width, height, device, timing: {...}}
"""

from __future__ import annotations

import argparse
import gc
import os
import random
import sys
import threading
import time
import traceback
import uuid
from multiprocessing.connection import Listener
from pathlib import Path
from typing import Any, Optional

from model_download_template import (
    ModelDownloadTemplate,
    download_required_model,
    validate_model_dir,
)

PIPE_ADDRESS = r"\\.\pipe\txt2img"
AUTHKEY = b"txt2img-local"
DEFAULT_SHUTDOWN_TIMEOUT = 10.0
STATE_STARTING = "starting"
STATE_DOWNLOADING = "downloading"
STATE_LOADING = "loading"
STATE_RUNNING = "running"
STATE_ERROR = "error"

OPENVINO_ROOT = Path(os.environ.get("USERPROFILE", str(Path.home()))) / ".openvino"
MODELS_ROOT = OPENVINO_ROOT / "models"
OUTPUTS_ROOT = Path(os.environ.get("USERPROFILE", str(Path.home()))) / "Pictures"

MODEL_ID = "snake7gun/Z-Image-Turbo-int4-ov"
MODEL_DIR = MODELS_ROOT / "z-image-turbo-int4-ov"
REQUIRED_MODEL_FILES = ("model_index.json",)

REQUIRED_MODEL_TEMPLATE = ModelDownloadTemplate(
    models_root=MODELS_ROOT,
    required_files=REQUIRED_MODEL_FILES,
)

DEFAULT_WIDTH = 512
DEFAULT_HEIGHT = 512
DEFAULT_STEPS = 9
DEFAULT_GUIDANCE = 0.0
_INTEL_VENDOR_ID = "0x8086"

SERVER_VERSION = "0.1.0"

for stream_name in ("stdout", "stderr"):
    stream = getattr(sys, stream_name, None)
    if stream is not None and hasattr(stream, "reconfigure"):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass

LOG_LOCK = threading.Lock()


def _normalize_log_path(log_path: str | None) -> Path | None:
    if not log_path:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        log_path = f"~/.openvino/log/txt2img-server-py-{timestamp}.log"

    path = Path(log_path).expanduser()
    return path if path.is_absolute() else Path.cwd() / path


def _log_message(log_path: Path | None, message: str) -> None:
    if log_path is None:
        return
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with LOG_LOCK:
            with log_path.open("a", encoding="utf-8") as stream:
                stream.write(f"[{timestamp}] [server pid={os.getpid()}] {message}\n")
    except OSError:
        pass


def _report_download_message(log_path: Path | None, message: str) -> None:
    print(f"[server] {message}", flush=True)
    _log_message(log_path, message)


def _ensure_required_model(log_path: Path | None = None) -> None:
    """Download the Z-Image Turbo model to MODEL_DIR if not already valid."""
    validation = validate_model_dir(MODEL_DIR, REQUIRED_MODEL_FILES)
    if validation.ok:
        return

    try:
        from modelscope import snapshot_download
    except ImportError as exc:
        raise RuntimeError(
            "modelscope is required to download the Z-Image Turbo model. "
            "Please run 'scripts\\install-env.bat' first."
        ) from exc

    MODELS_ROOT.mkdir(parents=True, exist_ok=True)
    if validation.reason != "directory missing":
        _report_download_message(
            log_path,
            f"model {MODEL_ID} is incomplete: {validation.reason}; re-downloading",
        )
    download_required_model(
        model_id=MODEL_ID,
        local_dir=MODEL_DIR,
        snapshot_download=snapshot_download,
        template=REQUIRED_MODEL_TEMPLATE,
        logger=lambda message: _report_download_message(log_path, message),
    )

    validation = validate_model_dir(MODEL_DIR, REQUIRED_MODEL_FILES)
    if not validation.ok:
        raise RuntimeError(
            f"required model download did not complete: {MODEL_DIR} ({validation.reason})"
        )


# ---------------------------------------------------------------------------
# OpenVINO pipeline helpers (distilled from local-text-to-image generator.py)
# ---------------------------------------------------------------------------
def _resolve_ovzimage_pipeline() -> Any:
    errors: list[str] = []
    try:
        from optimum.intel import OVZImagePipeline  # type: ignore
        return OVZImagePipeline
    except Exception as exc:
        errors.append(f"OVZImagePipeline: {type(exc).__name__}: {exc}")
    try:
        from optimum.intel import OVPipelineForText2Image  # type: ignore
        return OVPipelineForText2Image
    except Exception as exc:
        errors.append(f"OVPipelineForText2Image: {type(exc).__name__}: {exc}")
    raise ImportError(
        "no Z-Image-capable pipeline class is importable from optimum.intel. "
        "Re-run scripts\\install-env.bat so the vendored optimum-intel wheel "
        "is installed into the venv. Tried: " + " | ".join(errors)
    )


def _resolve_device() -> str:
    """Pick the first Intel GPU if available, otherwise CPU."""
    try:
        from openvino import Core  # type: ignore
    except ImportError:
        return "CPU"
    try:
        core = Core()
        available = list(core.available_devices)
    except Exception:
        return "CPU"

    for dev in available:
        if dev != "GPU" and not dev.startswith("GPU."):
            continue
        try:
            arch = str(core.get_property(dev, "DEVICE_ARCHITECTURE"))
        except Exception:
            continue
        if _INTEL_VENDOR_ID in arch:
            return dev
    return "CPU"


def _resolve_torch_generator_cls() -> Any:
    try:
        import torch  # type: ignore
        return torch.Generator
    except Exception:
        return None


def _extract_first_image(result: Any) -> Optional[Any]:
    images = getattr(result, "images", None)
    if images is None and isinstance(result, (list, tuple)):
        images = result
    if images is None:
        return None
    for img in images:
        if img is not None:
            return img
    return None


def _safe_seed() -> int:
    return random.SystemRandom().randint(0, 2**31 - 1)


# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------
class Server:
    def __init__(self, log_path: Path | None = None) -> None:
        self.start_time = time.time()
        self.shutdown_event = threading.Event()
        self.shutdown_timeout = DEFAULT_SHUTDOWN_TIMEOUT
        self.listener: Listener | None = None
        self.runtime_lock = threading.Lock()
        self.pipeline: Any = None
        self.loaded_model_id: str | None = None
        self.loaded_device: str | None = None
        self.log_path = log_path
        self.state: str = STATE_STARTING
        self.init_error: str = ""
        self.init_thread: threading.Thread | None = None

    def log(self, message: str) -> None:
        _log_message(self.log_path, message)

    def _init_runtime_worker(self) -> None:
        try:
            with self.runtime_lock:
                self.state = STATE_DOWNLOADING
            self.log("init thread: downloading required model")
            _ensure_required_model(self.log_path)

            with self.runtime_lock:
                self.state = STATE_LOADING
            self.log("init thread: loading OpenVINO Z-Image pipeline")

            pipeline_cls = _resolve_ovzimage_pipeline()
            device = _resolve_device()
            self.log(f"init thread: resolved device={device}")

            pipeline = pipeline_cls.from_pretrained(str(MODEL_DIR), device=device)

            with self.runtime_lock:
                self.pipeline = pipeline
                self.loaded_model_id = MODEL_ID
                self.loaded_device = device
                self.state = STATE_RUNNING
            self.log(f"init thread: pipeline ready on device={device}")
        except Exception:
            error_text = traceback.format_exc()
            with self.runtime_lock:
                self.init_error = error_text
                self.state = STATE_ERROR
            self.log(f"init thread failed:\n{error_text}")

    def _start_init_thread(self) -> None:
        if self.init_thread is not None and self.init_thread.is_alive():
            return
        self.init_thread = threading.Thread(
            target=self._init_runtime_worker,
            name="runtime-init",
            daemon=True,
        )
        self.init_thread.start()
        self.log("init thread started")

    def _do_generate(self, prompt: str, negative_prompt: str | None, width: int,
                     height: int, steps: int, seed: int) -> dict:
        t0 = time.time()
        OUTPUTS_ROOT.mkdir(parents=True, exist_ok=True)
        output_path = OUTPUTS_ROOT / f"image_{int(seed)}_{uuid.uuid4().hex[:8]}.png"

        torch_gen_cls = _resolve_torch_generator_cls()
        call_kwargs: dict[str, Any] = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": int(width),
            "height": int(height),
            "num_inference_steps": int(steps),
            "guidance_scale": float(DEFAULT_GUIDANCE),
        }
        if torch_gen_cls is not None:
            call_kwargs["generator"] = torch_gen_cls("cpu").manual_seed(int(seed))

        infer_start = time.time()
        try:
            result = self.pipeline(**call_kwargs)
        except Exception as exc:
            return {
                "ok": True,
                "success": False,
                "error_code": "GENERATION_FAILED",
                "error": f"{type(exc).__name__}: {exc}",
                "prompt": prompt,
                "seed": seed,
                "timing": {"infer_s": time.time() - infer_start, "save_s": 0.0, "total_s": time.time() - t0},
            }
        infer_s = time.time() - infer_start

        image = _extract_first_image(result)
        if image is None:
            return {
                "ok": True,
                "success": False,
                "error_code": "GENERATION_FAILED",
                "error": "pipeline returned no images",
                "prompt": prompt,
                "seed": seed,
                "timing": {"infer_s": infer_s, "save_s": 0.0, "total_s": time.time() - t0},
            }

        save_start = time.time()
        try:
            image.save(output_path, format="PNG")
        except Exception as exc:
            return {
                "ok": True,
                "success": False,
                "error_code": "SAVE_FAILED",
                "error": f"{type(exc).__name__}: {exc}",
                "prompt": prompt,
                "seed": seed,
                "timing": {"infer_s": infer_s, "save_s": time.time() - save_start, "total_s": time.time() - t0},
            }
        save_s = time.time() - save_start

        return {
            "ok": True,
            "success": True,
            "image_path": str(output_path),
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "seed": int(seed),
            "steps": int(steps),
            "width": int(width),
            "height": int(height),
            "device": self.loaded_device,
            "model_id": self.loaded_model_id,
            "timing": {"infer_s": infer_s, "save_s": save_s, "total_s": time.time() - t0},
        }

    def dispatch(self, msg: dict) -> dict:
        op = msg.get("op")
        self.log(f"dispatching op={op!r}")
        if op == "generate":
            prompt = msg.get("prompt")
            if not isinstance(prompt, str) or not prompt.strip():
                return {
                    "ok": False,
                    "success": False,
                    "error_code": "BAD_PROMPT",
                    "error": "prompt must be a non-empty string",
                }
            with self.runtime_lock:
                state = self.state
                init_error = self.init_error
                pipeline = self.pipeline
            if state != STATE_RUNNING or pipeline is None:
                self.log(f"generate rejected: state={state}")
                reply = {
                    "ok": False,
                    "success": False,
                    "state": state,
                    "prompt": prompt,
                    "error": f"runtime not ready: {state}",
                }
                if state == STATE_ERROR and init_error:
                    reply["error"] = init_error
                return reply
            width = msg.get("width", DEFAULT_WIDTH)
            height = msg.get("height", DEFAULT_HEIGHT)
            steps = msg.get("steps", DEFAULT_STEPS)
            seed = msg.get("seed")
            if not isinstance(seed, int) or isinstance(seed, bool):
                seed = _safe_seed()
            negative_prompt = msg.get("negative_prompt")
            try:
                reply = self._do_generate(prompt, negative_prompt, width, height, steps, seed)
                reply["state"] = STATE_RUNNING
                self.log(
                    f"generate completed: success={reply.get('success')} "
                    f"image_path={reply.get('image_path')}"
                )
                return reply
            except Exception:
                error_text = traceback.format_exc()
                self.log(f"generate failed:\n{error_text}")
                return {
                    "ok": False,
                    "success": False,
                    "state": STATE_RUNNING,
                    "prompt": prompt,
                    "error": error_text,
                }
        if op == "status":
            with self.runtime_lock:
                state = self.state
                init_error = self.init_error
                loaded_model_id = self.loaded_model_id
                loaded_device = self.loaded_device
            self.log(f"status requested: state={state}")
            reply = {
                "ok": True,
                "state": state,
                "pid": os.getpid(),
                "uptime_s": time.time() - self.start_time,
                "loaded_model_id": loaded_model_id,
                "loaded_device": loaded_device,
                "server_version": SERVER_VERSION,
            }
            if state == STATE_ERROR and init_error:
                reply["error"] = init_error
            return reply
        if op == "shutdown":
            timeout = msg.get("timeout", DEFAULT_SHUTDOWN_TIMEOUT)
            try:
                self.shutdown_timeout = float(timeout)
            except (TypeError, ValueError):
                self.shutdown_timeout = DEFAULT_SHUTDOWN_TIMEOUT
            self.log(f"shutdown requested with timeout={self.shutdown_timeout:.1f}s")
            # Release the pipeline so GPU memory / DLL handles drop before exit.
            try:
                with self.runtime_lock:
                    self.pipeline = None
                    self.loaded_model_id = None
                    self.loaded_device = None
                gc.collect()
            except Exception:
                pass
            self.shutdown_event.set()
            return {"ok": True, "state": "shutting_down"}
        self.log(f"unknown operation received: {op!r}")
        return {"ok": False, "error": f"unknown op: {op!r}"}

    def serve_forever(self) -> None:
        assert self.listener is not None
        while not self.shutdown_event.is_set():
            try:
                conn = self.listener.accept()
                self.log("accepted client connection")
            except OSError:
                if self.shutdown_event.is_set():
                    self.log("listener stopped after shutdown was requested")
                    return
                raise

            try:
                msg = conn.recv()
                self.log(f"client request: op={msg.get('op') if isinstance(msg, dict) else None}")

                reply = self.dispatch(msg if isinstance(msg, dict) else {})
                conn.send(reply)

                self.log(f"server reply: ok={reply.get('ok')} success={reply.get('success')}")
            except EOFError:
                self.log("client connection closed before a full request was received")
            except Exception:
                error_text = traceback.format_exc()
                try:
                    conn.send({"ok": False, "error": error_text})
                except Exception:
                    pass
                self.log(f"accept-loop error:\n{error_text}")
                print(f"[server] accept-loop error:\n{error_text}", flush=True)
            finally:
                try:
                    conn.close()
                except Exception:
                    pass


def main() -> int:
    parser = argparse.ArgumentParser(description="persistent local-txt2img server")
    parser.add_argument(
        "--log",
        type=str,
        default=None,
        help="append debug logs to this file",
    )
    args = parser.parse_args()

    server = Server(log_path=_normalize_log_path(args.log))
    server.log(f"server starting with argv={sys.argv[1:]}")
    try:
        server.listener = Listener(PIPE_ADDRESS, family="AF_PIPE", authkey=AUTHKEY)
    except OSError as e:
        server.log(f"bind failed: {e}")
        print(f"[server] bind failed: {e}", flush=True)
        return 2

    server.log(f"listener ready on {PIPE_ADDRESS}")
    server.log("kicking off background runtime init")
    server._start_init_thread()
    print(
        f"local-txt2img server listening on {PIPE_ADDRESS} (pid={os.getpid()}, "
        f"version={SERVER_VERSION})",
        flush=True,
    )

    worker = threading.Thread(target=server.serve_forever, name="accept-loop", daemon=True)
    worker.start()

    try:
        while not server.shutdown_event.wait(timeout=0.5):
            if not worker.is_alive():
                server.log("accept-loop thread exited unexpectedly")
                return 1
    finally:
        try:
            if server.listener is not None:
                server.listener.close()
        except Exception:
            pass

    worker.join(timeout=server.shutdown_timeout)
    if worker.is_alive():
        server.log(
            f"worker did not finish within {server.shutdown_timeout:.1f}s; forcing exit"
        )
        print(
            f"[server] worker did not finish within {server.shutdown_timeout:.1f}s; forcing exit",
            flush=True,
        )
        os._exit(1)
    server.log("server exited cleanly")
    return 0


if __name__ == "__main__":
    sys.exit(main())
