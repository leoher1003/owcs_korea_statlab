# Validation

## Validation Principle

AI-assisted extraction is used to reduce manual transcription work. **AI output is not treated as ground truth.**

The pipeline separates visual extraction, parsing/normalization, deterministic validation, canonical identity validation, and downstream aggregation.

## Deterministic Validation

The extraction/cleaning workflow checks the structure and consistency of result-screen records, including:

- expected 10-player result-screen structure
- duplicate players within a result screen
- player identity against canonical roster information
- numeric validity of core statistics
- non-negative core statistic values
- playtime validity
- map/type consistency
- team consistency
- source-file traceability
- exact duplicate raw rows

Invalid numeric values are not silently converted to zero.

## Final Dataset QA

The final Stage 2 dataset contains:

- **188** map/result-screen blocks
- **1,880** player-map rows

Final QA confirmed:

- 10 player rows per result screen
- no duplicate player within a result screen
- no exact duplicate raw player row
- no missing map block in the final match dataset
- no negative/non-numeric core statistic values in the final data
- no duplicate player rows in the accumulated or Per-10 outputs
- accumulated totals and Per-10 values matched recomputation from the clean player-map source data

## Manual Source-Screen Audit

A separate manual audit compared **20 maps** against the corresponding original result screens.

That sample contained:

- **20 / 188 maps**
- **200 player-map records**
- **9 checked fields per player-map record**
- **1,800 audited fields**

The checked fields were:

1. Player identity
2. Map position
3. Eliminations
4. Deaths
5. Assists
6. Damage
7. Healing
8. Mitigation
9. Playtime

### Result

```text
Maps audited:                 20
Player-map records audited:  200
Fields audited:             1,800
Observed discrepancies:         0
Observed sample discrepancy: 0 / 1,800 (0.00%)
```

No correction was required as a result of this audit.

The result means that **no discrepancy was observed in the 1,800 fields manually checked**. It does not establish that the complete 188-map dataset has a 0% error rate.

No reproducible random seed is claimed for this audit.

## Residual Extraction Risk

Deterministic validation can identify structural inconsistencies, invalid identities, malformed values, and aggregation errors, but it cannot guarantee that every visually extracted numeric value is correct.

For example, two different damage values can both be syntactically valid. A plausible transcription error can therefore pass structural validation.

The manual source-screen audit provides an additional empirical check, but the project remains an unofficial dataset and should be interpreted accordingly.

## Semantic Validation

A semantic check should only be used when the underlying game statistic has a valid accounting identity.

In particular, team eliminations should **not** be required to equal opponent deaths: Overwatch elimination credit is not a one-to-one accounting identity with opponent deaths.

## Known Corrections During QA

Confirmed issues identified during dataset review were corrected against source/reference information before the final public dataset was produced. These included identity/spelling normalization, metadata corrections, and confirmed statistic-field corrections.

The public files represent the corrected final dataset.
