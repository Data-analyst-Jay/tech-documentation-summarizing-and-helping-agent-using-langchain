from typing import Optional
import trafilatura
from bs4 import BeautifulSoup

def exctract_title(html: str) -> Optional[str]:
    """
    Extract the page title from raw HTML.

    Args:
        html (str): Raw HTML content.

    Returns:
        Optional[str]: Clean page title if available.
    """

    if not html:
        return None
    
    try:
        # First try Trafilatura metadata extraction
        metadata = trafilatura.extract_metadata(html)

        if metadata and metadata.title:
            return metadata.title.strip()

        # Fallback to HTML <title> tag
        soup = BeautifulSoup(html, "html.parser")
        if soup.title and soup.title.string:
            return soup.title.string.strip()

        return None

    except Exception:
        return None