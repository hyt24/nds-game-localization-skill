# Tiled Graphics Localization

## Decode and locate

- NDS tiles are commonly 8×8; verify 4bpp nibble order and 8bpp layout.
- Tile maps, sprite tables, affine layouts, animation pages, and palettes may be separate.
- Reassemble suspected frame grids in row-major and column-major layouts before calling them animation.
- Escalate discovery through strict decode/contact sheets, brute rendering, palette signatures, executable path strings, ROM diffs, then VRAM/OAM capture.

## Edit

- Export clean base, Japanese reference, and translated result at native resolution.
- Match x/y, visible bounds, baseline, center, foreground/background, outline, shadow/glow, spacing, and clipping.
- Remove Japanese shadows without covering UI borders or rounded corners.
- Preserve original pixels for identical glyphs when useful.
- For tiny text, render at target integer size; test bitmap fonts and threshold antialiasing when quantization muddies strokes.
- For art titles, compose per character when size, color, rotation, spacing, or glow differs.
- Apply manual PNG overrides last and protect them from regeneration.

## Encode and verify

- Preserve palette bytes unless a verified engine path supports changes.
- Use existing colors where possible, then nearest-index quantization.
- Keep sprite index 0 transparent.
- Assert page, block, record, and decompressed lengths; preserve outer compression.
- Decode the candidate ROM and inspect the actual encoded result.
