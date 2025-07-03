import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
import re

# Config
base_url = 'https://attack.mitre.org/'
output_dir = 'scraped_pages'
os.makedirs(output_dir, exist_ok=True)

visited_urls = set()

def is_valid_url(url):
    """Check if URL is part of the target domain and not a file."""
    parsed = urlparse(url)
    if parsed.netloc != urlparse(base_url).netloc:
        return False
    if any(parsed.path.endswith(ext) for ext in ['.pdf', '.jpg', '.png', '.zip']):
        return False
    return True

def generate_filename(url):
    """Convert URL path to a safe filename."""
    parsed = urlparse(url)
    path = unquote(parsed.path)
    if not path or path == '/':
        return 'index.txt'
    filename = path.strip('/').replace('/', '_')
    return f"{filename}.txt" if filename else 'index.txt'

def clean_text(soup):
    """Extract text while preserving line breaks and structure."""
    for element in soup(["script", "style", "nav", "footer", "head", "iframe"]):
        element.decompose()
    for br in soup.find_all("br"):
        br.replace_with("\n")
    for block in soup.find_all(["div", "p", "li"]):
        if block.name == "li":
            block.insert_before("\n- ")
        block.append("\n\n")
    text = soup.get_text()
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

def scrape_page(url):
    """Scrape a page if not already visited."""
    parsed = urlparse(url)
    normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    if normalized_url in visited_urls or not is_valid_url(normalized_url):
        return
    visited_urls.add(normalized_url)

    try:
        response = requests.get(url, timeout=10)
        if not response.ok or not response.headers.get('Content-Type', '').startswith('text/html'):
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        main_content = soup.find('main') or soup.find('article') or soup.find('body')
        if not main_content:
            return

        cleaned_text = clean_text(main_content)
        filename = generate_filename(normalized_url)
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        print(f"Saved: {filepath}")

        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(base_url, href)
            scrape_page(absolute_url)

    except Exception as e:
        print(f"Error scraping {url}: {e}")

# Start crawling
scrape_page(base_url)
print(f"Done! Scraped {len(visited_urls)} pages.")