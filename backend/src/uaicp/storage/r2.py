"""R2 backend stub — active once R2 is enabled and configured (ADR-005)."""

from __future__ import annotations

import os

from uaicp.storage.base import StoredArtifact


class R2Store:
    """S3-compatible R2 backend. Disabled until R2 is enabled on the account."""

    def __init__(self, bucket: str | None = None) -> None:
        self.bucket = bucket or os.getenv("R2_BUCKET", "")
        self.enabled = bool(self.bucket) and os.getenv("R2_ACCESS_KEY_ID") is not None

    def put(self, key: str, data: bytes, mime: str, max_bytes: int) -> StoredArtifact:
        if not self.enabled:
            raise RuntimeError("R2 is not enabled; set R2_BUCKET and R2 credentials (ADR-005)")
        raise NotImplementedError("R2 upload activates after R2 is enabled on the account")

    def get(self, storage_uri: str) -> bytes:
        raise NotImplementedError("R2 download activates after R2 is enabled")


def is_r2_configured() -> bool:
    return R2Store().enabled