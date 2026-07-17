import json
import requests
from ddgs import DDGS

from .formatter import extract_page_text


def search_topic(query, max_results=7, fetch_content=False):
    """Search the web and return structured results for a single topic."""
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must be a non-empty string")

    query = query.strip()
    with DDGS() as ddgs:
        results = list(ddgs.text(query, region="wt-wt", safesearch="off", timelimit=None, max_results=max_results))
    sources = []

    if not results:
        return {"topic": query, "sources": []}

    for index, item in enumerate(results[:max_results], start=1):
        title = item.get("title") or item.get("body") or "No title"
        url = item.get("href") or item.get("url") or item.get("link") or ""
        snippet = item.get("body") or item.get("snippet") or item.get("excerpt") or ""

        source = {
            "title": title,
            "url": url,
            "snippet": snippet,
        }

        if fetch_content and url:
            content = extract_page_text(url)
            if content:
                source["content"] = content

        sources.append(source)

    return {"topic": query, "sources": sources}


if __name__ == "__main__":
    results = search_topic("OpenAI Windsurf", fetch_content=False)
    print(json.dumps(results, indent=2, ensure_ascii=False))
