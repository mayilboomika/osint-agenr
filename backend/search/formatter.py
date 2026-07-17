import requests
from bs4 import BeautifulSoup


def extract_page_text(url, timeout=8):
    """Fetch the webpage and return visible text content."""
    try:
        response = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except requests.RequestException:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "noscript", "iframe", "header", "footer", "nav"]):
        tag.extract()

    text = "\n".join(
        part.strip()
        for part in soup.stripped_strings
        if part.strip()
    )
    return text[:2000] if text else None
