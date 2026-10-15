# Reproducibility

## Public Components

The repository provides:

- processed Stage 2 CSV datasets and the Stage 3 data published so far
- the static Stat Lab
- the public extraction / validation notebook
- the site export, teamfight checks, Liquipedia fetcher and VOD hero-playtime scripts
- methodology, validation, and data documentation

Raw broadcast result-screen images, the broadcast VODs and their scans, and the Excel master workbook are not redistributed in the repository.

## Website

The Stat Lab is a static website and can be served locally from the repository root with:

```bash
python3 -m http.server 8000 --directory site
```

Then open:

```text
http://localhost:8000
```

## Extraction Pipeline

The public extraction notebook is located under `pipeline/`.

API credentials are supplied through the environment rather than stored in source:

```bash
export GEMINI_API_KEY="your_key_here"
```

The notebook is the authoritative public reference for the extraction prompt, model call, parsing logic, normalization, and validation code used in the published workflow.

Because hosted AI model availability and behavior can change, the exact model identifier and configuration should be read from the notebook/version being run rather than inferred from this document.

## Site Data Export and Teamfight Checks

The site data files are exported from the Excel master (not in the repository):

```bash
pip install -r pipeline/requirements.txt
python3 pipeline/tf_db.py OWCS_STAT_LAB_26_KR_STAGE3.xlsx     # teamfight checks; prints any problem rows
```

`pipeline/sql/checks_teamfights.sql` holds the teamfight checks (each query must return zero rows) and `pipeline/sql/teamfights.sql` the team and composition statistics. `pipeline/export_site_data.py` runs the same checks during export.

## Match Results from Liquipedia

`pipeline/fetch_liquipedia.py` reads the Stage 3 Korea tournament page through the Liquipedia API (identifying User-Agent, at most one request every 2 seconds, cached responses) and writes match-info, series and POTM CSVs under `tmp/liquipedia/`. With `--compare site/data/data_s3.js` it diffs the fetched results against the site data and exits 1 on any difference. `pipeline/liquipedia_schedule.sh start` schedules a daily fetch on macOS during match days.

## VOD Hero Playtime

The scripts in `pipeline/vod/` turn the broadcast VODs into per-hero playtime. They need the VODs (streamed with `yt-dlp`), `ffmpeg`, and a Python environment with NumPy, OpenCV and PyTorch.

```bash
export PYTHONPATH=pipeline/vod
X=OWCS_STAT_LAB_26_KR_STAGE3.xlsx; R=tmp/vod; S="$R/261002_scan.npz $R/261003_scan.npz $R/261004_scan.npz"

python pipeline/vod/scan_vod.py <vod or stream> $R/261002_scan.npz            # once per broadcast day
python pipeline/vod/classify_heroes.py <labelled cluster folders, comma-separated> $S
python pipeline/vod/validate_vs_teamfight.py $X $S
python pipeline/vod/setup_grab.py $X $R/setup/banner.npz 261002=<stream url file> ...   # banner crops around map/round starts
python pipeline/vod/setup_phases.py $R/setup/banner.npz pipeline/vod/setup_templates.npz $R/setup/exclude_frames.npz
python pipeline/vod/hero_playtime.py $X $R/s3w1_hero_playtime_nosetup.csv $S --exclude $R/setup/exclude_frames.npz
python pipeline/vod/player_playtime.py $X $R/plates/plate_readings.csv $R/s3w1_hero_playtime_nosetup.csv $R/s3w1_player_hero_playtime_nosetup.csv
python pipeline/vod/export_hero_playtime.py $X $R/s3w1_player_hero_playtime_nosetup.csv data/stage3/vod_hero_playtime.csv site/data/hero_playtime_s3.js
```

The portrait labels are made by hand: `cluster_portraits.py` groups the crops and draws contact sheets, the sheets are named in each folder's `labels.csv`, and `split_clusters.py`, `unknown_sheet.py`, `targeted_sheet.py` and `slot_gap_sheet.py` produce follow-up sheets for mixed or unread portraits. These labels, the scans and the name-plate readings stay outside the repository, so this step cannot be reproduced from the repository alone.

## Tests

```bash
python3 -m pytest pipeline/test_names.py
PYTHONPATH=pipeline/vod python3 -m pytest pipeline/vod/test_hero_playtime.py
```

## Reproducibility Boundary

The repository makes the processing workflow and final structured outputs inspectable.

Exact end-to-end reproduction of visual extraction also requires access to the same source result screens. Those raw broadcast images are not included here.

Accordingly, this repository provides transparency into the workflow and processed dataset, but it is not a complete archival redistribution of the source broadcast material.

## Data Outputs

The Stage 2 public data layer consists of eight CSV files under `data/`. Stage 3 outputs go to `data/stage3/`.

Their schemas and meanings are documented in [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md).

Validation results for the published dataset are documented in [`VALIDATION.md`](VALIDATION.md).
