# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: Intel OBL

"""One-shot local ASR client.

Each invocation:
  1. Ensures the Qwen3-ASR OpenVINO model is present under
     ``%USERPROFILE%\\.openvino\\models\\Qwen3-ASR-0.6B-fp16-ov``.
     If it is missing, a detached background worker is spawned to download it
     via ModelScope and the client polls for completion for up to
     ``DOWNLOAD_WAIT_TIMEOUT`` seconds. If the download is still in progress
     when the timeout elapses, the client records a pending request and exits
     with code 3 so the caller can retry with ``--continue``.
  2. Extracts audio from video inputs when needed (ffmpeg -> moviepy fallback).
  3. Loads the model, transcribes the file, prints a JSON result, exits.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

OPENVINO_ROOT = Path(os.environ.get("USERPROFILE", str(Path.home()))) / ".openvino"
MODELS_ROOT = OPENVINO_ROOT / "models"
LOG_ROOT = OPENVINO_ROOT / "log"
PENDING_REQUEST_PATH = OPENVINO_ROOT / "asr-pending-request.json"
MODEL_ID = "snake7gun/Qwen3-ASR-0.6B-fp16-ov"
MODEL_DIR = MODELS_ROOT / "Qwen3-ASR-0.6B-fp16-ov"
DOWNLOAD_MARKER = MODELS_ROOT / ".asr-download.lock"

DOWNLOAD_WAIT_TIMEOUT = 8 * 60.0
DOWNLOAD_POLL_INTERVAL = 2.0

REQUIRED_MODEL_FILES = (
    "config.json",
    "thinker/openvino_thinker_language_model.bin",
    "thinker/openvino_thinker_audio_encoder_model.bin",
    "thinker/openvino_thinker_audio_model.bin",
    "thinker/openvino_thinker_embedding_model.bin",
)

AUDIO_FORMATS = {".wav", ".mp3", ".flac", ".m4a", ".ogg", ".aac", ".wma", ".opus"}
VIDEO_FORMATS = {".mp4", ".mkv", ".webm", ".flv", ".mov", ".avi", ".mts", ".m2ts", ".ts", ".m3u8"}


def _has_glob_pattern(value: str) -> bool:
    return any(char in value for char in "*?[")


def _expand_audio_inputs(audio_spec: str) -> list[Path]:
    resolved_paths: list[Path] = []
    seen_paths: set[str] = set()

    for raw_item in audio_spec.split(";"):
        item = raw_item.strip().strip('"')
        if not item:
            continue

        if _has_glob_pattern(item):
            matches = sorted(glob.glob(item))
            if not matches:
                raise FileNotFoundError(f"No files matched pattern: {item}")
            candidates = [Path(match) for match in matches]
        else:
            candidates = [Path(item).expanduser()]

        for candidate in candidates:
            resolved = candidate.resolve()
            key = os.path.normcase(str(resolved)) if os.name == "nt" else str(resolved)
            if key in seen_paths:
                continue
            seen_paths.add(key)
            resolved_paths.append(resolved)

    if not resolved_paths:
        raise ValueError("No input files were provided")

    return resolved_paths


def _configure_stream_encoding(stream, *, line_buffering: bool = False) -> None:
    reconfigure = getattr(stream, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(
            encoding="utf-8",
            errors="replace",
            line_buffering=line_buffering,
        )


_configure_stream_encoding(sys.stdout, line_buffering=True)
_configure_stream_encoding(sys.stderr)
os.environ.setdefault("PYTHONUTF8", "1")


def _normalize_log_path(log_path: Optional[str]) -> Path:
    if not log_path:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        log_path = str(LOG_ROOT / f"asr-client-py-{timestamp}.log")
    path = Path(log_path).expanduser()
    return path if path.is_absolute() else Path.cwd() / path


def _log(log_path: Path, message: str) -> None:
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as stream:
            stamp = time.strftime("%Y-%m-%d %H:%M:%S")
            stream.write(f"[{stamp}] [asr pid={os.getpid()}] {message}\n")
    except OSError:
        pass


def _model_complete(model_dir: Path) -> bool:
    from model_download_template import validate_model_dir
    return validate_model_dir(model_dir, REQUIRED_MODEL_FILES).ok


def _save_pending_request(audio_path: str, language: str, log_path: Path) -> None:
    try:
        PENDING_REQUEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "audio": audio_path,
            "language": language,
            "saved_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "log_path": str(log_path),
        }
        PENDING_REQUEST_PATH.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        _log(log_path, f"saved pending request -> {PENDING_REQUEST_PATH}")
    except OSError as exc:
        _log(log_path, f"failed to save pending request: {exc}")


def _load_pending_request() -> Optional[dict]:
    try:
        text = PENDING_REQUEST_PATH.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError):
        return None
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict) or "audio" not in data:
        return None
    return data


def _delete_pending_request(log_path: Path) -> None:
    try:
        PENDING_REQUEST_PATH.unlink()
        _log(log_path, f"deleted pending request at {PENDING_REQUEST_PATH}")
    except FileNotFoundError:
        pass
    except OSError as exc:
        _log(log_path, f"failed to delete pending request: {exc}")


def _hidden_startupinfo():
    if os.name != "nt" or not hasattr(subprocess, "STARTUPINFO"):
        return None
    info = subprocess.STARTUPINFO()
    info.dwFlags |= getattr(subprocess, "STARTF_USESHOWWINDOW", 0)
    info.wShowWindow = getattr(subprocess, "SW_HIDE", 0)
    return info


def _pythonw_executable() -> str:
    python_exe = Path(sys.executable)
    pythonw_exe = python_exe.with_name("pythonw.exe")
    return str(pythonw_exe) if pythonw_exe.exists() else str(python_exe)


def _download_worker_running() -> bool:
    if not DOWNLOAD_MARKER.exists():
        return False
    try:
        text = DOWNLOAD_MARKER.read_text(encoding="utf-8").strip()
        pid = int(text)
    except (OSError, ValueError):
        return False
    try:
        import psutil
        return psutil.pid_exists(pid)
    except ImportError:
        return True


def _spawn_download_worker(log_path: Path) -> None:
    MODELS_ROOT.mkdir(parents=True, exist_ok=True)
    creationflags = (
        getattr(subprocess, "CREATE_NO_WINDOW", 0)
        | getattr(subprocess, "DETACHED_PROCESS", 0)
        | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    )
    command = [
        _pythonw_executable(),
        str(Path(__file__).resolve()),
        "--download-worker",
        "--log", str(log_path),
    ]
    worker = subprocess.Popen(
        command,
        creationflags=creationflags,
        startupinfo=_hidden_startupinfo(),
        close_fds=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=str(OPENVINO_ROOT),
    )
    try:
        DOWNLOAD_MARKER.write_text(str(worker.pid), encoding="utf-8")
    except OSError as exc:
        _log(log_path, f"failed to record spawned worker pid: {exc}")
    _log(log_path, f"spawned detached download worker pid={worker.pid}")


def _run_download_worker(log_path: Path) -> int:
    MODELS_ROOT.mkdir(parents=True, exist_ok=True)
    try:
        DOWNLOAD_MARKER.write_text(str(os.getpid()), encoding="utf-8")
    except OSError as exc:
        _log(log_path, f"download worker failed to write marker: {exc}")
        return 1
    try:
        from modelscope import snapshot_download
        from model_download_template import (
            ModelDownloadTemplate,
            download_required_model,
        )
        template = ModelDownloadTemplate(
            models_root=MODELS_ROOT,
            required_files=REQUIRED_MODEL_FILES,
        )
        _log(log_path, f"download worker starting: {MODEL_ID}")
        download_required_model(
            model_id=MODEL_ID,
            local_dir=MODEL_DIR,
            snapshot_download=snapshot_download,
            template=template,
            logger=lambda msg: _log(log_path, f"[dl] {msg}"),
        )
        _log(log_path, "download worker finished successfully")
        return 0
    except Exception as exc:
        import traceback
        _log(log_path, f"download worker FAILED: {type(exc).__name__}: {exc}")
        _log(log_path, traceback.format_exc())
        return 1
    finally:
        try:
            DOWNLOAD_MARKER.unlink()
        except FileNotFoundError:
            pass
        except OSError:
            pass


def _ensure_model(log_path: Path) -> str:
    """Return 'ready', 'downloading', or raise on hard failure."""
    if _model_complete(MODEL_DIR):
        _log(log_path, f"model already present at {MODEL_DIR}")
        return "ready"

    if not _download_worker_running():
        print(f"Model not found. Spawning background downloader for {MODEL_ID} (~2 GB).", flush=True)
        _log(log_path, "model missing; spawning worker")
        _spawn_download_worker(log_path)

    deadline = time.time() + DOWNLOAD_WAIT_TIMEOUT
    last_print = 0.0
    while time.time() < deadline:
        if _model_complete(MODEL_DIR):
            _log(log_path, "model became ready during poll")
            return "ready"
        if not _download_worker_running():
            if _model_complete(MODEL_DIR):
                return "ready"
            _log(log_path, "download worker exited without producing a complete model")
            raise RuntimeError("Download worker exited without producing a complete model. Re-run to retry.")
        now = time.time()
        if now - last_print > 15.0:
            remaining = int(deadline - now)
            print(f"Download in progress ... ({remaining}s left before timeout)", flush=True)
            last_print = now
        time.sleep(DOWNLOAD_POLL_INTERVAL)

    _log(log_path, "download still in progress at timeout")
    return "downloading"


def _pick_device(log_path: Path) -> str:
    import openvino as ov
    devices = ov.Core().available_devices
    _log(log_path, f"openvino devices: {devices}")
    for d in devices:
        if "GPU" in d:
            return d
    return "CPU"


def _extract_audio_from_video(video_path: Path, log_path: Path) -> Path:
    out_wav = video_path.parent / f"{video_path.stem}__asr_extracted.wav"
    _log(log_path, f"extracting audio: {video_path} -> {out_wav}")
   
    try:
        from moviepy import VideoFileClip
    except ImportError as exc:
        raise RuntimeError(
            "Cannot extract audio: moviepy not installed. "
            "Please run `uv pip install moviepy` into the ASR venv."
        ) from exc

    clip = VideoFileClip(str(video_path))
    try:
        if clip.audio is None:
            raise RuntimeError(f"Video has no audio track: {video_path}")
        clip.audio.write_audiofile(str(out_wav), logger=None)
    finally:
        clip.close()
    return out_wav


def _prepare_audio(file_path: Path, log_path: Path) -> tuple[Path, bool]:
    suffix = file_path.suffix.lower()
    if suffix in AUDIO_FORMATS:
        return file_path, False
    if suffix in VIDEO_FORMATS:
        return _extract_audio_from_video(file_path, log_path), True
    raise ValueError(f"Unsupported file format: {suffix}")


def _transcribe(audio_path: Path, language: Optional[str], log_path: Path) -> dict:
    device = _pick_device(log_path)
    print(f"Loading model on {device} ...", flush=True)
    _log(log_path, f"loading model on {device}")

    sys.path.insert(0, str(Path(__file__).parent))
    from asr_engine import OVQwen3ASRModel

    t0 = time.time()
    model = OVQwen3ASRModel.from_pretrained(str(MODEL_DIR), device=device)
    load_seconds = time.time() - t0
    _log(log_path, f"model loaded in {load_seconds:.2f}s")

    print(f"Transcribing {audio_path} ...", flush=True)
    t1 = time.time()
    results = model.transcribe(audio=str(audio_path), language=language)
    infer_seconds = time.time() - t1

    if not results:
        raise RuntimeError("Empty transcription result")

    return {
        "text": results[0].text,
        "language": results[0].language,
        "load_seconds": round(load_seconds, 3),
        "inference_seconds": round(infer_seconds, 3),
        "device": device,
    }


def _print_result(result: dict, index: int, total: int) -> None:
    if total == 1:
        print("\n=== RESULT ===")
    else:
        print(f"\n=== RESULT {index}/{total} ===")
    print(json.dumps(result, ensure_ascii=False, indent=2))


def _do_request(audio: str, language_arg: str, log_path: Path) -> int:
    file_paths = _expand_audio_inputs(audio)
    for file_path in file_paths:
        if not file_path.exists():
            _delete_pending_request(log_path)
            raise FileNotFoundError(f"Input file not found: {file_path}")

    language = None if language_arg.lower() in ("", "auto", "none", "null") else language_arg

    state = _ensure_model(log_path)
    if state == "downloading":
        _save_pending_request(audio, language_arg, log_path)
        print(
            "模型正在下载, 请用命令 `scripts\\client.bat --continue` 继续运行",
            flush=True,
        )
        _log(log_path, "exiting 3: download still in progress")
        return 3

    total = len(file_paths)
    exit_code = 0
    for index, file_path in enumerate(file_paths, start=1):
        if total > 1:
            print(f"\n=== INPUT {index}/{total} ===")
            print(str(file_path))

        try:
            audio_path, extracted = _prepare_audio(file_path, log_path)
            try:
                result = _transcribe(audio_path, language, log_path)
            finally:
                if extracted:
                    try:
                        audio_path.unlink()
                    except OSError:
                        pass
        except Exception:
            if total == 1:
                raise
            exit_code = 1
            import traceback
            details = traceback.format_exc()
            _log(log_path, f"failure for {file_path}: {details}")
            print(f"\n[ERROR] Failed to transcribe: {file_path}", file=sys.stderr)
            continue

        result["source_file"] = str(file_path)
        result["source_format"] = file_path.suffix.lower()
        _print_result(result, index, total)
        _log(log_path, f"success: lang={result['language']} chars={len(result['text'])} file={file_path}")

    _delete_pending_request(log_path)
    return exit_code


def _do_continue(log_path: Path) -> int:
    pending = _load_pending_request()
    if pending is None:
        print(
            "无待处理请求, 请先使用 `scripts\\client.bat \"<audio_path>\" [language]` 发起请求",
            file=sys.stderr,
            flush=True,
        )
        _log(log_path, "--continue invoked but no pending request found")
        return 1
    saved_audio = pending.get("audio", "")
    saved_language = pending.get("language", "auto")
    saved_log = pending.get("log_path")
    if saved_log:
        log_path = Path(saved_log).expanduser()
    _log(log_path, f"--continue resuming audio={saved_audio!r} language={saved_language!r}")
    return _do_request(saved_audio, saved_language, log_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Local Qwen3-ASR one-shot transcribe")
    parser.add_argument("--audio", help="path to audio or video file")
    parser.add_argument(
        "--language",
        default="auto",
        help="language hint (e.g. Chinese, English) or 'auto' for auto-detect",
    )
    parser.add_argument("--log", default=None, help="path to append debug log")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--continue",
        dest="cont",
        action="store_true",
        help="resume the last pending request (used after a download-timeout exit)",
    )
    group.add_argument(
        "--download-worker",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args()

    log_path = _normalize_log_path(args.log)
    _log(log_path, f"client.py started argv={sys.argv[1:]}")

    try:
        if args.download_worker:
            return _run_download_worker(log_path)
        if args.cont:
            return _do_continue(log_path)
        if not args.audio:
            print("--audio is required (or use --continue)", file=sys.stderr)
            return 2
        return _do_request(args.audio, args.language, log_path)
    except Exception as exc:
        import traceback
        _log(log_path, f"FAILURE: {type(exc).__name__}: {exc}")
        _log(log_path, traceback.format_exc())
        print(f"\n[ERROR] {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
