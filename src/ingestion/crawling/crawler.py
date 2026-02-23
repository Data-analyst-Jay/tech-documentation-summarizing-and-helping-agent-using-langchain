from urllib import response

import requests
from collections import deque
from urllib.parse import urlparse, urljoin
from xml.etree import ElementTree

from src.ingestion.crawling.link_utils import extract_links
from src.ingestion.crawling.url_filters import is_allowed_url, is_allowed_url_sitemap

class Crawler:
    '''Sitemap-first crawler with BFS fallback based document crawling'''

    def __init__(self, start_url: str, max_pages: int = 50, max_depth: int = 3):
        self.start_url = start_url
        self.max_pages = max_pages
        self.max_depth = max_depth

        self.visited = set()
        self.session = requests.Session()

    def get_sitemap_urls(self):
        parsed = urlparse(self.start_url)
        base = f"{parsed.scheme}://{parsed.netloc}"

        sitemap_url = urljoin(base, "sitemap.xml")

        try:
            response = self.session.get(sitemap_url, timeout=10)
            response.raise_for_status()

            # if "xml" not in response.headers.get("Content-Type", ""):
            #     return
            
            root = ElementTree.fromstring(response.content)

            urls = []

            for elem in root.iter():
                if elem.tag.endswith("loc") and elem.text:
                    urls.append(elem.text.strip())

            print("Sitemap status:", response.status_code)
            print("Content-Type:", response.headers.get("Content-Type"))
            return urls
        
        except Exception:
            return
    
    def fetch_page(self, url: str) -> str | None:
        """
        Fetch HTML content safely.
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                return None

            return response.text

        except requests.RequestException:
            return None
        
    def crawl(self):
        '''Generator that yields (url, html) for each crawled page.'''
        # Try sitemap first
        sitemap_urls = self.get_sitemap_urls()
        candidates_checked = 0

        if sitemap_urls:
            print("Using sitemap for ingestion...")
            print(f"Total URLs in sitemap: {len(sitemap_urls)}")
            for url in sitemap_urls:
                if len(self.visited) >= self.max_pages:
                    break

                # candidates_checked += 1
                # if candidates_checked > self.max_pages * 20:
                #     break

                if not is_allowed_url_sitemap(url):
                    # print("Not allowed")
                    continue

                html = self.fetch_page(url)
                if not html:
                    continue

                self.visited.add(url)
                yield url, html
            return

        print("No sitemap found. Falling back to BFS crawling.....")

        queue = deque([(self.start_url, 0)]) # (url, depth)

        while queue and len(self.visited) < self.max_pages:
            current_url, depth = queue.popleft()

            if current_url in self.visited:
                continue

            if depth > self.max_depth:
                continue

            html = self.fetch_page(current_url)
            if not html:
                continue

            self.visited.add(current_url)

            yield current_url, html

            # Extract and enqueue new links
            links = extract_links(html, current_url) 

            for link in links:
                if link not in self.visited:
                    queue.append((link, depth + 1))

        
        # print('Extracted_links: ', len(links))