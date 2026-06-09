"""process_guide_extractor.py

Utility module that extracts a *process guide* from existing legal HTML documents.
The goal is to turn free‑form legal text into a structured, numbered guide that
contains:

1. **Steps** – ordered actions extracted from the text.
2. **Deadlines** – any time‑frames or notice periods mentioned.
3. **Forms** – references to official forms (e.g., "LJ‑100").
4. **Requirements / Rights** – short bullet points extracted from a "what you
   need" or "your rights" paragraph.

The extraction logic uses a set of regular‑expression patterns that target the
most common phrasing found in the Illinois legal aid pages (e.g. eviction,
divorce, custody).  It is deliberately simple – the aim is to be *usable* without
requiring any heavy‑weight NLP libraries, while still providing useful output.

Typical usage:
    >>> from process_guide_extractor import extract_guide_for_topic
    >>> guide = extract_guide_for_topic('eviction')
    >>> print(guide['title'])
    >>> for i, step in enumerate(guide['steps'], 1):
    ...     print(f"{i}. {step}")

The function reads the raw HTML file from the ``data`` directory, extracts the
readable text (mirroring the logic in ``legal_triage.py``) and then applies the
regex patterns.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Any

# ---------------------------------------------------------------------------
# Helper – same text‑extraction used by the main triage script
# ---------------------------------------------------------------------------

def _extract_text_from_html(html_path: Path) -> str:
    """Return the cleaned readable text from an HTML file.

    This mirrors the ``extract_text_from_html`` function in ``legal_triage.py``
    so that the extractor works on exactly the same content that is indexed.
    """
    from bs4 import BeautifulSoup

    html_content = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html_content, "html.parser")
    # Drop noisy elements
    for element in soup(["script", "style", "noscript", "meta", "link", "head", "iframe"]):
        element.decompose()
    content_div = soup.find("div", class_="entry-content")
    if content_div:
        text = content_div.get_text(separator=" ")
    else:
        text = soup.get_text(separator=" ")
    # Normalise whitespace
    return re.sub(r"\s+", " ", text).strip()

# ---------------------------------------------------------------------------
# Regex patterns for each topic – these have been tuned on the existing HTML
# files (eviction‑illinois.html, divorce‑illinois.html, etc.)
# ---------------------------------------------------------------------------

_PATTERNS: Dict[str, Dict[str, Any]] = {
    "eviction": {
        "step": r"(?:file|submit|serve|request|appeal|schedule|attend|pay|receive)[^\.\n]*",
        # Look for time‑frames like "3‑day notice" or "within 5 days"
        "deadline": r"(?:\d+[-–]?day|\d+\s+day|within \d+ days?|notice period of \d+ days?)",
        "form": r"form\s*[-:]?\s*([A-Z]{1,3}[ -]?\d{1,4}[A-Z]?)",
        "right": r"you (?:may|have|are entitled) to [^\.\n]*",
    },
    "divorce": {
        "step": r"(?:file|serve|submit|petition|request|attend|mediation|wait|appear)[^\.\n]*",
        "deadline": r"(?:\d+\s+days?|\d+\s+weeks?|\d+\s+months?)",
        "form": r"form\s*[-:]?\s*([A-Z]{1,3}[ -]?\d{1,4}[A-Z]?)",
        "right": r"you (?:may|have|are entitled) to [^\.\n]*",
    },
    "custody": {
        "step": r"(?:file|serve|request|attend|evaluate|court|mediation)[^\.\n]*",
        "deadline": r"(?:\d+\s+days?|\d+\s+weeks?)",
        "form": r"form\s*[-:]?\s*([A-Z]{1,3}[ -]?\d{1,4}[A-Z]?)",
        "right": r"you (?:may|have|are entitled) to [^\.\n]*",
    },
}

# ---------------------------------------------------------------------------
# Core extraction routine
# ---------------------------------------------------------------------------

def _find_all(pattern: str, text: str) -> List[str]:
    """Utility that returns all non‑empty, stripped matches for ``pattern``.
    ``re.IGNORECASE`` is always used.
    """
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    # ``findall`` can return tuples when groups are used – flatten them
    flattened: List[str] = []
    for m in matches:
        if isinstance(m, tuple):
            flattened.extend([s for s in m if s])
        else:
            flattened.append(m)
    # Remove duplicates while preserving order
    seen = set()
    unique: List[str] = []
    for item in flattened:
        cleaned = item.strip()
        if cleaned and cleaned.lower() not in seen:
            seen.add(cleaned.lower())
            unique.append(cleaned)
    return unique


def extract_guide_from_html(html_path: Path, topic: str) -> Dict[str, Any]:
    """Extract a structured guide from a single HTML file.

    Args:
        html_path: Path to the HTML file that contains the legal content.
        topic: The legal topic – must be a key present in ``_PATTERNS``.
    Returns:
        A dict with keys ``title``, ``steps``, ``deadlines``, ``forms``,
        ``rights``.  Missing sections are represented by empty lists.
    """
    if topic not in _PATTERNS:
        raise ValueError(f"Unsupported topic {topic!r}. Available: {list(_PATTERNS)}")

    raw_text = _extract_text_from_html(html_path)
    patterns = _PATTERNS[topic]

    steps = _find_all(patterns["step"], raw_text)
    deadlines = _find_all(patterns["deadline"], raw_text)
    forms = _find_all(patterns["form"], raw_text)
    rights = _find_all(patterns["right"], raw_text)

    return {
        "topic": topic,
        "title": f"{topic.title()} Process Guide",
        "steps": steps,
        "deadlines": deadlines,
        "forms": forms,
        "rights": rights,
    }


def extract_guide_for_topic(topic: str) -> Dict[str, Any]:
    """Convenient wrapper that scans the ``data`` directory for a file that
    mentions the given ``topic`` and returns the first successfully parsed guide.

    The function looks for files whose name contains the topic (e.g. ``eviction``)
    and runs ``extract_guide_from_html`` on the first match.
    """
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    # Find candidate HTML files – we don't care about sub‑folders here
    candidates = list(data_dir.rglob(f"*{topic}*\.html"))
    if not candidates:
        raise FileNotFoundError(f"No HTML files found for topic {topic!r} under {data_dir}")
    for html_path in candidates:
        try:
            guide = extract_guide_from_html(html_path, topic)
            # If we managed to extract at least one step, assume success
            if guide["steps"]:
                return guide
        except Exception:  # pragma: no cover – safe fallback
            continue
    # If we get here, nothing was extracted – return an empty scaffold
    return {
        "topic": topic,
        "title": f"{topic.title()} Process Guide",
        "steps": [],
        "deadlines": [],
        "forms": [],
        "rights": [],
    }


def format_guide(guide: Dict[str, Any]) -> str:
    """Pretty‑print a guide for CLI display.

    Returns a multi‑line string that enumerates steps, deadlines, forms and
    rights.
    """
    lines: List[str] = []
    lines.append(f"=== {guide.get('title', 'Process Guide')} ===")
    if guide.get("steps"):
        lines.append("\nSteps:")
        for i, step in enumerate(guide["steps"], 1):
            lines.append(f"{i}. {step.strip()}")
    if guide.get("deadlines"):
        lines.append("\nDeadlines / Time‑frames:")
        for d in guide["deadlines"]:
            lines.append(f"- {d}")
    if guide.get("forms"):
        lines.append("\nRequired Forms:")
        for f in guide["forms"]:
            lines.append(f"- {f}")
    if guide.get("rights"):
        lines.append("\nYour Rights / Requirements:")
        for r in guide["rights"]:
            lines.append(f"- {r.strip()}")
    return "\n".join(lines)

# Exported symbols – handy for ``from process_guide_extractor import *``
__all__ = [
    "extract_guide_from_html",
    "extract_guide_for_topic",
    "format_guide",
]
