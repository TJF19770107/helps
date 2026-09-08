"""Watchdog for the local-tts server.

Polls the process list for the host claw (e.g. WorkBuddy / openclaw /
Marvis). When the claw disappears, sends a ``shutdown`` request to the
server over the named pipe so OpenVINO DLLs and GPU memory are released.
"""

import argparse
import logging
import os
import time
from datetime import datetime
from multiprocessing.connection import Client
from pathlib import Path

import psutil

PIPE_ADDRESS = r"\\.\pipe\tts"
AUTHKEY = b"tts-local"
CHECK_INTERVAL_SECONDS = 30.0
SERVER_SHUTDOWN_TIMEOUT = 10.0
SHUTDOWN_REPLY_TIMEOUT = 5.0

log = logging.getLogger("tts-server-dog")


def _setup_logging() -> None:
    log_dir = Path.home() / ".openvino" / "log"
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = log_dir / f"tts-server-dog-py-{timestamp}.log"

    handler = logging.FileHandler(log_file, encoding="utf-8")
    handler.setFormatter(
        logging.Formatter("%(asctime)s  %(levelname)-8s  %(message)s")
    )
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)
    log.info("logging to %s", log_file)


def _iter_command_lines():
    my_pid = os.getpid()
    for proc in psutil.process_iter(["cmdline"], ad_value=None):
        if proc.pid == my_pid:
            continue
        try:
            cmdline = proc.info.get("cmdline")
        except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess) as exc:
            log.debug("skipped pid %s: %s", proc.pid, exc)
            continue
        if not cmdline:
            continue
        if isinstance(cmdline, str):
            yield cmdline
        else:
            yield " ".join(str(part) for part in cmdline if part)


def _shutdown_server() -> None:
    log.info("attempting to shut down server via %s", PIPE_ADDRESS)
    try:
        conn = Client(PIPE_ADDRESS, authkey=AUTHKEY)
    except (FileNotFoundError, OSError) as exc:
        log.info("server pipe not available, skip shutdown: %s", exc)
        return

    try:
        conn.send({"op": "shutdown", "timeout": SERVER_SHUTDOWN_TIMEOUT})
        if conn.poll(SHUTDOWN_REPLY_TIMEOUT):
            reply = conn.recv()
            log.info("shutdown reply: %s", reply)
        else:
            log.warning("no reply within %.1fs", SHUTDOWN_REPLY_TIMEOUT)
    except (EOFError, OSError) as exc:
        log.warning("error during shutdown handshake: %s", exc)
    finally:
        conn.close()
        log.info("shutdown request completed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claw-name", required=True)
    args = parser.parse_args()
    keyword = args.claw_name.casefold()

    _setup_logging()
    log.info("started – watching for keyword %r", keyword)

    def is_running() -> bool:
        return any(keyword in cmdline.casefold() for cmdline in _iter_command_lines())

    if not is_running():
        log.info("target process not found on initial check, shutting down server")
        _shutdown_server()
        return 0

    log.info("target process is running, entering watch loop (interval=%.0fs)", CHECK_INTERVAL_SECONDS)
    while True:
        time.sleep(CHECK_INTERVAL_SECONDS)
        if is_running():
            log.debug("target process still alive")
            continue
        log.info("target process gone, shutting down server")
        _shutdown_server()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
