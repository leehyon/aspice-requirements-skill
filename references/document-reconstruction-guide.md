# Document Reconstruction Guide

## Reuse Installed PDF or Document Processing Skills First

Before running custom scripts or attempting manual PDF parsing, check whether the agent environment already has a dedicated PDF-processing, Office-document-processing, OCR, or document-layout skill installed.

Fallback order:

1. Installed PDF/document-processing skill
2. Docling, marker, GROBID, or equivalent external tools
3. Lightweight reconstruction script on extracted Markdown/text
4. Manual reconstruction with explicit extraction warnings

## Directory Processing

When the input is a directory, process all relevant extracted text or Markdown files under the directory and create a Source Document Registry plus Combined Document Analysis Model.

## Line Repair Rules

Merge adjacent lines only when safe. Do not merge headings, list items, table rows, or requirement ID lines.
