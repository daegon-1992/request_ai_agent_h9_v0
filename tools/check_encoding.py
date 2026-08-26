#!/usr/bin/env python3
"""Check project text files for UTF-8 decoding errors and mojibake."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


TARGET_SUFFIXES = {
    ".py",
    ".html",
    ".css",
    ".js",
    ".json",
    ".md",
    ".txt",
    ".yml",
    ".yaml",
}
EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    ".mypy_cache",
    ".pytest_cache",
}
# Escape the signatures so this checker does not flag its own pattern table.
MOJIBAKE_PATTERNS = (
    "\u00ed\u2022",
    "\u00ed\u017d",
    "\u00ea\u00b8",
    "\u00ec\u201e",
    "\u00ec\u2014",
    "\u00ec\u017e",
    "\u00ec\u0153",
    "\u00eb\u2039",
    "\u00eb\u00a5",
    "\u00c3",
    "\u00c2",
    "\ufffd",
)


def is_target(path: Path) -> bool:
    return (
        path.suffix.lower() in TARGET_SUFFIXES
        and not any(part in EXCLUDED_DIRS or "pycache" in part.lower() for part in path.parts)
    )


def changed_files(root: Path) -> list[Path]:
    """Return tracked changes (staged or unstaged) plus untracked files."""
    commands = (
        ["git", "diff", "--name-only", "--relative", "-z", "HEAD", "--", "."],
        ["git", "ls-files", "--others", "--exclude-standard", "-z", "--", "."],
    )
    names: set[str] = set()
    for command in commands:
        try:
            result = subprocess.run(command, cwd=root, check=True, capture_output=True)
        except FileNotFoundError as exc:
            raise RuntimeError("git command was not found; use --all or install Git.") from exc
        except subprocess.CalledProcessError as exc:
            detail = exc.stderr.decode("utf-8", "replace").strip() or "Git command failed"
            raise RuntimeError(f"could not list changed files: {detail}") from exc
        names.update(name for name in result.stdout.decode("utf-8", "strict").split("\0") if name)
    return sorted((root / name for name in names if is_target(Path(name))), key=lambda path: str(path))


def all_files(root: Path) -> list[Path]:
    return sorted((path for path in root.rglob("*") if path.is_file() and is_target(path)), key=lambda path: str(path))


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def check_file(path: Path, root: Path) -> list[str]:
    relative = path.relative_to(root)
    try:
        text = path.read_text(encoding="utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        return [f"{relative}:{exc.start + 1}: UTF-8 decode error: {exc.reason}"]

    errors: list[str] = []
    for pattern in MOJIBAKE_PATTERNS:
        start = 0
        while (index := text.find(pattern, start)) != -1:
            errors.append(f"{relative}:{line_number(text, index)}: suspicious encoding pattern {pattern!r}")
            start = index + len(pattern)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check text files for UTF-8 encoding problems.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--changed", action="store_true", help="check Git-changed and untracked files (default)")
    mode.add_argument("--all", action="store_true", help="check all target files")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    files = all_files(root) if args.all else changed_files(root)
    # Deleted files appear in Git's changed-file list but no longer exist to inspect.
    errors = [error for path in files if path.exists() for error in check_file(path, root)]
    if errors:
        print("Encoding check failed:", file=sys.stderr)
        print("\n".join(errors), file=sys.stderr)
        return 1

    print("Encoding check passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"Encoding check failed: {exc}", file=sys.stderr)
        raise SystemExit(2)
