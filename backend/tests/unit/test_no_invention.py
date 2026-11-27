"""No invented metrics tests (US2, SC-001)."""

from __future__ import annotations

from uaicp.evaluation.evaluator import evaluate


def test_unknown_dimensions_are_not_zero():
    result = evaluate("tool:1", evidence={})
    for dim in result.dimensions.values():
        assert dim.value is None  # never 0, never fabricated


def test_inferred_value_is_flagged_verify():
    result = evaluate("tool:1", evidence={"cost": {"value": 0.5, "mark": "INFERRED"}})
    assert result.dimensions["cost"].verify is True