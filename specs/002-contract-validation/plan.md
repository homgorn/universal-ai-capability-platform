# Implementation Plan: Contract Validation and Error Taxonomy

**Branch**: `002-contract-validation` | **Date**: 2026-11-25 | **Spec**: [spec.md](./spec.md)

## Summary

Pure-logic validation layer: canonical ports, JSON Schema validation, seven-dimension
compatibility checking, a 15-code error taxonomy with normalization, deterministic
fingerprinting/drift, and a CI-friendly CLI. Reuses the existing `uaicp` backend package.

## Technical Context

**Language/Version**: Python 3.13
**Primary Dependencies**: jsonschema (draft 2020-12), pydantic (optional), existing uaicp
**Storage**: none (stateless logic)
**Testing**: pytest
**Target Platform**: Linux/Windows
**Project Type**: library + CLI
**Performance Goals**: validate a contract under 50 ms
**Constraints**: deterministic; no provider calls
**Scale/Scope**: single-contract validation

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| I Provider Neutrality | PASS | no provider specifics |
| II Contracts Immutable | PASS | fingerprint deterministic |
| III Discovered != Executable | PASS | no execution |
| IV Evidence First | PASS | no invented facts |
| V Test-Backed | PASS | tests per story |
| VI Simplicity | PASS | no new datastore |
| VII LLM-Readable | PASS | bilingual docs |

No violations.

## Project Structure

```text
backend/src/uaicp/validation/
├── ports.py        # CanonicalPort + parsing
├── errors.py       # ErrorCode (15) + NormalizedError + normalize
├── fingerprint.py  # deterministic fingerprint + drift
├── compat.py       # seven-dimension compatibility
├── validate.py     # validate_contract -> ValidationResult
└── cli.py          # python -m uaicp.validation.cli <file>
backend/tests/contract|unit/  # tests
```

## RU — Резюме
Стек: Python + jsonschema, без хранилища. Модуль `uaicp/validation/*` + CLI. Constitution
Check PASS. Граф/БД не затрагиваются.