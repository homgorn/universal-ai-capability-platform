# Phase 1 Data Model: Knowledge Foundation

**Feature**: 001-knowledge-foundation | **Date**: 2026-11-25

All entities carry: `id` (immutable UUID), `tenant_id`, `created_at`, `updated_at`,
`provenance` (embedded), `evidence_mark`. Contract versions are append-only.

## Canonical Domain Entities

### Provider
Organization/system exposing resources or execution.
Fields: `id`, `tenant_id`, `name`, `kind` (enum: HF, REPLICATE, FAL, INTERNAL, OTHER),
`source_url`, `provenance`, `evidence_mark`.

### Resource
Provider-owned/discovered thing.
Fields: `id`, `tenant_id`, `provider_id` (FK), `resource_type` (enum: MODEL, SPACE,
API_SERVICE, MCP_SERVER, AGENT_SERVICE, DATASET, REPOSITORY), `name`, `source_url`,
`source_revision`, `raw_snapshot` (jsonb), `provenance`, `evidence_mark`.

### Interface
Access mechanism. Fields: `id`, `tenant_id`, `interface_type` (enum: HTTP_REST, OPENAPI,
GRADIO, MCP, A2A, SDK, EMBED, WEBHOOK, CLI), `resource_id` (FK), `schema_snapshot` (jsonb),
`provenance`, `evidence_mark`.

### Operation
Callable action. Fields: `id`, `tenant_id`, `name` (e.g. generate, transcribe), `provenance`.

### Tool
Executable implementation of an operation.
Fields: `id`, `tenant_id`, `resource_id` (FK), `interface_id` (FK), `operation_id` (FK),
`status` (lifecycle enum), `provenance`, `evidence_mark`.
Invariant: Tool != Capability.

### Capability
Stable semantic function. Fields: `id`, `tenant_id`, `capability_id` (`<domain>.<function>`,
unique per tenant), `name`, `status` (lifecycle enum), `provenance`.

### Contract (versioned, immutable)
Fields: `id`, `tenant_id`, `capability_id` (FK), `version` (int), `supersedes_id` (FK,
nullable), `inputs` (jsonb), `outputs` (jsonb), `fingerprint` (sha256), `parser_version`,
`normalized_version`, `created_at`. Append-only; unique `(capability_id, version)`.

### Evaluation
Fields: `id`, `tenant_id`, `tool_id` (FK), `quality`, `reliability`, `latency_p50`,
`latency_p95`, `cost`, `safety`, `evidence_mark`, `observed_at`.

### Health
Fields: `id`, `tenant_id`, `tool_id` (FK), `availability`, `latency_p50`, `latency_p95`,
`error_rate`, `queue_delay`, `schema_status`, `quota_status`, `last_success_at`.

### Policy
Fields: `id`, `tenant_id`, `version`, `decision` (enum: ALLOW, DENY, REQUIRE_APPROVAL,
ALLOW_WITH_LIMITS), `data_classes` (array), `created_at`.

### Provenance (embedded value object)
Fields: `source`, `source_url`, `observed_at`, `source_revision`, `raw_snapshot`,
`parser_version`, `normalized_version`.

### Execution
Fields: `id`, `tenant_id`, `target_type` (TOOL|RECIPE), `target_id`, `status` (state enum),
`idempotency_key` (unique per tenant), `trace_id`, `estimated_cost`, `actual_cost`,
`created_at`.

### Artifact
Fields: `id`, `tenant_id`, `type`, `mime`, `size`, `hash`, `storage_uri`, `classification`
(enum: PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED), `retention`, `expires_at`.

### Recipe
Fields: `id`, `tenant_id`, `name`, `dag` (jsonb, acyclic), `created_at`.

### App
Fields: `id`, `tenant_id`, `name`, `recipe_id` (FK), `created_at`.

### Deployment
Fields: `id`, `tenant_id`, `app_id` (FK), `channel` (enum), `status`, `created_at`.

## Knowledge Graph Entities

### kg_entity (node)
Fields: `entity_id` (UUID), `tenant_id`, `entity_type` (enum mirroring domain types),
`domain_id` (FK to the domain row), `name`, `labels` (text[]).

### kg_triple (edge)
Fields: `triple_id` (UUID), `tenant_id`, `subject_id` (FK kg_entity), `predicate` (text),
`object_id` (FK kg_entity, nullable), `object_literal` (jsonb, nullable),
`subject_type`, `object_type`, `evidence_mark`, `source`, `source_url`, `observed_at`,
`graph_version` (int), `created_at`.
Constraint: exactly one of `object_id` / `object_literal` non-null.

## Relationships (triple predicates)

- `provider owns resource` (Provider → Resource)
- `resource exposes interface` (Resource → Interface)
- `interface implements operation` (Interface → Operation)
- `tool implements operation` (Tool → Operation)
- `tool satisfies capability` (Tool → Capability)
- `capability has contract` (Capability → Contract)
- `tool has evaluation` (Tool → Evaluation)
- `tool has health` (Tool → Health)
- `execution targets tool` (Execution → Tool)
- `execution produces artifact` (Execution → Artifact)
- `recipe uses capability` (Recipe → Capability)
- `app built_from recipe` (App → Recipe)
- `deployment publishes app` (Deployment → App)

## Validation Rules

- `capability_id` MUST match `^[a-z_]+\.[a-z_]+$`.
- `REPORTED` evidence MUST have `source_url` and `observed_at`.
- Contract `fingerprint` MUST be deterministic over canonical JSON.
- Recipe `dag` MUST be acyclic at write time.
- `tenant_id` is mandatory on every row; RLS enforces session scoping.

## State Transitions

- Capability lifecycle: DRAFT → DISCOVERED → CONTRACT_VERIFIED → EVALUATED → APPROVED →
  ACTIVE → DEGRADED → SUSPENDED → DEPRECATED. Discovered MUST NOT be executable.
- Execution: CREATED → POLICY_CHECK → QUEUED → STARTING → RUNNING → STREAMING → SUCCEEDED;
  terminals: FAILED, CANCELLED, EXPIRED, DENIED.

## RU — Резюме модели данных

Канонические сущности: Provider, Resource, Interface, Operation, Tool, Capability, Contract
(версионируется, append-only), Evaluation, Health, Policy, Provenance (встроенный), Execution,
Artifact, Recipe, App, Deployment. Граф: `kg_entity` (узлы) и `kg_triple` (рёбра
subject-predicate-object) с evidence_mark и tenant_id. Инварианты: Tool ≠ Capability,
capability_id по маске, REPORTED требует URL+дату, DAG ацикличен, RLS по tenant_id.