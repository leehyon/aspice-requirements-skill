# Scripts

## Important: Prefer Installed PDF/Document Skills

Do not use `reconstruct_document.py` as a replacement for a proper PDF/Office extraction skill. If the agent environment has an installed PDF-processing or document-processing skill, use that skill first.

Recommended flow for PDF/Word:

```bash
# 1. Use installed PDF/document-processing skill or external tool to extract Markdown/text.
# 2. Then use this script only for reconstruction/global modeling:
python scripts/reconstruct_document.py ./extracted_customer_requirements   --out reconstruct-output   --document-id-prefix SRC   --portfolio-id REQ-PORTFOLIO-0001   --extraction-tool installed-pdf-skill
```

## `reconstruct_document.py`

Reconstructs one `.txt`, `.md`, or `.markdown` file, or all supported files under a directory.

Single file:

```bash
python scripts/reconstruct_document.py extracted.md --out reconstruct-output --document-id SRC-0001 --extraction-tool docling
```

Directory:

```bash
python scripts/reconstruct_document.py ./customer_requirements --out reconstruct-output --document-id-prefix SRC --portfolio-id REQ-PORTFOLIO-0001 --extraction-tool docling
```

This script does not generate CRS, SRS, or SWRS.
