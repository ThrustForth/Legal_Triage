"""Legal triage system for legal aid callers.

Uses semantic search (LanceDB + Ollama embeddings) to help callers find legal info
for eviction, divorce, custody, debt, etc."

import lancedb
import ollama
import sys
from pathlib import Path
from bs4 import BeautifulSoup
import re
import os

# Import process guide handler
from process_guide_handler import get_process_guide
from process_guides import PROCESS_GUIDES, guide_to_search_text, format_guide_for_display

# Get the project root
PROJECT_ROOT = Path(__file__).parent.parent
db = lancedb.connect(str(PROJECT_ROOT / "db"))
legal_dir = PROJECT_ROOT / "data"  # Search all HTML files under data/

def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove non-content elements
    for element in soup(['script', 'style', 'noscript', 'meta', 'link', 'head', 'iframe']):
        element.decompose()

    # Get main content
    content_div = soup.find('div', class_='entry-content')
    if content_div:
        text = content_div.get_text()
    else:
        text = soup.body.get_text() if soup.body else soup.get_text()

    # Clean whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text
def index_legal_docs():
    """Index all legal documents AND process guides into LanceDB""
    docs = []

    # 1. Process ALL HTML files under data/ (including subdirectories)
    for html_file in legal_dir.rglob("*.html"):
        content = html_file.read_text(encoding='utf-8')
        clean_text = extract_text_from_html(content)
        docs.append({"text": clean_text, "path": str(html_file), "type": "html"})

    # 2. Process process guides
    for guide in PROCESS_GUIDES:
        search_text = guide_to_search_text(guide)
        docs.append({
            "text": search_text,
            "path": f"process_guide:{guide['topic']}",
            "type": guide['type']  # Mark as guide for special handling
        })

    print(f"Found {len(docs)} total documents ({len([d for d in docs if d['type'] == 'html'])} HTML + {len(PROCESS_GUIDES)} guides)")

    if docs:
        print(f"Getting embeddings for {len(docs)} documents...")
        for i, doc in enumerate(docs):
            resp = ollama.embed(model="nomic-embed-text", input=[doc["text"]])
            doc["vector"] = resp["embeddings"][0]
            print(f"Embedded {i+1}/{len(docs)}: {doc['path']}")

        table = db.create_table("legal_docs", data=docs, mode="overwrite")
        print(f"\n Indexed {len(docs)} documents")
    else:
        print("No documents!")
        print("No documents!")

def search_legal_docs(query, top_k=5):
    """Search LanceDB and prioritize process guides"
    table = db.open_table("legal_docs")

    # Embed query
    resp = ollama.embed(model="nomic-embed-text", input=[query])
    query_embedding = resp["embeddings"][0]

    # Search LanceDB
    results = table.search(query_embedding).limit(top_k).to_pandas()

    # Format and prioritize results
    formatted_results = []
    for _, row in results.iterrows():
        # Check if this is a guide
        if row['type'] == 'process_guide':
            # Format guide for display
            display_text = format_guide_for_display(row)
            formatted_results.insert(0, (
                row['path'],
                display_text,
                row['_distance']
            ))
        else:
            # Regular document
            formatted_results.append(
                (row['path'], row['text'][:500], row['_distance'])
            )

    print(f"\nFound {len(formatted_results)} results:\n")
    for path, content, distance in formatted_results:
        if path.startswith('process_guide:'):
            topic = path.split(':')[1]
            print(f"\n PROCESS GUIDE: {PROCESS_GUIDES[0]['title']} (Topic: {topic})\n")
        else:
            print(f"{Path(path).name}")
        print(f"   {content}...")
        print(f"   Distance: {distance}\n")

if len(sys.argv) > 1:
    search_legal_docs(" ".join(sys.argv[1:]))
else:
    index_legal_docs()
