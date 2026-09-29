# Reproducibility

## Public Components

The repository provides:

- processed Stage 2 CSV datasets
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

## Reproducibility Boundary

The repository makes the processing workflow and final structured outputs inspectable.

Exact end-to-end reproduction of visual extraction also requires access to the same source result screens. Those raw broadcast images are not included here.

Accordingly, this repository provides transparency into the workflow and processed dataset, but it is not a complete archival redistribution of the source broadcast material.

## Data Outputs

The public data layer consists of eight CSV files under `data/`.

Their schemas and meanings are documented in [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md).

Validation results for the published dataset are documented in [`VALIDATION.md`](VALIDATION.md).
