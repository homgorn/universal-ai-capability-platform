# Implementation Plan: HF Ingestion

**Branch**: `004-hf-ingestion` | **Date**: 2026-11-25 | **Spec**: spec.md

## Summary
Offline-testable HF adapter with injected transport; paginated discovery, provenance snapshots,
Gradio/OpenAPI contract extraction, fingerprints, dead-letter queue and SSRF denials.

## Technical Context
Python 3.13, httpx interface (injected callable), uaicp.validation ports/fingerprint, pytest.
No new datastore; raw snapshots stored as JSON via existing provenance fields.

## Constitution Check
Provider-neutral core (PASS: HF is adapter), discovered != executable (PASS),
evidence first (PASS), tests (PASS), no graph DB (PASS), bilingual (PASS).

## Structure
`backend/src/uaicp/ingestion/{hf.py,contract.py,deadletter.py}` + tests.

## RU
Адаптер HF с инъекцией HTTP; без сети в тестах; использует uaicp.validation.