"""Validation and provenance heuristics for extracted content.

This module implements simple, deterministic heuristics to produce a
trust_score and evidence markers. It's intentionally conservative and
meant to be a starting point for more advanced checks.
"""
from urllib.parse import urlparse
from typing import Dict


def validate_extracted(extracted: Dict, url: str) -> Dict:
    """Return a validation dict with trust_score (0-1) and evidence.

    Evidence keys include: is_official_domain, has_author, has_date.
    """
    hostname = urlparse(url).hostname or ""
    hostname = hostname.lower()

    is_official = False
    if hostname.endswith((".gov", ".edu")):
        is_official = True
    # treat well-known organizations slightly more trustworthily
    if hostname.endswith(".org") and hostname.count(".") <= 2:
        is_official = True

    has_author = bool(extracted.get("author"))
    has_date = bool(extracted.get("date"))

    score = 0.5
    if is_official:
        score += 0.2
    if has_author:
        score += 0.15
    if has_date:
        score += 0.15
    if score > 1.0:
        score = 1.0

    evidence = {"is_official_domain": is_official, "has_author": has_author, "has_date": has_date}
    return {"trust_score": score, "evidence": evidence}
