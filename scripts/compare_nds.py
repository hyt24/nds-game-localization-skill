#!/usr/bin/env python3
"""Compare NDS executable components, banner, and NitroFS files by path."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import ndspy.rom


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def walk(folder, prefix=""):
    for index, name in enumerate(folder.files):
        yield prefix + name, folder.firstID + index
    for name, child in folder.folders:
        yield from walk(child, prefix + name + "/")


def file_map(rom):
    return {path: bytes(rom.files[file_id]) for path, file_id in walk(rom.filenames)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    a_raw, b_raw = args.baseline.read_bytes(), args.candidate.read_bytes()
    a, b = ndspy.rom.NintendoDSRom(a_raw), ndspy.rom.NintendoDSRom(b_raw)
    components = {}
    for name, attribute in (("arm9", "arm9"), ("arm7", "arm7"), ("arm9OverlayTable", "arm9OverlayTable"), ("arm7OverlayTable", "arm7OverlayTable"), ("banner", "iconBanner")):
        av, bv = bytes(getattr(a, attribute)), bytes(getattr(b, attribute))
        components[name] = {"changed": av != bv, "baseline_size": len(av), "candidate_size": len(bv), "baseline_sha256": digest(av), "candidate_sha256": digest(bv)}
    af, bf, rows = file_map(a), file_map(b), []
    for path in sorted(set(af) | set(bf)):
        av, bv = af.get(path), bf.get(path)
        status = "added" if av is None else "removed" if bv is None else "changed" if av != bv else "same"
        if status != "same":
            rows.append({"path": path, "status": status, "baseline_size": None if av is None else len(av), "candidate_size": None if bv is None else len(bv), "baseline_sha256": None if av is None else digest(av), "candidate_sha256": None if bv is None else digest(bv)})
    report = {"baseline": {"path": str(args.baseline), "size": len(a_raw), "sha256": digest(a_raw)}, "candidate": {"path": str(args.candidate), "size": len(b_raw), "sha256": digest(b_raw)}, "components": components, "nitrofs_changed_count": len(rows), "nitrofs_changes": rows}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "diff.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.out / "changed-files.tsv").write_text("status\tpath\tbaseline_size\tcandidate_size\n" + "".join(f'{r["status"]}\t{r["path"]}\t{r["baseline_size"]}\t{r["candidate_size"]}\n' for r in rows), encoding="utf-8")
    print(json.dumps({"components_changed": [k for k, v in components.items() if v["changed"]], "nitrofs_changed_count": len(rows)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
