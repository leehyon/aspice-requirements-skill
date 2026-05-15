# Requirement Extraction Guide

Extract CRS Working Set items after document reconstruction and global briefing.

## CRS Working Set Fields

- CRS ID
- Customer Requirement
- Domain
- Source Reference
- Status
- Issue

## Multi-Document Extraction

When multiple customer requirement documents are provided:

1. Extract CRS across the entire document set.
2. Preserve source references with document IDs, for example `SRC-0003 / Section 4.2`.
3. Consolidate duplicates across documents when they express the same customer intent.
4. Keep module-specific requirements only when the scope or target module is clearly different.
5. Flag conflicts between documents as open issues.
6. Do not let one module document override another unless priority or applicability is stated.
7. If document precedence, version priority, or module ownership is unclear, create an open issue.

## Non-Requirement Content

Do not promote background explanations, marketing text, revision history, glossary definitions, legal/commercial terms, or implementation suggestions to CRS unless explicitly stated as requirements or confirmed by the user.
