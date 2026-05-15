# Derivation Rules

## CRS to SRS

Derive SRS items from CRS Working Set items using the Global Requirement Brief for context. Each SRS item shall trace to one or more CRS items.

## SRS Fields

- SRS ID
- System Requirement
- Domain
- Parent CRS ID
- Derived
- Rationale
- Verification Method
- Status
- Issue

## SRS to SWRS

Derive SWRS items from reviewed SRS items. Each SWRS item shall trace to one or more SRS items and describe externally observable software behavior.

## SWRS Fields

- SWRS ID
- Software Requirement
- Domain
- Parent SRS ID
- Software Boundary
- Derived
- Rationale
- Verification Method
- Status
- Issue

## SRS to SWRS Transformation Guidance

Do not copy SRS text directly into SWRS.

An SRS describes system-level behavior or constraints. An SWRS shall describe software-relevant, externally observable behavior needed to realize or support that system requirement.

When deriving SWRS from SRS, perform the following reasoning steps:

1. Identify the system behavior, constraint, or interface described by the SRS.
2. Determine whether the SRS is software-relevant, system-only, hardware-only, mechanical-only, process-only, or unclear.
3. If software-relevant, identify the software boundary involved, such as application software, diagnostic software, communication stack, platform software, safety software, cybersecurity software, calibration/configuration, or software-hardware interface.
4. Define the externally observable software behavior using clear `shall` language.
5. Identify required software inputs, outputs, states, modes, data, timing, diagnostic behavior, configuration, calibration, safety, or security behavior where supported by source or parent requirements.
6. Avoid internal design details such as functions, classes, threads, tasks, private algorithms, internal scheduling, file names, or architecture allocation unless explicitly required.
7. If necessary details are missing, create an open issue rather than inventing them.

Use ISO/IEC/IEEE 29148-inspired writing principles: requirements should be necessary, implementation-independent where appropriate, unambiguous, complete enough for the level, singular, feasible, verifiable, traceable, and consistent.

### Example

SRS:

`The system shall provide diagnostic read access to configured DID values using UDS service 0x22.`

Poor SWRS copied from SRS:

`The software shall provide diagnostic read access to configured DID values using UDS service 0x22.`

Better SWRS from a software development perspective:

`The software shall accept UDS service 0x22 requests for supported DID identifiers through the diagnostic communication interface.`

`The software shall return DID data values according to the configured DID-to-data mapping for supported UDS service 0x22 requests.`

If the negative response behavior is not specified, create an open issue instead of inventing the exact response code.

## Missing Information

Do not invent timing thresholds, units, operating modes, interface definitions, diagnostic negative response behavior, safety assumptions, security assumptions, calibration ranges, data mapping, or verification criteria.
