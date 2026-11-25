"""CLI: python -m uaicp.validation.cli <contract.json> (exit non-zero on invalid)."""

from __future__ import annotations

import argparse
import json

from uaicp.validation.validate import validate_contract


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a capability contract JSON file")
    parser.add_argument("file", help="path to contract JSON")
    args = parser.parse_args(argv)

    with open(args.file, encoding="utf-8") as fh:
        contract = json.load(fh)

    result = validate_contract(contract)
    if result.valid:
        print("VALID")
        for w in result.warnings:
            print(f"warning: {w}")
        return 0
    print("INVALID")
    for e in result.errors:
        print(f"error: {e}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())