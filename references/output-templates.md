# Output Templates

## Recommended Output Filenames

Use the rules in `file-naming-convention.md`.

Default final output filenames:

```text
<portfolio-id>_srs_full-system_<date>.md
<portfolio-id>_swrs_full-system_<date>.md
<portfolio-id>_traceability-matrix_full-system_<date>.md
<portfolio-id>_open-issues_full-system_<date>.md
```

Default intermediate or analysis filenames:

```text
<portfolio-id>_source-document-registry_document-set_<date>.md
<portfolio-id>_combined-document-analysis-model_document-set_<date>.md
<portfolio-id>_combined-document-analysis-model_document-set_<date>.json
<portfolio-id>_global-requirement-brief_document-set_<date>.md
<portfolio-id>_crs-working-set_full-system_<date>.md
```

## Source Document Registry

| Document ID | File | Relative Path | Title | Quality | Domains | Potential Requirement Regions |
|---|---|---|---|---|---|---:|

## CRS Working Set

| CRS ID | Customer Requirement | Domain | Source Reference | Status | Issue |
|---|---|---|---|---|---|

## SRS Requirement Table

| SRS ID | System Requirement | Domain | Parent CRS ID | Derived | Rationale | Verification Method | Status | Issue |
|---|---|---|---|---|---|---|---|---|

## SWRS Requirement Table

| SWRS ID | Software Requirement | Domain | Parent SRS ID | Software Boundary | Derived | Rationale | Verification Method | Status | Issue |
|---|---|---|---|---|---|---|---|---|---|

## Main Traceability Matrix

| Trace ID | CRS ID | SRS ID | SWRS ID | Trace Status | Notes |
|---|---|---|---|---|---|

## Open Issues

| Open Issue ID | Related ID | Issue Type | Description | Question | Status |
|---|---|---|---|---|---|

## Extraction Tool / Skill Note

When documenting source processing, record whether extraction was performed by an installed PDF/document-processing skill, Docling, marker, GROBID, another external tool, or manual reconstruction.
