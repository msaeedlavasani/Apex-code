#!/usr/bin/env python3
"""Lean static validation for the architecture-first Apex Code repository."""

from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "docs/architecture/00-PRODUCT-VISION-AND-PRINCIPLES.md",
    "docs/architecture/01-MODULAR-PRODUCT-ARCHITECTURE-v1.md",
    "docs/architecture/02-EXECUTION-DATA-MODEL-v1.md",
    "docs/architecture/03-EXECUTION-MODEL-v1.md",
    "docs/architecture/04-EXECUTION-API-v1.md",
    "docs/architecture/05-ARCHITECTURE-STATUS.md",
    "docs/evidence/OPENWORK-FEASIBILITY.md",
    "docs/evidence/OPEN-QUESTIONS.md",
]
STATUSES = {"FROZEN", "FREEZE_CANDIDATE", "PROPOSED", "INFERENCE", "UNKNOWN", "NOT_PROVEN"}
SECRET_NAME = re.compile(r"(^|/)(\.env(?:\..*)?|id_rsa(?:\..*)?|credentials?\.(?:json|yml|yaml)|.*\.(?:pem|key|p12|pfx))$", re.I)
SECRET_CONTENT = re.compile(
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:AKIA|ASIA)[0-9A-Z]{16}\b|\bgh[pousr]_[A-Za-z0-9_]{20,}\b|\bsk-[A-Za-z0-9_-]{20,}\b"
)
LINK = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")


def tracked_files():
    result = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, check=True, stdout=subprocess.PIPE)
    return [ROOT / item for item in result.stdout.decode().split("\0") if item]


def fail(message):
    print(f"ERROR: {message}")


def main():
    errors = []
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    files = tracked_files()
    markdown = [path for path in files if path.suffix.lower() in {".md", ".markdown"}]
    for path in markdown:
        text = path.read_text(encoding="utf-8")
        if len(re.findall(r"^```", text, re.MULTILINE)) % 2:
            errors.append(f"unbalanced fenced code block: {path.relative_to(ROOT)}")
        for target in LINK.findall(text):
            target = target.split("#", 1)[0].strip().strip("<>")
            if not target or re.match(r"(?:https?:|mailto:|#)", target):
                continue
            if not (path.parent / target).resolve().is_file():
                errors.append(f"broken internal link in {path.relative_to(ROOT)}: {target}")

    status_re = re.compile(r"Status:\s*\*\*([A-Z_]+)\*\*|\|[^|]+\|\s*([A-Z_]+)\s*\|")
    for path in (ROOT / "docs/architecture").glob("*.md"):
        for match in status_re.finditer(path.read_text(encoding="utf-8")):
            status = match.group(1) or match.group(2)
            if status not in STATUSES:
                errors.append(f"invalid architecture status in {path.relative_to(ROOT)}: {status}")

    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        if SECRET_NAME.search(relative):
            errors.append(f"secret-bearing filename is tracked: {relative}")
            continue
        if path.stat().st_size > 2_000_000:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if SECRET_CONTENT.search(content):
            errors.append(f"obvious secret pattern in tracked file: {relative}")

    if errors:
        for error in errors:
            fail(error)
        return 1
    print(f"Documentation validation passed ({len(markdown)} Markdown files; {len(files)} tracked files scanned).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
