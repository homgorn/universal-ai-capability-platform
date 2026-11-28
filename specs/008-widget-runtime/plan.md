# Implementation Plan: Widget Runtime

**Branch**: `008-widget-runtime` | **Date**: 2026-11-28

## Summary
In-process widget runtime: scoped token mint/verify, channel constraint contracts, mode
resolution to Execution API. No provider secrets in browser payloads.

## Technical Context
Python 3.13, existing execution gateway + errors, pytest. No new datastore (token is signed
stateless; channel contracts are code).

## Constitution Check
Secrets never to browser (PASS), policy before execution (PASS), tests (PASS), simplicity (PASS).

## Structure
`backend/src/uaicp/widget/{tokens.py,channels.py,runtime.py}` + tests.

## RU
Виджет-runtime: токены, контракты каналов, режимы; без секретов в браузере.