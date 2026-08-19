# Validation and Release

## Separate gates

1. Format: bounds, offsets, decompression, lengths, no-op roundtrip.
2. Semantic: reviewed text, glossary consistency, image translations, variables.
3. Build: no fallback/overflow, valid controls/cursors, correct banner CRC.
4. Scope: only intended executables, overlays, banner, and NitroFS files changed.
5. Roundtrip: candidate extraction matches approved artifacts.
6. Runtime: emulator/hardware traverses representative and fragile paths.

An earlier gate never substitutes for a later one.

## Runtime matrix

Test boot/title/new/continue/save/load, first page, ordinary and long pages, every style/color, every choice including wrong paths, touch/minigame/map/inventory/card transitions, chapter boundaries, credits, and every regression. Record ROM SHA, emulator/version, save provenance, expected/actual result, evidence, and verdict.

## Public release

Publish code, docs, schemas, checksums, and a patch—not a ROM. Include supported source hashes, reproduction command, changed-component manifest, limitations, intentional omissions, and licenses. Never redistribute extracted game art, dialogue, music, or commercial fonts without permission.
