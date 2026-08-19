# Progress Management

Localization projects fail when “a script ran” is confused with “the game is translated.” Maintain evidence-backed state that another agent can resume without reconstructing history.

## Required records

### Human-readable progress

Keep `progress.md` concise and current. Record the active baseline/candidate, completed scope, terminology decisions, manual overrides, known limitations, validation state, and exact next action. Link to detailed ledgers rather than duplicating every row.

### Resource inventory

Track every resource family and review unit with stable IDs. Use these statuses only:

- `discovered`: located but not decoded;
- `decoded`: parser/export confirmed;
- `recognized`: source text/image identified;
- `translated`: translation exists but is unreviewed;
- `reviewed`: human-approved source and translation;
- `patched`: written into a candidate;
- `offline_verified`: candidate roundtrip/diff checks pass;
- `runtime_verified`: emulator/hardware evidence passes;
- `preserve_original`: intentionally unchanged with reason;
- `blocked`: cannot progress; record the concrete blocker.

Do not use percentages without defining the denominator. Report counts by status and resource family.

### Build ledger

Append one row per candidate. Never rewrite failed build history. Record parent SHA, output SHA, exact command, changed components, offline checks, runtime checks, and disposition (`test`, `rejected`, `candidate`, `release`). A newer version number does not imply better quality.

### Hypothesis log

Record resource-source hypotheses, format assumptions, runtime theories, and failures. Mark each `open`, `confirmed`, or `disproven` with evidence. Keep disproven rows; they prevent repeated dead ends.

### Runtime matrix

Record scene-specific expected/actual behavior, emulator/hardware version, save-state provenance, screenshot/log, and ROM SHA. Never reuse runtime approval from a different SHA unless component equivalence is proven.

## Agent update cadence

Update records:

1. after initial ROM inventory and denominator definition;
2. after every parser/recognition/translation review batch;
3. after every manual image or glossary decision;
4. immediately after each candidate build and diff;
5. immediately after runtime feedback, including failures;
6. before handoff, release, or stopping a long task.

When a user changes a translation or visual rule, update the authoritative glossary/config first, then the artifact, then progress records. Do not leave a decision only in conversation history.

## Reconciliation checks

Before reporting progress:

- verify every referenced path exists;
- recompute candidate SHA-256;
- compare inventory counts with source exports;
- ensure `patched` rows name a build SHA;
- ensure `offline_verified` rows link to roundtrip/diff output;
- ensure `runtime_verified` rows link to scene evidence;
- ensure the next action names its input, command/tool, and expected output.
