"""Seven-dimension compatibility checking (SPECS.md §4, §8)."""

from __future__ import annotations

from uaicp.validation.fingerprint import Compatibility, classify_drift


def _max_size(contract: dict, direction: str) -> float | None:
    limits = contract.get("limits", {})
    value = limits.get(f"max_{direction}_bytes")
    return float(value) if isinstance(value, (int, float)) else None


def check_compatibility(reference: dict, candidate: dict) -> Compatibility:
    """Compare candidate against reference across the seven dimensions.

    Dimensions: transport, semantic type, schema, cardinality, required metadata,
    dimensions/duration, language, size limits. A smaller candidate size limit is
    BREAKING; otherwise defer to the structural drift classifier.
    """
    ref_size = _max_size(reference, "input")
    cand_size = _max_size(candidate, "input")
    if ref_size is not None and cand_size is not None and cand_size < ref_size:
        return Compatibility.BREAKING

    return classify_drift(reference, candidate)