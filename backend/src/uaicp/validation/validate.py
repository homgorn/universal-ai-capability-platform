"""Contract validation -> structured result (FR-001, FR-002, FR-009)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import jsonschema

from uaicp.validation.ports import CanonicalPort


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {"valid": self.valid, "errors": self.errors, "warnings": self.warnings}


def _validate_port(raw: Any, where: str, errors: list[str], warnings: list[str]) -> None:
    if not isinstance(raw, dict):
        errors.append(f"{where}: port must be an object")
        return
    port = CanonicalPort.from_dict(raw)
    errors.extend(f"{where}: {e}" for e in port.validate())
    if port.schema is not None:
        try:
            jsonschema.Draft202012Validator.check_schema(port.schema)
        except jsonschema.SchemaError as exc:
            errors.append(f"{where}: invalid JSON Schema: {exc.message}")
    if port.sensitive and not port.artifact_type:
        warnings.append(f"{where}: sensitive port '{port.name}' has no artifact_type")


def validate_contract(contract: dict) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(contract, dict):
        return ValidationResult(False, ["contract must be an object"])

    for direction in ("inputs", "outputs"):
        ports = contract.get(direction, [])
        if not isinstance(ports, list):
            errors.append(f"{direction}: must be a list")
            continue
        if not ports:
            warnings.append(f"{direction}: empty")
        for i, raw in enumerate(ports):
            _validate_port(raw, f"{direction}[{i}]", errors, warnings)

    return ValidationResult(valid=len(errors) == 0, errors=errors, warnings=warnings)