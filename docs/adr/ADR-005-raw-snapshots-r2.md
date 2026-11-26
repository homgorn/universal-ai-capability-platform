# ADR-005 — Raw snapshots: PostgreSQL now, R2 later

**Date**: 2026-11-26
**Status**: Accepted (owner decision, deferred work)

## Context

MVP-1 stores each HF Space's raw provider response as JSON in PostgreSQL alongside the
canonical record. This is simple and sufficient for a bounded sample. A full inventory will
produce a much larger volume of snapshots and long-term retention needs.

## Decision

1. For MVP-1 and the first bounded crawls, keep `hf_space.raw_snapshot` and
   `snapshot_history` as JSON in the canonical store.
2. In the roadmap (before a full production inventory), move raw snapshots to Cloudflare R2:
   store `storage_uri`, `sha`, `size` and `observed_at` in PostgreSQL; keep the object as the
   authoritative immutable snapshot.
3. The canonical record and inventory report must remain independent of where the raw bytes
   live, so the migration is behind the catalog layer, not the consumer layer.

## Consequences

- No R2 bucket or binding is created in this feature.
- A future migration task must backfill existing JSON snapshots into R2 and verify hashes.
- `docs/original-research-2026-10-07.md` §23 already separates PostgreSQL (truth) from
  object/vector/graph concerns; this ADR makes the object-storage choice explicit.

## Alternatives rejected

- Creating an R2 bucket now: premature before measured catalog volume.
- Dropping raw snapshots: breaks provenance and drift comparison (constitution II).