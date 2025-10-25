"""HTTP fetching utilities used by the scraper agent.

This module uses requests and returns structured results so callers can
record provenance and handle errors safely.
"""
from typing import Dict
import requests


def fetch_url(url: str, user_agent: str = "briefly-bot/1.0", timeout: int = 10) -> Dict:
    """Fetch a URL and return a structured result.

    Result keys:
      - ok: bool
      - status_code (if ok)
      - final_url (if ok)
      - headers (if ok)
      - text (if ok)
      - error (if not ok)
    """
    headers = {"User-Agent": user_agent}
    try:
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        return {
            "ok": True,
            "status_code": resp.status_code,
            "final_url": resp.url,
            "headers": dict(resp.headers),
            "text": resp.text,
        }
    except requests.RequestException as exc:
        return {"ok": False, "error": str(exc)}
