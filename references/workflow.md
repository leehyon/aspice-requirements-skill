# Workflow

This workflow prioritizes global document understanding before requirement extraction and derivation.

## Stage 0: Check Existing Skills and Tools

Before reconstructing PDF or Office documents manually, check whether a dedicated PDF/document-processing skill is installed or available. If available, use that skill first to extract text, tables, headings, page references, OCR results, and layout information.

Only use this skill's lightweight reconstruction script after the source content has been extracted to Markdown or text, or when no suitable installed skill/tool exists.

## Stage 1: Document Reconstruction

Reconstruct all relevant documents into readable representations. For PDF/Word, first extract to Markdown or text using an installed skill, Docling, marker, GROBID, or equivalent tools.

## Stage 2: Source Document Registry and Combined Document Analysis Model

For one file, create a document model. For a directory, create:

- Source Document Registry
- Combined Document Analysis Model
- Domain index across documents
- Potential requirement regions across documents
- Extraction warnings

## Stage 3: Global Requirement Brief

Create one global brief before CRS extraction. For a document set, summarize the whole portfolio, not each file independently.

## Stage 4: CRS Working Set Extraction

Extract CRS items by domain or section group across all documents. Consolidate duplicates and flag conflicts.

## Stage 5: SRS Derivation

Derive system requirements from CRS Working Set items. Organize by domain and module where useful.

## Stage 6: SWRS Derivation

Derive software requirements from reviewed SRS items. Focus on externally observable software behavior.

## Stage 7: Traceability and Open Issues

Generate the main CRS-to-SRS-to-SWRS traceability matrix and open issues.

## Multi-Document Rule

Do not generate disconnected SRS/SWRS fragments for each source file unless explicitly requested. Prefer one coherent SRS and one coherent SWRS organized by domain and, when needed, by module.

## Output File Naming Rule

Before exporting final or intermediate artifacts, apply `references/file-naming-convention.md`.

Use stable, explicit filenames that include portfolio/source ID, artifact name, scope, and version or date.

Do not use vague filenames such as `output.md`, `requirements.md`, `srs.md`, or `final.md` when generating files for the user.
