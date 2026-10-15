# Teamfight Rules

Teamfight data is a new section in progress (Stage 3 onward). It is recorded **manually** by the user in the Excel master's `TEAMFIGHT INFO` sheet. It is not AI-extracted, but it is still not ground truth: manual entry produces typos, omissions, and inconsistent judgment calls.

## 1. Source Format (`TEAMFIGHT INFO`)

| Column | Meaning |
|---|---|
| `Match_Id` | Map-level `match_id`; filled **only on the first row of each map block** |
| `Count` | Fight number within the map |
| `Team 1 P1..P5` | Team 1's hero composition during the fight |
| `Team 2 P1..P5` | Team 2's hero composition during the fight |
| `Teamfight Winner` | `team_id` of the winning team |

Team 1 and Team 2 follow the same order as `MATCH INFO` for that `match_id`.

- **Blank `Match_Id`:** Forward-fill it on read. A data row before any `Match_Id` is an error.
- **Slot order:** P1..P5 order is not meaningful and is not linked to players. Compare compositions as unordered sets.
- **Hero names:** Use the sheet's uppercase spelling (e.g. `D.VA`, `JETPACK CAT`). Public `hero_bans.csv` uses display spelling (`D.Va`), so map names explicitly at export. Never fuzzy-match them.

## 2. Definitions Owned by the User

The definition is in `docs/TEAMFIGHT_DEFINITION.md` (finalized 2026-10-09). That file is the single source of truth.

- Do not reinterpret, extend, or "improve" it. If a case is not covered, flag it to the user.
- There is no draw. Every fight has exactly one winning team.
- The recorded composition is the one at the start of the fight.
- When publishing, summarize it in `docs/METHODOLOGY.md` without changing its meaning.

Decided 2026-10-10:

- **Map completeness:** marked in the `Map Complete` column, the rightmost column of `TEAMFIGHT INFO`. Aggregate only maps marked complete. A blank cell means incomplete; never infer completeness.
- **Team teamfight win rate:** no minimum sample, but always show n.
- **Composition win rate:** rank only compositions with 10 or more teamfights.
- **The 9 Week 1 maps recorded before the definition:** the user re-checks them personally. Do not modify or re-judge them.

## 3. Validation (Before Any Aggregation or Export)

Report every failure with the sheet row and `match_id`. Never silently fix or drop a row.

- `match_id` exists in `MATCH INFO`.
- `Teamfight Winner` is one of that map's `team_1` / `team_2`.
- Each side has exactly 5 non-blank heroes, with no duplicates.
- Every hero name is in the known hero list. A new name is flagged for confirmation, not accepted.
- `Count` runs 1..n with no gaps within each map. A blank `Count` is a validation failure, not a value to infer.
- Optional consistency warning: the map winner normally wins at least one fight. Treat a violation as a warning, not an error.

Structural checks do not prove the winners are correct. Before publication, also run a manual re-watch audit of a sample, as was done for Stage 2.

## 4. Coverage

- Teamfight logs cover only some maps while entry is in progress. A map with no log is **missing**, never "0 fights".
- Aggregate only over maps whose log is complete. Always report coverage as "N of M maps".
- Do not compare teams with different coverage without showing each team's map and fight counts.

## 5. Statistics

- Teamfight statistics are **team-level and composition-level only**. The sheet does not record which player played which hero, so never attribute fights to individual players or join them to `player_id`.
- Teamfight win rate = fights won / fights recorded. Always show the denominator (n).
- Composition statistics group by the unordered 5-hero set per side.
- Use small-sample thresholds for rankings. The user sets the threshold; do not reuse the 30-minute player rule.
- Keep teamfight metrics separate from scoreboard and Per-10 metrics. Do not combine them into a single rating.

## 6. Publication

- Publish teamfight data only through an explicit, user-approved export from the Excel master to `data/stage<N>/` and `site/data/`.
- Add the public schema to `docs/DATA_DICTIONARY.md` before publishing.
- The site section must show coverage and sample sizes, and must label the data as manually recorded.
