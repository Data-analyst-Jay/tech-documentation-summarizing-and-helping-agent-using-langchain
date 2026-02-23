import re
from urllib.parse import urlparse

# def is_allowed_url(url, include_patterns, exclude_patterns):
#     if include_patterns:
#         if not any(p in url for p in include_patterns):
#             return False
        
#     if exclude_patterns:
#         if any(p in url for p in exclude_patterns):
#             return False
    
#     return True

EXCLUDE_PATTERNS = [
    # Search / Query Pages
    r".*/search(/|$).*",
    r".*/results(/|$).*",

    # Blog / News / Marketing
    r".*/blog(/|$).*",
    r".*/news(/|$).*",
    r".*/changelog(/|$).*",
    r".*/release(-|_)?notes(/|$).*",
    r".*/announcements(/|$).*",

    # Auth / Account
    r".*/login(/|$).*",
    r".*/logout(/|$).*",
    r".*/signup(/|$).*",
    r".*/register(/|$).*",
    r".*/account(/|$).*",
    r".*/profile(/|$).*",
    r".*/admin(/|$).*",

    # Legal / Static
    r".*/privacy(-policy)?(/|$).*",
    r".*/terms(-of-service)?(/|$).*",
    r".*/license(/|$).*",
    r".*/cookies?(/|$).*",

    # Pagination
    r".*/page/\d+(/|$).*",

    # Print / Download views
    r".*/print(/|$).*",
    r".*/download(/|$).*",

    # Non-HTML / Static Assets
    r".*\.(png|jpg|jpeg|gif|svg|webp)$",
    r".*\.(css|js|map)$",
    r".*\.(zip|tar|gz|rar)$",
    r".*\.(xml|rss)$",
]


def is_allowed_url(url:str, base_domain:str, include_patterns: list[str] | None = None, exclude_patterns: list[str] | None = None,) -> bool:
    """
    Determines whether a URL should be crawled.

    Rules:
    1. Must belong to the same domain.
    2. Must not match internal exclusion patterns.
    3. Must not match user-provided exclude_patterns.
    4. If include_patterns provided, must match at least one.
    5. Ignore anchor-only links.
    """

    parsed = urlparse(url)

    # domain restriction
    if parsed.netloc != base_domain:
        return False
    
    # Ignore anchor-only links
    if parsed.fragment:
        return False
    
    # Internal exclusion rules
    for pattern in exclude_regex:
        if pattern.match(url):
            return False
        
    # User-provided exclude patterns
    if exclude_patterns:
        for pattern in exclude_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return False
            
    # Include filtering (if provided)
    if include_patterns:
        allowed = any(
            re.search(pattern, url, re.IGNORECASE)
            for pattern in include_patterns
        )
        if not allowed:
            return False
        
    return True



ALLOWED_PREFIXES = [
    "/oss/python/langchain/"
]

EXCLUDE_PATTERNS_SITEMAP = [
    r".*\?.*",
    r".*/search.*",
    r".*/tag/.*",

    # Search / Query Pages
    r".*/search(/|$).*",
    r".*/results(/|$).*",

    # Blog / News / Marketing
    r".*/blog(/|$).*",
    r".*/news(/|$).*",
    r".*/changelog(/|$).*",
    r".*/release(-|_)?notes(/|$).*",
    r".*/announcements(/|$).*",

    # Auth / Account
    r".*/login(/|$).*",
    r".*/logout(/|$).*",
    r".*/signup(/|$).*",
    r".*/register(/|$).*",
    r".*/account(/|$).*",
    r".*/profile(/|$).*",
    r".*/admin(/|$).*",

    # Legal / Static
    r".*/privacy(-policy)?(/|$).*",
    r".*/terms(-of-service)?(/|$).*",
    r".*/license(/|$).*",
    r".*/cookies?(/|$).*",

    # Pagination
    r".*/page/\d+(/|$).*",

    # Print / Download views
    r".*/print(/|$).*",
    r".*/download(/|$).*",

    # Non-HTML / Static Assets
    r".*\.(png|jpg|jpeg|gif|svg|webp)$",
    r".*\.(css|js|map)$",
    r".*\.(zip|tar|gz|rar)$",
    r".*\.(xml|rss)$",
]

# Precompile regex 
exclude_regex = [re.compile(pattern, re.IGNORECASE) for pattern in EXCLUDE_PATTERNS]

include_regex = [re.compile(pattern, re.IGNORECASE) for pattern in ALLOWED_PREFIXES]


def is_allowed_url_sitemap(url:str) -> bool:
    parsed = urlparse(url)

    path = parsed.path

    # Must match allowed prefixes
    if not any(path.startswith(prefix) for prefix in ALLOWED_PREFIXES):
        return False
    
    # Exclude unwanted patterns
    for pattern in EXCLUDE_PATTERNS_SITEMAP:
        if re.match(pattern, url):
            return False
        

    return True