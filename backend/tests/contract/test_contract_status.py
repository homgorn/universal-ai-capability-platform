"""Contract status and MCP detection tests (US3)."""

from __future__ import annotations

from uaicp.toolcontract.extract import extract_contract

INFO = {"named_endpoints": {"/predict": {"parameters": [{"parameter_name": "x", "type": "string"}]}}}


def test_verified_with_info_and_mcp():
    def fetcher(url):
        if url.endswith("agents.md"):
            return "# Tool\nhttps://demo.hf.space/gradio_api/openapi.json"
        if url.endswith("/info"):
            return INFO
        if url.endswith("mcp/schema"):
            return {"tools": [{"name": "predict"}]}
        return ""

    result = extract_contract(fetcher, "demo/app", subdomain="demo")
    assert result["status"] == "VERIFIED"
    assert result["mcp"]["found"] is True
    assert result["executed_provider_code"] is False


def test_missing_schema_is_unknown_not_active():
    result = extract_contract(lambda _u: "", "demo/app", subdomain="demo")
    assert result["status"] == "UNKNOWN"
    assert result["ports"]["inputs"] == []