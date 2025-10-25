"""HTML parsing helpers using BeautifulSoup.

Keep parsing lightweight and return extracted fields and snippets.
"""
from typing import Dict, Optional
from bs4 import BeautifulSoup


def parse_html(html: str, selectors: Optional[Dict[str, str]] = None) -> Dict:
    """Parse HTML and return common fields.

    selectors: optional mapping to CSS selectors for title/author/date/content.
    """
    soup = BeautifulSoup(html, "html.parser")

    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()

    meta_desc = ""
    m = soup.find("meta", attrs={"name": "description"})
    if m and m.get("content"):
        meta_desc = m["content"].strip()

    # first paragraph
    first_p = ""
    p = soup.find("p")
    if p:
        first_p = p.get_text(strip=True)

    snippets = []
    for para in soup.find_all("p", limit=5):
        text = para.get_text(strip=True)
        if text:
            snippets.append(text)

    # simple author/date heuristics
    author = ""
    author_meta = soup.find("meta", attrs={"name": "author"})
    if author_meta and author_meta.get("content"):
        author = author_meta["content"].strip()

    date = ""
    time_tag = soup.find("time")
    if time_tag and time_tag.get("datetime"):
        date = time_tag["datetime"].strip()
    elif time_tag:
        date = time_tag.get_text(strip=True)

    return {
        "title": title,
        "meta_description": meta_desc,
        "first_paragraph": first_p,
        "snippets": snippets,
        "author": author,
        "date": date,
        "html": html,
    }
