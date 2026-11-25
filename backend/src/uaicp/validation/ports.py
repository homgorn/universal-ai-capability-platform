"""Canonical input/output ports (SPECS.md §4)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CanonicalPort:
    name: str
    required: bool = False
    semantic_type: str | None = None
    transport_type: str | None = None
    schema: dict | None = None
    constraints: dict = field(default_factory=dict)
    examples: list = field(default_factory=list)
    sensitive: bool = False
    artifact_type: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CanonicalPort:
        return cls(
            name=data.get("name", ""),
            required=bool(data.get("required", False)),
            semantic_type=data.get("semantic_type"),
            transport_type=data.get("transport_type"),
            schema=data.get("schema"),
            constraints=data.get("constraints") or {},
            examples=data.get("examples") or [],
            sensitive=bool(data.get("sensitive", False)),
            artifact_type=data.get("artifact_type"),
        )

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.name:
            errors.append("port.name is required")
        if not self.semantic_type:
            errors.append(f"port '{self.name}': semantic_type is required")
        if not self.transport_type:
            errors.append(f"port '{self.name}': transport_type is required")
        return errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "required": self.required,
            "semantic_type": self.semantic_type,
            "transport_type": self.transport_type,
            "schema": self.schema,
            "constraints": self.constraints,
            "examples": self.examples,
            "sensitive": self.sensitive,
            "artifact_type": self.artifact_type,
        }