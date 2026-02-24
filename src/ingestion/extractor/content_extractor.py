from typing import Optional
from bs4 import BeautifulSoup
import trafilatura

def extract_main_content(html: str) -> Optional[str]:
    """
    Extract main readable content using Trafilatura.

    Args:
        html (str): Raw HTML content.

    Returns:
        Optional[str]: Cleaned text suitable for RAG ingestion.
    """
    if not html:
        return None
    
    soup = BeautifulSoup(html, "html.parser")

    # Remove scripts/styles
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # First try structured extraction
    main_container = soup.find("div", id="content-container")

    if main_container:
        text = main_container.get_text(separator="\n", strip=True)
        if text:
            return text
    
    try:
        extracted_text = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=True,
            favor_recall=True
        )

        if not extracted_text:
            return None

        return extracted_text.strip()
    
    except Exception:
        return None