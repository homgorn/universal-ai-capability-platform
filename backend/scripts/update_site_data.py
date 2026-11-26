"""One command to refresh DB-derived data, wiki, nav and knowledge graph.

Run from backend/:  PYTHONPATH=src python scripts/update_site_data.py
"""

from __future__ import annotations

import shutil
from pathlib import Path

from uaicp.catalog.graph import build_catalog_graph
from uaicp.db.session import engine, session_scope
from uaicp.wiki.generate import generate

# Imported via scripts path below (kept as functions so CI can reuse them).
ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    # 1. canonical catalog -> site JSON + API endpoints
    import importlib.util

    def run_script(name: str) -> None:
        path = Path(__file__).resolve().parent / name
        spec = importlib.util.spec_from_file_location(name.replace(".py", ""), path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.main()

    run_script("export_catalog_for_site.py")
    run_script("export_nav_for_site.py")

    # 2. knowledge graph from catalog
    with session_scope(engine) as session:
        graph = build_catalog_graph(session)
    print("graph:", graph)

    # 3. wiki regeneration + sync into the site
    generate()
    wiki = ROOT / "wiki"
    shutil.copy2(wiki / "llms.txt", ROOT / "llms.txt")
    for target in (ROOT / "site" / "public", ROOT / "site" / "src" / "content" / "topics"):
        target.mkdir(parents=True, exist_ok=True)
        shutil.copy2(wiki / "llms.txt", target / "llms.txt")
        shutil.copy2(wiki / "llms-full.txt", target / "llms-full.txt")
    for page in (wiki / "pages").glob("*.md"):
        shutil.copy2(page, ROOT / "site" / "src" / "content" / "topics" / page.name)
    print("site data, navigation, graph and wiki updated")


if __name__ == "__main__":
    main()