# Security Policy

## Reporting a vulnerability

Do **not** open a public issue for a security vulnerability. Contact the maintainer privately via GitHub Security Advisories on this repository.

## Invariants enforced in code

- Provider secrets never reach browser clients; scoped session tokens are used instead.
- Every external execution passes a policy decision (ALLOW / DENY / REQUIRE_APPROVAL / ALLOW_WITH_LIMITS).
- Tenant isolation is enforced at the repository layer and via PostgreSQL RLS.
- Discovered resources are not executable until trust is promoted (T0–T4).
- Historical contract versions are immutable and append-only.
- SSRF, private-network access and oversized artifacts are denied by default.

## Known verification gaps (VERIFY)

Live provider inventory and exact API limits, license/redistribution status, channel feasibility and provider pricing are marked VERIFY in `wiki/pages/verify.md`. They are not asserted as facts.

## Health checks

Run `python scripts/health.py` before releases. Production additionally requires backup/restore, queue recovery, provider outage, SSRF and tenant-isolation suites (see `docs/SPECS.md` §22).