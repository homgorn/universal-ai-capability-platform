"""Embeddability classification for HF Spaces (SPECS.md §2, §15).

Measured sample 2026-11-27: /api/spaces?limit=20 returns only id/_id/likes/
trendingScore/private/sdk/tags — no `runtime` or `subdomain`. Therefore most
embed URLs must be derived and verified live; `runtime` can be requested with
`expand[]=runtime` for a subset.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

EMBED_IPS = re.compile(r"^\d+\.\d+\.\d+\.\d+$")


@dataclass(frozen=True)
class EmbedInfo:
    subdomain: str | None
    embed_url: str | None
    web_component: bool
    status: str  # EMBEDDABLE | VERIFY | NOT_EMBEDDABLE
    reason: str


def embed_info(resource: dict) -> EmbedInfo:
    """Classify a Space for iframe/Web Component embedding.

    A Space is a candidate only if it is public and its SDK is gradio (Web
    Component) or static/docker with a resolvable subdomain. Private Spaces and
    unknown runtimes stay VERIFY — never claimed embeddable.
    """
    if resource.get("private"):
        return EmbedInfo(None, None, False, "NOT_EMBEDDABLE", "private space")

    subdomain = resource.get("subdomain")
    sdk = (resource.get("sdk") or "").lower()
    runtime = resource.get("runtime") or {}
    stage = (runtime.get("stage") or "").upper() if isinstance(runtime, dict) else ""

    if not subdomain:
        # Try to derive from id only when it is a simple slug.
        space_id = resource.get("id", "")
        if space_id and "/" in space_id and " " not in space_id:
            derived = space_id.replace("/", "-").lower()
            if not EMBED_IPS.match(derived):
                subdomain = derived
    if not subdomain:
        return EmbedInfo(None, None, False, "VERIFY", "subdomain not resolvable from catalog")

    embed_url = f"https://{subdomain}.hf.space"
    if stage and stage not in ("RUNNING", "RUNNING_BUILDING", "APP_STARTING"):
        return EmbedInfo(subdomain, embed_url, sdk == "gradio", "VERIFY", f"runtime stage {stage}")

    if sdk == "gradio":
        return EmbedInfo(subdomain, embed_url, True, "EMBEDDABLE", "public gradio space")
    if sdk in ("static", "docker"):
        return EmbedInfo(subdomain, embed_url, False, "EMBEDDABLE", f"public {sdk} space")
    return EmbedInfo(subdomain, embed_url, False, "VERIFY", f"sdk {sdk or 'unknown'}")