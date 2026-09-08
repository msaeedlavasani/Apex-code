#!/usr/bin/env python3
"""Validate bounded durable evidence receipts against the current registry."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from development_control import validate_receipt_file


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=ROOT / "development_control/agent_skill_registry.json")
    parser.add_argument("--receipt", type=Path, action="append", required=True)
    parser.add_argument("--repository-root", type=Path, default=ROOT)
    args = parser.parse_args()

    reports = []
    for receipt_path in args.receipt:
        report = validate_receipt_file(
            receipt_path,
            args.registry,
            repository_root=args.repository_root,
        )
        reports.append({"receipt": str(receipt_path), **report})
    print(json.dumps(reports, indent=2, sort_keys=True))
    return 0 if all(report["valid"] for report in reports) else 1


if __name__ == "__main__":
    sys.exit(main())
