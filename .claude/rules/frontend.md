---
paths:
  - "site/**"
---

# Frontend Rules

## 1. Deployment

- `site/` is deployed to GitHub Pages on every push to `main`. Treat any `site/` change as publishing.
- The site is static (no build step). Verify locally with `python3 -m http.server 8000 --directory site`.

## 2. Data Contract

- The site reads `site/data/*.js` (e.g. `window.OWCS_DATA`, `window.OWCS_STAGE3_PREVIEW`) and `*.json`. It does not read `data/*.csv`.
- `site/data/data.js` uses the Excel master's column names (`"Player Name"`, `"Shortened"`, `"Detailed"`, …). Those keys are the contract. Do not rename them without updating every consumer in `app.js`.
- Site data files are manual exports from the Excel master (see `pipeline.md`). Do not hand-edit statistics in them.
- Do not change a published stage's site data unless explicitly asked.

## 3. Display Rules

- Rankings, percentiles, and scatterplots use only `eligible_30min` players. Below-threshold players still appear where totals are shown.
- Percentiles compare players within the same detailed position. Players with a blank detailed position must not be silently placed in a group.
- Show missing values as missing, never as 0.
- Do not present unverified or preview values as final statistics.
- Keep existing design conventions in `styles.css` and the bilingual (EN/KO) labels.
