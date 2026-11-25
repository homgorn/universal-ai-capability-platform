"""Contract tests for the validation CLI (US5, FR-010, SC-006)."""

from __future__ import annotations

import json

from uaicp.validation.cli import main

VALID = {
    "inputs": [
        {"name": "x", "required": True, "semantic_type": "text", "transport_type": "string"}
    ],
    "outputs": [],
}
INVALID = {"inputs": [{"name": "x", "required": True}], "outputs": []}


def _write(tmp_path, name, data):
    p = tmp_path / name
    p.write_text(json.dumps(data), encoding="utf-8")
    return str(p)


def test_cli_valid_exit_zero(tmp_path):
    assert main([_write(tmp_path, "ok.json", VALID)]) == 0


def test_cli_invalid_exit_nonzero(tmp_path):
    assert main([_write(tmp_path, "bad.json", INVALID)]) == 1