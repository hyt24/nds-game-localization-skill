#!/usr/bin/env python3
"""Create a deterministic high-level Nintendo DS ROM inventory."""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
from pathlib import Path

import ndspy.rom


def walk(folder, prefix=""):
    for index, name in enumerate(folder.files):
        yield prefix + name, folder.firstID + index
    for name, child in folder.folders:
        yield from walk(child, prefix + name + "/")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("nds", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    raw = args.nds.read_bytes()
    rom = ndspy.rom.NintendoDSRom(raw)
    files, extensions, directories = [], collections.Counter(), collections.Counter()
    for path, file_id in walk(rom.filenames):
        data = bytes(rom.files[file_id])
        extensions[Path(path).suffix.lower() or "<none>"] += 1
        directories[path.split("/", 1)[0] if "/" in path else "<root>"] += 1
        files.append({"id": file_id, "path": path, "size": len(data), "sha256": digest(data), "magic_hex": data[:16].hex(), "lz10_candidate": bool(data) and data[0] == 0x10})
    report = {
        "rom": str(args.nds), "rom_size": len(raw), "rom_sha256": digest(raw),
        "game_title_ascii": bytes(rom.name).rstrip(b"\0").decode("ascii", "replace"),
        "game_code_ascii": bytes(rom.idCode).decode("ascii", "replace"),
        "arm9_size": len(rom.arm9), "arm7_size": len(rom.arm7),
        "arm9_overlay_count": len(rom.arm9OverlayTable) // 32,
        "arm7_overlay_count": len(rom.arm7OverlayTable) // 32,
        "nitrofs_file_count": len(files), "extensions": dict(sorted(extensions.items())),
        "top_directories": dict(sorted(directories.items())), "files": files,
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "inventory.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.out / "files.tsv").write_text("id\tpath\tsize\tsha256\tmagic_hex\tlz10_candidate\n" + "".join(f'{x["id"]}\t{x["path"]}\t{x["size"]}\t{x["sha256"]}\t{x["magic_hex"]}\t{int(x["lz10_candidate"])}\n' for x in files), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("rom_sha256", "game_title_ascii", "game_code_ascii", "nitrofs_file_count")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
