# Reproducibility

## What Is Public

The repository is intended to expose:

- processed Stage 2 CSV datasets
- the static Stat Lab
- the AI-assisted extraction / validation notebook
- methodology and validation documentation

Raw broadcast screenshots are not included.

## Environment

The website itself requires no build system. A local static server is sufficient:

```bash
python3 -m http.server 8000 --directory site
```

For the extraction notebook, install the Python dependencies imported by the notebook and provide the Gemini credential through:

```bash
export GEMINI_API_KEY="your_key_here"
```

API credentials must never be committed to the repository.

## Extraction Configuration

The public notebook should keep the following configuration visible in code:

- model identifier used for extraction
- extraction prompt / schema
- parsing rules
- canonical roster reference
- validation rules
- Per-10 calculation
- eligibility threshold

The exact model identifier should be pinned in the notebook rather than described only as "Gemini", because hosted model behavior can change over time.

## Reproduction Boundary

A third party can inspect and rerun the code, but exact end-to-end reproduction also requires access to the same source result screens.

Because raw broadcast screenshots are not redistributed here, the repository provides **workflow reproducibility and processed-data transparency**, not a complete archival copy of all source media.

## Recommended Run Record

For future dataset releases, record:

```text
Tournament / stage:
Extraction notebook commit:
Model identifier:
Extraction date:
Number of source screens:
PASS / WARNING / FAIL counts:
Manual audit sample size:
Observed audit discrepancy rate:
```

This makes later releases easier to compare and audit.
