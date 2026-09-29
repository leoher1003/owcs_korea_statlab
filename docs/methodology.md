# Methodology

## Overview

The OWCS Korea Stat Lab uses an AI-assisted data pipeline to transform publicly available broadcast result screens into structured player and match statistics.

The pipeline is designed around the following process:

**Broadcast Result Screens → AI-Assisted Extraction → Automated Validation → Review → Structured Dataset → Statistical Processing → Stat Lab**

AI is used as an extraction tool rather than as a source of truth. Extracted data must pass deterministic validation checks before it is included in the processed dataset.

## Data Source

Player statistics are collected from in-game result screens shown during OWCS Korea broadcasts.

These result screens provide player-level statistics for individual maps, including:

- Eliminations
- Deaths
- Assists
- Damage
- Healing
- Mitigation

Additional match information such as teams, maps, map types, match results, map duration, and hero bans is also recorded where available.

The current version of the project focuses on the 2026 OWCS Korea Stage 2 competition.

## AI-Assisted Data Extraction

Result screen screenshots are processed individually using an AI-assisted visual extraction pipeline.

The extraction model converts information visible in each screenshot into structured player-level records.

AI-generated output is treated as an intermediate extraction result and is not assumed to be perfectly accurate.

Each record also retains its source information so that statistics can be traced back to the corresponding result screen when necessary.

## Automated Validation

Extracted data is passed through deterministic validation checks before being accepted into the processed dataset.

Validation checks include:

- expected player count
- duplicate player IDs
- unknown player IDs
- canonical roster matching
- numeric field validation
- playtime validation
- categorical field validation
- consistency checks within each result screen

Player identity is validated against a canonical roster. Team and position information are assigned using this reference data rather than relying solely on AI-generated labels.

Records that fail required validation checks are excluded from the clean dataset. Records containing potential inconsistencies can be flagged for additional review.

## Statistical Processing

Validated map-level records are used to generate accumulated and rate-based player statistics.

### Accumulated Statistics

Player statistics are aggregated across maps using Player ID as the primary identifier.

This produces season-level totals for statistics such as eliminations, deaths, assists, damage, healing, and mitigation.

### Per-10-Minute Statistics

Per-10-minute statistics normalize player performance by total playtime.

The calculation is:

**Per10 = (Accumulated Stat / Total Playtime in Seconds) × 600**

Accumulated statistics and Per-10 statistics are generated from the same validated underlying dataset to maintain consistency between the two views.

Players must record at least **30 minutes of total playtime** to be included in Per-10-minute rankings.

## Player Roles

Players are categorized into detailed competitive roles:

- Tank
- Main DPS
- Flex DPS
- Main Support
- Flex Support

While there are flexible players who can play multiple roles, these role classifications are used for position-based comparisons and percentile calculations within the Stat Lab.

## Percentile Rankings

Player percentile values are calculated relative to other eligible players within the same role.

This allows players to be compared against others performing similar competitive roles rather than against the entire player population.

Percentiles are descriptive measures of a player's statistical position within the dataset and should not be interpreted as a complete measure of player impact.

## Data Traceability

Source information is retained during the extraction process so that individual records can be traced back to the original broadcast result screen.

This provides a way to investigate questionable values and review potential extraction errors.

## Scope

The current methodology is designed specifically for the 2026 OWCS Korea Stage 2 dataset.

The underlying pipeline is designed to support future expansion to additional competitions, stages, and regions while maintaining a consistent data structure and validation process.