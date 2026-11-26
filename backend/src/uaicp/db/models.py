"""ORM models for the canonical domain + knowledge graph projection.

Invariants enforced here:
- Tool != Capability (separate tables).
- Resource != Interface (separate tables).
- Historical contracts are immutable (append-only ContractVersion).
- Every claim carries provenance + evidence_mark.
- discovered != executable (Capability.status defaults to DISCOVERED, never ACTIVE).
"""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import (
    JSON,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy import (
    Enum as SAEnum,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from uaicp.db.base import Base
from uaicp.domain.enums import (
    CapabilityStatus,
    Channel,
    DataClass,
    EntityType,
    EvidenceMark,
    ExecutionStatus,
    InterfaceType,
    ResourceType,
)

# JSON that upgrades to JSONB on Postgres, stays JSON on SQLite.
JSONType = JSON().with_variant(JSONB(), "postgresql")


def _now() -> datetime:
    return datetime.now(UTC)


class TenantMixin:
    tenant_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class ProvenanceMixin:
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    source_url: Mapped[str | None] = mapped_column(String(1024))
    observed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    source_revision: Mapped[str | None] = mapped_column(String(128))
    raw_snapshot: Mapped[dict | None] = mapped_column(JSONType)
    parser_version: Mapped[str] = mapped_column(String(32), default="1")
    normalized_version: Mapped[str] = mapped_column(String(32), default="1")
    evidence_mark: Mapped[EvidenceMark] = mapped_column(
        SAEnum(EvidenceMark, native_enum=False), nullable=False, default=EvidenceMark.INFERRED
    )


class Provider(TenantMixin, Base):
    __tablename__ = "provider"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    kind: Mapped[str] = mapped_column(String(32), nullable=False)


class Resource(TenantMixin, ProvenanceMixin, Base):
    __tablename__ = "resource"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("provider.id"), nullable=False)
    resource_type: Mapped[ResourceType] = mapped_column(
        SAEnum(ResourceType, native_enum=False), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)


class Interface(TenantMixin, ProvenanceMixin, Base):
    __tablename__ = "interface"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resource_id: Mapped[int] = mapped_column(ForeignKey("resource.id"), nullable=False)
    interface_type: Mapped[InterfaceType] = mapped_column(
        SAEnum(InterfaceType, native_enum=False), nullable=False
    )
    schema_snapshot: Mapped[dict | None] = mapped_column(JSONType)


class Operation(TenantMixin, Base):
    __tablename__ = "operation"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)


class Tool(TenantMixin, ProvenanceMixin, Base):
    __tablename__ = "tool"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resource_id: Mapped[int] = mapped_column(ForeignKey("resource.id"), nullable=False)
    interface_id: Mapped[int] = mapped_column(ForeignKey("interface.id"), nullable=False)
    operation_id: Mapped[int] = mapped_column(ForeignKey("operation.id"), nullable=False)
    # A tool may satisfy one capability (Tool != Capability; many tools per capability).
    capability_id: Mapped[int | None] = mapped_column(ForeignKey("capability.id"))
    status: Mapped[CapabilityStatus] = mapped_column(
        SAEnum(CapabilityStatus, native_enum=False), nullable=False
    )


class Capability(TenantMixin, Base):
    __tablename__ = "capability"
    __table_args__ = (UniqueConstraint("tenant_id", "capability_id", name="uq_capability"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    capability_id: Mapped[str] = mapped_column(String(128), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    # discovered != executable: default is DISCOVERED, never ACTIVE.
    status: Mapped[CapabilityStatus] = mapped_column(
        SAEnum(CapabilityStatus, native_enum=False),
        nullable=False,
        default=CapabilityStatus.DISCOVERED,
    )


class ContractVersion(TenantMixin, Base):
    """Append-only, immutable contract version (FR-004, SC-004)."""

    __tablename__ = "contract_version"
    __table_args__ = (
        UniqueConstraint("capability_id", "version", name="uq_contract_version"),
        CheckConstraint("version >= 1", name="ck_contract_version_positive"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    capability_id: Mapped[int] = mapped_column(ForeignKey("capability.id"), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    supersedes_id: Mapped[int | None] = mapped_column(ForeignKey("contract_version.id"))
    inputs: Mapped[dict] = mapped_column(JSONType, nullable=False)
    outputs: Mapped[dict] = mapped_column(JSONType, nullable=False)
    fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    parser_version: Mapped[str] = mapped_column(String(32), default="1")
    normalized_version: Mapped[str] = mapped_column(String(32), default="1")


class Evaluation(TenantMixin, Base):
    __tablename__ = "evaluation"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tool_id: Mapped[int] = mapped_column(ForeignKey("tool.id"), nullable=False)
    quality: Mapped[float | None] = mapped_column(Float)
    reliability: Mapped[float | None] = mapped_column(Float)
    latency_p50: Mapped[float | None] = mapped_column(Float)
    latency_p95: Mapped[float | None] = mapped_column(Float)
    cost: Mapped[float | None] = mapped_column(Float)
    safety: Mapped[float | None] = mapped_column(Float)
    evidence_mark: Mapped[EvidenceMark] = mapped_column(
        SAEnum(EvidenceMark, native_enum=False), nullable=False, default=EvidenceMark.INFERRED
    )
    observed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Health(TenantMixin, Base):
    __tablename__ = "health"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tool_id: Mapped[int] = mapped_column(ForeignKey("tool.id"), nullable=False)
    availability: Mapped[float | None] = mapped_column(Float)
    latency_p50: Mapped[float | None] = mapped_column(Float)
    latency_p95: Mapped[float | None] = mapped_column(Float)
    error_rate: Mapped[float | None] = mapped_column(Float)
    queue_delay: Mapped[float | None] = mapped_column(Float)
    schema_status: Mapped[str | None] = mapped_column(String(32))
    quota_status: Mapped[str | None] = mapped_column(String(32))
    last_success_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Policy(TenantMixin, Base):
    __tablename__ = "policy"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    decision: Mapped[str] = mapped_column(String(32), nullable=False)
    data_classes: Mapped[list] = mapped_column(JSONType, default=list)


class Execution(TenantMixin, Base):
    __tablename__ = "execution"
    __table_args__ = (
        UniqueConstraint("tenant_id", "idempotency_key", name="uq_execution_idem"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    target_type: Mapped[str] = mapped_column(String(16), nullable=False)
    target_id: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[ExecutionStatus] = mapped_column(
        SAEnum(ExecutionStatus, native_enum=False),
        nullable=False,
        default=ExecutionStatus.CREATED,
    )
    idempotency_key: Mapped[str] = mapped_column(String(128), nullable=False)
    trace_id: Mapped[str] = mapped_column(String(64), nullable=False)
    estimated_cost: Mapped[float | None] = mapped_column(Float)
    actual_cost: Mapped[float | None] = mapped_column(Float)


class Artifact(TenantMixin, Base):
    __tablename__ = "artifact"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(64), nullable=False)
    mime: Mapped[str] = mapped_column(String(128), nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    hash: Mapped[str] = mapped_column(String(128), nullable=False)
    storage_uri: Mapped[str] = mapped_column(String(1024), nullable=False)
    classification: Mapped[DataClass] = mapped_column(
        SAEnum(DataClass, native_enum=False), nullable=False, default=DataClass.INTERNAL
    )
    retention: Mapped[str | None] = mapped_column(String(32))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Recipe(TenantMixin, Base):
    __tablename__ = "recipe"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    dag: Mapped[dict] = mapped_column(JSONType, nullable=False)


class App(TenantMixin, Base):
    __tablename__ = "app"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipe.id"), nullable=False)


class Deployment(TenantMixin, Base):
    __tablename__ = "deployment"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    app_id: Mapped[int] = mapped_column(ForeignKey("app.id"), nullable=False)
    channel: Mapped[Channel] = mapped_column(SAEnum(Channel, native_enum=False), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)


class ExecutionAttempt(TenantMixin, Base):
    """One attempt of a logical execution (retry or fallback)."""

    __tablename__ = "execution_attempt"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    execution_id: Mapped[int] = mapped_column(ForeignKey("execution.id"), nullable=False)
    attempt_no: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    error_code: Mapped[str | None] = mapped_column(String(64))
    reason: Mapped[str | None] = mapped_column(String(255))
    provider: Mapped[str | None] = mapped_column(String(128))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class ExecutionEvent(TenantMixin, Base):
    """Structured state-transition event."""

    __tablename__ = "execution_event"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    execution_id: Mapped[int] = mapped_column(ForeignKey("execution.id"), nullable=False)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    from_state: Mapped[str | None] = mapped_column(String(32))
    to_state: Mapped[str | None] = mapped_column(String(32))
    payload: Mapped[dict | None] = mapped_column(JSONType)


class ArtifactRef(TenantMixin, Base):
    """Typed artifact metadata + URI (never inline binary)."""

    __tablename__ = "artifact_ref"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    execution_id: Mapped[int] = mapped_column(ForeignKey("execution.id"), nullable=False)
    artifact_type: Mapped[str] = mapped_column(String(64), nullable=False)
    mime: Mapped[str] = mapped_column(String(128), nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    hash: Mapped[str] = mapped_column(String(128), nullable=False)
    storage_uri: Mapped[str] = mapped_column(String(1024), nullable=False)
    classification: Mapped[DataClass] = mapped_column(
        SAEnum(DataClass, native_enum=False), nullable=False, default=DataClass.INTERNAL
    )


class HFSpace(TenantMixin, Base):
    """Canonical minimal record for a Hugging Face Space (MVP-1)."""

    __tablename__ = "hf_space"
    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    author: Mapped[str | None] = mapped_column(String(255))
    title: Mapped[str | None] = mapped_column(String(512))
    sdk: Mapped[str | None] = mapped_column(String(64))
    category: Mapped[str | None] = mapped_column(String(64), index=True)
    tags: Mapped[list] = mapped_column(JSONType, default=list)
    likes: Mapped[int | None] = mapped_column(Integer)
    trending_score: Mapped[float | None] = mapped_column(Float)
    runtime: Mapped[dict | None] = mapped_column(JSONType)
    subdomain: Mapped[str | None] = mapped_column(String(255))
    sha: Mapped[str | None] = mapped_column(String(128), index=True)
    created_at_hf: Mapped[str | None] = mapped_column(String(64))
    last_modified_hf: Mapped[str | None] = mapped_column(String(64))
    license: Mapped[str | None] = mapped_column(String(128))
    models: Mapped[list] = mapped_column(JSONType, default=list)
    datasets: Mapped[list] = mapped_column(JSONType, default=list)
    source_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    raw_snapshot: Mapped[dict] = mapped_column(JSONType, nullable=False)
    snapshot_history: Mapped[list] = mapped_column(JSONType, default=list)
    observed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    times_seen: Mapped[int] = mapped_column(Integer, default=1)


class IngestCheckpoint(Base):
    """Resumable cursor state for a crawl source."""

    __tablename__ = "ingest_checkpoint"
    source: Mapped[str] = mapped_column(String(128), primary_key=True)
    cursor: Mapped[str | None] = mapped_column(Text)
    items_seen: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class KGEntity(TenantMixin, Base):
    """Graph node (derived projection)."""

    __tablename__ = "kg_entity"
    __table_args__ = (UniqueConstraint("tenant_id", "domain_id", "entity_type", name="uq_kg_node"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entity_type: Mapped[EntityType] = mapped_column(
        SAEnum(EntityType, native_enum=False), nullable=False
    )
    domain_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    labels: Mapped[list] = mapped_column(JSONType, default=list)


class KGTriple(TenantMixin, Base):
    """Graph edge (subject, predicate, object) with evidence + provenance."""

    __tablename__ = "kg_triple"
    __table_args__ = (
        CheckConstraint(
            "(object_id IS NOT NULL) <> (object_literal IS NOT NULL)",
            name="ck_triple_object_xor",
        ),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("kg_entity.id"), nullable=False)
    predicate: Mapped[str] = mapped_column(String(128), nullable=False)
    object_id: Mapped[int | None] = mapped_column(ForeignKey("kg_entity.id"))
    object_literal: Mapped[str | None] = mapped_column(Text)
    subject_type: Mapped[EntityType] = mapped_column(
        SAEnum(EntityType, native_enum=False), nullable=False
    )
    object_type: Mapped[EntityType | None] = mapped_column(
        SAEnum(EntityType, native_enum=False)
    )
    evidence_mark: Mapped[EvidenceMark] = mapped_column(
        SAEnum(EvidenceMark, native_enum=False), nullable=False, default=EvidenceMark.INFERRED
    )
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    source_url: Mapped[str | None] = mapped_column(String(1024))
    observed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    graph_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)