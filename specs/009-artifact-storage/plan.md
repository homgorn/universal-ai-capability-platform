# Implementation Plan: Artifact Storage

**Branch**: `009-artifact-storage` | **Date**: 2026-11-28

## Summary
Storage abstraction with LocalStore (default) and R2Store (ready, gated by config). Registry
keeps metadata only; hash verified on read.

## Technical Context
Python 3.13, SQLAlchemy Artifact model, pytest, tmp_path for local tests. R2 via S3 API when
enabled (not now — account lacks R2).

## Constitution Check
Simplicity (PASS), evidence (PASS), no inline binaries (PASS), tests (PASS).

## Structure
`backend/src/uaicp/storage/{base.py,local.py,r2.py,service.py}` + tests.

## RU
Абстракция хранилища: LocalStore сейчас, R2Store готов; в БД только метаданные.