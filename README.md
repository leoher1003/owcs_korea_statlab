# OWCS Korea Stat Lab

An unofficial interactive analytics project for **2026 Overwatch Champions Series (OWCS) Korea Stages 2–3**.

> I built an end-to-end analytics pipeline for OWCS Korea — from AI-assisted data collection and deterministic validation to statistical processing and an interactive Stat Lab — without access to an official public statistics API.

**Live Stat Lab:** https://leoher1003.github.io/owcs_korea_statlab/

## Overview

As a longtime Overwatch player and esports viewer, I wanted a deeper way to explore OWCS beyond match results alone.

This project is an attempt to build the kind of statistical experience I wished existed for Overwatch Esports: a place where fans can explore player performance, compare statistical profiles, examine team and map trends, and investigate match-level results interactively.

The current release covers **2026 OWCS Korea Stage 2** (complete) and **Stage 3** (in progress: Weeks 1–2 of player statistics, Week 1 of teamfights). A stage switch in the site header selects which stage every tab shows.

## Features

- **Overview** — standings, map pools, roster changes, and tournament context
- **Teams & Players** — team records, map performance, hero-ban tendencies, player profiles, POTM awards, and championship history
- **Player Rankings** — accumulated and Per-10 comparisons across core scoreboard statistics
- **Plotting** — interactive player scatterplots using selectable Per-10 metrics
- **Head-to-Head** — same-position player comparisons
- **Match Explorer** — match/map results and hero-ban exploration
- **Teamfights** (Stage 3) — team teamfight win rates, composition frequency / share / win rate, and composition-vs-composition records
- **Info** — methodology, scope, limitations, and disclaimer

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
Manual Review / QA
        ↓
Clean Structured Dataset
        ↓
Statistical Processing
        ↓
OWCS Korea Stat Lab
```

A structured public statistics API was not available for this project, so player statistics were collected from result screens shown during OWCS Korea broadcasts.

AI output is **not treated as ground truth**. Extracted records pass through deterministic validation and roster checks before being used downstream. The final dataset was also checked for structural and aggregation consistency, and a 20-map manual source-screen audit found no discrepancies in the audited fields.

From Stage 3 on, the reviewed stage workbook is exported to the site by [`pipeline/export_site_data.py`](pipeline/export_site_data.py), which re-checks it before writing anything: 10 player rows per map, every map in the match list, one pairing per series, and workbook totals equal to the sum of the exported player-map rows.

Stage 3 also adds **teamfight data**, recorded by hand from VODs (one row per teamfight: both compositions and the winner). It is loaded into DuckDB by [`pipeline/tf_db.py`](pipeline/tf_db.py), checked with the zero-row SQL checks in [`pipeline/sql/checks_teamfights.sql`](pipeline/sql/checks_teamfights.sql), and summarized by the views in [`pipeline/sql/teamfights.sql`](pipeline/sql/teamfights.sql).

See [`docs/methodology.md`](docs/methodology.md) and [`docs/VALIDATION.md`](docs/VALIDATION.md).

## Statistical Methodology

### Per-10

```text
Per10 = Statistic / Total Playtime (seconds) × 600
```

### Eligibility

Players must have at least **30 minutes of total playtime** to be included in rankings, percentile comparisons, and most player-level visualizations. Players below the threshold remain in the processed dataset.

### Percentiles

Percentiles compare eligible players within the same **detailed position**. They are descriptive comparisons within the observed sample of the selected stage, **not an overall player rating**.

### Interpretation

Scoreboard statistics should not be interpreted as direct measurements of overall player skill or impact.

Eliminations, deaths, assists, damage, healing, and mitigation are influenced by hero selection, team composition, map, opponent, team strategy, and role responsibilities. Because the current dataset does not contain hero-level usage or event-level context, Per-10 statistics and percentiles are **context-unadjusted descriptive statistics**.

Small eligible player pools can also make position-level percentiles coarse. The 30-minute threshold reduces extreme low-playtime cases but does not eliminate sampling variability.

### Teamfights (Stage 3)

A teamfight is a fight for control of the point, payload, or robot (4v5 and 3v5 fights included). The winner is the team that ends up in control; there are no draws. Compositions are recorded at the start of each fight, and two compositions are the same when they have the same five heroes.

- **Team teamfight win rate** = fights won / fights played, always shown with n.
- **Composition win rate** = W / (W + L). Mirror fights (both teams on the same composition) are excluded from W/L and counted separately.
- **Share** = fights in which the composition appeared / all fights (a mirror counts once).
- Compositions need at least **10 non-mirror teamfights** to be ranked; smaller samples are shown on demand, unranked.

Teamfights are judged by a single annotator. Win rates are descriptive and not context-adjusted. See [`docs/methodology.md`](docs/methodology.md#teamfights-stage-3).

## Dataset

### Stage 2 (public CSVs)

The public processed Stage 2 dataset contains:

- **188 maps**
- **1,880 player-map records**
- **60 players**
- **9 teams**
- **376 hero-ban records**
- **51 POTM records**

The eight public CSVs are stored in [`data/`](data/). See [`docs/data_dictionary.md`](docs/data_dictionary.md) for field-level definitions.

| File | Rows | Description |
|---|---:|---|
| `teams.csv` | 9 | Team information |
| `players.csv` | 60 | Player and roster information |
| `matches.csv` | 188 | Map-level match metadata and results |
| `player_map_stats.csv` | 1,880 | Player statistics for individual maps |
| `player_total_stats.csv` | 60 | Accumulated player statistics |
| `player_per10_stats.csv` | 60 | Per-10 player statistics and eligibility |
| `hero_bans.csv` | 376 | Hero-ban records |
| `potm.csv` | 51 | Player of the Match records |

### Stage 3 (in progress)

Stage 3 data is published in the site format only, as [`site/data/data_s3.js`](site/data/data_s3.js) (`window.OWCS_DATA_S3`), generated by `pipeline/export_site_data.py`. At the time of writing it covers:

- **63 maps** and **630 player-map records** (Weeks 1–2)
- **9 teams** and **62 player entries** (two players who switched position mid-stage are kept as one entry per position, e.g. `LIP (DPS)` / `LIP (SPT)`)
- **18 POTM records**
- **338 teamfights on 30 maps** (Week 1)

Its structure, and the DuckDB tables and views used for teamfights, are documented in [`docs/data_dictionary.md`](docs/data_dictionary.md#stage-3-site-dataset-sitedatadata_s3js).

## Validation Summary

Final Stage 2 dataset QA found:

- 188 map/result-screen blocks represented in match data
- 1,880 player-map rows
- 10 player rows per result screen
- no duplicate player within a result screen
- no exact duplicate raw player row
- no missing map block in the final match dataset
- no negative/non-numeric core statistic values in the final data
- total and Per-10 outputs consistent with recomputation from the clean source data

A separate manual audit compared **20 maps (200 player-map records)** against their original result screens. For each player-map record, nine fields were checked: player identity, map position, eliminations, deaths, assists, damage, healing, mitigation, and playtime.

**1,800 audited fields; 0 observed discrepancies (0/1,800).**

This is an audit result for the sampled records, not a claim that the complete dataset has a 0% error rate.

Full details: [`docs/VALIDATION.md`](docs/VALIDATION.md).

## Repository Structure

```text
owcs_korea_statlab/
├── data/                 # Public processed CSV datasets
├── docs/                 # Methodology, validation, and data documentation
├── pipeline/             # Extraction notebook, stage export, teamfight DuckDB/SQL
│   └── sql/              # Teamfight views and data checks
├── site/                 # Interactive Stat Lab
├── .github/workflows/    # GitHub Pages deployment
├── LICENSE
├── NOTICE.md
└── README.md
```

## Running Locally

The Stat Lab is a static site:

```bash
git clone https://github.com/leoher1003/owcs_korea_statlab.git
cd owcs_korea_statlab
python3 -m http.server 8000 --directory site
```

Then open `http://localhost:8000`.

The public extraction notebook is under `pipeline/`. It reads the Gemini API credential from the `GEMINI_API_KEY` environment variable rather than storing a key in the repository.

The stage export and teamfight scripts need a stage workbook (not included in the repository) that has been saved by Excel, so formula results are cached:

```bash
pip install -r pipeline/requirements.txt
python3 pipeline/export_site_data.py OWCS_STAT_LAB_26_KR_STAGE3.xlsx site/data/data_s3.js OWCS_DATA_S3
python3 pipeline/tf_db.py OWCS_STAT_LAB_26_KR_STAGE3.xlsx                 # run the teamfight checks
python3 pipeline/tf_db.py OWCS_STAT_LAB_26_KR_STAGE3.xlsx "SELECT * FROM team_tf_stats"
python3 pipeline/build_comp_sheet.py OWCS_STAT_LAB_26_KR_STAGE3.xlsx      # write the COMP STATS sheet
```

For the reproducibility boundary and pipeline notes, see [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md).

## Limitations

1. **Scoreboard context** — player statistics are affected by heroes, compositions, maps, opponents, team strategy, and role responsibilities.
2. **No hero-level attribution** — the current dataset cannot separate a player's statistics by hero usage.
3. **Limited event-level data** — Stage 3 teamfights and compositions at fight start are recorded by hand by a single annotator and currently cover Week 1 only. Ultimates, mid-fight hero swaps, and spatial positions are not available, and there is no telemetry.
4. **Residual extraction risk** — plausible transcription errors can pass structural checks even after deterministic validation.
5. **Small samples** — a single (or in-progress) tournament stage, position-level eligibility filters, and per-composition teamfight counts can produce small comparison groups.
6. **Unofficial source** — this project should not be treated as an official OWCS statistics source.

## Future Work

### With the current data

- Uncertainty-aware team comparisons
- Map-result-based team rating models
- Small-sample / shrinkage approaches for player comparisons
- Additional descriptive tournament analysis

### Extending the Stage 3 teamfight data

- Teamfight coverage for the remaining weeks
- Uncertainty intervals for teamfight and composition win rates

### If more granular data becomes available

- Hero swap and adaptation analysis
- Ultimate economy
- Spatial/teamfight location analysis
- Context-adjusted player and team impact modeling
- An **ASK STAT LAB** layer in which deterministic calculations produce the statistics and an LLM helps explain them conversationally

## License & Third-Party Content

Original source code and original project documentation are released under the **MIT License**. See [`LICENSE`](LICENSE).

The MIT License does **not** grant rights to third-party names, logos, trademarks, broadcast material, screenshots, or other third-party assets. See [`NOTICE.md`](NOTICE.md).

## Disclaimer

This project was independently created as a personal fan analytics project and is **not affiliated with, endorsed by, or sponsored by Blizzard Entertainment or Overwatch Esports**.

All Overwatch and Overwatch Champions Series (OWCS) names, logos, and related assets belong to their respective owners.
