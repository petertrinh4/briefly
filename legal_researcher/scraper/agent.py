"""High-level WebScraperAgent that composes fetch/parse/validate utilities.

This class provides a simple, safe API used by higher-level agents. It
does not perform JS rendering; use a separate module (e.g., playwright)
if you need that behavior.
"""
from typing import Optional, Dict
from .fetch import fetch_url
from .parse import parse_html
from .validate import validate_extracted
import time


class WebScraperAgent:
    def __init__(self, user_agent: str = "briefly-bot/1.0", timeout: int = 10):
        self.user_agent = user_agent
        self.timeout = timeout

    def fetch(self, url: str) -> Dict:
        return fetch_url(url, user_agent=self.user_agent, timeout=self.timeout)

    def parse(self, html: str, selectors: Optional[Dict[str, str]] = None) -> Dict:
        return parse_html(html, selectors=selectors)

    def validate(self, extracted: Dict, url: str) -> Dict:
        return validate_extracted(extracted, url)

    def fetch_and_validate(self, url: str, selectors: Optional[Dict[str, str]] = None) -> Dict:
        """Convenience method: fetch -> parse -> validate.

        Returns a dictionary with keys: fetch, parsed, validation, fetched_at
        """
        started = time.time()
        fetch_result = self.fetch(url)
        parsed = {}
        validation = {}

        if fetch_result.get("ok"):
            parsed = self.parse(fetch_result.get("text", ""), selectors=selectors)
            validation = self.validate(parsed, fetch_result.get("final_url", url))
        else:
            # Return minimal structure with the error preserved
            parsed = {"title": "", "snippets": [], "author": "", "date": "", "html": ""}
            validation = {"trust_score": 0.0, "evidence": {}}

        return {
            "fetch": fetch_result,
            "parsed": parsed,
            "validation": validation,
            "fetched_at": started,
        }
