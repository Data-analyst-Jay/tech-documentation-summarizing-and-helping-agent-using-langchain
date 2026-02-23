from typing import Optional
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