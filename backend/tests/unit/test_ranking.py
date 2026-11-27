"""Profile ranking tests (US3, SC-003, SC-004)."""

from __future__ import annotations

from uaicp.evaluation.evaluator import evaluate
from uaicp.evaluation.ranking import rank


def _ev(tool_id: str, **evidence) -> object:
    return evaluate(tool_id, evidence=evidence)


def test_missing_dimensions_do_not_score_as_zero():
    a = _ev("a", quality={"value": 0.9, "mark": "MEASURED"})
    b = _ev("b", quality={"value": 0.9, "mark": "MEASURED"}, latency={"value": 10, "mark": "MEASURED"})
    ranked = rank([a, b], "QUALITY_FIRST")
    assert ranked[0].score is not None
    assert all(not r.verify for r in ranked)


def test_all_unknown_is_verify_last():
    ranked = rank([_ev("a")], "BALANCED")
    assert ranked[0].verify is True
    assert ranked[0].score is None


def test_unknown_license_excluded_from_private_profile():
    a = _ev("a", quality={"value": 1, "mark": "MEASURED"}, safety={"value": 1, "mark": "MEASURED"})
    ranked = rank([a], "PRIVATE")
    assert ranked[0].verify is True
    assert "license" in ranked[0].reason


def test_ranking_is_stable():
    evals = [
        _ev("a", quality={"value": 0.8, "mark": "MEASURED"}),
        _ev("b", quality={"value": 0.5, "mark": "MEASURED"}),
    ]
    assert [r.tool_id for r in rank(evals, "QUALITY_FIRST")] == [r.tool_id for r in rank(evals, "QUALITY_FIRST")]