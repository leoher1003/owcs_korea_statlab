# Methodology

## Scope

This release covers **2026 OWCS Korea Stage 2** and is based primarily on map-level result screens and competition metadata available from public broadcasts.

The analytical unit for raw player statistics is a **player-map appearance**.

## Player Identity and Roles

`player_id` is the primary player aggregation key.

Three role concepts are intentionally kept separate:

- **map_position** — position shown for the player on that specific result screen
- **roster_position** — canonical primary roster position
- **detailed_position** — analytical role used for position-level comparison

Canonical roster metadata is used to validate player identity, but it does not overwrite the observed map-level position.

## Accumulated Statistics

Player totals are aggregated from validated player-map records.

Core fields:

- Eliminations
- Deaths
- Assists
- Damage
- Healing
- Mitigated damage
- Playtime

## Per-10 Statistics

For a statistic \(x\):

```text
Per10(x) = x / total_playtime_seconds × 600
```

Per-10 normalizes counting statistics to ten minutes of observed playtime.

It does **not** adjust for hero, map, opponent, composition, pace, or team strategy.

## Minimum Playtime

A player is percentile/ranking eligible when:

```text
total_playtime_minutes >= 30
```

The threshold is intended to reduce extreme low-playtime comparisons. It does not make small samples statistically equivalent or remove sampling uncertainty.

## Percentiles

Percentiles are calculated among eligible players within the same `detailed_position`.

They should be interpreted as:

> Where does this observed statistic fall relative to other eligible players in the same detailed position during this Stage 2 dataset?

They should **not** be interpreted as:

> How good is this player overall?

## Confounding and Interpretation

Overwatch scoreboard statistics are highly context dependent.

Examples include:

- Hero selection
- Team composition
- Map and mode
- Opponent quality/style
- Team strategy and tempo
- Role responsibilities
- Fight length and game state

The current dataset does not contain sufficient hero-level or event-level context to adjust for these factors. Therefore, player rankings, Per-10 values, plots, and percentiles are **descriptive and context-unadjusted**.

A high damage, healing, or elimination rate is not by itself evidence of greater player impact.

## Hero Bans

Hero-ban records are stored at the banning-team level and can be explored by team and match/map context.

Observed relationships between bans and results should be treated as descriptive associations. The current dataset is not designed to establish that a particular ban caused a match outcome.

## Best / Worst Map Records

Team map summaries use a minimum of **3 map appearances** before a map is eligible for best/worst-map labeling.

When records are tied, more map appearances are preferred; remaining ties can be resolved deterministically for display.

## POTM

Player of the Match records are stored separately and joined by player identity where needed. POTM is an award record, not a modeled performance metric.

## What This Methodology Does Not Claim

This project does not currently provide:

- Hero-adjusted player ratings
- Causal estimates
- Event-level player impact
- Teamfight-level value
- Ultimate-efficiency models
- Context-adjusted impact ratings

Those would require substantially more granular data and/or stronger modeling assumptions.
