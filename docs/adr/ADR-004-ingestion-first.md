# ADR-004 — Ingestion-first reordering

**Date**: 2026-11-26
**Status**: Accepted (owner instruction)

## Context

The owner clarified that the original goal was to extract all Hugging Face Spaces first and
build the registry/routing/product layers on top. The spec package (`docs/SPECS.md` v1) had
already abstracted those upper layers, and our first SDD feature (Knowledge Foundation) built
a wiki/store/graph before a real catalog existed. The site built on top of that is therefore
a rendered README rather than a product surface.

## Decision

1. The next feature is **HF Catalog Crawler (MVP-1)**: bounded, resumable, cursor-paginated
   ingestion of HF Spaces into PostgreSQL, with raw snapshots, SHA-based incremental updates,
   provenance and measured corpus statistics.
2. Subsequent order follows the original research: contract extractor → evaluator → widget
   runtime → Telegram adapter → planner → other providers.
3. Existing artifacts (wiki, DB models, validation, execution gateway, site, analytics) are
   kept as foundations and re-used, not deleted. They are no longer treated as the roadmap.
4. A new governing principle is added to the constitution: "Ingestion before intelligence" —
   no planner/SEO/analytics work is justified until the catalog exists and is measured.

## Consequences

- Spec Kit features 001–003 remain valid as reusable components but are deprioritized.
- New feature `005-hf-catalog-crawler` becomes the active task.
- The site must eventually be generated from real catalog data, not from README prose.

## Alternatives rejected

- Continue polishing the site/SEO: building distribution for a catalog that does not exist.
- Follow `SPECS.md` P0 order literally: it starts with repository discipline and HF ingestion,
  but our implementation had already skipped to later layers; reorder explicitly rather than
  silently.