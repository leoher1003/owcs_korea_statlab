# Methodology

## Scope

This release covers **2026 OWCS Korea Stage 2** (complete) and **Stage 3** (in progress; Weeks 1–2 scoreboard data). The primary analytical unit for raw player statistics is a **player-map appearance**.

The project uses scoreboard-level statistics and tournament metadata available from public competition broadcasts. It does not contain official event-level game telemetry. Stage 3 adds two VOD-based layers, kept separate from the scoreboard statistics: manually recorded **teamfights** and VOD-estimated **hero playtime** (see below).

Each stage is processed and shown separately. Statistics are never pooled across stages, because balance patches change what a statistic is worth. Hero roles are resolved by match date: Sombra is a DPS hero before the October 2026 patch (live from 2026-10-06, before Stage 3 Week 2) and a Support hero from then on.

## Player Identity and Roles

`player_id` is the primary player aggregation key.

The project distinguishes:

- **Map Position** — the position recorded for the player on a specific result screen
- **Roster Position** — the player's canonical primary roster position
- **Detailed Position** — the analytical role used for position-level comparisons

Canonical roster information is used to validate player identity. Map-level position is preserved separately so that an observed role on an individual map is not overwritten by the player's primary roster role.

A player who played more than one position in a stage is shown as one roster entry, with a selector for each position's statistics; position-level statistics are not merged.

## Map Names

Result screens show map names in their on-screen spelling (for example `ROUTE 66`, `ESPERANÇA`). Before any comparison, names are folded to one canonical spelling by ignoring case, accents and punctuation (`pipeline/names.py`). An unknown name is reported, never guessed.

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

> Where does this observed statistic fall relative to other eligible players in the same detailed position in the same stage?

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

Teamfights are recorded **manually** by one annotator watching the broadcast VODs, following the author's definition in [`TEAMFIGHT_DEFINITION.md`](TEAMFIGHT_DEFINITION.md). In summary:

- A teamfight is a fight for control of the objective (point, payload or robot). It need not be 5v5, and it may happen in two or three places at once. Side fights are not recorded separately; their result shows up in the main fight.
- The first fight after the map starts counts. Later fights start when one team re-engages a team that holds position. A re-engage that collapses on the way from spawn is not a fight.
- A fight continues through regrouping near the objective, players rejoining, or the objective briefly changing hands. Regrouping near spawn, out of contact, starts a new fight.
- A fight ends when one team keeps or regains control of the objective, and that team wins. An irreversible result during the fight (round end, checkpoint, capture complete) goes to the team that gained it. A fight from a neutral state goes to the team that takes control first. There are no draws.
- The composition recorded is each team's five heroes at the start of the fight.

**Coverage.** Only maps whose log is complete are aggregated. All 30 Stage 3 Week 1 maps (338 teamfights) are complete, as confirmed by the annotator on 2026-10-14; Week 2 is not yet logged. A map without a log is missing, not "0 fights". Coverage is always shown as maps and fights.

**Statistics.** Teamfight statistics are team-level and composition-level only. The log does not record which player played which hero, so fights are never attributed to individual players.

- Team teamfight win rate = fights won / fights recorded, always shown with n. There is no minimum sample.
- Compositions are grouped by the unordered set of five heroes per side.
- Composition win rates are ranked only for compositions that appear in **10 or more teamfights, mirror fights included**. In a mirror fight (both teams on the same composition), the fight counts once toward that threshold but is excluded from the composition's win/loss across all teams and shown separately as a mirror; a single team's record includes its mirror fights.
- Teamfight metrics are kept separate from scoreboard and Per-10 statistics and are never combined into one rating.

## Hero Playtime (Stage 3, VOD estimate)

The scoreboard does not split a player's playtime by hero. For Stage 3 Week 1, per-hero playtime is **estimated** from the broadcast VODs:

1. The broadcast is decoded at 2 frames per second and the ten HUD hero portraits are cropped from every frame.
2. Portraits are grouped by visual similarity, the groups are labelled by hand, and every frame is classified against those labels.
3. Each HUD side is matched to its team for that map, and each slot to a player by reading the on-screen name plates against the canonical roster and that map's scoreboard.

Playtime rules (set by the author, 2026-10-14):

- Only time inside a map counts. Setup phases (doors closed) and time between rounds are excluded.
- A hero change counts only when the new hero is held for at least 3 seconds; shorter runs are treated as misreads.
- Gaps of 30 seconds or less in which the portrait cannot be read are filled with the hero shown just before the gap. Longer gaps are not counted.
- Dead time counts toward the current hero.

This is an estimate, not an official per-hero statistic. It is checked against the official per-map playtime (see [`VALIDATION.md`](VALIDATION.md)) and is kept separate from scoreboard, Per-10 and teamfight statistics.

## Current Analytical Boundary

The current release does not provide:

- Hero-adjusted player ratings
- Causal player or team effects
- Player-level teamfight attribution or teamfight-level value
- Ultimate-efficiency models
- Context-adjusted player-impact ratings

Those analyses would require more granular data and/or additional modeling assumptions.
