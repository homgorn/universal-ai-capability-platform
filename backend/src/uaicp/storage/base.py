"""Artifact storage backends (SPECS.md §11, ADR-005)."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


class ArtifactTooLarge(ValueError):
    pass


class ArtifactUnsafe(ValueError):
    pass


@dataclass
class StoredArtifact:
    storage_uri: str
    size: int
    hash: str


class ArtifactStore(Protocol):
    def put(self, key: str, data: bytes, mime: str, max_bytes: int) -> StoredArtifact: ...
    def get(self, storage_uri: str) -> bytes: ...


class LocalStore:
    """Filesystem backend for dev/tests. Production uses R2Store."""

    def __init__(self, root: str | Path, *, base_uri: str = "file://") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.base_uri = base_uri

    def put(self, key: str, data: bytes, mime: str, max_bytes: int) -> StoredArtifact:
        if len(data) > max_bytes:
            raise ArtifactTooLarge(f"{len(data)} > {max_bytes}")
        digest = hashlib.sha256(data).hexdigest()
        path = self.root / key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return StoredArtifact(f"{self.base_uri}{path.as_posix()}", len(data), f"sha256:{digest}")

    def get(self, storage_uri: str) -> bytes:
        path = Path(storage_uri.removeprefix("file://"))
        return path.read_bytes()


def verify_hash(data: bytes, expected: str) -> bool:
    return f"sha256:{hashlib.sha256(data).hexdigest()}" == expected