# Validation

## Validation Philosophy

AI-assisted extraction is used to reduce manual transcription work. It is **not treated as ground truth**.

The pipeline separates:

1. visual extraction,
2. parsing/normalization,
3. deterministic validation,
4. canonical identity validation,
5. aggregation.

A record that fails required validation is excluded from the clean downstream dataset.

## Deterministic Checks

The pipeline is designed to check, where applicable:

- exactly 10 player rows per result screen
- unique player IDs within a result screen
- player IDs against a canonical roster reference
- valid numeric fields
- non-negative core statistics
- valid playtime formatting
- map/type consistency
- team consistency
- source-file traceability
- duplicate raw rows
- aggregation consistency between raw, total, and Per-10 outputs

## Current Dataset QA

For the final Stage 2 dataset:

- 188 result-screen/map blocks
- 1,880 player-map rows
- 10 player rows per map block
- no duplicate player within a result screen
- no exact duplicate raw player row
- no missing map block in the final match dataset
- total and Per-10 outputs were recomputed from the clean source data and checked for consistency

## Known Blind Spot: Plausible Transcription Errors

Structural validation cannot detect every visually plausible error.

Example:

```text
Source: 12,840 damage
Extracted: 12,540 damage
```

Both values are numeric, non-negative, and structurally valid. A deterministic rule may therefore accept the incorrect value.

For this reason, validation should not be described as proof that every extracted field is error-free.

## Random Source-Screen Audit

A random audit is the recommended next validation layer.

Suggested protocol:

1. Randomly sample **30 of 188 maps** without selecting based on warning status.
2. Compare all 10 player rows against the original broadcast result screen.
3. Audit player identity, map position, eliminations, deaths, assists, damage, healing, mitigation, and playtime.
4. Record every field-level discrepancy.
5. Correct confirmed errors in the source dataset.
6. Publish both the sample size and observed discrepancy rate.

Recommended reporting format after completion:

```text
Random audit: 30 / 188 maps (300 player-map records)
Fields checked: N
Discrepant fields before correction: X
Observed field-level discrepancy rate: X / N
Confirmed discrepancies corrected: X
```

**Do not publish an error rate before the audit is actually completed.**

## Semantic Consistency Checks

Semantic checks are useful only when the game statistic has a valid accounting identity.

For example, simple equality between a team's total eliminations and the opponent's total deaths should **not** be used as a hard validation rule: Overwatch eliminations can credit multiple players for participation in the same kill and therefore do not form a one-to-one accounting identity with opponent deaths.

Any future semantic validation rule should first be justified against the exact in-game statistic definition.

## Validation Status Labels

A useful operational interpretation is:

- **PASS** — required deterministic checks passed
- **WARNING** — usable record with a condition worth review
- **FAIL** — excluded from clean downstream processing

These labels indicate pipeline validation status, not certainty that every visible number is correct.
