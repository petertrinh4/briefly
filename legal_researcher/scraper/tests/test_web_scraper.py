"""Basic tests for the WebScraperAgent.

These tests are intentionally small and verify the fetch-parse-validate
happy path against https://example.com which is stable and fast.
"""
from legal_researcher.scraper.agent import WebScraperAgent


def test_fetch_parse_validate_example():
    agent = WebScraperAgent()
    result = agent.fetch_and_validate("https://example.com")

    # fetch should succeed
    assert result["fetch"]["ok"] is True

    # parsed should contain a title and snippets list
    assert isinstance(result["parsed"].get("title"), str)
    assert isinstance(result["parsed"].get("snippets"), list)

    # validation trust_score should be a float between 0 and 1
    ts = result["validation"].get("trust_score")
    assert isinstance(ts, float)
    assert 0.0 <= ts <= 1.0
