# Implementation Plan: HF Catalog Crawler

**Branch**: `005-hf-catalog-crawler` | **Date**: 2026-11-26 | **Spec**: spec.md

## Summary
Bounded, resumable crawler for the full public HF Space catalog. REST Hub API with Link
cursor pagination, canonical records + immutable raw snapshots, SHA-driven incremental
updates, checkpoints, dead-letter and a measured inventory report.

## Technical Context
Python 3.13, httpx, SQLAlchemy 2, Alembic, pytest. Storage: PostgreSQL (SQLite locally).
No execution of provider code, no cloning, no vector DB.

## Constitution Check
Principle VIII (ingestion first): PASS — this is the first active feature.
Provider-neutral (PASS), evidence first (PASS), tests (PASS), simplicity (PASS).

## Structure
`backend/src/uaicp/catalog/{client.py,crawler.py,report.py}` + `hf_space`, `ingest_checkpoint`
models + tests. CLI: `python -m uaicp.catalog.crawl --limit N`.

## RU
Стек: Python + httpx + SQLAlchemy. Модуль catalog + две новые таблицы + CLI с --limit.