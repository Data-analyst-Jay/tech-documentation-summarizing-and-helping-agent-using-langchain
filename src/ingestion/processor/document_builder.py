from langchain_core.documents import Document

def build_document(url: str, text: str, title: str, domain: str) -> Document:
    """
    Builds a LangChain Document object from extracted data.
    """
    metadata = {
        "source": url,
        "url": url,
        "title": title,
        "domain": domain,
        "content_length": len(text)
    }

    return Document(
        page_content=text,
        metadata=metadata
    )