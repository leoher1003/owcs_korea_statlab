# Methodology

## Scope

This release covers **2026 OWCS Korea Stage 2** (complete) and **Stage 3** (in progress). Each stage is analyzed separately; the site's stage switch selects which one every page uses. The primary analytical unit for raw player statistics is a **player-map appearance**.

The project uses scoreboard-level statistics and tournament metadata available from public competition broadcasts. For Stage 3 it also uses **teamfight records annotated by hand from VODs** (see [Teamfights](#teamfights-stage-3)). It does not contain event-level game telemetry.

## Stage 3 Export

Stage 3 player statistics follow the same extraction and validation workflow as Stage 2 and are kept in a stage workbook. `pipeline/export_site_data.py` converts that workbook into the site dataset (`site/data/data_s3.js`) and stops with a list of problems instead of exporting when:

- a map does not have exactly 10 player rows, or a map in the match list has no player rows
- a player row or teamfight refers to a map that is not in the match list
- one week/day/match key mixes two different team pairings
- a player's workbook totals differ from the sum of the exported player-map rows
- any teamfight check fails (see [Teamfight Checks](#teamfight-checks))

Map name and map type for player rows always come from the match list via the map identifier, not from the player rows.

## Player Identity and Roles

`player_id` is the primary player aggregation key.

The project distinguishes:

- **Map Position** — the position recorded for the player on a specific result screen
- **Roster Position** — the player's canonical primary roster position
- **Detailed Position** — the analytical role used for position-level comparisons

Canonical roster information is used to validate player identity. Map-level position is preserved separately so that an observed role on an individual map is not overwritten by the player's primary roster role.

A player who switched position mid-stage (in Stage 3: LIP and TAEJONG) has one totals row per position. Their statistics are kept as separate entries named `PLAYER (POS)`, e.g. `LIP (DPS)` and `LIP (SPT)`, so that totals, Per-10 values, eligibility, and percentiles are computed within each position. The player profile shows them under one name with a position selector.

## Accumulated Statistics

Validated player-map records are aggregated by player to produce totals for:

- Eliminations
- Deaths
- Assists
- Damage
- Healing
- Mitigation
- Playtime

## Per-10 Statistics

Per-10 statistics normalize counting statistics to ten minutes of observed playtime:

```text
Per10 = Statistic / Total Playtime (seconds) × 600
```

Per-10 makes different amounts of playtime easier to compare. It does **not** adjust for hero selection, team composition, map, opponent, team strategy, or game state.

## Minimum Playtime

A player must have at least **30 minutes of total playtime** to be included in rankings, percentile comparisons, and most player-level visualizations.

Players below the threshold remain in the underlying processed dataset.

The threshold reduces extreme low-playtime comparisons but does not eliminate sampling uncertainty.

## Percentile Rankings

Percentiles compare eligible players within the same **Detailed Position**.

They answer a descriptive question:

> Where does this observed statistic fall relative to other eligible players in the same detailed position in this stage's dataset?

They should not be interpreted as an overall player-skill or player-impact rating.

## Interpretation and Confounding

Overwatch scoreboard statistics are context dependent. They can be affected by:

- Hero selection
- Team composition
- Map and mode
- Opponent
- Team strategy and tempo
- Role responsibilities
- Fight length and game state

The current dataset does not contain sufficient hero-level or event-level context to adjust for these factors.

Accordingly, player rankings, Per-10 statistics, plots, and percentiles are **descriptive, context-unadjusted comparisons**. A higher damage, healing, elimination, or mitigation rate is not by itself evidence of greater overall player impact.

Small eligible player pools can also make percentile differences coarse.

## Hero Bans

Hero-ban records can be explored by banning team and match/map context.

Relationships between bans and results in the current Stat Lab are descriptive associations. The project does not claim that an observed ban caused a particular match result.

## Team Map Summaries

A map must have at least **3 team appearances** to be eligible for Best Record Map / Worst Record Map labeling.

When records are tied, more map appearances are preferred; any remaining display tie is resolved deterministically.

## POTM

Player of the Match records are stored separately and linked by player identity where needed.

POTM is an award record, not a modeled performance metric.

## Teamfights (Stage 3)

### Definition

A **teamfight** is a fight for control of the point, payload, or robot. Uneven fights (4v5, 3v5) count. The **winner** is the team that ends up in control; there are no draws.

Each teamfight is recorded by hand from the VOD as one row: the map, its order within the map, the five heroes on each side **at the start of the fight**, and the winner. All fights are judged by a single annotator. Hero swaps during a fight are not recorded.

Stage 3 teamfight coverage is currently Week 1 (338 teamfights on 30 maps).

### Compositions

A **composition** is the set of five heroes on one side. Two compositions are the same when they contain the same five heroes, in any order. Compositions are displayed Tank, DPS, Support, then alphabetically within each role, using the hero roles in `HERO_ROLES` (`pipeline/export_site_data.py`).

Roles for heroes added after the reference list were inferred from the records themselves: every recorded composition is 1 tank / 2 DPS / 2 support, and only one role assignment satisfies that for every fight.

### Statistics

- **Team teamfight record / win rate**: fights won and lost by a team; win rate = W / n. It is always shown with n. A team's own record includes its mirror fights.
- **Frequency**: team-side uses of a composition. A mirror fight counts twice, once per side.
- **Mirror**: a fight in which both teams played the same composition. Across all teams, mirrors are excluded from the composition's W/L and win rate (one side always wins) and counted separately.
- **Composition win rate** = W / (W + L), mirrors excluded.
- **Share** = fights in which the composition appeared / all fights, with a mirror counted once.
- **Team filter**: filtered to one team, the composition table shows that team's own record (mirrors included in W/L), and share is out of that team's fights.
- **Favorite team**: the team that used the composition most often (ties listed together).
- **Composition vs composition**: the teamfight record between two chosen compositions, with a per-map breakdown.

A composition needs at least **10 non-mirror teamfights** to be ranked or shown as a team's best win-rate composition. Compositions below that are available on demand and are not ranked.

The same definitions are implemented in SQL (`pipeline/sql/teamfights.sql`: `tf_side`, `tf_matchup`, `comp_stats`, `team_tf_stats`) for the workbook `COMP STATS` sheet, and in `site/app.js` for the site.

### Teamfight Checks

`pipeline/sql/checks_teamfights.sql` holds zero-row checks; any returned row is a problem and blocks the export:

- the teamfight's map is in the match list
- the winner is one of the two teams
- each side has five distinct heroes
- every hero has a role
- each side is 1 tank / 2 DPS / 2 support

### Interpretation

Teamfight and composition win rates are **descriptive and context-unadjusted**. They are affected by team strength, opponent, map, fight type, and game state, and a composition's record largely reflects the teams that played it. Many compositions have few fights, so differences between win rates can be within sampling noise. The fight boundaries and winners are one annotator's judgment.

## Current Analytical Boundary

The current release does not provide:

- Hero-adjusted player ratings
- Causal player or team effects
- Teamfight-level value (teamfight win rates are recorded, but no player or fight value model is fitted)
- Ultimate-efficiency models
- Context-adjusted player-impact ratings

Those analyses would require more granular data and/or additional modeling assumptions.
