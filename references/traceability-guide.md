# Traceability Guide

Maintain this conceptual chain:

Source Document → Reconstructed Document → Combined Document Analysis Model → Global Requirement Brief → CRS Working Set → SRS → SWRS

## Main Traceability Matrix

- Trace ID
- CRS ID
- SRS ID
- SWRS ID
- Trace Status
- Notes

Every accepted CRS shall have a source reference. Every SRS shall trace to at least one CRS. Every SWRS shall trace to at least one SRS.

## SRS-to-SWRS Traceability Quality

A valid SRS-to-SWRS trace is not only an ID link. The SWRS shall show a software-level refinement of the parent SRS. If an SWRS merely copies the SRS wording without identifying software behavior or software boundary, mark it for rewrite or review.
