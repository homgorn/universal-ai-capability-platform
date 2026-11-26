"""agents.md parsing tests (US1)."""

from __future__ import annotations

from uaicp.toolcontract.agents import parse_agents_md

TEXT = """
# Tool

Schema: https://demo.hf.space/gradio_api/openapi.json
Call: POST https://demo.hf.space/gradio_api/call/predict
Poll: GET https://demo.hf.space/gradio_api/queue/data
Upload a file to the endpoint using multipart.
Authorization: Bearer <HF_TOKEN>
"""


def test_agents_parses_endpoints_and_hints():
    result = parse_agents_md(TEXT, "https://huggingface.co/spaces/demo/app/agents.md")
    assert any("openapi" in u for u in result.schema_urls)
    assert any("/call/predict" in u for u in result.call_endpoints)
    assert any("queue/data" in u for u in result.poll_endpoints)
    assert result.upload_hints and result.auth_hints
    assert result.source_url.endswith("agents.md")