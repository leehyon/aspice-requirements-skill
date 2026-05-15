# Workflow

## Stage 0: Check Existing Skills and Tools

Before reconstructing PDF or Office documents manually, check whether a dedicated PDF/document-processing skill is installed or available. If available, use that skill first.

## Stage 1: Document Reconstruction

Reconstruct all relevant documents into readable representations. For PDF/Word, first extract to Markdown or text using an installed skill, Docling, marker, GROBID, or equivalent tools.

## Stage 2: Source Document Registry and Combined Document Analysis Model

For a directory, create a Source Document Registry, Combined Document Analysis Model, domain index, potential requirement regions, and extraction warnings.

## Stage 3: Global Requirement Brief

Create one global brief before CRS extraction. For a document set, summarize the whole portfolio.

## Stage 4: CRS Working Set Extraction

Extract CRS items by domain or section group across all documents. Consolidate duplicates and flag conflicts.

## Stage 5: SRS Derivation

Derive system requirements from CRS Working Set items.

## Stage 6: SWRS Derivation

Derive software requirements from reviewed SRS items. Do not copy SRS text directly. Transform SRS into software-relevant, externally observable behavior.

## Stage 7: Traceability and Open Issues

Generate the main CRS-to-SRS-to-SWRS traceability matrix and open issues.

## Output File Naming Rule

Apply `references/file-naming-convention.md`. Do not use vague filenames such as `output.md`, `requirements.md`, `srs.md`, or `final.md`.
