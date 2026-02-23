from urllib.parse import urljoin, urlparse, urlunparse
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from src.ingestion.crawling.url_filters import is_allowed_url
# from .link_utils import normalize_url  # if same file, remove this line


def normalize_url(url: str, base_url: str) -> str | None:
    """
    Normalize a URL for consistent crawling.
    
    Steps:
    - Skip invalid schemes (mailto, javascript, tel, etc.)
    - Convert relative URLs to absolute
    - Remove fragments
    - Standardize scheme and domain
    - Remove default ports
    - Remove trailing slash (except root)
    """
    if not url:
        return None
    url = url.strip()

    # Skip non-http links
    if url.startswith(('mailto:', 'javascript:', 'tel:')):
        return None
    
    # Convert relative url -> absolute
    absolute_url = urljoin(base_url, url)

    parsed = urlparse(absolute_url)

    # Only allow http/https
    if parsed.scheme not in ("http", "https"):
        return None
    
    # Remove fragment
    parsed = parsed._replace(fragment="")

    # Normalize scheme and netloc
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

    # Remove default ports
    if scheme == "http" and netloc.endswith(":80"):
        netloc = netloc[:-3]
    if scheme == "https" and netloc.endswith(":443"):
        netloc = netloc[:-4]

    # Remove trailing slash (except root)
    path = parsed.path.rstrip("/")
    if not path:
        path = "/"

    normalized = parsed._replace(
        scheme=scheme,
        netloc=netloc,
        path=path
    )

    return urlunparse(normalized)

# def remove_fragment(url: str) -> str | None:
#     """
#     Remove fragment (#section) from URL.
#     """

#     if not url:
#         return None

#     parsed = urlparse(url)

#     # Remove fragment
#     cleaned = parsed._replace(fragment="")

#     return urlunparse(cleaned)


def extract_links(html: str, base_url: str) -> set[str]:
    """
    Extract and return a set of normalized, crawlable links
    restricted to the same domain as base_url.
    """

    if not html:
        return set()

    soup = BeautifulSoup(html, "html.parser")
    links = set()

    base_domain = urlparse(base_url).netloc.lower()

    for tag in soup.find_all("a", href=True):
        raw_href = tag.get("href")

        normalized = normalize_url(str(raw_href), base_url)
        if not normalized:
            continue

        parsed = urlparse(normalized)

        # Same-domain restriction
        if parsed.netloc.lower() != base_domain:
            continue

        # Apply custom URL filters
        if not is_allowed_url(normalized, base_url):
            continue

        links.add(normalized)

    return links
