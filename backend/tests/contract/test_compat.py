"""Contract tests for compatibility checking (US2, FR-003/FR-004)."""

from __future__ import annotations

from uaicp.validation import Compatibility, check_compatibility

REF = {
    "inputs": [
        {"name": "image", "required": True, "semantic_type": "image", "transport_type": "bytes"}
    ],
    "outputs": [
        {"name": "image", "required": True, "semantic_type": "image", "transport_type": "bytes"}
    ],
}


def test_optional_addition_is_patch():
    cand = {
        "inputs": REF["inputs"]
        + [{"name": "mask", "required": False, "semantic_type": "image", "transport_type": "bytes"}],
        "outputs": REF["outputs"],
    }
    assert check_compatibility(REF, cand) is Compatibility.PATCH_COMPATIBLE


def test_required_type_change_is_breaking():
    cand = {
        "inputs": [
            {"name": "image", "required": True, "semantic_type": "text", "transport_type": "string"}
        ],
        "outputs": REF["outputs"],
    }
    assert check_compatibility(REF, cand) is Compatibility.BREAKING


def test_smaller_size_limit_is_breaking():
    ref = dict(REF, limits={"max_input_bytes": 1000})
    cand = dict(REF, limits={"max_input_bytes": 500})
    assert check_compatibility(ref, cand) is Compatibility.BREAKING


def test_optional_type_change_is_unknown():
    ref = {
        "inputs": [
            {"name": "a", "required": True, "semantic_type": "image", "transport_type": "bytes"},
            {"name": "b", "required": False, "semantic_type": "text", "transport_type": "string"},
        ],
        "outputs": [],
    }
    cand = {
        "inputs": [
            ref["inputs"][0],
            {"name": "b", "required": False, "semantic_type": "json", "transport_type": "string"},
        ],
        "outputs": [],
    }
    assert check_compatibility(ref, cand) is Compatibility.UNKNOWN