#!/usr/bin/env python3
"""Validate and summarize an NDS localization resource inventory."""
from __future__ import annotations

import argparse
import collections
import csv
import json
from pathlib import Path


STATUSES = {
    "discovered", "decoded", "recognized", "translated", "reviewed",
    "patched", "offline_verified", "runtime_verified", "preserve_original", "blocked",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inventory", type=Path)
    args = parser.parse_args()
    rows = list(csv.DictReader(args.inventory.open(encoding="utf-8-sig", newline="")))
    errors, seen = [], set()
    counts = collections.defaultdict(collections.Counter)
    for number, row in enumerate(rows, 2):
        resource_id = row.get("resource_id", "").strip()
        family = row.get("family", "").strip() or "<unspecified>"
        status = row.get("status", "").strip()
        if not resource_id:
            errors.append(f"line {number}: missing resource_id")
        elif resource_id in seen:
            errors.append(f"line {number}: duplicate resource_id {resource_id}")
        seen.add(resource_id)
        if status not in STATUSES:
            errors.append(f"line {number}: invalid status {status!r}")
        else:
            counts[family][status] += 1
        if status in {"patched", "offline_verified", "runtime_verified"} and not row.get("patched_rom_sha256", "").strip():
            errors.append(f"line {number}: {status} requires patched_rom_sha256")
        if status in {"offline_verified", "runtime_verified"} and not row.get("offline_evidence", "").strip():
            errors.append(f"line {number}: {status} requires offline_evidence")
        if status == "runtime_verified" and not row.get("runtime_evidence", "").strip():
            errors.append(f"line {number}: runtime_verified requires runtime_evidence")
        if status == "blocked" and not row.get("notes", "").strip():
            errors.append(f"line {number}: blocked requires notes")
    summary = {
        "total": len(rows),
        "families": {family: {"total": sum(counter.values()), **dict(sorted(counter.items()))} for family, counter in sorted(counts.items())},
        "errors": errors,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
