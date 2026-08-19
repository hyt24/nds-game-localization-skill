# Reconnaissance

Produce a resource map before translating. Do not infer that a familiar extension has a familiar format.

## Inventory

- Record title, game code, region, ROM size, banner version, source SHA-256, ARM9/ARM7 sizes, overlay counts, and NitroFS paths.
- Group files by directory, extension, size, magic bytes, entropy, and compression signature.
- Detect nested compression; LZ10 commonly starts with `0x10`, but validate decompressed length.
- Search ARM9 and overlays for path fragments and formatted resource paths. Associate loaders with resource families.
- Search representative Japanese strings as Shift-JIS, UTF-16LE, EUC-JP, UTF-8, and game-specific encodings.

If visible text is absent from encoded searches, test raster art and custom glyph indices.

## Establish format hypotheses

For each family, document header/offset tables, compression layers, record boundaries, dimensions, bpp, palette fields, page/grid semantics, alignment/checksums, and loader evidence.

Build strict parsers with bounds checks. Require parse → encode no-op byte identity before patching.

## Coverage trap

A strict decoder reports only assets it understands. It does not prove full-ROM coverage. Brute-render undecoded blocks in plausible tile layouts, generate labeled contact sheets, and audit files unchanged between source and candidate ROMs.
