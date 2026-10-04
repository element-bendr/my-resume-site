from __future__ import annotations

import os
import tempfile
from pathlib import Path


class RepositoryPathError(ValueError):
    pass


def safe_repo_path(root: Path, relative: str | Path) -> Path:
    root = Path(root).resolve()
    relative_path = Path(relative)
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise RepositoryPathError(f"unsafe repository-relative path: {str(relative)!r}")
    candidate = (root / relative_path).resolve()
    if candidate != root and root not in candidate.parents:
        raise RepositoryPathError(f"path escapes repository root: {str(relative)!r}")
    return candidate


def fsync_directory(path: Path) -> None:
    if os.name == "nt":
        return
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    fd = os.open(Path(path), flags)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic_write_text(path: Path, content: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
        fsync_directory(path.parent)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise
