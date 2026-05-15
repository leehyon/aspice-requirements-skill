# Scripts

Use installed PDF/document skills first. `reconstruct_document.py` only processes already extracted `.txt`, `.md`, or `.markdown` files.

```bash
# 1. Use installed PDF/document-processing skill or external tool to extract Markdown/text.
# 2. Then use this script only for reconstruction/global modeling:
python scripts/reconstruct_document.py ./extracted_customer_requirements --out reconstruct-output --document-id-prefix SRC --portfolio-id REQ-PORTFOLIO-0001 --extraction-tool installed-pdf-skill
```

This script does not generate CRS, SRS, or SWRS.
