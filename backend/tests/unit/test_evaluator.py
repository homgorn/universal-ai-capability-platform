"""Evaluator tests (US1)."""

from __future__ import annotations

from uaicp.domain.enums import EvidenceMark
from uaicp.evaluation.evaluator import evaluate


def test_provided_evidence_becomes_value():
    result = evaluate(
        "tool:1",
        evidence={
            "quality": {"value": 0.9, "mark": "MEASURED"},
            "latency": {"value": 120, "mark": "MEASURED"},
        },
    )
    assert result.dimensions["quality"].value == 0.9
    assert result.dimensions["quality"].mark is EvidenceMark.MEASURED
    assert result.dimensions["quality"].verify is False


def test_missing_dimension_is_null_and_verify():
    result = evaluate("tool:1", evidence={})
    dim = result.dimensions["quality"]
    assert dim.value is None
    assert dim.verify is True
    assert dim.mark is EvidenceMark.INFERRED