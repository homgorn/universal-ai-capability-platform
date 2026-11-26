# Tasks: HF Catalog Crawler

- [x] T001 Create `backend/src/uaicp/catalog/` package
- [x] T002 Add `hf_space` + `ingest_checkpoint` models in `backend/src/uaicp/db/models.py`
- [x] T003 [P] [US1] Tests for cursor pagination in `backend/tests/contract/test_catalog_pages.py`
- [x] T004 [US1] Implement `HFClient.iter_pages` in `backend/src/uaicp/catalog/client.py`
- [x] T005 [P] [US2] Tests for SHA incremental updates in `backend/tests/integration/test_catalog_incremental.py`
- [x] T006 [US2/US3] Implement canonical upsert in `backend/src/uaicp/catalog/crawler.py`
- [x] T007 [P] [US4] Tests for 429/backoff/dead-letter in `backend/tests/unit/test_catalog_resilience.py`
- [x] T008 [US4] Implement retry + dead-letter in client.py
- [x] T009 [P] [US5] Tests for report in `backend/tests/unit/test_catalog_report.py`
- [x] T010 [US5] Implement `inventory_report` in `backend/src/uaicp/catalog/report.py`
- [x] T011 Add CLI `backend/src/uaicp/catalog/crawl.py`
- [x] T012 Run bounded live crawl (500) and record measured results
- [x] T013 Run `python scripts/health.py`

## RU
T001–T002 setup; T003–T004 пагинация; T005–T006 инкремент; T007–T008 устойчивость;
T009–T010 отчёт; T011 CLI; T012 живой прогон 500; T013 health.