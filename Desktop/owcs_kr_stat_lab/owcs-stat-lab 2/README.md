# OWCS Korea 2026 Stage 2 Stat Lab — MVP

A dependency-free static web prototype generated from `OWCS_STAT_LAB_26_KR_STAGE2.xlsx`.

## Run
You can open `index.html` directly, or serve the folder locally:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

## Implemented
- Teams / Players: overall Stage 2 match & map record, roster, player profile
- Player Profile: position percentile (30 min minimum), accumulated/per-10 season stats, POTM records
- Player Rankings: accumulated and per-10, position filters, 30 min per-10 eligibility
- Plotting: position / X / Y / phase, phase-level aggregation, 30 min filter, mean reference lines
- Head-to-Head: per-10 actual values + same-position percentile
- Match Explorer: series score, map list, hero-ban counts by team/phase, map-type W-L and win rate

## Pending source data
- Team logos
- Player photos
- Career accomplishments beyond Stage 2 POTM

## Data snapshot
The current `data/data.js` is a static export of the uploaded workbook. When the workbook changes, regenerate this file or replace the data layer with an API/database later.
