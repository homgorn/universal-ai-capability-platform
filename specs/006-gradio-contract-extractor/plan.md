# Implementation Plan: Gradio Contract Extractor

**Branch**: `006-gradio-contract-extractor` | **Date**: 2026-11-26

## Summary
Pure parsing layer for HF Gradio contract sources: agents.md, /gradio_api/info and MCP schema.
Injected fetcher, no provider execution, deterministic fingerprint.

## Technical Context
Python 3.13, existing `uaicp.validation` ports/fingerprint, pytest. No new datastore; results
are dicts stored later by the registry layer.

## Constitution Check
Evidence first (PASS), no execution (PASS), tests (PASS), simplicity (PASS).

## Structure
`backend/src/uaicp/toolcontract/{agents.py,gradio.py,extract.py}` + tests.

## RU
Слой парсинга контрактов: agents.py, gradio.py, extract.py; без исполнения провайдеров.