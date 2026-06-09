"""Process guides for legal triage.

Defines structured step‑by‑step guides (currently only eviction) and helper
functions to turn a guide into searchable text and pretty‑print it for the
CLI.
"""

from __future__ import annotations

from typing import List, Dict, Any

# ---------------------------------------------------------------------------
# Data definitions
# ---------------------------------------------------------------------------

EVICITON_GUIDE: Dict[str, Any] = {
    "topic": "eviction",
    "title": "Eviction Process – Step by Step",
    "jurisdiction": "IL",
    "last_updated": "2026-01-01",
    "keywords": ["eviction", "tenant", "landlord", "notice"],
    "steps": [
        {
            "number": 1,
            "title": "Receive Notice",
            "description": "Landlord gives a 3‑day, 5‑day, or 30‑day notice to vacate."
        },
        {
            "number": 2,
            "title": "File Response",
            "description": "You can file an appearance with the court and request a hearing."
        },
        {
            "number": 3,
            "title": "Court Hearing",
            "description": "A judge reviews the case, hears both parties, and decides."
        },
        {
            "number": 4,
            "title": "Judgment & Order",
            "description": "If the judge rules for the landlord, a writ of execution is issued."
        },
        {
            "number": 5,
            "title": "Eviction / Move‑out",
            "description": "Sheriff enforces the order; you must vacate by the deadline."
        },
    ],
    "your_rights": [
        "Right to respond to the notice",
        "Right to request mediation",
        "Right to appeal the judgment",
    ],
    "contact": {
        "name": "Eviction Hotline",
        "phone": "855-601-9474",
    },
    # Mark the document type so we can prioritize it in search results
    "type": "process_guide",
}

# If we ever add more guides, just append them here.
PROCESS_GUIDES: List[Dict[str, Any]] = [EVICITON_GUIDE]

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def guide_to_search_text(guide: Dict[str, Any]) -> str:
    """Flatten a guide into a single searchable string.

    The text includes the title, steps, rights, contact info and keywords.
    This mirrors how the HTML documents are turned into a single "text"
    field before embedding.
    """
    parts: List[str] = []
    parts.append(guide.get("title", ""))
    parts.append(" ".join(guide.get("keywords", [])))
    # Steps
    for step in guide.get("steps", []):
        parts.append(f"Step {step.get('number')}: {step.get('title')} {step.get('description')}")
    # Rights
    parts.append("Your rights: " + ", ".join(guide.get("your_rights", [])))
    # Contact
    contact = guide.get("contact", {})
    if contact:
        parts.append(f"Contact {contact.get('name')}: {contact.get('phone')}")
    return " ".join(parts)


def format_guide_for_display(guide: Dict[str, Any]) -> str:
    """Pretty‑print a guide for CLI output.

    Returns a multi‑line string that mimics the style of the existing search
    results but highlights the step‑by‑step flow.
    """
    lines: List[str] = []
    lines.append(f"=== {guide.get('title')} (Jurisdiction: {guide.get('jurisdiction')}) ===")
    lines.append(f"Last updated: {guide.get('last_updated')}")
    lines.append("")
    for step in guide.get("steps", []):
        lines.append(f"{step.get('number')}. {step.get('title')}")
        lines.append(f"   {step.get('description')}")
    lines.append("")
    lines.append("Your rights:")
    for right in guide.get("your_rights", []):
        lines.append(f"- {right}")
    lines.append("")
    contact = guide.get("contact", {})
    if contact:
        lines.append(f"Contact: {contact.get('name')} – {contact.get('phone')}")
    return "\n".join(lines)

# Exported symbols
__all__ = [
    "PROCESS_GUIDES",
    "guide_to_search_text",
    "format_guide_for_display",
]
