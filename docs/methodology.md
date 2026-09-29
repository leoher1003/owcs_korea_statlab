# Methodology

## Scope

This release covers **2026 OWCS Korea Stage 2**. The primary analytical unit for raw player statistics is a **player-map appearance**.

The project uses scoreboard-level statistics and tournament metadata available from public competition broadcasts. It does not contain event-level game telemetry.

## Player Identity and Roles

`player_id` is the primary player aggregation key.

The project distinguishes:

- **Map Position** — the position recorded for the player on a specific result screen
- **Roster Position** — the player's canonical primary roster position
- **Detailed Position** — the analytical role used for position-level comparisons

Canonical roster information is used to validate player identity. Map-level position is preserved separately so that an observed role on an individual map is not overwritten by the player's primary roster role.

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

> Where does this observed statistic fall relative to other eligible players in the same detailed position in this Stage 2 dataset?

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

## Current Analytical Boundary

The current release does not provide:

- Hero-adjusted player ratings
- Causal player or team effects
- Teamfight-level value
- Ultimate-efficiency models
- Context-adjusted player-impact ratings

Those analyses would require more granular data and/or additional modeling assumptions.
