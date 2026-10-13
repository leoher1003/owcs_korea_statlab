# Data Dictionary

This document describes the eight public CSV files for **2026 OWCS Korea Stage 2**, the Stage 3 site dataset (`site/data/data_s3.js`), including its teamfight records, and the DuckDB tables and views used for teamfight analysis.

## Conventions

- `player_id` is the primary player identity / aggregation key.
- `team_id` is the canonical team identifier.
- `match_id` is the map-level join key used by match, player-map, and hero-ban data.
- `map_position` records the observed position for that map and is intentionally separate from canonical roster position.
- `eligible_30min` records whether a player meets the 30-minute comparison threshold.
- Blank/unused statistical values should not be interpreted as zero unless the source field itself is zero.

## `teams.csv`

**Rows:** 9

| Field | Description |
|---|---|
| `team_id` | Canonical team identifier used for joins. |
| `team_name` | Team display name. |

## `players.csv`

**Rows:** 60

| Field | Description |
|---|---|
| `player_id` | Canonical player identifier and primary player aggregation key. |
| `team_id` | Canonical team identifier. |
| `roster_position` | Canonical primary roster position. |
| `detailed_position` | Analytical role used for position-level comparisons. |

## `matches.csv`

**Rows:** 188

| Field | Description |
|---|---|
| `week` | Competition week. |
| `day` | Competition day field. |
| `match` | Match label/number. |
| `set_number` | Map/set number within the match. |
| `date` | Match date. |
| `phase` | Tournament phase. |
| `team_1` | Canonical team identifier for team 1. |
| `team_2` | Canonical team identifier for team 2. |
| `map` | Map name. |
| `map_type` | Game mode / map type. |
| `map_duration` | Recorded map duration. |
| `winner` | Canonical team identifier of the map winner. |
| `match_id` | Unique map-level identifier used for joins. |
| `team_1_score` | Recorded score field for team 1. |
| `team_2_score` | Recorded score field for team 2. |

## `player_map_stats.csv`

**Rows:** 1,880

| Field | Description |
|---|---|
| `match_id` | Map-level identifier joining to matches.csv. |
| `week` | Competition week. |
| `team_id` | Canonical team identifier. |
| `player_id` | Canonical player identifier. |
| `map_position` | Position recorded for this player on this result screen. |
| `map` | Map name. |
| `map_type` | Game mode / map type. |
| `eliminations` | Map-level eliminations. |
| `deaths` | Map-level deaths. |
| `assists` | Map-level assists. |
| `damage` | Map-level damage. |
| `healing` | Map-level healing. |
| `mitigated` | Map-level mitigation. |
| `playtime` | Recorded human-readable playtime. |
| `playtime_seconds` | Playtime converted to seconds. |

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
| `total_mitigated` | Accumulated mitigation. |
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
| `mitigated_per10` | Mitigation per 10 minutes. |
| `eligible_30min` | Whether total playtime meets the 30-minute comparison threshold. |

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
| `position` | Position recorded with the POTM entry. |

## Stage 3 Site Dataset (`site/data/data_s3.js`)

Stage 3 is published in the site format only. `pipeline/export_site_data.py` writes it as a single JavaScript assignment, `window.OWCS_DATA_S3 = {...}`, with the same shape as the Stage 2 site dataset (`window.OWCS_DATA` in `site/data/data.js`) plus two teamfight keys. Field names are the original workbook column names, not the snake_case CSV names.

Players who switched position mid-stage appear as one entry per position, named `PLAYER (POS)` (e.g. `LIP (DPS)`, `LIP (SPT)`), in every key that holds a player name.

| Key | Rows (at time of writing) | Description |
|---|---:|---|
| `teamInfo` | 71 | One header row per team (`Team Name`, `Shortened`), then one row per player entry (`Player Name`, `Player Position`, `Detailed`). |
| `matchInfo` | 63 | One row per map: `WEEK`, `DAY`, `MATCH`, `Set #`, `DATE`, `PHASE`, `TEAM 1`, `TEAM 2`, `MAP`, `MAP TYPE`, `TIME` (longest player playtime on the map), `WINNER`, `TEAM 1 BAN`, `TEAM 2 BAN`, `MATCH_ID`, `TEAM 1 SCORE`, `TEAM 2 SCORE`, `DETAIL_SCORE` (Push scores carry an `m` suffix). |
| `rawStats` | 630 | One row per player-map: `Team`, `Player`, `Position` (map position), `Map`, `Map Type`, `Elim`, `Death`, `Assists`, `Damage`, `Heal`, `Mitigated`, `Playtime`, `Playtime(Seconds)`, `MATCH_ID`. |
| `totalStats` | 62 | Accumulated stats per player entry: `TEAM`, `PLAYER`, `POSITION` (detailed position), `TOTAL ELIMS`, `TOTAL DEATHS`, `TOTAL ASSISTS`, `TOTAL DAMAGE`, `TOTAL HEAL`, `TOTAL MITIGATED`, `TOTAL E/D`, `TOTAL PLAYTIME` (seconds). |
| `per10Stats` | 62 | Per-10 stats per player entry: `Team`, `Player`, `Position` (detailed position), `Playtime_Min`, `Elim / 10`, `Death / 10`, `Assists / 10`, `Damage / 10`, `Heal / 10`, `Mitigated / 10`. |
| `potm` | 18 | `Date`, `Match`, `POTM` (player), `Position`. |
| `teamfights` | 338 | One row per teamfight (see below). |
| `heroRoles` | 33 | Hero name → role: `T` (tank), `D` (DPS), `S` (support). From `HERO_ROLES` in `pipeline/export_site_data.py`. Empty when there are no teamfights. |

### `teamfights`

| Field | Description |
|---|---|
| `MATCH_ID` | Map identifier joining to `matchInfo`. |
| `Order` | Order of the fight within the map, starting at 1. |
| `TEAM 1` | Team 1 of the map (from `matchInfo`). |
| `TEAM 2` | Team 2 of the map (from `matchInfo`). |
| `TEAM 1 COMP` | Team 1's five heroes at the start of the fight (list, recorded order). |
| `TEAM 2 COMP` | Team 2's five heroes at the start of the fight (list, recorded order). |
| `WINNER` | Team that won the fight; always `TEAM 1` or `TEAM 2`. |

Hero names are normalized to title case, with aliases fixed (e.g. `Rammatra` → `Ramattra`, `Lúcio` → `Lucio`).

## Teamfight DuckDB Tables and Views

`pipeline/tf_db.py` loads a stage workbook into DuckDB (in memory, or a file with `--save`) and runs `pipeline/sql/teamfights.sql`. These are not published as files; they back the checks and the workbook `COMP STATS` sheet.

### Base tables

| Table | Fields | Description |
|---|---|---|
| `match_info` | `match_id`, `week`, `day`, `match_no`, `set_no`, `team1`, `team2`, `map`, `map_type`, `map_winner` | One row per map. |
| `teamfights` | `tf_id`, `match_id`, `ord`, `team1`, `team2`, `winner` | One row per teamfight. |
| `tf_hero` | `tf_id`, `side`, `hero` | Five rows per side; `side` is 1 or 2. |
| `hero_roles` | `hero`, `role`, `role_rank` | `role` T/D/S; `role_rank` 1/2/3 orders comps Tank, DPS, Support. |

### Views

| View | Grain | Fields |
|---|---|---|
| `tf_side` | teamfight × side | `tf_id`, `match_id`, `ord`, `side`, `team`, `opp_team`, `comp_key` (heroes ordered by role then name, joined by ` / `), `roles` (e.g. `TDDSS`), `won` |
| `tf_matchup` | teamfight × side | `tf_side` fields plus `opp_comp` and `is_mirror` |
| `comp_stats` | composition | `comp_key`, `tank`, `dps1`, `dps2`, `support1`, `support2`, `freq`, `mirror`, `w`, `l`, `win_rate` (mirrors excluded; null with no non-mirror fights), `fight_share`, `favorite_team`, `all_teams` |
| `team_tf_stats` | team | `team`, `w`, `l`, `n`, `win_rate`, `maps`, `fights_per_map` |

Definitions of frequency, mirror, win rate, and share are in [`methodology.md`](methodology.md#statistics).
