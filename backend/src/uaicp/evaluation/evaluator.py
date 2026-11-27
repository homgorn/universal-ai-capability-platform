"""Deterministic, evidence-backed evaluation (SPECS.md §1 Correction 7, §12)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from uaicp.domain.enums import EvidenceMark

DIMENSIONS = ("quality", "reliability", "latency", "cost", "safety")


@dataclass
class Dimension:
    value: float | None
    mark: EvidenceMark
    observed_at: datetime
    verify: bool = False


@dataclass
class Evaluation:
    tool_id: str
    dimensions: dict[str, Dimension] = field(default_factory=dict)
    license: str | None = None

    def as_dict(self) -> dict:
        return {
            "tool_id": self.tool_id,
            "license": self.license,
            "dimensions": {
                name: {
                    "value": d.value,
                    "mark": d.mark.value,
                    "observed_at": d.observed_at.isoformat(),
                    "verify": d.verify,
                }
                for name, d in self.dimensions.items()
            },
        }


def evaluate(
    tool_id: str,
    *,
    evidence: dict | None = None,
    license_value: str | None = None,
) -> Evaluation:
    """Build an evaluation. Only provided, marked evidence becomes a value.

    Missing dimensions stay value=None, mark=INFERRED, verify=True — never 0
    and never a fabricated number.
    """
    evidence = evidence or {}
    now = datetime.now(UTC)
    result = Evaluation(tool_id=tool_id, license=license_value)
    for name in DIMENSIONS:
        raw = evidence.get(name)
        if isinstance(raw, dict) and raw.get("value") is not None:
            mark = EvidenceMark(raw.get("mark", EvidenceMark.INFERRED.value))
            result.dimensions[name] = Dimension(
                value=float(raw["value"]),
                mark=mark,
                observed_at=now,
                verify=mark is EvidenceMark.INFERRED,
            )
        else:
            result.dimensions[name] = Dimension(
                value=None, mark=EvidenceMark.INFERRED, observed_at=now, verify=True
            )
    return result