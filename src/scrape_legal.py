import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time

# Create directory for legal docs
legal_dir = Path("/home/mine/projects/legal_aid/site_spider/legal_docs/lincolnlegal.org/")
legal_dir.mkdir(parents=True, exist_ok=True)

# Pages to scrape
pages = [
    ("https://lincolnlegal.org/housing-law/", "housing-law.html"),
    ("https://lincolnlegal.org/family-law/", "family-law.html"),
    ("https://lincolnlegal.org/consumer-law/", "consumer-law.html"),
    ("https://lincolnlegal.org/", "index.html"),
    ("https://lincolnlegal.org/contact-us/", "contact-us.html"),
]

# Also try education law
education_urls = [
    "https://lincolnlegal.org/education-law/",
    "https://lincolnlegal.org/our-services/",
    "https://lincolnlegal.org/about-us/",
]

def scrape_page(url, filename):
    """Scrape a single page"""
    try:
        print(f"Scraping: {url}")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Save HTML
        filepath = legal_dir / filename
        filepath.write_text(response.text, encoding='utf-8')
        print(f"  ✅ Saved: {filename}")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

# Scrape main pages
print("Scraping legal aid pages...\n")
for url, filename in pages:
    scrape_page(url, filename)
    time.sleep(1)  # Be nice to the server

# Try education and other pages
print("\nTrying additional pages...")
for url in education_urls:
    filename = url.split('/')[-2] + ".html"
    scrape_page(url, filename)
    time.sleep(1)

print(f"\n✅ Done! Saved to: {legal_dir}")
print(f"Files: {list(legal_dir.glob('*.html'))}")
