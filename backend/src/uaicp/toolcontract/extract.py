"""Assemble a candidate Tool contract without executing provider code."""

from __future__ import annotations

from collections.abc import Callable
from enum import Enum

from uaicp.toolcontract.agents import parse_agents_md
from uaicp.toolcontract.gradio import ports_from_info
from uaicp.validation.fingerprint import canonical_fingerprint

Fetcher = Callable[[str], object]


class ContractStatus(str, Enum):
    VERIFIED = "VERIFIED"
    UNKNOWN = "UNKNOWN"


def extract_contract(
    fetcher: Fetcher,
    space_id: str,
    *,
    subdomain: str | None = None,
) -> dict:
    """Fetch agents.md + info + MCP schema and build a candidate contract."""
    source_url = f"https://huggingface.co/spaces/{space_id}/agents.md"
    agents = None
    try:
        text = fetcher(source_url)
        if isinstance(text, str) and text.strip():
            agents = parse_agents_md(text, source_url).as_dict()
    except Exception:
        agents = None

    ports: dict[str, list] = {"inputs": [], "outputs": []}
    info_url = None
    if subdomain:
        info_url = f"https://{subdomain}.hf.space/gradio_api/info"
        try:
            info = fetcher(info_url)
            if isinstance(info, dict):
                ports = ports_from_info(info)
        except Exception:
            ports = {"inputs": [], "outputs": []}

    mcp_url = None
    mcp_found = False
    if subdomain:
        mcp_url = f"https://{subdomain}.hf.space/gradio_api/mcp/schema"
        try:
            mcp = fetcher(mcp_url)
            mcp_found = isinstance(mcp, dict) and bool(mcp.get("tools"))
        except Exception:
            mcp_found = False

    inputs, outputs = ports["inputs"], ports["outputs"]
    status = ContractStatus.VERIFIED if inputs else ContractStatus.UNKNOWN
    return {
        "status": status.value,
        "space_id": space_id,
        "agents": agents,
        "ports": ports,
        "fingerprint": canonical_fingerprint(inputs, outputs),
        "mcp": {"url": mcp_url, "found": mcp_found},
        "source_urls": [u for u in (source_url, info_url) if u],
        "executed_provider_code": False,
    }