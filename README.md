# OWCS Korea Stat Lab

An unofficial interactive analytics project for **2026 Overwatch Champions Series (OWCS) Korea Stage 2**.

> I built an end-to-end analytics pipeline for OWCS Korea — from AI-assisted data collection and deterministic validation to statistical processing and an interactive Stat Lab — without access to an official public statistics API.

**Live Stat Lab:** https://leoher1003.github.io/owcs_korea_statlab/

## Why I Built This

As a longtime Overwatch player and esports viewer, I wanted a deeper way to explore OWCS beyond match results alone.

This project is an attempt to build the kind of statistical experience I wished existed for Overwatch Esports: a place where fans can explore player performance, compare statistical profiles, examine team and map trends, and investigate match-level results interactively.

The current public release focuses on **2026 OWCS Korea Stage 2**.

## Features

The Stat Lab currently includes:

- **Overview** — standings, map pools, roster changes, and competition context
- **Teams & Players** — team records, map performance, hero-ban tendencies, player profiles, POTM awards, and championship history
- **Player Rankings** — accumulated and Per-10 comparisons across core scoreboard statistics
- **Plotting** — interactive player scatterplots using selectable Per-10 metrics
- **Head-to-Head** — same-position player comparisons
- **Match Explorer** — match/map results and hero-ban exploration
- **Info** — methodology, scope, limitations, and project disclaimer

## Data Pipeline

```text
Broadcast Result Screens
        ↓
AI-Assisted Extraction
        ↓
Parsing & Normalization
        ↓
Deterministic Validation
        ↓
Canonical Roster Validation
        ↓
Manual Review
        ↓
Clean Structured Dataset
        ↓
Statistical Processing
        ↓
OWCS Korea Stat Lab
```

A structured public statistics API was not available for this project, so player statistics were collected from result screens shown during OWCS Korea broadcasts.

AI output is **not treated as ground truth**. Extracted records pass through deterministic checks such as expected row count, duplicate-player detection, canonical player-ID validation, numeric/playtime checks, team and map consistency, and source-file traceability. Records that fail validation are excluded from downstream processing.

Player identity and canonical roster metadata are validated against reference roster data, while **map-level position is preserved from the result screen**.

For more detail, see [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) and [`docs/VALIDATION.md`](docs/VALIDATION.md).

## Statistical Methodology

### Per-10

Per-10 statistics normalize accumulated statistics to 10 minutes of playtime:

```text
Per10 = Statistic / Total Playtime (seconds) × 600
```

### Eligibility

Players must have at least **30 minutes of total playtime** to be included in rankings, percentile comparisons, and most player-level visualizations. Players below the threshold remain in the underlying processed dataset.

### Percentiles

Percentiles compare eligible players within the same **detailed position**. They are descriptive comparisons within the observed Stage 2 sample, **not an overall player rating**.

### Interpretation

Scoreboard statistics should not be interpreted as direct measurements of overall player skill or impact.

Eliminations, deaths, assists, damage, healing, and mitigation are influenced by hero selection, team composition, map, opponent, team strategy, and role responsibilities. Because the current dataset does not contain hero-level usage or event-level context, Per-10 statistics and percentiles are **context-unadjusted descriptive statistics**.

Small eligible player pools also make some position-level percentiles coarse. The 30-minute threshold reduces extreme low-playtime cases but does not eliminate sampling variability.

## Dataset

The public processed dataset contains:

- **188 maps**
- **1,880 player-map records**
- **60 players**
- **9 teams**
- **376 hero-ban records**
- **51 POTM records**

Public CSVs are stored in [`data/`](data/):

| File | Rows | Description |
|---|---:|---|
| `teams.csv` | 9 | Team identifiers and names |
| `players.csv` | 60 | Player, team, roster position, and detailed position |
| `matches.csv` | 188 | Map-level match metadata and results |
| `player_map_stats.csv` | 1,880 | Player statistics for each map appearance |
| `player_total_stats.csv` | 60 | Accumulated player statistics |
| `player_per10_stats.csv` | 60 | Per-10 player statistics and eligibility flag |
| `hero_bans.csv` | 376 | Hero bans by team |
| `potm.csv` | 51 | Player of the Match records |

See [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md) for field-level definitions.

## Repository Structure

```text
owcs_korea_statlab/
├── data/                 # Public processed CSV datasets
├── docs/                 # Methodology, validation, and data documentation
├── pipeline/             # AI-assisted extraction / validation notebook
├── site/                 # Static interactive Stat Lab
├── .github/workflows/    # GitHub Pages deployment
├── LICENSE
├── NOTICE.md
└── README.md
```

## Running Locally

The Stat Lab is a static site.

```bash
git clone https://github.com/leoher1003/owcs_korea_statlab.git
cd owcs_korea_statlab
python3 -m http.server 8000 --directory site
```

Then open `http://localhost:8000`.

### Extraction Pipeline

The public extraction notebook is under `pipeline/`.

The pipeline expects the Gemini API credential through the environment variable:

```bash
export GEMINI_API_KEY="your_key_here"
```

The extraction prompt, schema, parsing logic, validation rules, and model configuration are kept with the notebook so the workflow can be inspected alongside the code. Raw broadcast screenshots are not included in the public repository.

## Validation & Audit Status

The dataset has undergone deterministic QA across the complete Stage 2 dataset, including row-count, duplicate, identity, numeric, playtime, map, and aggregation consistency checks.

A deterministic validator cannot detect every plausible transcription error. For example, a visually misread number can remain syntactically valid. For that reason, a **random source-screen audit** is documented as an additional validation step in [`docs/VALIDATION.md`](docs/VALIDATION.md).

No random-audit error rate is claimed until that audit has been completed and recorded.

## Example Questions

The current Stat Lab is designed for exploratory questions such as:

- How do statistical profiles differ among players in the same detailed position?
- Which teams show stronger or weaker records on particular maps?
- How do hero-ban patterns vary by team, opponent, map type, or map?
- Which players combine unusual Per-10 profiles within their position?

These are exploratory comparisons; the current data does not support causal claims about why a player or team performed a certain way.

## Limitations

1. **Scoreboard context:** player statistics are affected by heroes, compositions, maps, opponents, and team strategy.
2. **No hero-level attribution:** the current dataset cannot separate a player's statistics by hero usage.
3. **No event-level telemetry:** teamfights, ultimates, hero swaps, composition states, and spatial positions are not available.
4. **Extraction risk:** plausible transcription errors may pass structural validation.
5. **Small samples:** one tournament stage and position-level eligibility filters can produce small comparison groups.
6. **Unofficial source:** this project should not be treated as an official OWCS statistics source.

## Future Work

### With the current data

- Random source-screen auditing and published audit results
- Uncertainty-aware team comparisons
- Map-result-based team rating models
- Small-sample / shrinkage approaches for player comparisons
- Additional descriptive tournament insights

### If more granular data becomes available

- Teamfight identification and outcomes
- Team composition usage and effectiveness
- Hero swap and adaptation analysis
- Ultimate economy
- Spatial/teamfight location analysis
- Context-adjusted player and team impact modeling
- An **ASK STAT LAB** layer where deterministic calculations produce the statistics and an LLM explains them conversationally

## License & Third-Party Content

Source code and original project documentation are released under the **MIT License**. See [`LICENSE`](LICENSE).

The MIT License does **not** grant rights to third-party names, logos, trademarks, broadcast material, screenshots, or other assets. Dataset and asset usage is further described in [`NOTICE.md`](NOTICE.md).

## Disclaimer

This project was independently created as a personal fan analytics project and is **not affiliated with, endorsed by, or sponsored by Blizzard Entertainment or Overwatch Esports**.

All Overwatch and Overwatch Champions Series (OWCS) names, logos, and related assets belong to their respective owners.
