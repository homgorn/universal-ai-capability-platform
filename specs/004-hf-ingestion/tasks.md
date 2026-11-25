# Tasks: HF Ingestion

- [x] T001 Create `backend/src/uaicp/ingestion/` package
- [x] T002 [P] [US1] Tests for pagination/backoff in `backend/tests/unit/test_hf_discovery.py`
- [x] T003 [US1] Implement paginated `discover` in `backend/src/uaicp/ingestion/hf.py`
- [x] T004 [P] [US2] Tests for snapshots/provenance in `backend/tests/contract/test_hf_snapshot.py`
- [x] T005 [US2] Implement `ingest_resource` with provenance in hf.py
- [x] T006 [P] [US3] Tests for contract extraction in `backend/tests/contract/test_hf_contract.py`
- [x] T007 [US3] Implement Gradio/OpenAPI extraction in `backend/src/uaicp/ingestion/contract.py`
- [x] T008 [P] Implement dead-letter + SSRF guard in `backend/src/uaicp/ingestion/deadletter.py`
- [x] T009 Run `python scripts/health.py`

## RU
T001 setup; T002–T003 discovery; T004–T005 snapshot; T006–T007 contract; T008 dead-letter/SSRF; T009 health.