# Implementation Plan: Evaluator

**Branch**: `007-evaluator` | **Date**: 2026-11-27

## Summary
Pure deterministic evaluator + profile ranking over evidence-marked dimensions. No network,
no invented values; unknown stays null + VERIFY.

## Technical Context
Python 3.13, existing enums/provenance, pytest. No new datastore.

## Constitution Check
Evidence first (PASS), multidimensional quality (PASS), no invented prices (PASS), tests (PASS).

## Structure
`backend/src/uaicp/evaluation/{evaluator.py,ranking.py}` + tests.

## RU
Чистый детерминированный оценщик + профили; без сети и выдуманных значений.