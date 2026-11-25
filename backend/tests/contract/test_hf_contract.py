"""Gradio/OpenAPI contract extraction tests (US3)."""

from __future__ import annotations

from uaicp.ingestion.contract import extract_from_agents_md, extract_from_openapi

SCHEMA = {
    "paths": {
        "/predict": {
            "post": {
                "requestBody": {"content": {"image/png": {"schema": {"type": "string"}}}},
                "responses": {"200": {"content": {"image/png": {"schema": {"type": "string"}}}}},
            }
        }
    }
}


def test_openapi_extracts_canonical_ports():
    result = extract_from_openapi(SCHEMA)
    assert len(result["inputs"]) == 1
    assert len(result["outputs"]) == 1
    assert result["inputs"][0]["semantic_type"] == "image"
    assert result["inputs"][0]["transport_type"] == "HTTP_REST"
    assert len(result["fingerprint"]) == 64


def test_fingerprint_is_stable():
    assert extract_from_openapi(SCHEMA)["fingerprint"] == extract_from_openapi(SCHEMA)["fingerprint"]


def test_agents_md_capabilities():
    result = extract_from_agents_md("# Demo\n\n- remove background\n- upscale image\n")
    assert result["capabilities"] == ["remove background", "upscale image"]