# Software Requirements Specification Template

Use this template when generating a printable Software Requirements Specification, SWRS.

## Document Structure

```markdown
# Software Requirements Specification

Document ID: <portfolio-id>_swrs_full-system_<version-or-date>
Project / Product: <project-or-product-name>
Parent SRS: <srs-document-id>
Version: <version>
Date: <date>
Status: Draft / Review / Released

## 1. Purpose

Describe the purpose of this SWRS and how it is derived from the reviewed SRS.

## 2. Scope

Describe the software scope covered by this SWRS.

Include software components, software boundaries, and what is out of scope if known.

## 3. Software Context and Boundary

Describe the software boundary and relevant external interfaces, such as:

- Application software
- Basic software
- Middleware
- Diagnostic software
- Communication stack
- Safety software
- Cybersecurity software
- Platform software
- Calibration/configuration interface
- Software-hardware interface

## 4. Source Inputs

List parent SRS document, Global Requirement Brief, CRS Working Set, source document set, and assumptions.

## 5. Requirement Overview

Summarize software requirement domains:

- Functional Software Requirements
- Diagnostic Software Requirements
- Communication Software Requirements
- Interface Software Requirements
- Safety Software Requirements
- Security Software Requirements
- Calibration and Configuration Software Requirements
- Timing and Performance Software Requirements
- Data and Error Handling Software Requirements
- Resource or Constraint Software Requirements

## 6. Software Requirements

### 6.1 Functional Software Requirements

#### SWRS-0001 — <Short Requirement Title>

**Requirement:**  
The software shall <externally observable software behavior>.

**Domain:** Functional  
**Parent SRS ID:** SRS-xxxx  
**Software Boundary:** Application Software / Platform Software / Unknown  
**Derived:** No / Yes / Partial  
**Rationale:** <how this software requirement refines or allocates the parent SRS>  
**Verification Method:** Review / Analysis / Inspection / Test / Demonstration / Unknown  
**Status:** Draft / Accepted / Needs Clarification / Rejected  
**Issue:** None / OI-xxxx  
**Notes:** <optional notes>

### 6.2 Diagnostic Software Requirements

#### SWRS-xxxx — <Short Requirement Title>

**Requirement:**  
The software shall <diagnostic software behavior visible at a diagnostic or communication interface>.

**Domain:** Diagnostic  
**Parent SRS ID:** SRS-xxxx  
**Software Boundary:** Diagnostic Software  
**Derived:** Yes / Partial  
**Rationale:** <rationale>  
**Verification Method:** <method>  
**Status:** <status>  
**Issue:** <issue>

### 6.3 Communication Software Requirements

### 6.4 Interface Software Requirements

### 6.5 Safety Software Requirements

### 6.6 Security Software Requirements

### 6.7 Calibration and Configuration Software Requirements

### 6.8 Timing and Performance Software Requirements

### 6.9 Data and Error Handling Software Requirements

### 6.10 Resource and Constraint Software Requirements

## 7. Open Issues

List unresolved SWRS-related open issues or reference the Open Issues List.

## 8. Traceability Summary

Summarize SRS-to-SWRS coverage and reference the traceability matrix.

## 9. Requirement Quality Summary

Summarize quality findings:

- Total SWRS items
- Derived / partially derived items
- Items needing clarification
- Items with unknown software boundary
- Items with unknown verification method
- Items requiring customer clarification

## 10. Revision History

| Version | Date | Author | Change Summary |
|---|---|---|---|
```

## SWRS Writing Rules

Each SWRS requirement shall:

1. Be derived from or traceable to at least one SRS item.
2. Not directly copy or mechanically reword the SRS text.
3. Be written from a software development perspective.
4. Describe externally observable software behavior.
5. Identify the relevant software boundary.
6. Be singular, feasible, verifiable, traceable, and consistent.
7. Use clear mandatory language, preferably `shall`.
8. Avoid internal implementation details unless explicitly required.
9. Mark derived or partially derived content and provide rationale.
10. Create open issues for missing, ambiguous, conflicting, or unverifiable information.

## SRS-to-SWRS Transformation Checklist

For each parent SRS, consider:

- Is this SRS software-relevant?
- What software boundary is involved?
- What software input is observed?
- What software output or response is externally visible?
- What data mapping, diagnostic behavior, state/mode behavior, timing, configuration, calibration, safety, or security behavior is needed?
- What can be verified by review, analysis, inspection, test, or demonstration?
- What information is missing and should become an open issue?
