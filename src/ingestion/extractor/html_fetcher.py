import requests
from typing import Optional


default_headers = {
    "User-Agent":(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        "AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def fetch_html(url: str, timeout: int = 10) -> Optional[str]:
    '''
    Fetch raw HTML content from a given URL.

    Args:
        url (str): The URL to fetch.
        timeout (int): Request timeout in seconds.

    Returns:
        Optional[str]: HTML content if successful, otherwise None.
    '''
    try:
        response = requests.get(
            url,
            headers = default_headers,
            timeout=timeout
        )

        # Raise HTTPError for bad status codes (4xx, 5xx)
        response.raise_for_status()

        # Ensure content type is HTML
        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            return None

        return response.text
    
    except requests.exceptions.RequestException:
        # Can be later replace this with proper logging
        return None