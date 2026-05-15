# System Requirements Specification Template

Use this template when generating a printable System Requirements Specification, SRS.

## Document Structure

```markdown
# System Requirements Specification

Document ID: <portfolio-id>_srs_full-system_<version-or-date>
Project / Product: <project-or-product-name>
Source Document Set: <source-document-set-id>
Version: <version>
Date: <date>
Status: Draft / Review / Released

## 1. Purpose

Describe the purpose of this SRS and how it is derived from the CRS Working Set.

## 2. Scope

Describe the system scope covered by this SRS.

Include what is in scope and, if known, what is out of scope.

## 3. Source Documents and Inputs

List source documents, reconstructed document models, global requirement brief, and CRS Working Set used as inputs.

## 4. System Context

Describe the target system, ECU, vehicle function, system boundary, operating environment, and relevant external systems.

## 5. Requirement Overview

Summarize the requirement domains covered by this SRS:

- Functional Requirements
- Diagnostic Requirements
- Communication Requirements
- Interface Requirements
- Safety Requirements
- Security Requirements
- Calibration and Configuration Requirements
- Timing and Performance Requirements
- Data and Error Handling Requirements
- Resource or Constraint Requirements

## 6. System Requirements

### 6.1 Functional Requirements

#### SRS-0001 — <Short Requirement Title>

**Requirement:**  
The system shall <system-level behavior>.

**Domain:** Functional  
**Parent CRS ID:** CRS-xxxx  
**Derived:** No / Yes / Partial  
**Rationale:** <why this SRS exists and how it refines the CRS>  
**Verification Method:** Review / Analysis / Inspection / Test / Demonstration / Unknown  
**Status:** Draft / Accepted / Needs Clarification / Rejected  
**Issue:** None / OI-xxxx  
**Notes:** <optional notes>

### 6.2 Diagnostic Requirements

#### SRS-xxxx — <Short Requirement Title>

**Requirement:**  
The system shall <diagnostic behavior>.

**Domain:** Diagnostic  
**Parent CRS ID:** CRS-xxxx  
**Derived:** No / Yes / Partial  
**Rationale:** <rationale>  
**Verification Method:** <method>  
**Status:** <status>  
**Issue:** <issue>

### 6.3 Communication Requirements

### 6.4 Interface Requirements

### 6.5 Safety Requirements

### 6.6 Security Requirements

### 6.7 Calibration and Configuration Requirements

### 6.8 Timing and Performance Requirements

### 6.9 Data and Error Handling Requirements

### 6.10 Resource and Constraint Requirements

## 7. Open Issues

List unresolved SRS-related open issues or reference the Open Issues List.

## 8. Traceability Summary

Summarize CRS-to-SRS coverage and reference the traceability matrix.

## 9. Requirement Quality Summary

Summarize requirement quality findings:

- Total SRS items
- Derived / partially derived items
- Items needing clarification
- Items with unknown verification method
- Potential duplicates or conflicts

## 10. Revision History

| Version | Date | Author | Change Summary |
|---|---|---|---|
```

## SRS Requirement Writing Rules

Each SRS requirement shall:

1. Use clear mandatory language, preferably `shall`.
2. Describe one system-level need only.
3. Be traceable to one or more CRS Working Set items.
4. Be feasible and verifiable.
5. Avoid internal software design details.
6. Mark derived or partially derived content and provide rationale.
7. Create open issues for missing, ambiguous, conflicting, or unverifiable information.
