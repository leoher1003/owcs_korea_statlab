# Reproducibility

## Public Components

The repository provides:

- processed Stage 2 CSV datasets
- the Stage 3 site dataset (`site/data/data_s3.js`)
- the stage export and teamfight scripts (`pipeline/export_site_data.py`, `pipeline/tf_db.py`, `pipeline/build_comp_sheet.py`, `pipeline/sql/`)
- the static Stat Lab
- the public extraction / validation notebook
- methodology, validation, and data documentation

Raw broadcast result-screen images are not redistributed in the repository.

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

## Stage Export and Teamfight Scripts

These scripts read a stage workbook that has been saved by Excel (formula results cached). The workbook is not in the repository.

```bash
pip install -r pipeline/requirements.txt   # openpyxl, duckdb
python3 pipeline/export_site_data.py OWCS_STAT_LAB_26_KR_STAGE3.xlsx site/data/data_s3.js OWCS_DATA_S3
python3 pipeline/tf_db.py OWCS_STAT_LAB_26_KR_STAGE3.xlsx                             # teamfight checks
python3 pipeline/tf_db.py OWCS_STAT_LAB_26_KR_STAGE3.xlsx "SELECT * FROM comp_stats"   # ad-hoc query
python3 pipeline/tf_db.py OWCS_STAT_LAB_26_KR_STAGE3.xlsx --save teamfights.duckdb    # file for the duckdb CLI
python3 pipeline/build_comp_sheet.py OWCS_STAT_LAB_26_KR_STAGE3.xlsx                  # COMP STATS sheet
```

If any check fails, `export_site_data.py` still writes the output file but prints the problems and exits with status 1; treat that output as unusable until the problems are fixed. `build_comp_sheet.py` saves the workbook with openpyxl, which drops cached formula results, so open and save the workbook in Excel once before the next export.

## Reproducibility Boundary

The repository makes the processing workflow and final structured outputs inspectable.

Exact end-to-end reproduction of visual extraction also requires access to the same source result screens. Those raw broadcast images are not included here.

Accordingly, this repository provides transparency into the workflow and processed dataset, but it is not a complete archival redistribution of the source broadcast material.

## Data Outputs

The public Stage 2 data layer consists of eight CSV files under `data/`. Stage 3 is published in the site format as `site/data/data_s3.js`.

Their schemas and meanings are documented in [`data_dictionary.md`](data_dictionary.md).

Validation results for the published dataset are documented in [`VALIDATION.md`](VALIDATION.md).
