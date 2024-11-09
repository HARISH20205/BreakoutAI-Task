import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor
import os
from dotenv import load_dotenv

load_dotenv()

class SimpleTextScraper:
    def __init__(self, scraper_api_key):
        self.api_key = scraper_api_key
        self.visited_urls = set()
        self.all_text = {}
    
    def _make_request(self, url, render_js=True):
        api_url = f"http://api.scraperapi.com?api_key={self.api_key}&url={url}&render={str(render_js).lower()}"
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to fetch {url}. Status code: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Error fetching {url}: {str(e)}")
            return None

    def extract_text_content(self, url, depth=0, max_depth=2):
        if depth > max_depth or url in self.visited_urls:
            return
        
        print(f"Processing {url}")
        self.visited_urls.add(url)
        
        content = self._make_request(url)
        if not content:
            return
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Extract text content
        text_content = []
        
        # Get title
        if soup.title:
            text_content.append(f"Page Title: {soup.title.string.strip()}\n")
        
        # Get all text from paragraphs, headers, and other text elements
        for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'span', 'div']):
            text = element.get_text(strip=True)
            if text and len(text) > 1:  # Ignore single characters or empty strings
                text_content.append(text)
        
        # Store unique text content for this URL
        self.all_text[url] = list(dict.fromkeys(text_content))  # Remove duplicates while preserving order
        
        # Find internal links for further processing
        base_domain = urlparse(url).netloc
        internal_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/'):
                href = urljoin(url, href)
            if base_domain in href and href not in self.visited_urls:
                internal_links.append(href)
        
        # Process internal links if not at max depth
        if depth < max_depth:
            with ThreadPoolExecutor(max_workers=5) as executor:
                executor.map(lambda link: self.extract_text_content(link, depth + 1, max_depth), internal_links)

    def save_text_content(self, filename='website_content.txt'):
        with open(filename, 'w', encoding='utf-8') as f:
            for url, texts in self.all_text.items():
                f.write(f"\n{'='*50}\n")
                f.write(f"URL: {url}\n")
                f.write(f"{'='*50}\n\n")
                
                for text in texts:
                    if text.strip():  # Only write non-empty lines
                        f.write(f"{text}\n")
                f.write("\n")

def data_scrap(website_url):
    # Replace with your actual ScraperAPI key
    API_KEY = os.getenv("SCRAPER_API_KEY")
    
    if not website_url.startswith(('http://', 'https://')):
        website_url = 'https://' + website_url
    
    scraper = SimpleTextScraper(API_KEY)
    
    try:
        print(f"Starting to scrape text content from {website_url}")
        scraper.extract_text_content(website_url, max_depth=2)
        
        # Save to file
        scraper.save_text_content()
        
        print("\nScraping completed!")
        print(f"Total pages scraped: {len(scraper.all_text)}")
        print("Text content has been saved to 'website_content.txt'")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
