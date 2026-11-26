"""Verify the catalog engine against the collected sample (no new crawl)."""

from __future__ import annotations

import json

from uaicp.catalog.report import inventory_report
from uaicp.db.models import IngestCheckpoint, KGTriple
from uaicp.db.session import engine, session_scope


def main() -> int:
    failures: list[str] = []
    with session_scope(engine) as session:
        report = inventory_report(session)
        checkpoint = session.get(IngestCheckpoint, "hf:spaces")
        graph_triples = session.query(KGTriple).filter(KGTriple.tenant_id == "public").count()

    if report["total"] < 500:
        failures.append(f"expected >=500 records, got {report['total']}")
    if checkpoint is None or not checkpoint.cursor:
        failures.append("resume checkpoint missing")
    elif checkpoint.items_seen < 500:
        failures.append(f"checkpoint items_seen={checkpoint.items_seen} < 500")
    if report["sdk_distribution"].get("gradio", 0) < 100:
        failures.append("gradio records missing")
    if report["with_models"] < 100:
        failures.append("expanded models missing (check expand[] fields)")
    if report["license_known"] == 0 or report["license_unknown"] == 0:
        failures.append("license parsing not exercised")
    if graph_triples < 1000:
        failures.append(f"knowledge graph has only {graph_triples} triples")

    payload = {"report": report, "graph_triples": graph_triples, "failures": failures}
    print(json.dumps(payload, indent=2))
    print("CATALOG VERIFY: " + ("PASS" if not failures else "FAIL"))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())