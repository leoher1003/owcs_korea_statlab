---
paths:
  - "pipeline/**"
  - "data/**"
  - "output/**"
  - "result_screen_*/**"
  - "*.xlsx"
---

# Pipeline Rules

## 1. Data Flow

```
result_screen_s<N>/*.png
  → pipeline/result_screen_pipeline.ipynb   (Gemini extraction + deterministic validation)
  → output/validated_results.xlsx, output/player_statistics.xlsx, output/*.csv
  → OWCS_STAT_LAB_26_KR_STAGE<N>.xlsx        (metadata master, maintained manually)
  → data/stage<N>/*.csv, site/data/*.js      (manual export)
```

- The notebook reads the canonical roster from the master's `TEAM INFO` sheet.
- Master sheets: `TEAM INFO`, `MATCH INFO`, `TEAMFIGHT INFO`, `MATCH_W1..W6`, `TOTAL STATISTICS`, `Per10 STATISTICS`, `POTM`.
- `TEAMFIGHT INFO` is manually recorded and not yet public. Follow `teamfight.md`, and export it only with explicit approval.

## 2. Stage Separation

- Each stage has its own directories: `data/stage<N>/`, `result_screen_s<N>/`.
- New Stage 3 outputs go to `data/stage3/`. Never write Stage 3 data to `data/` root or `data/stage2/`.
- Stage 2 CSVs currently sit at `data/*.csv`. Moving them to `data/stage2/` changes public file URLs and README/docs links, so do it only as a separate, explicitly approved change.
- Public CSV schemas must stay identical across stages unless a schema change is approved and documented in `docs/DATA_DICTIONARY.md`.

## 3. Manual Export Steps

Because CSV/JS exports are manual:

- After any export, reconcile the export against the master: row counts, key uniqueness, and a sample of values.
- If the CSV/JS and the master disagree, report it. Do not decide which one is correct.
- Write CSVs as UTF-8 with BOM (`utf-8-sig`), matching existing files.

## 4. Notebook Editing

- Use NotebookEdit for `.ipynb` changes. Do not rewrite the notebook JSON by hand.
- Before a notebook is committed, clear cell outputs; they can contain raw extracted rows, local paths, or secrets.
- Never print, log, or hard-code `GEMINI_API_KEY`.
- Do not run cells that call the Gemini API without explicit approval (it costs money and uploads images).

## 5. Identity and Aliases

- `PLAYER_ALIASES` and `TEAM_ALIASES` in the notebook remap extracted names to canonical IDs. Never add or change an alias without the evidence (the source screen and the conflicting name) and the user's approval. A wrong alias silently merges two players' statistics.
- A missing or unreadable roster file must stop the run. It must never be downgraded to a warning, because unknown-player checks depend on it.
- A player in the stats but not in the roster must be reported, never dropped by an inner join.

## 6. Known Issues (as of 2026-10-09)

- `ROSTER_XLSX` points to `etc/excel/...`, but the master sits at the repo root.
- `load_roster` only warns when the roster file is missing.
- Player totals use `identity.merge(stats, how="inner")`, which can drop unmatched players without a report.
- The notebook rounds Per-10 values to 2 decimals, but the published Stage 2 CSV stores full precision.

Raise these when touching related code. Do not fix them silently.
