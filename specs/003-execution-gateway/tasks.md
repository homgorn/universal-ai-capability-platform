# Tasks: Execution Gateway

## Phase 1 Setup
- [x] T001 Create `backend/src/uaicp/execution/` package

## Phase 2 Foundational
- [x] T002 Add ExecutionAttempt/ExecutionEvent/ArtifactRef models in `backend/src/uaicp/db/models.py`
- [x] T003 Implement transition table + validator in `backend/src/uaicp/execution/events.py`

## Phase 3 US1 (P1)
- [x] T004 [P] [US1] Tests for idempotency in `backend/tests/contract/test_execution_idempotency.py`
- [x] T005 [US1] Implement `create_execution` in `backend/src/uaicp/execution/gateway.py`

## Phase 4 US2 (P1)
- [x] T006 [P] [US2] Tests for state machine in `backend/tests/contract/test_execution_state.py`
- [x] T007 [US2] Implement `advance` + `cancel` in gateway.py

## Phase 5 US3 (P2)
- [x] T008 [P] [US3] Tests for retry/fallback in `backend/tests/unit/test_retry.py`
- [x] T009 [US3] Implement `run_with_retry` in `backend/src/uaicp/execution/attempts.py`

## Phase 6 US4 (P2)
- [x] T010 [P] [US4] Tests for events/artifacts in `backend/tests/integration/test_execution_events.py`

## Phase 7 Polish
- [x] T011 Run `python scripts/health.py`

## RU
Setup T001 → Foundational T002–T003 → US1 T004–T005 → US2 T006–T007 → US3 T008–T009 →
US4 T010 → Polish T011.