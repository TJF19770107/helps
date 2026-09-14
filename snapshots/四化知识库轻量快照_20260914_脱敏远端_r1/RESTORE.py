#!/usr/bin/env python3
"""Verify, inspect, or restore a four-knowledge-base lightweight snapshot."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path


MAPPINGS = {
    "obsidian_wiki": Path(r"G:\龙虾AI主控中心\Obsidian\wiki"),
    "skill_library": Path(
        r"E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v3.0"
    ),
    "avatar_entity": Path(
        r"E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v3.0"
        r"\我的AI分身\AI分身实体"
    ),
}

INFRA_MAPPINGS = {
    "infra/connector-proxy-relay.js": Path(
        r"C:\Users\Administrator\.workbuddy\connector-proxy-relay.js"
    ),
    "infra/connector-proxy-call.js": Path(
        r"C:\Users\Administrator\.workbuddy\connector-proxy-call.js"
    ),
    "infra/ima-upload-markdown.js": Path(
        r"C:\Users\Administrator\.workbuddy\ima-upload-markdown.js"
    ),
    "infra/lexiang-attach-zip.js": Path(
        r"C:\Users\Administrator\.workbuddy\lexiang-attach-zip.js"
    ),
    "infra/MEMORY.workbuddy.md": Path(
        r"C:\Users\Administrator\.workbuddy\MEMORY.md"
    ),
    "infra/MEMORY.workbuddy_data.md": Path(r"G:\WorkBuddy_Data\MEMORY.md"),
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_expected_hash(zip_path: Path) -> str | None:
    sha_path = Path(str(zip_path) + ".sha256")
    if not sha_path.exists():
        return None
    first_token = sha_path.read_text(encoding="utf-8").strip().split()
    return first_token[0].lower() if first_token else None


def iter_payload_files(root: Path):
    for name in MAPPINGS:
        base = root / name
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file():
                yield path

    for rel in INFRA_MAPPINGS:
        path = root / rel
        if path.is_file():
            yield path


def target_for(root: Path, payload_file: Path) -> Path | None:
    relative = payload_file.relative_to(root)
    parts = relative.parts
    if not parts:
        return None
    if parts[0] in MAPPINGS:
        return MAPPINGS[parts[0]] / Path(*parts[1:])
    relative_name = relative.as_posix()
    return INFRA_MAPPINGS.get(relative_name)


def verify(zip_path: Path, extracted: Path | None = None) -> int:
    actual = sha256_file(zip_path)
    expected = load_expected_hash(zip_path)
    print(f"zip={zip_path}")
    print(f"sha256={actual}")
    print(f"expected={expected or 'missing'}")
    if expected and actual != expected:
        print("status=hash_mismatch")
        return 2
    if extracted is None:
        with zipfile.ZipFile(zip_path) as archive:
            bad = archive.testzip()
            print(f"zip_test={'ok' if bad is None else bad}")
            print(f"entries={len(archive.infolist())}")
        print("status=ok")
        return 0
    files = list(iter_payload_files(extracted))
    print(f"payload_files={len(files)}")
    for path in files:
        target = target_for(extracted, path)
        print(f"{path.relative_to(extracted)} -> {target or 'unmapped'}")
    print("status=ok")
    return 0


def restore(zip_path: Path, apply: bool) -> int:
    verified = verify(zip_path)
    if verified != 0:
        return verified

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with tempfile.TemporaryDirectory(prefix="four_kb_restore_") as temp:
        root = Path(temp)
        with zipfile.ZipFile(zip_path) as archive:
            archive.extractall(root)

        payload_files = list(iter_payload_files(root))
        print(f"mode={'restore' if apply else 'dry-run'} payload_files={len(payload_files)}")

        backup_root = zip_path.parent / f"pre_restore_backup_{stamp}"
        for source in payload_files:
            target = target_for(root, source)
            if target is None:
                print(f"skip_unmapped={source.relative_to(root)}")
                continue
            print(f"{'restore' if apply else 'would_restore'} {source.relative_to(root)} -> {target}")
            if not apply:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                backup = backup_root / source.relative_to(root)
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target, backup)
            shutil.copy2(source, target)

        if apply:
            print(f"pre_restore_backup={backup_root}")
            print("status=restored")
        else:
            print("status=dry_run")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_path", type=Path)
    parser.add_argument("--restore", action="store_true")
    args = parser.parse_args()

    if not args.zip_path.is_file():
        parser.error(f"zip not found: {args.zip_path}")
    if args.restore:
        return restore(args.zip_path, apply=True)
    return verify(args.zip_path)


if __name__ == "__main__":
    raise SystemExit(main())
