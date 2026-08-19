#!/usr/bin/env python3
"""Validate the localization glossary before batch translation."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path


REQUIRED_COLUMNS = {
    "term_id",
    "source",
    "target",
    "type",
    "context",
    "evidence",
    "status",
}
VALID_STATUSES = {"proposed", "reviewed", "locked", "preserve_original"}
READY_STATUSES = {"reviewed", "locked", "preserve_original"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    parser.add_argument(
        "--require-ready",
        action="store_true",
        help="fail when the glossary is empty or contains proposed entries",
    )
    args = parser.parse_args()

    errors: list[str] = []
    with args.csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing = sorted(REQUIRED_COLUMNS - columns)
        if missing:
            errors.append(f"missing columns: {', '.join(missing)}")
        rows = list(reader)

    ids: dict[str, int] = {}
    meanings: dict[tuple[str, str], set[str]] = defaultdict(set)
    for line_no, row in enumerate(rows, start=2):
        term_id = row.get("term_id", "").strip()
        source = row.get("source", "").strip()
        target = row.get("target", "").strip()
        context = row.get("context", "").strip()
        status = row.get("status", "").strip()

        if not term_id:
            errors.append(f"line {line_no}: empty term_id")
        elif term_id in ids:
            errors.append(f"line {line_no}: duplicate term_id {term_id!r} (first at line {ids[term_id]})")
        else:
            ids[term_id] = line_no
        if not source:
            errors.append(f"line {line_no}: empty source")
        if not target:
            errors.append(f"line {line_no}: empty target")
        if status not in VALID_STATUSES:
            errors.append(f"line {line_no}: invalid status {status!r}")
        if args.require_ready and status not in READY_STATUSES:
            errors.append(f"line {line_no}: status {status!r} is not translation-ready")
        if source and target:
            meanings[(source, context)].add(target)

    for (source, context), targets in meanings.items():
        if len(targets) > 1:
            errors.append(
                f"conflicting targets for source={source!r}, context={context!r}: "
                + ", ".join(sorted(repr(value) for value in targets))
            )

    if args.require_ready and not rows:
        errors.append("glossary is empty")

    if errors:
        print("Glossary check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Glossary check passed: {len(rows)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
