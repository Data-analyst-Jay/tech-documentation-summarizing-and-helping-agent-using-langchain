import hashlib

_seen_hashes = set()

def is_duplicate(text: str) -> bool:
    """
    Checks whether a given text content has already been processed.
    
    Uses SHA-256 hashing on normalized text to detect duplicates.
    """
    if not text or not text.strip():
        return True  # empty content treated as duplicate
    
    # Normalize text
    normalized = " ".join(text.split()).lower()

    # Create hash
    text_hash = hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    if text_hash in _seen_hashes:
        return True

    _seen_hashes.add(text_hash)
    return False