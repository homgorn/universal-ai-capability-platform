"""Contract tests for contract validation (US1, FR-001/FR-002/FR-009)."""

from __future__ import annotations

from uaicp.validation import validate_contract

VALID = {
    "inputs": [
        {
            "name": "image",
            "required": True,
            "semantic_type": "image",
            "transport_type": "bytes",
            "schema": {"type": "string"},
        }
    ],
    "outputs": [
        {
            "name": "image",
            "required": True,
            "semantic_type": "image",
            "transport_type": "bytes",
            "schema": {"type": "string"},
        }
    ],
}


def test_valid_contract_passes():
    result = validate_contract(VALID)
    assert result.valid, result.errors
    assert result.errors == []


def test_missing_semantic_type_fails():
    bad = {"inputs": [{"name": "x", "required": True, "transport_type": "bytes"}], "outputs": []}
    result = validate_contract(bad)
    assert not result.valid
    assert any("semantic_type" in e for e in result.errors)


def test_invalid_json_schema_fails():
    bad = {
        "inputs": [
            {"name": "x", "required": True, "semantic_type": "text", "transport_type": "string",
             "schema": {"type": "nonsense"}}
        ],
        "outputs": [],
    }
    result = validate_contract(bad)
    assert not result.valid
    assert any("JSON Schema" in e for e in result.errors)


def test_sensitive_without_artifact_type_warns():
    c = {
        "inputs": [
            {"name": "doc", "required": True, "semantic_type": "document",
             "transport_type": "bytes", "sensitive": True}
        ],
        "outputs": [],
    }
    result = validate_contract(c)
    assert result.valid
    assert any("artifact_type" in w for w in result.warnings)