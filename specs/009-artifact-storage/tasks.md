# Tasks: Artifact Storage

- [x] T001 Create `backend/src/uaicp/storage/` package
- [x] T002 Implement `ArtifactStore` protocol + `LocalStore` in `storage/base.py`, `storage/local.py`
- [x] T003 [P] [US1] Tests for store+metadata in `backend/tests/integration/test_artifact_store.py`
- [x] T004 [P] [US3] Tests for hash mismatch + max size in `backend/tests/unit/test_artifact_limits.py`
- [x] T005 Implement `R2Store` stub in `storage/r2.py` (raises until R2 enabled)
- [x] T006 Implement `store_artifact` service in `storage/service.py`
- [x] T007 Run `python scripts/health.py`

## RU
T001 setup; T002 local; T003 метаданные; T004 лимиты/hash; T005 R2 stub; T006 сервис; T007 health.