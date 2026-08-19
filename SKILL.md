---
name: nds-game-localization
description: Reverse-engineer, translate, patch, audit, and validate Nintendo DS ROM localization projects. Use for .nds files, NitroFS inventories, ARM9/overlay resource discovery, custom glyph-stream text, OCR-assisted script recovery, 4bpp/8bpp tiled graphics, palette-safe image editing, LZ10 containers, reproducible ROM builds, binary diffs, emulator testing, or preparing an open-source NDS translation workflow.
---

# NDS Game Localization

Build a reproducible localization pipeline. Treat every game format as unknown until evidence proves otherwise.

The bundled audit scripts require Python 3 and `ndspy`. Install Pillow only for project-specific image decoders and renderers.

## Configure OCR and translation

Before extracting text, read [references/ocr-and-translation-setup.md](references/ocr-and-translation-setup.md), copy `assets/env.example` to the project as `.env`, and run `scripts/check_setup.py`.

Keep services optional:

- **Manual mode:** no API; export contact sheets and review CSVs for human transcription/translation.
- **Local mode:** use local OCR such as manga-ocr; no source text leaves the machine.
- **Recommended mode:** use full-line Vision OCR as primary, a second OCR as evidence, and a translation API with glossary/context prompts.
- **Sensitive material:** obtain consent before sending dialogue or images to external services; record provider/model and avoid secrets in logs.

Never commit `.env`. Do not make builds depend on live APIs: save raw OCR/translation responses and reviewed results so packaging remains deterministic.

## Non-negotiable rules

- Work only with ROMs the user is authorized to modify. Never bundle or publish copyrighted ROM data, extracted commercial assets, proprietary fonts, keys, or credentials.
- Preserve an immutable source ROM. Write every candidate to a new path and record SHA-256.
- Script every extraction and patch. Keep human edits in review files or replacement PNGs, not ad-hoc binary edits.
- Prefer the smallest patch that works. Preserve compression state, block sizes, offsets, controls, palettes, file order, and unrelated files unless runtime evidence permits a change.
- Never call a build “final” from static checks alone. Separate offline integrity from emulator/hardware validation.
- Maintain progress records from the first audit onward. Update them after every material discovery, reviewed batch, patch, build, validation result, regression, or disproven hypothesis.

## Maintain project state

Read [references/progress-management.md](references/progress-management.md). At project start, copy these templates into a tracked project directory:

- `assets/progress-template.md`: human-readable handoff and current state;
- `assets/resource-inventory.csv`: every text/image/code resource and its state;
- `assets/build-ledger.csv`: immutable candidate lineage, hashes, diffs, and validation;
- `assets/hypothesis-log.csv`: discoveries, uncertainties, failures, and disproven assumptions;
- `assets/runtime-test-matrix.csv`: emulator/hardware evidence.

Use only defined status values. Never mark an item complete because a file was generated. “Patched,” “offline verified,” and “runtime verified” are different states. Before ending substantial work, reconcile the records with actual artifacts and state the next reproducible action.

Run `scripts/check_progress.py path/to/resource-inventory.csv` before reporting completion or handing off the project.

## Start here

1. Read [references/existing-localization-check.md](references/existing-localization-check.md). Identify the exact game title, region, revision, and game code, then **browse the current public internet** for existing translations, patches, active projects, and abandoned partial work. A local repository search or asking the user from memory is not sufficient.
2. If any existing localization is found, stop before extraction or translation and ask the user whether to use it, audit/improve it, continue it with permission, or start over. Record the decision and provenance. Do not assume a complete-looking patch is authorized, accurate, compatible, or reusable.
3. Copy `assets/project-manifest.yaml` into the project and fill it in.
4. Run `scripts/inspect_nds.py game.nds --out audit/source`.
5. Configure OCR/translation or explicitly select manual mode.
6. Read [references/reconnaissance.md](references/reconnaissance.md) and map NitroFS, executables, overlays, compression, and resource families.
7. Classify visible text as ordinary strings, custom glyph streams, raster/tiled art, or runtime/code-embedded text.
8. Follow only the applicable branch below.

## Text branch

Read [references/text-and-glyphs.md](references/text-and-glyphs.md).

1. Prove the container model with a byte-identical no-op roundtrip.
2. Export stable IDs, source, context, control metadata, capacity, and previews to review CSV.
3. Recover glyphs using full-line OCR, contextual voting, and authoritative human overrides.
4. Freeze names, UI terms, item/card titles, chapter titles, and domain terminology in a glossary.
5. Translate semantic units with speaker/scene context; preserve styles, variables, punctuation intent, and interaction labels.
6. Rebuild glyph slots while preserving unknown controls and stream rhythm.
7. Use strategies in risk order: static per-file remapping; capacity-aware wording; statically proven bounded expansion; runtime cache/hook only with instrumentation.
8. Reject fallback boxes, overflow, controls interpreted as glyphs, invalid page cursors, and unreviewed capacity excess.

## Graphics branch

Read [references/graphics.md](references/graphics.md).

1. Build a strict decoder and contact sheets.
2. Brute-render undecoded blocks as plausible 4bpp/8bpp tiles; strict coverage is not full-ROM coverage.
3. Use screenshot colors, palette signatures, loader strings, and source-vs-current diffs to locate missed assets.
4. Export clean base, Japanese original, and current translation for manual editing.
5. Match source bounds, baseline, center, colors, outline, shadow/glow, spacing, and UI edges.
6. Quantize to the original palette and preserve sprite transparency index 0.
7. Preserve page/block sizes unless allocator behavior is proven.
8. Re-decode the finished ROM and inspect the encoded result, not only the source PNG.

## Build and validation branch

Read [references/validation-and-release.md](references/validation-and-release.md).

1. Select an explicit baseline so completed localization layers do not regress.
2. Apply deterministic stages in documented order; reviewed/manual overrides go last.
3. Run format, stream, capacity, decompression, and banner checks.
4. Run `scripts/compare_nds.py baseline.nds candidate.nds --out audit/diff` and approve every changed component.
5. Re-extract candidate text and graphics and compare with reviewed artifacts.
6. Execute `assets/runtime-test-matrix.csv` in emulator/hardware, including fragile interaction paths.
7. Treat failures as evidence. Do not guess new cursor offsets, hook points, or VRAM addresses without traces.
8. Reconcile all progress ledgers, hashes, changed files, limitations, intentional omissions, evidence links, and reproduction commands.

## Runtime hooks

Read [references/runtime-hooks.md](references/runtime-hooks.md) before changing ARM9 or overlays.

- Prove hook entry, runtime cursor, selected record, upload completion, destination VRAM, and tile residency immediately before draw.
- Recompute overlay/BSS/arena boundaries whenever code grows.
- Prefer the game’s upload wrapper; direct writes can bypass DMA, bank, or cache behavior.
- A record existing, a tile having uploaded once, and an offline replay passing are necessary evidence—not runtime proof.

## Durable deliverables

Maintain source/candidate hashes, a resource map, roundtrip-tested parsers, glossary, reviewed translation data, image inventory, deterministic build, component diff, roundtrip QA, runtime evidence, and a handoff that records disproven hypotheses.

For public releases, publish code, schemas, checksums, and patch formats such as BPS/xdelta where lawful. Do not publish ROMs or extracted copyrighted assets.

## Acknowledgements

Read and preserve [references/acknowledgements.md](references/acknowledgements.md) when redistributing or adapting this Skill. Keep upstream names, links, and licenses intact.
