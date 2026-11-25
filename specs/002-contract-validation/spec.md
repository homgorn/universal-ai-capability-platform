# Feature Specification: Contract Validation and Error Taxonomy

**Feature Branch**: `002-contract-validation`

**Created**: 2026-11-25

**Status**: Draft

**Input**: User description: "Contract Validation and Error Taxonomy: canonical input/output ports, compatibility checking (transport, semantic type, schema, cardinality, metadata, size), and a normalized error taxonomy with code/message/retryable/stage/details."

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Validate a capability contract (Priority: P1)

A maintainer can submit a capability contract (inputs and outputs as canonical ports) and get
a structured validation result that says whether it is valid and, if not, exactly which port
and rule failed.

**Why this priority**: Contracts are the canonical unit of the platform; without validation
nothing downstream (routing, execution) can trust them.

**Independent Test**: Submit a valid contract → passes; submit a contract whose output lacks a
required `semantic_type` → fails with a precise error.

**Acceptance Scenarios**:

1. **Given** a contract with all required port fields, **When** validated, **Then** the result
   is valid with zero errors.
2. **Given** a port missing `semantic_type`, **When** validated, **Then** the result is invalid
   and names the offending port.
3. **Given** an input port whose `schema` violates its declared JSON Schema, **When** validated,
   **Then** validation fails with a schema error.

---

### User Story 2 - Check contract compatibility (Priority: P1)

A maintainer can compare a candidate contract against a reference contract and get a
compatibility classification across seven dimensions: transport, semantic type, schema,
cardinality, required metadata, dimensions/duration, language, and size limits.

**Why this priority**: Routing and drift handling depend on a deterministic compatibility
verdict; a wrong verdict blocks or allows the wrong provider.

**Independent Test**: Reference vs candidate differing only in an added optional field →
PATCH_COMPATIBLE; differing in a required field's type → BREAKING.

**Acceptance Scenarios**:

1. **Given** a candidate that only adds optional fields, **When** compared, **Then** the
   verdict is PATCH_COMPATIBLE.
2. **Given** a candidate that changes a required input's semantic type, **When** compared,
   **Then** the verdict is BREAKING.
3. **Given** an unknown difference, **When** compared, **Then** the verdict is UNKNOWN (safe).

---

### User Story 3 - Normalize provider errors (Priority: P2)

A provider error (arbitrary shape) can be normalized into the platform's fixed taxonomy with
`code`, `message`, `retryable`, `stage`, `details`, and optional `retry_after` and
`provider_error`.

**Why this priority**: Consistent error handling drives retry/fallback and user messaging;
without it every adapter invents its own errors.

**Independent Test**: A 429 provider error normalizes to RATE_LIMITED with retryable=true; a
400 to INVALID_INPUT with retryable=false.

**Acceptance Scenarios**:

1. **Given** an HTTP 429, **When** normalized, **Then** code is RATE_LIMITED and retryable.
2. **Given** an HTTP 400, **When** normalized, **Then** code is INVALID_INPUT and not retryable.
3. **Given** an unknown error, **When** normalized, **Then** code is INTERNAL_ERROR.

---

### User Story 4 - Deterministic fingerprint and drift (Priority: P2)

A contract's fingerprint is deterministic over canonical JSON, and a change classifies drift as
PATCH_COMPATIBLE, BACKWARD_COMPATIBLE, BREAKING, or UNKNOWN.

**Why this priority**: Drift detection and immutability rely on a stable fingerprint.

**Independent Test**: Same contract → same fingerprint; a field reorder → same fingerprint; a
type change → different fingerprint and BREAKING.

**Acceptance Scenarios**:

1. **Given** the same contract, **When** fingerprinted twice, **Then** identical.
2. **Given** reordered keys, **When** fingerprinted, **Then** identical.
3. **Given** a changed type, **When** drift classified, **Then** BREAKING.

---

### User Story 5 - Validate from the command line (Priority: P3)

A maintainer can run a CLI that validates a contract file and exits non-zero on invalid input,
suitable for CI.

**Why this priority**: Automation keeps contracts healthy in CI.

**Independent Test**: Valid file → exit 0; invalid file → non-zero with a printed error.

**Acceptance Scenarios**:

1. **Given** a valid file, **When** the CLI runs, **Then** exit code is 0.
2. **Given** an invalid file, **When** the CLI runs, **Then** exit code is non-zero.

---

### Edge Cases

- A port with `sensitive=true` and no `artifact_type` is allowed but flagged.
- A schema that is valid JSON but not a valid JSON Schema is rejected.
- A candidate with a smaller size limit than the reference is BREAKING.
- An empty contract (no inputs/outputs) is valid but flagged as empty.
- Unknown provider error shapes fall back to INTERNAL_ERROR, never crash.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A canonical port MUST declare name, required, semantic_type, transport_type,
  schema, constraints, examples, sensitive, artifact_type.
- **FR-002**: The system MUST validate port `schema` values as JSON Schema.
- **FR-003**: The system MUST check compatibility across transport, semantic type, schema,
  cardinality, required metadata, dimensions/duration, language, and size limits.
- **FR-004**: Compatibility MUST be classified as PATCH_COMPATIBLE, BACKWARD_COMPATIBLE,
  BREAKING, or UNKNOWN.
- **FR-005**: The system MUST define exactly 15 error codes: INVALID_INPUT, CONTRACT_MISMATCH,
  AUTH_REQUIRED, AUTH_FAILED, POLICY_DENIED, RATE_LIMITED, QUOTA_EXCEEDED,
  PROVIDER_UNAVAILABLE, PROVIDER_TIMEOUT, SCHEMA_DRIFT, ARTIFACT_TOO_LARGE, ARTIFACT_UNSAFE,
  EXECUTION_CANCELLED, EXECUTION_FAILED, INTERNAL_ERROR.
- **FR-006**: Every normalized error MUST include code, message, retryable, stage, details;
  optionally retry_after and provider_error.
- **FR-007**: The system MUST compute a deterministic contract fingerprint over canonical JSON.
- **FR-008**: The system MUST classify drift as PATCH_COMPATIBLE, BACKWARD_COMPATIBLE, BREAKING,
  or UNKNOWN.
- **FR-009**: Validation MUST return a structured result with `valid`, `errors`, and `warnings`.
- **FR-010**: The system MUST provide a CLI that exits non-zero on invalid contracts.

### Key Entities

- **Canonical Port**: name, required, semantic_type, transport_type, schema, constraints,
  examples, sensitive, artifact_type.
- **Contract**: capability_id, version, inputs[], outputs[], fingerprint.
- **Validation Result**: valid, errors[], warnings[].
- **Normalized Error**: code, message, retryable, stage, details, retry_after?, provider_error?.
- **Compatibility Verdict**: PATCH_COMPATIBLE | BACKWARD_COMPATIBLE | BREAKING | UNKNOWN.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A valid contract passes with 0 errors.
- **SC-002**: An invalid schema fails with a precise port-level error.
- **SC-003**: Incompatible contracts are classified BREAKING with 100% accuracy on fixtures.
- **SC-004**: 100% of normalized errors carry all required fields.
- **SC-005**: Fingerprints are stable across key reordering (100%).
- **SC-006**: CLI exit code is 0 for valid and non-zero for invalid on fixtures.

## Assumptions

- The source specification package is the authoritative basis.
- JSON Schema draft 2020-12 is the reference dialect.
- This feature is pure logic and does not execute providers.
- Bilingual (EN + RU) artifacts are maintained.

---

## RU — Резюме

**Фича**: Contract Validation & Error Taxonomy.
**US1 (P1)**: валидация канонических портов + JSON Schema. **US2 (P1)**: совместимость по 7
измерениям → PATCH/BACKWARD/BREAKING/UNKNOWN. **US3 (P2)**: нормализация ошибок в 15 кодов.
**US4 (P2)**: детерминированный fingerprint + дрейф. **US5 (P3)**: CLI с ненулевым кодом при
ошибке. **FR-001…010, SC-001…006**. Без исполнения провайдеров; двуязычно.