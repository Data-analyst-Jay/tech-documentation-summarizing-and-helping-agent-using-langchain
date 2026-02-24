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

    if content:
        print("CONTENT PREVIEW:\n")
        print(content[:1500])
    else:
        print("No content extracted.")


if __name__ == "__main__":
    test_extractor()