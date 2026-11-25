"""Validation layer: ports, errors, fingerprint, compatibility, CLI."""

from uaicp.validation.compat import check_compatibility
from uaicp.validation.errors import ErrorCode, NormalizedError, from_http_status, normalize
from uaicp.validation.fingerprint import Compatibility, canonical_fingerprint, classify_drift
from uaicp.validation.ports import CanonicalPort
from uaicp.validation.validate import ValidationResult, validate_contract

__all__ = [
    "CanonicalPort",
    "Compatibility",
    "ErrorCode",
    "NormalizedError",
    "ValidationResult",
    "canonical_fingerprint",
    "check_compatibility",
    "classify_drift",
    "from_http_status",
    "normalize",
    "validate_contract",
]