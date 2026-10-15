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

## Stage 3 Additions

### Scoreboard data

Stage 3 result screens go through the same deterministic validation, with two additions:

- Map names are folded to one canonical spelling (case, accents and punctuation ignored) and checked against the map recorded for that `match_id`. A mismatch or an unknown map is reported, never guessed.
- A player ID that differs from the roster only by look-alike characters (0/O, 1/I/L, 5/S, 8/B) is matched to the roster automatically, but only when exactly one roster player matches. Every such change is logged; anything else fails as an unknown player.

Map results can also be compared against Liquipedia (`pipeline/fetch_liquipedia.py --compare`), which reports any difference rather than correcting it.

The Stage 3 scoreboard data has been checked by the author (2026-10-15).

### Teamfight records

Before export, every teamfight row is checked:

- its `match_id` exists in the match records;
- the winner is one of the map's two teams;
- each side has exactly five distinct heroes;
- every hero is a known hero with a role;
- each side is one tank, two DPS and two supports.

Failures are reported with the map and fight number; rows are never silently fixed or dropped.

These checks confirm structure, not judgment: they cannot show that a fight's winner or boundaries were called correctly. As a cross-check in the other direction, the VOD hero classifier (below) found 392 of the 395 heroes recorded in the Week 1 teamfight log (99.2%). A manual re-watch audit of a sample of teamfights has not been done yet.

### Hero playtime (VOD estimate)

For each of the 300 Stage 3 Week 1 player-maps, the VOD-estimated playtime summed over heroes is compared with the official per-map playtime from the result screen:

```text
Player-maps compared:        300
Within ±10% of official:     300 / 300 (100%)
Within ±5% of official:      96%
Median absolute difference:  6.5 s
```

Slot-to-player assignments come from the on-screen name plates and must match that map's scoreboard players exactly; otherwise the run stops.

Known limitations:

- A transition between rounds of 30 seconds or less cannot be told apart from a short HUD gap, so it is filled with the previous hero. The per-map gap report is the check for this.
- Brief portrait misreads can leave a few seconds on a hero the player did not really play. On the site, heroes below 0.5% of a player's time in a position are shown only as "Other".
