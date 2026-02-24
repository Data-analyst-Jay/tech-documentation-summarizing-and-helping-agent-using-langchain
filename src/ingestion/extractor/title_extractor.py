from typing import Optional
import trafilatura
from bs4 import BeautifulSoup

def exctract_title(html: str) -> Optional[str]:
    """
    Extract the page title from raw HTML.
    Priority:
    1. <h1> inside main content
    2. <title> tag
    3. Trafilatura meatadata

    Args:
        html (str): Raw HTML content.

    Returns:
        Optional[str]: Clean page title if available.
    """

    if not html:
        return None
    
    try:
        soup = BeautifulSoup(html, "html.parser")
        # 1️⃣ Try H1 first (most reliable for docs)
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        
        # 2️⃣ Fallback to <title>
        if soup.title and soup.title.string:
            raw_title = soup.title.string.strip()

            # Remove branding if present
            if "|" in raw_title:
                raw_title = raw_title.split("|")[0].strip()
            if "-" in raw_title:
                raw_title = raw_title.split("-")[0].strip()

            return raw_title
    
        # 3️⃣ Final fallback: Trafilatura metadata
        metadata = trafilatura.extract_metadata(html)

        if metadata and metadata.title:
            return metadata.title.strip()

        return None

    except Exception:
        return None