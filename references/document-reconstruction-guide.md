# Document Reconstruction Guide

## Purpose

PDF and Office extraction often creates broken lines, repeated headers/footers, damaged tables, and lost section context. Reconstruct the document before extracting requirements.

## Reuse Installed PDF or Document Processing Skills First

Before running custom scripts or attempting manual PDF parsing, check whether the agent environment already has a dedicated PDF-processing, Office-document-processing, OCR, or document-layout skill installed.

If such a skill is available, use it first for:

- PDF text extraction
- Word document extraction
- OCR for scanned pages
- Table extraction
- Page reference preservation
- Heading and layout reconstruction
- Figure or caption extraction

This skill should not duplicate specialized PDF parsing when a better installed skill is available. The result from the installed skill should be converted into reconstructed Markdown or text and then passed into this skill's global analysis workflow.

Fallback order:

1. Installed PDF/document-processing skill
2. Docling, marker, GROBID, or equivalent external tools
3. Lightweight reconstruction script on extracted Markdown/text
4. Manual reconstruction with explicit extraction warnings

## Directory Processing

When the input is a directory, process all relevant extracted text or Markdown files under the directory.

Create a Source Document Registry and a Combined Document Analysis Model that indexes sections and potential requirement regions across all documents.

Preserve relative paths because they often indicate module ownership, such as diagnostics, communication, platform, application, or safety.

## Line Repair Rules

Merge adjacent lines only when safe. Do not merge headings, list items, table rows, or requirement ID lines. When unsure, preserve the line break and add an extraction warning.

## Table Handling

Do not force damaged table content into requirements. Preserve table-like blocks, mark them as structured data regions, and ask for clarification if values are needed for SRS/SWRS.
