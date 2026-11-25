# Tasks: Contract Validation and Error Taxonomy

## Phase 1: Setup
- [x] T001 Create `backend/src/uaicp/validation/` package
- [x] T002 Add `jsonschema` dependency in `backend/pyproject.toml`

## Phase 2: Foundational
- [x] T003 Implement `CanonicalPort` + parsing in `backend/src/uaicp/validation/ports.py`
- [x] T004 Implement `ErrorCode` (15) + `NormalizedError` + `normalize` in `backend/src/uaicp/validation/errors.py`
- [x] T005 Implement deterministic `fingerprint` + `classify_drift` in `backend/src/uaicp/validation/fingerprint.py`

## Phase 3: US1 Validate contract (P1)
- [x] T006 [P] [US1] Contract tests for validation in `backend/tests/contract/test_validate.py`
- [x] T007 [US1] Implement `validate_contract` in `backend/src/uaicp/validation/validate.py`

## Phase 4: US2 Compatibility (P1)
- [x] T008 [P] [US2] Contract tests for compatibility in `backend/tests/contract/test_compat.py`
- [x] T009 [US2] Implement seven-dimension `check_compatibility` in `backend/src/uaicp/validation/compat.py`

## Phase 5: US3 Error normalization (P2)
- [x] T010 [P] [US3] Unit tests for normalization in `backend/tests/unit/test_errors.py`
- [x] T011 [US3] Wire `normalize` (depends on T004)

## Phase 6: US4 Fingerprint/drift (P2)
- [x] T012 [P] [US4] Unit tests for fingerprint/drift in `backend/tests/unit/test_fingerprint.py`

## Phase 7: US5 CLI (P3)
- [x] T013 [P] [US5] Contract test for CLI exit codes in `backend/tests/contract/test_cli.py`
- [x] T014 [US5] Implement `cli.py` in `backend/src/uaicp/validation/cli.py`

## Phase 8: Polish
- [x] T015 [P] Update `backend/README.md`
- [x] T016 Run `python scripts/health.py`

## RU
Setup T001–T002 → Foundational T003–T005 → US1 T006–T007 → US2 T008–T009 → US3 T010–T011 →
US4 T012 → US5 T013–T014 → Polish T015–T016.