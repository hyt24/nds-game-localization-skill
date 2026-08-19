# OCR and Translation Setup

## Choose a mode

| Mode | OCR | Translation | Network | Best for |
|---|---|---|---|---|
| Manual | Human review | Human review | No | Small projects, sensitive content |
| Local | manga-ocr or another local model | Manual/local model | No after model install | Privacy and repeatability |
| Hybrid | Full-line Vision OCR + local secondary OCR | Cloud API | Yes | Large projects and difficult glyph maps |

Do not require all providers. Detect what is available, report missing optional capabilities, and continue with a lower mode.

## OCR guidance

- Prefer full-line recognition over isolated tiny glyph OCR because sentence context resolves ambiguous bitmaps.
- Use a second engine as evidence, not automatic truth.
- On macOS, Apple Vision can provide strong local full-line Japanese OCR without an API key.
- manga-ocr is useful as a local secondary engine; model installation/download can require network access and substantial disk space.
- Preserve OCR outputs, model names/versions, image IDs, confidence/evidence, and human overrides.
- Never overwrite reviewed source text when the glyph map changes; produce a new audit column or revision.

## Translation API guidance

Support provider-neutral settings. At minimum configure provider, model, endpoint when non-default, and API key through environment variables. A translation prompt should include:

- source language and target locale/script;
- speaker, scene, neighboring lines, and UI purpose;
- authoritative glossary entries;
- punctuation/color/variable preservation rules;
- visible slot or line capacity;
- instruction to return stable structured output.

Cache the raw response and save reviewed translations separately. Packaging must consume reviewed local files, never call an API live.

## Security and privacy

- Put secrets only in `.env`; add `.env` to `.gitignore`.
- Do not print keys, authorization headers, or full provider responses containing secrets.
- Ask before sending extracted game text or screenshots to a third party.
- Document which provider received which content and whether retention/training controls apply.
- Remove credentials and copyrighted extracted data before open-source release.

## Setup verification

Copy `assets/env.example` to `.env`, fill only the selected provider, then run:

```bash
python scripts/check_setup.py --env .env
```

The check reports capabilities without validating or exposing API keys. Test provider connectivity separately only after user authorization.
