# Feature Specification: Execution Gateway

**Feature Branch**: `003-execution-gateway`
**Created**: 2026-11-25
**Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create a durable execution (Priority: P1)
A caller submits a target (tool or recipe), inputs and policy limits with an idempotency key.
The gateway creates a durable execution in CREATED and returns it.

**Independent Test**: two submissions with the same idempotency key return one execution.

### Acceptance Scenarios
1. Given a new key, when submitted, then a CREATED execution exists.
2. Given a duplicate key, when submitted, then no second execution is created.

---

### User Story 2 - Advance through the state machine (Priority: P1)
The execution moves CREATED → POLICY_CHECK → QUEUED → STARTING → RUNNING → SUCCEEDED,
with terminal FAILED/CANCELLED/EXPIRED/DENIED.

**Acceptance Scenarios**
1. Given CREATED, when policy allows, then state becomes QUEUED.
2. Given a denied policy, then state becomes DENIED and no execution runs.
3. Given RUNNING, when cancel is called, then state becomes CANCELLED.

---

### User Story 3 - Bounded retries and recorded fallback (Priority: P2)
Only transient errors (429/5xx/timeout) are retried within max_attempts; a fallback is a
distinct attempt with a reason under the same logical execution.

**Acceptance Scenarios**
1. Given 429 and max_attempts=3, then at most 3 attempts occur.
2. Given INVALID_INPUT, then no retry occurs.
3. Given a fallback, then a second attempt with reason is recorded.

---

### User Story 4 - Artifacts and events (Priority: P2)
Each execution records structured events and typed artifact references (never inline binaries).

**Acceptance Scenarios**
1. Given a completed execution, then events include state transitions.
2. Given an output artifact, then only its URI/metadata is stored.

---

### Edge Cases
- Duplicate idempotency key across tenants MUST be isolated.
- Retry after budget exhausted MUST stop with FAILED.
- Cancellation during STARTING MUST be honored.

## Requirements *(mandatory)*

### Functional Requirements
- FR-001: System MUST create execution with durable ID, idempotency key, trace ID.
- FR-002: duplicate idempotency key MUST NOT create a second logical execution.
- FR-003: System MUST enforce state machine CREATED→POLICY_CHECK→QUEUED→STARTING→RUNNING→STREAMING→SUCCEEDED and terminals.
- FR-004: policy DENY MUST set DENIED without running.
- FR-005: retries MUST be bounded by max_attempts and only for transient errors.
- FR-006: fallback MUST create a distinct attempt with reason.
- FR-007: System MUST record structured events for transitions.
- FR-008: artifacts MUST be stored as typed metadata + URI, never inline binary.
- FR-009: cost estimate MUST be captured before execution and actual after.
- FR-010: idempotency and attempts MUST be tenant-isolated.

### Key Entities
- Execution, Attempt, ExecutionEvent, ArtifactRef, PolicyDecision.

## Success Criteria *(mandatory)*
- SC-001: 0 duplicate executions on repeated idempotency key.
- SC-002: 100% invalid transitions rejected.
- SC-003: 0 retries on non-transient errors.
- SC-004: attempts ≤ max_attempts in 100% of cases.
- SC-005: fallbacks recorded as distinct attempts with reason.
- SC-006: tenant isolation holds for all executions.

## Assumptions
- Pure in-process gateway; provider calls injected as a callable (no network).
- Reuses uaicp.db Execution model + ErrorCode taxonomy.

## RU — Резюме
Execution Gateway: идемпотентность, конечный автомат, политика, ограниченные повторы,
fallback-попытки, события и артефакты. US1–US4, FR-001…010, SC-001…006. Провайдер — инъекция,
без сети.