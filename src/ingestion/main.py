from src.ingestion.crawling.crawler import Crawler

if __name__ == "__main__":
    start_url = "https://docs.langchain.com"

    crawler = Crawler(
        start_url= start_url,
        max_pages=50,
        max_depth=2
    )
    for url, html in crawler.crawl():
        print("=" * 100)
        print("URL: ", url)
        print("HTML LENGTH: ", len(html))
        print('Total Visited: ', len(crawler.visited))