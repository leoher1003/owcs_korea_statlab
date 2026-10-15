# Data Quality Rules

## 1. Purpose

Protect the accuracy, consistency, and reproducibility of OWCS STAT LAB data.

These rules apply to data extraction, validation, cleaning, aggregation, CSV generation, and downstream visualizations.

## 2. Source of Truth

- Treat validated datasets as the source of truth for downstream calculations.
- AI-extracted data is not ground truth and must pass deterministic validation.
- Inspect existing schemas and pipeline behavior before changing data-processing logic.
- Never invent missing values or silently modify source data to make validation pass.
- Preserve the distinction between raw, validated, aggregated, and published data.

## 3. Player and Team Identity

- Use the project's existing canonical player identifier as the primary player aggregation key.
- Do not use map-level Position as player identity; a player may compete in multiple roles.
- Preserve team, roster, and detailed-position associations according to existing project rules.
- Flag conflicting identity mappings instead of silently selecting one.
- Investigate unexpected player or team identifiers before accepting the dataset.

## 4. Input Validation

Before processing a dataset, check applicable requirements:

- Required columns exist and have the expected names.
- Numeric statistics can be converted to valid numeric values.
- Playtime values are present and parse correctly.
- Player and team identifiers are valid and consistently mapped.
- Missing values, malformed records, and duplicate records are explicitly handled.
- Joins do not unexpectedly multiply or remove records.
- Record counts remain consistent with the expected transformations.

Do not assume every dataset has the same schema. Inspect the actual input and existing validation code first.

## 5. Statistical Integrity

- Calculate player totals from the validated map-level dataset.
- Calculate per-10-minute statistics using total playtime in seconds:

  `per10 = total_stat / total_playtime_seconds * 600`

- Apply the existing 30-minute eligibility threshold to per-10-minute rankings and visualizations. The threshold is `playtime_seconds >= 1800`: inclusive, computed on unrounded seconds, never on rounded minutes.
- Zero or missing playtime produces a missing Per-10 value, never 0.
- Round only for display. Keep the precision of stored values consistent with the existing published files.
- Retain valid player statistics even when a player does not meet the ranking eligibility threshold, unless the project specification explicitly requires filtering them out.
- Keep accumulated statistics separate from rate statistics.
- Do not silently change formulas, rounding, grouping keys, or eligibility rules.
- Document the rationale and impact of any change to a statistical definition.

## 6. Aggregation and Reconciliation

When changing aggregation logic:

- Verify that the intended grouping key is used.
- Check that each source record contributes to the appropriate aggregate.
- Compare output record counts against expected counts.
- Reconcile accumulated statistics against the validated source data.
- Check total playtime and per-10-minute calculations for representative players.
- Investigate unexpected differences instead of automatically accepting them.

Do not assume that matching row counts alone prove the output is correct.

## 7. Error Handling

- Fail clearly when required fields are missing or invalid.
- Include the affected file, field, player, or record identifier in error messages when available.
- Do not suppress validation errors merely to complete a pipeline run.
- Distinguish warnings from errors.
- Document accepted exceptions and their reasons.
- Avoid silent coercion, silent row removal, and undocumented imputation.

## 8. Testing Requirements

For changes affecting data quality, identity, aggregation, or statistical formulas:

- Add or update regression tests where practical.
- Test missing values, malformed playtime, invalid numeric fields, duplicate records, and identity conflicts when relevant.
- Verify boundary cases for the 30-minute eligibility threshold.
- Check that zero or missing playtime cannot produce misleading rate statistics.
- Run the relevant tests and report their actual results.
- Never claim that a test passed if it was not executed.

## 9. Change Safety

- Inspect the existing implementation before modifying it.
- Prefer small, targeted changes over unnecessary rewrites.
- Preserve unrelated user changes.
- Do not overwrite source data or important generated files without understanding their role.
- Do not commit, push, publish, or deploy without explicit authorization.
- Never expose API keys, access tokens, or other secrets.

## 10. Required Data Quality Report

When reviewing or modifying a data-processing pipeline, report:

1. Files and processing steps inspected.
2. Validation checks performed.
3. Record counts and aggregate comparisons checked.
4. Errors, warnings, and unresolved assumptions.
5. Changes made, if any.
6. Tests executed and their actual outcomes.

Clearly distinguish verified results from checks that remain incomplete.