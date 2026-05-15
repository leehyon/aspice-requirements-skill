# ASPICE Requirements Skill

`aspice-requirements` is an Agent Skill for analyzing automotive customer requirement documents and deriving structured requirements in an Automotive SPICE-oriented manner.

## What This Skill Does

This skill helps an AI agent process customer requirement documents in a staged way instead of directly generating software requirements from raw documents.

```text
Customer documents
  ↓
Document reconstruction
  ↓
Source Document Registry
  ↓
Combined Document Analysis Model
  ↓
Global Requirement Brief
  ↓
CRS Working Set
  ↓
SRS
  ↓
SWRS
  ↓
Traceability Matrix + Open Issues
```

Main outputs:

1. **SRS** — System Requirements Specification
2. **SWRS** — Software Requirements Specification
3. **Traceability Matrix** — CRS to SRS to SWRS traceability
4. **Open Issues List** — missing, ambiguous, conflicting, or unverifiable information

The CRS is normally treated as a lightweight **CRS Working Set** for AI reasoning and traceability. A formal CRS document can be generated if explicitly requested.

## Key Principles

- Do not directly generate SWRS from raw PDF, Word, or unstructured text.
- Reconstruct and understand the document first.
- Build a Global Requirement Brief before extracting or deriving requirements.
- Extract CRS items by domain or section group, not by isolated sentence fragments.
- Derive SRS from CRS.
- Derive SWRS from reviewed SRS.
- Do not copy SRS text directly into SWRS.
- Write SWRS from a software development perspective.
- Keep software requirements focused on externally observable software behavior.
- Preserve traceability.
- Create open issues instead of inventing missing information.

## Suggested Prompts

### 1. Analyze a Directory of Customer Requirement Documents

```text
Use the aspice-requirements skill.

Analyze all customer requirement documents under this directory:
<path-to-customer-requirements>

First, check whether a PDF/document-processing skill is available. If available, use it to extract PDF/Word content. Then reconstruct the document set, create a Source Document Registry, Combined Document Analysis Model, and Global Requirement Brief.

Do not generate SRS or SWRS yet. First show me the Global Requirement Brief and major open questions.
```

### 2. Extract CRS Working Set

```text
Use the aspice-requirements skill.

Based on the reconstructed documents and Global Requirement Brief, extract a CRS Working Set.

Group requirements by domain, such as Functional, Diagnostics, Communication, Safety, Security, Calibration/Configuration, Timing/Performance, Data, and Error Handling.

Do not include background, glossary, legal, commercial, or implementation suggestion content unless it is explicitly stated as a requirement.

For ambiguous or missing information, create open issues instead of guessing.
```

### 3. Derive SRS from CRS

```text
Use the aspice-requirements skill.

Derive a System Requirements Specification from the CRS Working Set.

Each SRS item shall:
- use clear shall language,
- describe one system-level need,
- trace to at least one CRS item,
- include domain, derived flag, rationale, verification method, status, and issue field,
- report missing or unclear information as open issues.

Organize the SRS by requirement domain.
```

### 4. Derive SWRS from SRS

```text
Use the aspice-requirements skill.

Derive a Software Requirements Specification from the reviewed SRS.

Do not directly copy SRS text into SWRS.

For each SRS item, determine whether it is software-relevant. If it is software-relevant, write SWRS items from a software development perspective, focusing on externally observable software behavior.

Each SWRS item shall include:
- SWRS ID,
- software requirement text,
- domain,
- parent SRS ID,
- software boundary,
- derived flag,
- rationale,
- verification method,
- status,
- issue field.

Use ISO/IEC/IEEE 29148-inspired principles: clear, necessary, singular, feasible, verifiable, traceable, consistent, and appropriate to the software requirement level.

If details are missing, create open issues instead of inventing behavior.
```

### 5. Generate Final Deliverables

```text
Use the aspice-requirements skill.

Generate the final deliverables:

1. SRS
2. SWRS
3. CRS-to-SRS-to-SWRS Traceability Matrix
4. Open Issues List

Use the file naming convention defined by the skill.

Default output language shall be English.
```

## Notes

This skill supports requirement analysis and drafting. It does not replace engineering review, customer clarification, safety analysis, cybersecurity analysis, or formal ASPICE assessment.
