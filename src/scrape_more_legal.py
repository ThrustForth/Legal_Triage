import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time

# Create directory for expanded legal docs
legal_dir = Path("/home/mine/projects/legal_triage/data/")

# Illinois Legal Aid Online pages to scrape
illinois_pages = [
    ("https://www.illinoislegalaid.org/legal-information/eviction", "eviction-illinois.html"),
    ("https://www.illinoislegalaid.org/legal-information/rental-assistance", "rental-assistance.html"),
    ("https://www.illinoislegalaid.org/legal-information/divorce", "divorce-illinois.html"),
    ("https://www.illinoislegalaid.org/legal-information/child-custody", "custody-illinois.html"),
    ("https://www.illinoislegalaid.org/legal-information/domestic-violence", "domestic-violence.html"),
    ("https://www.illinoislegalaid.org/legal-information/debt-collection", "debt-collection.html"),
    ("https://www.illinoislegalaid.org/legal-information/identity-theft", "identity-theft.html"),
    ("https://www.illinoislegalaid.org/legal-information/unemployment", "unemployment.html"),
    ("https://www.ilga.gov/legislation/ILCS/ilcs3.asp?ActID=1876", "eviction-law-ILCS.html"),
    ("https://www.ilga.gov/legislation/ILCS/ilcs3.asp?ActID=1027", "family-law-ILCS.html"),  # Family Law
]

# National resources
national_pages = [
    ("https://www.consumerfinance.gov/housing/housing-insecurity/help-for-renters/what-to-do-if-youre-facing-eviction/", "eviction-federal.html"),
    ("https://www.lawhelp.org/resource/rent-and-eviction-help-resources", "eviction-lawhelp.html"),
]

def scrape_page(url, filename):
    """Scrape a single page with better content extraction"""
    try:
        print(f"Scraping: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        # Extract main content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try different content selectors
        content = None
        for selector in [
            soup.find('div', class_='legal-information-content'),
            soup.find('article'),
            soup.find('div', class_='content'),
            soup.find('main'),
            soup.body
        ]:
            if selector:
                content = selector
                break

        if content:
            # Remove scripts and styles
            for element in content(['script', 'style', 'noscript']):
                element.decompose()
            text = content.get_text()

            # Save clean HTML
            filepath = legal_dir / filename
            filepath.write_text(f"<div class='entry-content'>{text}</div>", encoding='utf-8')
            print(f"  ✅ Saved: {filename}")
            return True
        else:
            print(f"  ❌ No content found")
            return False

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

# Scrape Illinois pages
print("Scraping Illinois Legal Aid Online...\n")
for url, filename in illinois_pages:
    scrape_page(url, filename)
    time.sleep(2)

# Scrape national pages
print("\nScraping national resources...\n")
for url, filename in national_pages:
    scrape_page(url, filename)
    time.sleep(2)

print(f"\n✅ Done! Files in: {legal_dir}")
print(f"Total HTML files: {len(list(legal_dir.glob('*.html')))}")
