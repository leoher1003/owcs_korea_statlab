# Data Dictionary
This document describes the eight public CSV files for **2026 OWCS Korea Stage 2**.

## General Conventions

- `player_id` is the primary player identity / aggregation key.
- `team_id` is the canonical team identifier.
- `match_id` is the map-level join key used by match, player-map, and hero-ban data.
- `map_position` is observed at the map/result-screen level and is intentionally separate from canonical roster position.
- Per-10 ranking eligibility is represented explicitly in `eligible_30min`.

## `teams.csv`

**Rows:** 9

| Field | Description |
|---|---|
| `team_id` | Canonical team identifier used for joins. |
| `team_name` | Display name of the team. |

## `players.csv`

**Rows:** 60

| Field | Description |
|---|---|
| `player_id` | Canonical player identifier and aggregation key. |
| `team_id` | Canonical team identifier. |
| `roster_position` | Player's canonical primary roster position. |
| `detailed_position` | Analytical position used for within-position comparisons. |

## `matches.csv`

**Rows:** 188

| Field | Description |
|---|---|
| `week` | Competition week. |
| `day` | Competition day within the week/phase source. |
| `match` | Match label/number from the source dataset. |
| `set_number` | Map/set number within the match. |
| `date` | Match date. |
| `phase` | Tournament phase. |
| `team_1` | Canonical identifier for team 1. |
| `team_2` | Canonical identifier for team 2. |
| `map` | Map name. |
| `map_type` | Game mode / map type. |
| `map_duration` | Observed map duration. |
| `winner` | Canonical identifier of the map winner. |
| `match_id` | Unique map-level identifier used for joins. |
| `team_1_score` | Team 1 map/match score field from match metadata. |
| `team_2_score` | Team 2 map/match score field from match metadata. |

## `player_map_stats.csv`

**Rows:** 1,880

| Field | Description |
|---|---|
| `match_id` | Map-level identifier joining to matches.csv. |
| `week` | Competition week. |
| `team_id` | Canonical team identifier. |
| `player_id` | Canonical player identifier. |
| `map_position` | Position shown for the player on this specific result screen. |
| `map` | Map name. |
| `map_type` | Game mode / map type. |
| `eliminations` | Map-level eliminations. |
| `deaths` | Map-level deaths. |
| `assists` | Map-level assists. |
| `damage` | Map-level damage. |
| `healing` | Map-level healing. |
| `mitigated` | Map-level mitigated damage. |
| `playtime` | Human-readable map playtime. |
| `playtime_seconds` | Map playtime converted to seconds. |

## `player_total_stats.csv`

**Rows:** 60

| Field | Description |
|---|---|
| `team_id` | Canonical team identifier. |
| `player_id` | Canonical player identifier. |
| `roster_position` | Canonical primary roster position. |
| `detailed_position` | Analytical detailed position. |
| `total_eliminations` | Accumulated eliminations. |
| `total_deaths` | Accumulated deaths. |
| `total_assists` | Accumulated assists. |
| `total_damage` | Accumulated damage. |
| `total_healing` | Accumulated healing. |
| `total_mitigated` | Accumulated mitigated damage. |
| `elim_death_ratio` | Accumulated elimination/death ratio. |
| `playtime_seconds` | Accumulated playtime in seconds. |
| `playtime_minutes` | Accumulated playtime in minutes. |

## `player_per10_stats.csv`

**Rows:** 60

| Field | Description |
|---|---|
| `team_id` | Canonical team identifier. |
| `player_id` | Canonical player identifier. |
| `roster_position` | Canonical primary roster position. |
| `detailed_position` | Analytical detailed position. |
| `playtime_minutes` | Accumulated playtime in minutes. |
| `eliminations_per10` | Eliminations per 10 minutes. |
| `deaths_per10` | Deaths per 10 minutes. |
| `assists_per10` | Assists per 10 minutes. |
| `damage_per10` | Damage per 10 minutes. |
| `healing_per10` | Healing per 10 minutes. |
| `mitigated_per10` | Mitigated damage per 10 minutes. |
| `eligible_30min` | Whether the player meets the 30-minute comparison threshold. |

## `hero_bans.csv`

**Rows:** 376

| Field | Description |
|---|---|
| `match_id` | Map-level identifier joining to matches.csv. |
| `banning_team_id` | Canonical identifier of the team making the ban. |
| `banned_hero` | Hero banned by that team. |

## `potm.csv`

**Rows:** 51

| Field | Description |
|---|---|
| `date` | Award date. |
| `match` | Match label/number associated with the award. |
| `player_id` | Canonical player identifier receiving POTM. |
| `position` | Position associated with the POTM record. |

