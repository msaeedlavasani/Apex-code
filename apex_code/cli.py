"""Command-line entry point for the first safe vertical slice."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import ExecutionCoordinator


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the bounded Apex Code REPORT.md vertical slice")
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--opencode", default="opencode")
    parser.add_argument("--model", default="opencode/big-pickle")
    args = parser.parse_args()
    from .runtime import OpenCodeRuntimeAdapter

    result = ExecutionCoordinator(OpenCodeRuntimeAdapter(args.opencode, args.model)).run_report(args.workspace)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["semantic_success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
