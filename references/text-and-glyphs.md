# Text, Glyphs, and Translation

## Custom glyph streams

Determine glyph dimensions/bpp, static capacity, stream word width/endianness, glyph/control values, line/page boundaries, colors, variables, waits, choices, mode switches, and state-marker tails. Preserve unknown controls and ordering. Apparent padding can be interaction state.

## Recognition workflow

1. Render full lines with stable file/line IDs.
2. Use strong full-line vision OCR as primary and a second engine as evidence.
3. Align OCR text to glyph sequences through repeated contexts and known anchors.
4. Vote per distinct line; repeated use of one glyph in one line counts once.
5. Exclude human overrides, transparent blanks, composites, and preserve-original symbols from anchors.
6. Export unresolved glyphs with complete sentence context for human review.

Track real conflicts and weak evidence; do not request review merely because two engines agree.

## Translation data

Use stable records such as:

```csv
resource,line_id,speaker,scene,jp_text,cn_text,color_info,slot_budget,status,notes
```

Keep recognition separate from translation. Never regenerate reviewed `jp_text` from an older glyph map. Keep one authoritative glossary for names, card/item titles, chapter names, UI verbs, and domain terms; synchronize it into dialogue and images.

## Capacity and safety

- Count rendered glyph slots, not Unicode code points alone.
- Prefer concise natural translation without silently changing meaning.
- Preserve page/control boundaries unless runtime behavior is understood.
- Preserve interaction-sensitive tail slots when evidence shows the engine consumes them.
- Rebuild color controls from localized spans.
- Use static remapping first. Expand only after proving destination capacity.
- Require instrumentation for dynamic caches and fail hard on overflow.
