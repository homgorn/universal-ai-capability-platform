"""Deterministic contract fingerprint and drift classification (SPECS.md §7)."""

from __future__ import annotations

import hashlib
import json
from enum import Enum


class Compatibility(str, Enum):
    PATCH_COMPATIBLE = "PATCH_COMPATIBLE"
    BACKWARD_COMPATIBLE = "BACKWARD_COMPATIBLE"
    BREAKING = "BREAKING"
    UNKNOWN = "UNKNOWN"


def canonical_fingerprint(inputs: list, outputs: list) -> str:
    payload = json.dumps(
        {"inputs": inputs, "outputs": outputs},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _index(ports: list) -> dict[str, dict]:
    return {p.get("name", ""): p for p in ports if isinstance(p, dict)}


def classify_drift(old: dict, new: dict) -> Compatibility:
    """Classify a contract change as PATCH/BACKWARD/BREAKING/UNKNOWN."""
    old_in, new_in = _index(old.get("inputs", [])), _index(new.get("inputs", []))
    old_out, new_out = _index(old.get("outputs", [])), _index(new.get("outputs", []))

    # Removed required input, or changed type/transport of a required input -> BREAKING.
    for name, ref in old_in.items():
        cand = new_in.get(name)
        if cand is None:
            if ref.get("required"):
                return Compatibility.BREAKING
            continue
        if ref.get("required") and (
            cand.get("semantic_type") != ref.get("semantic_type")
            or cand.get("transport_type") != ref.get("transport_type")
        ):
            return Compatibility.BREAKING

    # Output type changes are breaking for consumers.
    for name, ref in old_out.items():
        cand = new_out.get(name)
        if cand is None:
            return Compatibility.BREAKING
        if cand.get("semantic_type") != ref.get("semantic_type"):
            return Compatibility.BREAKING

    added_in = set(new_in) - set(old_in)
    added_out = set(new_out) - set(old_out)

    # A new required input breaks existing callers.
    if any(new_in[n].get("required", False) for n in added_in):
        return Compatibility.BREAKING
    # A new required output is backward compatible for existing consumers.
    if any(new_out[n].get("required", False) for n in added_out):
        return Compatibility.BACKWARD_COMPATIBLE
    # Only optional additions -> patch compatible.
    if added_in or added_out:
        return Compatibility.PATCH_COMPATIBLE

    # A changed type on an optional input is of unknown impact.
    for name, ref in old_in.items():
        cand = new_in.get(name)
        if (
            cand
            and not ref.get("required")
            and cand.get("semantic_type") != ref.get("semantic_type")
        ):
            return Compatibility.UNKNOWN

    return Compatibility.PATCH_COMPATIBLE