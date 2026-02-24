# from src.ingestion.crawling.crawler import Crawler

# if __name__ == "__main__":
#     start_url = "https://docs.langchain.com"

#     crawler = Crawler(
#         start_url= start_url,
#         max_pages=50,
#         max_depth=2
#     )
#     for url, html in crawler.crawl():
#         print("=" * 100)
#         print("URL: ", url)
#         print("HTML LENGTH: ", len(html))
#         print('Total Visited: ', len(crawler.visited))

from requests import Session

from src.ingestion.extractor.title_extractor import exctract_title
from src.ingestion.extractor.content_extractor import extract_main_content
from src.ingestion.extractor.html_fetcher import fetch_html
from src.ingestion.processor.chunker import chunk_documents
from src.ingestion.processor.deduplicator import deduplicate_chunks
from src.ingestion.processor.document_builder import build_document


def test_extractor():
    url = "https://docs.langchain.com/oss/python/langchain/quickstart"
    
    session = Session()

    print('fetching html...')
    html = fetch_html(url, session=session)

    if not html:
        print("Failed to fetch HTML content.")
        return
    
    print("Extracting title...")
    title = exctract_title(html)

    print("Extracting content...")
    content = extract_main_content(html)

    print("\n" + "=" * 80)
    print("TITLE:\n", title)
    print("=" * 80)

    text = []
    if content:
        print("\n" + "=" * 80)
        print("CONTENT PREVIEW:\n")
        print(content[:150])
        print("=" * 80)
        text.append(content)
    else:
        print("No content extracted.")

    documents = []
    for document in text:
        safe_title = title or 'Unown title'
        document = build_document(url, document, safe_title, 'quickstart')
        documents.append(document)
    
    print("\n" + "=" * 80)
    print(f'Documents are {documents}')
    print("=" * 80)

    chunked_docs = chunk_documents(documents)
    print("\n" + "=" * 80)

    print(f'Chunked Documents are {chunked_docs}')
    print("=" * 80)
    print(f"Total Chunks: {len(chunked_docs)}")

if __name__ == "__main__":
    test_extractor()