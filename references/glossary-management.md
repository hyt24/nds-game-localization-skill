# Glossary management

Build the glossary before batch translation. It is both translation context and a cross-resource consistency contract.

## Bootstrap

Copy `assets/glossary.csv` into the project. Populate candidates from:

- official title, manual, package, and trusted existing terminology;
- repeated source strings and OCR/glyph-recognition output;
- character names, aliases, honorifics, roles, organizations, and places;
- UI actions, modes, difficulty labels, save/load language, and interaction choices;
- chapter, item, card, record, operation, diagnosis, and technique names;
- medical, legal, military, historical, or other domain-specific terms;
- text embedded in images that must match dialogue or system messages.

Keep one canonical row per source term and meaning. Use separate rows when one source spelling genuinely has different meanings, and distinguish them with `context` and stable `term_id` values.

## Review states

- `proposed`: machine- or agent-suggested; translation may not rely on it as final.
- `reviewed`: human-confirmed and ready for translation prompts and consistency checks.
- `locked`: authoritative; agents must not alter it without explicit human approval.
- `preserve_original`: intentionally retain the source spelling or symbol.

Before batch/API translation, require high-impact and repeated terms to be `reviewed`, `locked`, or `preserve_original`. Ask the user to resolve ambiguous names, forms of address, title wording, and domain terms whose choice would propagate widely.

## Applying the glossary

Pass reviewed rows to the translation provider with speaker, scene, and surrounding-line context. Match by meaning and context, not blind substring replacement. Preserve variables and control markup.

Use the same canonical target for every rendering layer. For example, a card title shown as an image and a dialogue line announcing that card must derive from the same glossary entry. Preserve source punctuation when it is part of a formal title unless the user approves normalization.

When translation reveals a new term, add it as `proposed` and continue only where that unresolved term cannot create inconsistency. Never overwrite a reviewed or locked target from model output. Record conflicts and obtain human review.

Run:

```bash
python scripts/check_glossary.py path/to/glossary.csv --require-ready
```

Re-run the check after terminology edits and before packaging. Also audit translated text and image-title manifests against the glossary; the CSV checker validates the glossary itself, not every downstream occurrence.
