"""Profile ranking over evidence-marked evaluations (SPECS.md §8).

Missing dimensions are ignored, never scored as zero. Candidates with no usable
dimension are returned as VERIFY, not ranked.
"""

from __future__ import annotations

from dataclasses import dataclass

from uaicp.domain.enums import EvidenceMark
from uaicp.evaluation.evaluator import Evaluation

PROFILES = (
    "QUALITY_FIRST",
    "BALANCED",
    "CHEAPEST_VALID",
    "LOW_LATENCY",
    "PRIVATE",
    "SELF_HOSTED",
)

# dimension -> weight per profile; missing dimensions are skipped, not zeroed.
_WEIGHTS: dict[str, dict[str, float]] = {
    "QUALITY_FIRST": {"quality": 0.7, "safety": 0.2, "reliability": 0.1},
    "BALANCED": {"quality": 0.3, "reliability": 0.2, "latency": 0.2, "cost": 0.2, "safety": 0.1},
    "CHEAPEST_VALID": {"cost": 0.8, "quality": 0.2},
    "LOW_LATENCY": {"latency": 0.8, "reliability": 0.2},
    "PRIVATE": {"safety": 0.6, "quality": 0.4},
    "SELF_HOSTED": {"safety": 0.5, "quality": 0.3, "cost": 0.2},
}

# Profiles that require a redistributable license.
REDISTRIBUTABLE = {"PRIVATE", "SELF_HOSTED"}


@dataclass
class Ranked:
    tool_id: str
    score: float | None
    verify: bool
    reason: str = ""


def _score(evaluation: Evaluation, profile: str) -> tuple[float | None, bool, str]:
    weights = _WEIGHTS[profile]
    total = 0.0
    used = 0.0
    for name, weight in weights.items():
        dim = evaluation.dimensions.get(name)
        if dim is None or dim.value is None or dim.mark is EvidenceMark.INFERRED:
            continue
        # Normalize latency/cost so lower is better.
        value = dim.value
        if name in ("latency", "cost"):
            value = 1.0 / (1.0 + max(value, 0.0))
        total += weight * value
        used += weight
    if used == 0:
        return None, True, "no usable evidence"
    if profile in REDISTRIBUTABLE and (evaluation.license or "unknown") == "unknown":
        return None, True, "license unknown"
    return total / used, False, ""


def rank(evaluations: list[Evaluation], profile: str) -> list[Ranked]:
    if profile not in PROFILES:
        raise ValueError(f"unknown profile {profile}")
    out = []
    for evaluation in evaluations:
        score, verify, reason = _score(evaluation, profile)
        out.append(Ranked(evaluation.tool_id, score, verify, reason))
    # Ranked first by score desc; VERIFY last, stable by tool_id.
    return sorted(
        out,
        key=lambda r: (r.verify, -(r.score or 0.0), r.tool_id),
    )