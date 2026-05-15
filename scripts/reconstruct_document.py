#!/usr/bin/env python3
"""
Reconstruct and pre-analyze extracted customer requirement documents.

Supported input:
  - A single .txt / .md / .markdown file
  - A directory containing .txt / .md / .markdown files

This script does NOT generate CRS, SRS, or SWRS. It prepares a structured
source-document package that can be reviewed or used by downstream requirement
engineering steps.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


SUPPORTED_SUFFIXES = {".txt", ".md", ".markdown"}
EXCLUDE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    "reconstruct-output",
    "preprocess-output",
}

# Domain detection rules.
# Use regex patterns instead of plain substring matching to reduce false positives,
# e.g. English "can" should not always mean CAN bus.
DOMAIN_PATTERNS: Dict[str, Sequence[str]] = {
    "Diagnostics": [
        r"\bdiagnostic(?:s)?\b",
        r"\buds\b",
        r"\bdtc\b",
        r"\bdid\b",
        r"\bobd\b",
        r"negative response",
        r"\bservice\s+0x[0-9a-f]+\b",
        r"诊断",
        r"故障码",
        r"诊断服务",
    ],
    "Communication": [
        r"\bcommunication\b",
        r"\bcan\s+(?:bus|fd|network|message|signal|frame)\b",
        r"\bcanfd\b",
        r"\blin\b",
        r"\bethernet\b",
        r"\bflexray\b",
        r"\bsignal(?:s)?\b",
        r"\bmessage(?:s)?\b",
        r"\bpdu\b",
        r"通信",
        r"报文",
        r"信号",
        r"总线",
    ],
    "Interfaces": [
        r"\binterface(?:s)?\b",
        r"\binput(?:s)?\b",
        r"\boutput(?:s)?\b",
        r"\bconnector(?:s)?\b",
        r"\bapi\b",
        r"\bport(?:s)?\b",
        r"接口",
        r"输入",
        r"输出",
        r"连接器",
    ],
    "Safety": [
        r"\bsafety\b",
        r"\basil\b",
        r"safe state",
        r"\bhazard(?:s)?\b",
        r"fault reaction",
        r"fail[- ]safe",
        r"安全",
        r"失效安全",
        r"安全状态",
        r"危害",
    ],
    "Security": [
        r"\bsecurity\b",
        r"\bcybersecurity\b",
        r"\bauthentication\b",
        r"\bencryption\b",
        r"\bsecure\b",
        r"\bcrypto(?:graphy)?\b",
        r"网络安全",
        r"认证",
        r"加密",
        r"安全访问",
    ],
    "Calibration and Configuration": [
        r"\bcalibration\b",
        r"\bcalibratable\b",
        r"\bconfiguration\b",
        r"\bconfigurable\b",
        r"\bvariant(?:s)?\b",
        r"\bcoding\b",
        r"\bparameter(?:s)?\b",
        r"标定",
        r"配置",
        r"参数",
        r"变型",
    ],
    "Timing and Performance": [
        r"\btiming\b",
        r"\btimeout(?:s)?\b",
        r"response time",
        r"\blatency\b",
        r"\bperiod(?:s)?\b",
        r"\bcycle(?:s)?\b",
        r"\bdeadline(?:s)?\b",
        r"\bperformance\b",
        r"时序",
        r"超时",
        r"响应时间",
        r"周期",
        r"性能",
    ],
    "Data and Error Handling": [
        r"\bdata\b",
        r"\binvalid\b",
        r"\berror(?:s)?\b",
        r"\bfault(?:s)?\b",
        r"\bfallback\b",
        r"\brange\b",
        r"\bvalue(?:s)?\b",
        r"数据",
        r"错误",
        r"故障",
        r"无效",
        r"回退",
        r"范围",
    ],
    "Verification": [
        r"\bverification\b",
        r"\bvalidation\b",
        r"\btest(?:s|ing)?\b",
        r"acceptance criteria",
        r"验证",
        r"确认",
        r"测试",
        r"验收准则",
    ],
}

REQUIREMENT_CUE_PATTERNS = [
    r"\bshall\b",
    r"\bmust\b",
    r"\bis required to\b",
    r"\bare required to\b",
    r"\bhas to\b",
    r"\bhave to\b",
    r"\bshould\b",
    r"\bmay\b",
    r"\bsupports?\b",
    r"\bprovides?\b",
    r"\benables?\b",
    r"应",
    r"应当",
    r"必须",
    r"不得",
    r"需要",
    r"需",
    r"支持",
    r"提供",
    r"能够",
    r"允许",
    r"禁止",
]

AMBIGUOUS_WORDING_PATTERNS = [
    r"\bfast\b",
    r"\bsuitable\b",
    r"\bappropriate\b",
    r"user-friendly",
    r"\brobust\b",
    r"\boptimized\b",
    r"as needed",
    r"\bsufficient\b",
    r"\beasy\b",
    r"\bminimal\b",
    r"normal condition",
    r"if possible",
    r"where applicable",
    r"快速",
    r"合适",
    r"适当",
    r"友好",
    r"鲁棒",
    r"优化",
    r"按需",
    r"足够",
    r"尽可能",
    r"适用时",
]


@dataclass
class SectionInfo:
    section_id: str
    document_id: str
    number: str
    title: str
    level: int
    start_line: int
    end_line: int
    domains: List[str]
    potential_requirement_region: bool
    warnings: List[str]


@dataclass
class DocumentModel:
    document_id: str
    source_file: str
    relative_path: str
    extraction_tool: str
    reconstruction_date: str
    extraction_quality: str
    title: str
    outline: List[dict]
    section_groups: Dict[str, List[dict]]
    potential_requirement_regions: List[dict]
    table_or_structured_regions: List[dict]
    extraction_warnings: List[str]


def normalize_text(text: str) -> str:
    """Normalize line endings and obvious whitespace artifacts."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[\t\u00a0]+", " ", text)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return "\n".join(line.rstrip() for line in text.split("\n")).strip() + "\n"


def collect_files(path: Path, recursive: bool = True) -> List[Path]:
    """Collect supported files while skipping generated or irrelevant directories."""
    if path.is_file():
        if path.suffix.lower() not in SUPPORTED_SUFFIXES:
            raise ValueError(f"Unsupported suffix: {path.suffix}")
        return [path]

    if not path.is_dir():
        raise FileNotFoundError(path)

    iterator = path.rglob("*") if recursive else path.glob("*")
    files = []
    for candidate in iterator:
        if not candidate.is_file():
            continue
        if candidate.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        if any(part in EXCLUDE_DIRS for part in candidate.parts):
            continue
        files.append(candidate)

    return sorted(files, key=lambda item: item.as_posix().lower())


def first_match(patterns: Iterable[str], text: str) -> bool:
    """Return True if any regex pattern matches text."""
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def detect_domains(text: str) -> List[str]:
    """Detect likely requirement domains using regex-based keyword rules."""
    detected = [
        domain
        for domain, patterns in DOMAIN_PATTERNS.items()
        if first_match(patterns, text)
    ]
    return detected or ["Unknown"]


def has_requirement_cue(text: str) -> bool:
    """Detect whether text likely contains requirement-like wording."""
    return first_match(REQUIREMENT_CUE_PATTERNS, text)


def detect_ambiguous_wording(text: str) -> List[str]:
    """Return ambiguous words/phrases found in the source text."""
    found = []
    for pattern in AMBIGUOUS_WORDING_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            # Make the warning readable by removing common regex markers.
            label = pattern.replace(r"\b", "").replace("?:", "")
            found.append(label)
    return sorted(set(found))


def detect_heading(line: str) -> Tuple[str, str, int] | None:
    """Detect Markdown, numbered, or all-caps section headings."""
    stripped = line.strip()
    if not stripped:
        return None

    markdown = re.match(r"^(#{1,6})\s+(.+)$", stripped)
    if markdown:
        raw_title = markdown.group(2).strip()
        numbered = re.match(r"^(\d+(?:\.\d+)*\.?)\s+(.+)$", raw_title)
        if numbered:
            return numbered.group(1).rstrip("."), numbered.group(2).strip(), len(markdown.group(1))
        return "N/A", raw_title, len(markdown.group(1))

    numbered = re.match(
        r"^(\d+(?:\.\d+)*\.?)\s+([A-Z][A-Za-z0-9][^.]{2,120})$",
        stripped,
    )
    if numbered:
        number = numbered.group(1).rstrip(".")
        return number, numbered.group(2).strip(), number.count(".") + 1

    if len(stripped) <= 80 and stripped.isupper() and len(stripped.split()) <= 10:
        return "N/A", stripped.title(), 1

    return None


def is_table_like_line(line: str) -> bool:
    """Detect Markdown tables or fixed-width table-like rows."""
    stripped = line.strip()
    if not stripped:
        return False
    markdown_table = stripped.count("|") >= 2
    fixed_width_columns = bool(re.search(r"\S\s{2,}\S\s{2,}\S", stripped))
    return markdown_table or fixed_width_columns


def is_list_or_requirement_id(line: str) -> bool:
    """Detect list items or requirement IDs such as REQ-123:"""
    stripped = line.strip()
    return bool(
        re.match(r"^([-*•]|\d+[.)]|[A-Z]{2,}-?\d+[:.)])\s+", stripped)
    )


def has_sentence_end(line: str) -> bool:
    return bool(re.search(r"[.!?;:。！？；：]$", line.strip()))


def repair_wrapped_lines(lines: List[str]) -> List[str]:
    """Merge obvious line wraps caused by text extraction tools."""
    repaired = []
    i = 0

    while i < len(lines):
        current = lines[i].rstrip()

        if (
            not current.strip()
            or detect_heading(current)
            or is_table_like_line(current)
            or is_list_or_requirement_id(current)
        ):
            repaired.append(current)
            i += 1
            continue

        while i + 1 < len(lines):
            nxt = lines[i + 1].rstrip()
            if (
                not nxt.strip()
                or detect_heading(nxt)
                or is_table_like_line(nxt)
                or is_list_or_requirement_id(nxt)
                or has_sentence_end(current)
            ):
                break

            should_merge_short = len(current) < 120 and re.match(r"^[a-z,(（]", nxt.strip())
            should_merge_long = len(current) >= 40 and re.match(r"^[A-Za-z0-9\u4e00-\u9fff]", nxt.strip())
            if should_merge_short or should_merge_long:
                current = current + " " + nxt.strip()
                i += 1
                continue
            break

        repaired.append(current)
        i += 1

    return repaired


def remove_repeated_short_lines(lines: List[str], min_count: int = 3) -> Tuple[List[str], List[str]]:
    """Remove repeated short lines that are likely headers or footers."""
    counter = Counter(line.strip() for line in lines if 0 < len(line.strip()) <= 80)
    repeated = {
        text
        for text, count in counter.items()
        if count >= min_count
        and not detect_heading(text)
        and not is_list_or_requirement_id(text)
    }

    warnings = []
    output = []
    removed = Counter()

    for line in lines:
        if line.strip() in repeated:
            removed[line.strip()] += 1
        else:
            output.append(line)

    for text, count in removed.items():
        warnings.append(f"Removed repeated possible header/footer '{text}' ({count} occurrences).")

    return output, warnings


def detect_sections(lines: List[str], document_id: str) -> List[SectionInfo]:
    """Split the document into sections based on detected headings."""
    headings = []
    for index, line in enumerate(lines):
        heading = detect_heading(line)
        if heading:
            headings.append((index, *heading))

    if not headings:
        body = "\n".join(lines)
        return [
            SectionInfo(
                section_id=f"{document_id}-SEC-0001",
                document_id=document_id,
                number="N/A",
                title="Unstructured Document",
                level=1,
                start_line=0,
                end_line=len(lines),
                domains=detect_domains(body),
                potential_requirement_region=has_requirement_cue(body),
                warnings=["No explicit headings detected."],
            )
        ]

    sections = []
    for section_index, (start, number, title, level) in enumerate(headings):
        end = headings[section_index + 1][0] if section_index + 1 < len(headings) else len(lines)
        body = "\n".join(lines[start:end])
        warnings = []

        if any(is_table_like_line(line) for line in lines[start:end]):
            warnings.append(
                "Contains table-like content; verify structure if requirements depend on table values."
            )

        sections.append(
            SectionInfo(
                section_id=f"{document_id}-SEC-{len(sections) + 1:04d}",
                document_id=document_id,
                number=number,
                title=title,
                level=level,
                start_line=start,
                end_line=end,
                domains=detect_domains(title + "\n" + body),
                potential_requirement_region=has_requirement_cue(body),
                warnings=warnings,
            )
        )

    return sections


def evaluate_extraction_quality(lines: List[str], warnings: List[str]) -> str:
    """Heuristic quality rating: Good / Partial / Poor."""
    non_empty = [line for line in lines if line.strip()]
    if not non_empty:
        return "Poor"

    short_line_ratio = sum(1 for line in non_empty if len(line.strip()) < 25) / len(non_empty)
    table_line_ratio = sum(1 for line in non_empty if is_table_like_line(line)) / len(non_empty)

    if len(warnings) > 10 or short_line_ratio > 0.65:
        return "Poor"
    if len(warnings) > 3 or table_line_ratio > 0.20 or short_line_ratio > 0.45:
        return "Partial"
    return "Good"


def build_document_model(
    document_id: str,
    file_path: Path,
    relative_path: str,
    extraction_tool: str,
    lines: List[str],
    sections: List[SectionInfo],
    warnings: List[str],
) -> DocumentModel:
    """Build the machine-readable and human-readable model for one document."""
    title = next(
        (section.title for section in sections if section.title != "Unstructured Document"),
        file_path.stem,
    )

    outline = [
        {
            "section_id": section.section_id,
            "document_id": document_id,
            "number": section.number,
            "title": section.title,
            "level": section.level,
            "domains": section.domains,
        }
        for section in sections
    ]

    section_groups: Dict[str, List[dict]] = {}
    potential_regions = []
    table_regions = []

    for section in sections:
        for domain in section.domains:
            section_groups.setdefault(domain, []).append(
                {
                    "document_id": document_id,
                    "section_id": section.section_id,
                    "number": section.number,
                    "title": section.title,
                }
            )

        if section.potential_requirement_region:
            potential_regions.append(
                {
                    "document_id": document_id,
                    "section_id": section.section_id,
                    "number": section.number,
                    "title": section.title,
                    "domains": section.domains,
                }
            )

        section_lines = lines[section.start_line : section.end_line]
        if any(is_table_like_line(line) for line in section_lines):
            table_regions.append(
                {
                    "document_id": document_id,
                    "section_id": section.section_id,
                    "title": section.title,
                    "note": "Table-like content detected.",
                }
            )

        for warning in section.warnings:
            warnings.append(f"{section.section_id} {section.title}: {warning}")

    ambiguous = detect_ambiguous_wording("\n".join(lines))
    if ambiguous:
        warnings.append("Ambiguous wording found: " + ", ".join(ambiguous) + ".")

    return DocumentModel(
        document_id=document_id,
        source_file=file_path.name,
        relative_path=relative_path,
        extraction_tool=extraction_tool,
        reconstruction_date=date.today().isoformat(),
        extraction_quality=evaluate_extraction_quality(lines, warnings),
        title=title,
        outline=outline,
        section_groups=section_groups,
        potential_requirement_regions=potential_regions,
        table_or_structured_regions=table_regions,
        extraction_warnings=warnings,
    )


def safe_filename(value: str) -> str:
    """Make a conservative filename component."""
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)[:80] or "document"


def markdown_escape_cell(value: object) -> str:
    """Escape values for Markdown table cells."""
    text = str(value).replace("\n", " ").replace("|", r"\|")
    return text.strip()


def markdown_table(headers: Sequence[str], rows: Sequence[Sequence[object]]) -> str:
    """Create a valid GitHub-flavored Markdown table."""
    header_line = "| " + " | ".join(markdown_escape_cell(h) for h in headers) + " |"
    separator_line = "| " + " | ".join("---" for _ in headers) + " |"
    body_lines = [
        "| " + " | ".join(markdown_escape_cell(cell) for cell in row) + " |"
        for row in rows
    ]
    return "\n".join([header_line, separator_line, *body_lines])


def write_document_model_markdown(path: Path, model: DocumentModel) -> None:
    """Write a readable Markdown model for one source document."""
    lines = [
        "# Document Analysis Model",
        "",
        "## Document Metadata",
        "",
        f"- Document ID: `{model.document_id}`",
        f"- Document Title: `{model.title}`",
        f"- Source File: `{model.source_file}`",
        f"- Relative Path: `{model.relative_path}`",
        f"- Extraction Tool: `{model.extraction_tool}`",
        f"- Reconstruction Date: `{model.reconstruction_date}`",
        f"- Extraction Quality: `{model.extraction_quality}`",
        "",
        "## High-Level Outline",
        "",
    ]

    for item in model.outline:
        indent = "  " * max(item["level"] - 1, 0)
        number = "" if item["number"] == "N/A" else item["number"]
        domains = ", ".join(item["domains"])
        lines.append(f"{indent}- `{item['section_id']}` {number} {item['title']} — {domains}")

    lines.extend(["", "## Potential Requirement Regions", ""])
    if model.potential_requirement_regions:
        for region in model.potential_requirement_regions:
            number = "" if region.get("number") == "N/A" else region.get("number", "")
            lines.append(
                f"- `{region['section_id']}` {number} {region['title']} — {', '.join(region['domains'])}"
            )
    else:
        lines.append("- None detected.")

    lines.extend(["", "## Table or Structured Regions", ""])
    if model.table_or_structured_regions:
        for region in model.table_or_structured_regions:
            lines.append(f"- `{region['section_id']}` {region['title']} — {region['note']}")
    else:
        lines.append("- None detected.")

    lines.extend(["", "## Extraction Warnings", ""])
    if model.extraction_warnings:
        lines.extend(f"- {warning}" for warning in model.extraction_warnings)
    else:
        lines.append("- None.")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def relative_to_base(file_path: Path, base: Path) -> str:
    """Return relative path if possible, otherwise filename."""
    try:
        return file_path.relative_to(base).as_posix()
    except ValueError:
        return file_path.name


def process_document(
    file_path: Path,
    base_path: Path,
    output_dir: Path,
    document_id: str,
    extraction_tool: str,
    remove_repeated: bool,
) -> Tuple[dict, DocumentModel]:
    """Process one document and write per-document outputs."""
    raw_text = file_path.read_text(encoding="utf-8", errors="replace")
    lines = normalize_text(raw_text).splitlines()
    warnings = []

    if remove_repeated:
        lines, repeated_warnings = remove_repeated_short_lines(lines)
        warnings.extend(repeated_warnings)

    lines = repair_wrapped_lines(lines)
    sections = detect_sections(lines, document_id)
    relative_path = relative_to_base(file_path, base_path)

    model = build_document_model(
        document_id=document_id,
        file_path=file_path,
        relative_path=relative_path,
        extraction_tool=extraction_tool,
        lines=lines,
        sections=sections,
        warnings=warnings,
    )

    document_dir = output_dir / "documents" / document_id
    document_dir.mkdir(parents=True, exist_ok=True)

    reconstructed_path = document_dir / f"{document_id}_{safe_filename(file_path.stem)}_reconstructed.md"
    reconstructed_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")

    model_json_path = document_dir / "document_model.json"
    model_json_path.write_text(
        json.dumps(asdict(model), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    model_md_path = document_dir / "document_model.md"
    write_document_model_markdown(model_md_path, model)

    document_row = {
        "document_id": document_id,
        "file": file_path.name,
        "relative_path": relative_path,
        "title": model.title,
        "quality": model.extraction_quality,
        "domains": sorted({domain for item in model.outline for domain in item["domains"]}),
        "potential_requirement_regions": len(model.potential_requirement_regions),
        "reconstructed_reference": reconstructed_path.as_posix(),
        "model_reference": model_md_path.as_posix(),
    }

    return document_row, model


def write_source_registry(path: Path, documents: List[dict]) -> None:
    """Write a valid Markdown registry table for all source documents."""
    rows = [
        [
            document["document_id"],
            document["file"],
            document["relative_path"],
            document["title"],
            document["quality"],
            ", ".join(document["domains"]),
            document["potential_requirement_regions"],
        ]
        for document in documents
    ]

    content = "\n".join(
        [
            "# Source Document Registry",
            "",
            markdown_table(
                [
                    "Document ID",
                    "File",
                    "Relative Path",
                    "Title",
                    "Quality",
                    "Domains",
                    "Potential Requirement Regions",
                ],
                rows,
            ),
            "",
        ]
    )
    path.write_text(content, encoding="utf-8")


def write_combined_model(output_dir: Path, portfolio: dict) -> None:
    """Write combined JSON and readable Markdown outputs."""
    lines = [
        "# Combined Document Analysis Model",
        "",
        "## Portfolio Metadata",
        "",
        f"- Portfolio ID: `{portfolio['portfolio_id']}`",
        f"- Reconstruction Date: `{portfolio['reconstruction_date']}`",
        f"- Input Path: `{portfolio['input_path']}`",
        f"- Document Count: `{portfolio['document_count']}`",
        "",
        "## Source Documents",
        "",
    ]

    for document in portfolio["documents"]:
        lines.append(
            f"- `{document['document_id']}` {document['relative_path']} — "
            f"{document['title']} — Quality: `{document['quality']}`"
        )

    lines.extend(["", "## Domain Index", ""])
    for domain in sorted(portfolio["domain_index"]):
        lines.append(f"### {domain}")
        for section in portfolio["domain_index"][domain]:
            number = "" if section.get("number") == "N/A" else section.get("number", "")
            lines.append(
                f"- `{section['document_id']}` / `{section['section_id']}` {number} {section['title']}"
            )
        lines.append("")

    lines.extend(["## Potential Requirement Regions", ""])
    if portfolio["potential_requirement_regions"]:
        for region in portfolio["potential_requirement_regions"]:
            number = "" if region.get("number") == "N/A" else region.get("number", "")
            lines.append(
                f"- `{region['document_id']}` / `{region['section_id']}` "
                f"{number} {region['title']} — {', '.join(region['domains'])}"
            )
    else:
        lines.append("- None detected.")

    lines.extend(["", "## Extraction Warnings", ""])
    if portfolio["extraction_warnings"]:
        lines.extend(f"- {warning}" for warning in portfolio["extraction_warnings"])
    else:
        lines.append("- None.")

    (output_dir / "combined_document_model.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (output_dir / "combined_document_model.json").write_text(
        json.dumps(portfolio, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def write_global_requirement_brief(output_dir: Path, portfolio: dict) -> None:
    """Write a review-friendly skeleton for downstream CRS/SRS/SWRS work."""
    domains = [domain for domain in sorted(portfolio["domain_index"]) if domain != "Unknown"] or ["Unknown"]

    lines = [
        "# Global Requirement Brief",
        "",
        "## 1. Document Purpose",
        "TBD based on the source document set.",
        "",
        "## 2. Scope and System Context",
        "TBD.",
        "",
        "## 3. Source Document Set",
        "",
    ]

    for document in portfolio["documents"]:
        lines.append(f"- `{document['document_id']}` {document['relative_path']} — {document['title']}")

    lines.extend(["", "## 4. Main Requirement Domains", ""])
    lines.extend(f"- {domain}" for domain in domains)

    lines.extend(["", "## 5. Relevant Sections and Source Areas", ""])
    if portfolio["potential_requirement_regions"]:
        for region in portfolio["potential_requirement_regions"][:80]:
            number = "" if region.get("number") == "N/A" else region.get("number", "")
            lines.append(
                f"- `{region['document_id']}` / `{region['section_id']}` "
                f"{number} {region['title']} — {', '.join(region['domains'])}"
            )
    else:
        lines.append("- None detected.")

    lines.extend(
        [
            "",
            "## 6. Terminology and Abbreviations",
            "TBD.",
            "",
            "## 7. Key Assumptions",
            "- Do not invent missing thresholds, units, interfaces, safety assumptions, or security assumptions.",
            "",
            "## 8. Extraction Quality Notes",
            "TBD from extraction warnings.",
            "",
            "## 9. Duplicate, Overlap, and Conflict Risks",
            "TBD during CRS extraction.",
            "",
            "## 10. Major Open Questions",
            "TBD.",
            "",
            "## 11. Recommended Derivation Strategy",
            "- Extract a CRS working set by domain across all source documents.",
            "- Preserve source document IDs and section IDs in CRS source references.",
            "- Consolidate duplicates and flag conflicts.",
            "- Derive one coherent SRS and SWRS unless module-specific outputs are requested.",
        ]
    )

    (output_dir / "global_requirement_brief_skeleton.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def build_portfolio(
    args: argparse.Namespace,
    documents: List[dict],
    models: List[DocumentModel],
) -> dict:
    """Build the combined portfolio model."""
    domain_index: Dict[str, List[dict]] = {}
    potential_regions = []
    warnings = []

    for document, model in zip(documents, models):
        for domain, sections in model.section_groups.items():
            domain_index.setdefault(domain, []).extend(sections)

        potential_regions.extend(model.potential_requirement_regions)
        warnings.extend(
            f"{document['document_id']}: {warning}"
            for warning in model.extraction_warnings
        )

    return {
        "portfolio_id": args.portfolio_id,
        "reconstruction_date": date.today().isoformat(),
        "input_path": args.input.as_posix(),
        "document_count": len(documents),
        "documents": documents,
        "domain_index": domain_index,
        "potential_requirement_regions": potential_regions,
        "extraction_warnings": warnings,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reconstruct and pre-analyze extracted customer requirement documents."
    )
    parser.add_argument("input", type=Path, help="Input file or directory.")
    parser.add_argument("--out", type=Path, default=Path("reconstruct-output"), help="Output directory.")
    parser.add_argument("--document-id-prefix", default="SRC", help="Prefix for generated document IDs.")
    parser.add_argument("--document-id", help="Explicit document ID when processing a single file.")
    parser.add_argument("--portfolio-id", default="REQ-PORTFOLIO-0001", help="Portfolio ID.")
    parser.add_argument("--extraction-tool", default="manual-or-extracted-text", help="Name of upstream extraction tool.")
    parser.add_argument("--remove-repeated", action="store_true", help="Remove repeated short lines, likely headers/footers.")
    parser.add_argument("--no-recursive", action="store_true", help="Do not recursively scan input directories.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    files = collect_files(args.input, recursive=not args.no_recursive)

    if not files:
        raise FileNotFoundError(f"No supported files found under: {args.input}")

    args.out.mkdir(parents=True, exist_ok=True)
    base_path = args.input if args.input.is_dir() else args.input.parent

    documents = []
    models = []

    for index, file_path in enumerate(files, start=1):
        if len(files) == 1 and args.document_id:
            document_id = args.document_id
        else:
            document_id = f"{args.document_id_prefix}-{index:04d}"

        document_row, model = process_document(
            file_path=file_path,
            base_path=base_path,
            output_dir=args.out,
            document_id=document_id,
            extraction_tool=args.extraction_tool,
            remove_repeated=args.remove_repeated,
        )
        documents.append(document_row)
        models.append(model)

    portfolio = build_portfolio(args, documents, models)

    write_source_registry(args.out / "source_document_registry.md", documents)
    write_combined_model(args.out, portfolio)
    write_global_requirement_brief(args.out, portfolio)

    warnings_text = "\n".join(f"- {warning}" for warning in portfolio["extraction_warnings"])
    if not warnings_text:
        warnings_text = "- None."
    (args.out / "extraction_warnings.md").write_text(
        "# Extraction Warnings\n\n" + warnings_text + "\n",
        encoding="utf-8",
    )

    print(f"Reconstruction complete: {args.out}")
    print(
        f"Documents: {len(documents)} | "
        f"Potential requirement regions: {len(portfolio['potential_requirement_regions'])}"
    )


if __name__ == "__main__":
    main()
