"""CLI: python -m uaicp.catalog.crawl --limit 500 [--page-size 100]"""

from __future__ import annotations

import argparse
import json

from uaicp.catalog.client import HFClient
from uaicp.catalog.crawler import SOURCE, run_crawl
from uaicp.catalog.report import inventory_report
from uaicp.db.models import IngestCheckpoint
from uaicp.db.session import engine, init_db, session_scope


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Crawl the public Hugging Face Space catalog")
    parser.add_argument("--limit", type=int, default=500, help="max number of Spaces to ingest")
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument("--restart", action="store_true", help="ignore checkpoint cursor")
    parser.add_argument("--refresh", action="store_true", help="re-apply data for unchanged SHA")
    args = parser.parse_args(argv)

    init_db(engine)
    client = HFClient()
    with session_scope(engine) as session:
        checkpoint = session.get(IngestCheckpoint, SOURCE)
        if args.restart and checkpoint:
            checkpoint.cursor = None
            checkpoint.items_seen = 0
        run = run_crawl(
            session,
            client,
            limit=args.limit,
            page_size=args.page_size,
            refresh=args.refresh,
        )
        report = inventory_report(session)

    payload = {"run": run, "report": report, "client_dead_letters": client.dead_letters}
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())