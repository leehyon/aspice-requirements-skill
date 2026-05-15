# File Naming Convention

Use consistent, readable, automation-friendly filenames for all generated artifacts.

## General Rules

Use this general pattern:

```text
<project-or-portfolio-id>_<artifact-name>_<scope>_<version-or-date>.<extension>
```

If no project ID is provided, use the portfolio ID or source document ID. If no version is provided, use the generation date in `YYYYMMDD` format.

Use `_` to separate major filename fields. Use `-` inside a field. Do not use spaces.

## Recommended Artifact Names

- `source-document-registry`
- `combined-document-analysis-model`
- `global-requirement-brief`
- `crs-working-set`
- `srs`
- `swrs`
- `traceability-matrix`
- `open-issues`
- `coverage-summary`
- `extraction-warnings`
- `reconstructed-document`
- `document-analysis-model`

## Scope Token

Recommended scope values:

- `full-system`
- `diagnostics`
- `communication`
- `safety`
- `security`
- `platform`
- `application`
- `calibration-configuration`
- `timing-performance`
- `document-set`
- `src-0001`

## Final Output Filenames

```text
<portfolio-id>_srs_full-system_<date>.md
<portfolio-id>_swrs_full-system_<date>.md
<portfolio-id>_traceability-matrix_full-system_<date>.md
<portfolio-id>_open-issues_full-system_<date>.md
```

If a formal CRS document is requested:

```text
<portfolio-id>_crs_full-system_<date>.md
```

If using the CRS Working Set as an intermediate artifact:

```text
<portfolio-id>_crs-working-set_full-system_<date>.md
```

## Reconstruction and Analysis Filenames

```text
<portfolio-id>_source-document-registry_document-set_<date>.md
<portfolio-id>_combined-document-analysis-model_document-set_<date>.md
<portfolio-id>_combined-document-analysis-model_document-set_<date>.json
<portfolio-id>_global-requirement-brief_document-set_<date>.md
<portfolio-id>_extraction-warnings_document-set_<date>.md
<src-id>_reconstructed-document_<source-stem>_<date>.md
<src-id>_document-analysis-model_<source-stem>_<date>.md
<src-id>_document-analysis-model_<source-stem>_<date>.json
```

Do not use vague filenames such as `output.md`, `requirements.md`, `srs.md`, or `final.md`.
