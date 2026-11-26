"""Gradio info -> canonical ports tests (US2)."""

from __future__ import annotations

from uaicp.toolcontract.gradio import ports_from_info

INFO = {
    "named_endpoints": {
        "/predict": {
            "parameters": [
                {"parameter_name": "image", "type": "file", "required": True},
                {"parameter_name": "prompt", "type": "string", "required": False},
            ]
        }
    }
}


def test_ports_from_info():
    ports = ports_from_info(INFO)
    assert len(ports["inputs"]) == 2
    assert ports["inputs"][0]["semantic_type"] == "binary"
    assert ports["inputs"][1]["semantic_type"] == "text"
    assert ports["outputs"][0]["transport_type"] == "GRADIO"


def test_unknown_info_returns_empty():
    assert ports_from_info({"named_endpoints": []}) == {"inputs": [], "outputs": []}