# Limitations

The OWCS Korea Stat Lab is an independent analytics project built from publicly available competitive information. The following limitations should be considered when interpreting the statistics and visualizations presented in the project.

## Data Extraction Accuracy

Player statistics are collected from broadcast result screens using an AI-assisted visual extraction pipeline.

Extracted records are passed through deterministic validation checks designed to identify issues such as unexpected player counts, duplicate or unknown player IDs, invalid numeric values, playtime inconsistencies, and roster mismatches. Records can also be traced back to their original source screens for additional review.

However, AI-assisted visual extraction is not perfectly accurate. A transcription error may still pass automated validation if the extracted value is structurally valid and statistically plausible.

For this reason, the dataset should not be treated as an official source of OWCS statistics.

## Data Availability and Granularity

The scope of the project is limited by the competitive data that is publicly accessible through OWCS broadcasts.

The current dataset primarily contains scoreboard-level player statistics, match and map results, playtime, hero bans, and Player of the Match information.

While these data can describe many aspects of player and team performance, they do not capture the full context of what occurs during a match.

More granular event-level data would enable analysis of areas such as:

- hero and team composition usage
- composition matchups and effectiveness
- teamfight frequency, duration, and outcomes
- hero swaps and adaptation
- ultimate charge and usage patterns
- spatial patterns and frequently contested locations

As a result, the current Stat Lab primarily provides descriptive analysis of publicly observable competitive data rather than a complete model of player or team impact.

## Statistical Interpretation

Statistics should be interpreted within the context of playtime, role, team environment, opponents, maps, and other competitive factors.

Per-10-minute statistics normalize performance by playtime but do not control for differences in these contextual factors.

To reduce the influence of extremely small samples, players must record at least **30 minutes of total playtime** to be included in Per-10 rankings and related visualizations.

Percentile rankings compare eligible players within the same detailed role. They describe a player's statistical position within the dataset and should not be interpreted as an overall player rating or definitive measure of player quality.

## Player Role Classification

Players are assigned detailed role classifications to support position-based comparisons within the Stat Lab.

However, competitive roles are not always fixed. Some players may have flexible hero pools or compete in multiple roles during the competition.

Player identity is therefore maintained independently from map-level role information where necessary. Role classifications should be interpreted as analytical groupings used for statistical comparison rather than strict definitions of a player's capabilities.

## Project Scope

The current version of the Stat Lab focuses specifically on **2026 OWCS Korea Stage 2**.

Results, percentiles, rankings, and trends presented in the project describe this competition and should not automatically be generalized to other OWCS stages, regions, patches, or competitive environments.