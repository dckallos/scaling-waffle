#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
from pathlib import Path, PurePosixPath
from zipfile import ZipFile


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Populate a directory from a local zip archive.",
    )
    parser.add_argument("zip_file", type=Path, help="Path to the local zip archive.")
    parser.add_argument(
        "--destination",
        type=Path,
        default=Path.cwd(),
        help="Directory to populate. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--strip-components",
        type=int,
        default=0,
        help="Number of leading path components to remove from archive entries.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files in the destination.",
    )
    return parser.parse_args()


def sanitize_member(name: str, strip_components: int) -> Path | None:
    raw_path = PurePosixPath(name)
    if raw_path.is_absolute():
        raise ValueError(f"Refusing to extract unsafe absolute path: {name}")

    parts = [part for part in raw_path.parts if part not in ("", ".")]

    if len(parts) <= strip_components:
        return None

    parts = parts[strip_components:]
    if any(part == ".." for part in parts):
        raise ValueError(f"Refusing to extract unsafe path: {name}")
    if parts and parts[0].endswith(":"):
        raise ValueError(f"Refusing to extract unsafe drive path: {name}")
    if parts and parts[0] == ".git":
        return None

    return Path(*parts)


def extract_archive(
    zip_file: Path,
    destination: Path,
    strip_components: int = 0,
    force: bool = False,
) -> int:
    if strip_components < 0:
        raise ValueError("--strip-components must be zero or greater")
    if not zip_file.is_file():
        raise FileNotFoundError(f"Zip file not found: {zip_file}")

    destination.mkdir(parents=True, exist_ok=True)
    extracted = 0

    with ZipFile(zip_file) as archive:
        for member in archive.infolist():
            relative_path = sanitize_member(member.filename, strip_components)
            if relative_path is None:
                continue

            target_path = destination / relative_path

            if member.is_dir():
                target_path.mkdir(parents=True, exist_ok=True)
                continue

            if target_path.exists() and not force:
                raise FileExistsError(
                    f"Refusing to overwrite existing file without --force: {target_path}"
                )

            target_path.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(member) as source, target_path.open("wb") as target:
                shutil.copyfileobj(source, target)

            extracted += 1

    return extracted


def main() -> int:
    args = parse_args()
    extracted = extract_archive(
        zip_file=args.zip_file,
        destination=args.destination,
        strip_components=args.strip_components,
        force=args.force,
    )
    print(f"Extracted {extracted} file(s) into {args.destination.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
