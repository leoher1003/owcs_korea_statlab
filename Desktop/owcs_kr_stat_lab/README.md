# 2026 OWCS Korea Stage 2 Stat Lab

An unofficial fan analytics project exploring team and player performance during the 2026 Overwatch Champions Series (OWCS) Korea Stage 2. The project provides an interactive way to explore individual player performance, team results, and match-level trends throughout the competition.

## Overview

As a longtime Overwatch player and esports viewer, I wanted a deeper way to explore OWCS beyond simply watching the matches. This project is an attempt to build an interactive statistical experience for the competition, allowing fans to explore player performance, compare individual players, visualize statistical relationships, and examine match-level trends.

## Features

- **Teams & Players**: Explore the teams and players who participated in 2026 OWCS Korea Stage 2, including season records, player statistics, and past accomplishments.
- **Player Rankings**: View accumulated and Per-10 player statistics for Eliminations, Deaths, Assists, Damage, Healing, and Mitigation.
- **Plotting**: Visualize relationships between two user-selected Per-10 metrics using interactive scatterplots.
- **Head-to-Head**: Compare two players within the same position using raw statistics and position-based percentile rankings.
- **Match Explorer**: Explore match results, map statistics, and hero ban tendencies throughout the competition.

## Data Pipeline

Broadcast Result Screens → AI-Assisted Extraction → Automated Validation → Manual Review → Structured Dataset → Statistical Processing → Stat Lab

## Data Collection & Validation

Because a structured public statistics API was not available for this project, player statistics were collected from in-game result screens shown during OWCS Korea broadcasts.

To make this process more time-efficient, I built an AI-assisted extraction pipeline that converts screenshots of result screens into structured data. AI-generated output is not assumed to be perfectly accurate and is not treated as ground truth.

Each extraction is passed through automated validation checks designed to identify potential errors, including unexpected row counts, duplicate or unknown player IDs, invalid numeric fields, playtime formatting issues, and inconsistencies within a result screen. Player identity, team, and position information are also cross-referenced against a canonical roster.

Records containing potential inconsistencies are flagged for review. In addition to these automated checks, manual review is used to compare questionable records against the original broadcast result screens before they are included in the processed dataset.

The goal of this pipeline is not to assume perfect AI extraction, but to make data collection practical and time-efficient while identifying and reducing potential extraction errors.

## Limitations

### Data Extraction Accuracy

Although the extraction pipeline includes automated validation and manual review, AI-assisted visual extraction is not perfectly accurate. Some transcription errors may remain in the dataset despite the validation process. For this reason, this project should not be treated as an official source of OWCS statistics.

### Data Availability

The scope of this project is limited by the data that is publicly available through OWCS broadcasts. Without access to a structured public statistics API or more granular match data, the current version primarily focuses on scoreboard-level player statistics, match results, map information, and hero bans.

More granular data would enable deeper analysis of areas such as team compositions, teamfights, hero swaps, ultimate economy, and spatial patterns within matches.

## Future Work

### Player & Team Impact Modeling

Inspired by the player and team power rankings developed during the Overwatch League era in collaboration with IBM Watson, a future extension of this project could explore statistical or machine-learning models for evaluating player and team impact.

Rather than relying solely on individual scoreboard statistics, such a model could incorporate additional contextual information to examine how players and teams contribute to competitive performance.

### Composition & Hero-Level Analysis

The current dataset primarily supports analysis at the player, team, and match level. With access to more granular data, future versions could examine performance in the context of specific heroes and team compositions.

This could enable analysis of composition usage and effectiveness, hero-specific player performance, composition matchups, map-specific tendencies, and how teams adapt their compositions throughout a match.

## Disclaimer

This is an independent, unofficial fan project created for educational and analytical purposes. It is not affiliated with, endorsed by, or sponsored by Blizzard Entertainment or Overwatch Esports.

Overwatch, Overwatch Champions Series (OWCS), and related names and assets are the property of their respective owners.