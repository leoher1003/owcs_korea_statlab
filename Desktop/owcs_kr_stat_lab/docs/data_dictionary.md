# Data Dictionary

This document describes the datasets and primary variables used in the **2026 OWCS Korea Stage 2 Stat Lab**.

The dataset is organized around team and player reference information, match-level information, map-level player statistics, and derived season statistics.

---

## Dataset Structure

The Stage 2 dataset contains the following components:

| Dataset | Description |
|---|---|
| `TEAM INFO` | Team rosters and player role classifications. |
| `MATCH INFO` | Match- and map-level information, including results and hero bans. |
| `MATCH_W1` – `MATCH_W6` | Map-level player statistics organized by competition week. |
| `TOTAL STATISTICS` | Accumulated player statistics across Stage 2. |
| `Per10 STATISTICS` | Player statistics normalized by playtime. |
| `POTM` | Player of the Match records. |

---

## TEAM INFO

`TEAM INFO` serves as the primary roster reference used throughout the dataset.

| Field | Description |
|---|---|
| Team Name | Full team name. |
| Shortened | Abbreviated team identifier used throughout the dataset. |
| Player Name | Player's competitive display name. |
| Player Position | General competitive role: Tank, DPS, or Support. |
| Detailed | Detailed role classification used for role-based comparisons. |

### Detailed Roles

The Stat Lab uses the following role classifications:

- Tank
- Main DPS
- Flex DPS
- Main Support
- Flex Support

These classifications are used for position-based comparisons and percentile calculations.

Some players may compete across multiple roles or have flexible hero pools. The detailed role classification should therefore be interpreted as an analytical grouping used by the Stat Lab rather than a complete description of a player's capabilities.

---

## MATCH INFO

`MATCH INFO` contains the match- and map-level structure of the competition.

| Field | Description |
|---|---|
| WEEK | Competition week. |
| DAY | Competition day within the week. |
| MATCH | Match number within the competition day. |
| Set # | Map/set number within the match. |
| DATE | Date on which the match was played. |
| PHASE | Competition phase. |
| TEAM 1 | First team in the match record. |
| TEAM 2 | Second team in the match record. |
| MAP | Map played during the set. |
| MAP TYPE | Game mode associated with the map. |
| TIME | Recorded duration of the map, where available. |
| WINNER | Winner of the individual map. |
| TEAM 1 BAN | Hero banned by Team 1. |
| TEAM 2 BAN | Hero banned by Team 2. |
| MATCH_ID | Identifier used to associate map-level records across the dataset. |
| TEAM 1 SCORE | Recorded map score or objective result for Team 1. |
| TEAM 2 SCORE | Recorded map score or objective result for Team 2. |

### MATCH_ID

`MATCH_ID` provides a consistent identifier for linking map-level information with player statistics.

A single match series may therefore contain multiple `MATCH_ID` values corresponding to its individual maps/sets.

---

## MATCH_W1 – MATCH_W6

These datasets contain the underlying player-level statistics recorded for individual maps.

Each row represents the performance of one player on one map.

| Field | Description |
|---|---|
| Team | Team represented by the player. |
| Player | Player's competitive display name. |
| Position | Role played by the player in the corresponding record. |
| Map | Map on which the statistics were recorded. |
| Map Type | Game mode associated with the map. |
| Elim | Eliminations recorded by the player. |
| Death | Deaths recorded by the player. |
| Assists | Assists recorded by the player. |
| Damage | Damage recorded by the player. |
| Heal | Healing recorded by the player. |
| Mitigated | Damage mitigation recorded by the player. |
| Playtime | Player playtime recorded for the map. |
| Playtime (Seconds) | Player playtime represented in seconds for statistical processing. |
| MATCH_ID | Identifier linking the player record to the corresponding map in `MATCH INFO`. |

The Stage 2 dataset contains **10 player records per map**, representing five players from each participating team.

### Player Position

`Position` represents the role associated with the player for that particular record.

A player's map-level position may differ from their primary roster classification when the player competes in a different role.

This allows player identity to remain consistent while preserving the role actually associated with an individual appearance.

---

## TOTAL STATISTICS

`TOTAL STATISTICS` contains accumulated player statistics calculated from the underlying map-level records.

| Field | Description |
|---|---|
| TEAM | Player's team. |
| PLAYER | Player's competitive display name. |
| POSITION | Player role used in the accumulated statistics dataset. |
| TOTAL ELIMS | Total eliminations across included maps. |
| TOTAL DEATHS | Total deaths across included maps. |
| TOTAL ASSISTS | Total assists across included maps. |
| TOTAL DAMAGE | Total damage across included maps. |
| TOTAL HEAL | Total healing across included maps. |
| TOTAL MITIGATED | Total damage mitigation across included maps. |
| TOTAL E/D | Elimination-to-death ratio. |
| TOTAL PLAYTIME | Total recorded playtime in seconds. |

Player statistics are aggregated using player identity across the Stage 2 dataset.

### Elimination-to-Death Ratio

The elimination-to-death ratio is calculated as:

**E/D = Total Eliminations / Total Deaths**

This statistic describes the relationship between a player's recorded eliminations and deaths and should not be interpreted independently as an overall measure of player impact.

---

## Per10 STATISTICS

`Per10 STATISTICS` contains player statistics normalized by total playtime.

| Field | Description |
|---|---|
| Team | Player's team. |
| Player | Player's competitive display name. |
| Position | Player role used for statistical comparison. |
| Playtime_Min | Total recorded playtime expressed in minutes. |
| Elim / 10 | Eliminations per 10 minutes. |
| Death / 10 | Deaths per 10 minutes. |
| Assists / 10 | Assists per 10 minutes. |
| Damage / 10 | Damage per 10 minutes. |
| Heal / 10 | Healing per 10 minutes. |
| Mitigated / 10 | Damage mitigation per 10 minutes. |

Per-10-minute statistics are calculated using:

**Per10 = (Accumulated Stat / Total Playtime in Seconds) × 600**

The workbook may contain Per-10 values for players with limited playtime. However, players must record at least **30 minutes of total playtime** to be included in Per-10 rankings and related visualizations in the Stat Lab.

This eligibility threshold is intended to reduce the influence of extremely small playtime samples when comparing players.

---

## POTM

`POTM` contains Player of the Match records.

| Field | Description |
|---|---|
| Date | Date of the match. |
| Match | Teams participating in the match. |
| POTM | Player selected as Player of the Match. |
| Position | General role of the selected player. |

POTM records are used as an additional descriptive component of player profiles and accomplishments.

---

## Derived Statistics

Several statistics displayed in the Stat Lab are derived from the underlying Stage 2 dataset rather than directly recorded from broadcast result screens.

These include:

- accumulated player statistics
- Per-10-minute statistics
- elimination-to-death ratio
- role-based percentile rankings
- player and team summary statistics
- match and hero-ban summaries

---

## Percentile Rankings

Percentiles compare eligible players with other players in the same detailed role.

A higher percentile indicates that a player's recorded value for a particular statistic is higher than that of a larger proportion of eligible players within the comparison group.

Percentiles are descriptive measures of statistical position within the dataset. They should not be interpreted as an overall player rating or as a complete measure of player impact.

---

## Multi-Role Players

Player identity is maintained independently from individual map-level role information.

If a player competes in a different role during a particular map, the map-level record can retain that role without creating a separate player identity.

This distinction allows the dataset to preserve both:

- a consistent player identity across the competition
- the role associated with individual appearances

Role-based analyses should therefore account for the context in which a player's statistics were recorded.

---

## Data Scope

This data dictionary applies to the **2026 OWCS Korea Stage 2** dataset.

The current dataset primarily supports analysis of:

- player scoreboard statistics
- team and match results
- map-level results
- player playtime
- Player of the Match records
- hero bans

More granular gameplay information such as teamfight events, hero swaps, ultimate usage, compositions, and spatial events is outside the scope of the current dataset.