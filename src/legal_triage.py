import lancedb
import ollama
import sys
from pathlib import Path
from bs4 import BeautifulSoup
import re
import os
import argparse
from process_guide_handler import get_guide, format_guide
from eligibility_screening import screen_client, print_screening_result

# Get the project root (parent directory of src)
PROJECT_ROOT = Path(__file__).parent.parent
db = lancedb.connect(str(PROJECT_ROOT / "db"))
legal_dir = PROJECT_ROOT / "data" / "lincolnlegal.org"

def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    for element in soup(['script', 'style', 'noscript', 'meta', 'link', 'head', 'iframe']):
        element.decompose()

    content_div = soup.find('div', class_='entry-content')
    if content_div:
        text = content_div.get_text()
    else:
        text = soup.body.get_text() if soup.body else soup.get_text()

    text = re.sub(r'\s+', ' ', text).strip()
    return text

def index_legal_docs():
    docs = []
    for html_file in legal_dir.rglob("*.html"):
        content = html_file.read_text(encoding='utf-8')
        clean_text = extract_text_from_html(content)
        docs.append({"text": clean_text, "path": str(html_file)})

    print(f"Found {len(docs)} HTML files")

    if docs:
        print(f"Getting embeddings for {len(docs)} documents...")
        for i, doc in enumerate(docs):
            resp = ollama.embed(model="nomic-embed-text", input=[doc["text"]])
            doc["vector"] = resp["embeddings"][0]
            print(f"Embedded {i+1}/{len(docs)}: {Path(doc['path']).name}")

        table = db.create_table("legal_docs", data=docs, mode="overwrite")
        print(f"\n✅ Indexed {len(docs)} documents")
    else:
        print("No documents!")

def show_process_guide(query, guide):
    """Format and display a process guide based on the query"""
    if guide:
        print(f"\n=== {guide['title']} ===\n")
        formatted_guide = format_guide(guide)
        if formatted_guide:
            print(formatted_guide)
        print("\nFor detailed legal assistance, please contact a qualified attorney.")
    else:
        print(f"\nSorry, I couldn't find a guide for '{query}'.")
        print("Try searching for terms like: eviction, divorce, custody, debt collection, or identity theft.")

def search_legal_docs(query, top_k=5):
    # Check if query is asking for a process guide
    guide = get_guide(query)
    if guide:
        show_process_guide(query, guide)
        return
    
    # Otherwise proceed with regular semantic search
    table = db.open_table("legal_docs")

    resp = ollama.embed(model="nomic-embed-text", input=[query])
    query_embedding = resp["embeddings"][0]

    results = table.search(query_embedding).limit(top_k).to_pandas()

    print(f"\nFound {len(results)} documents:\n")
    for i, row in results.iterrows():
        snippet = row['text'][:500]
        print(f"{i+1}. {Path(row['path']).name}")
        print(f"   {snippet}...")
        print(f"   Distance: {row['_distance']}\n")

def main():
    parser = argparse.ArgumentParser(description='Legal Triage System')
    parser.add_argument('--screen', action='store_true', help='Run eligibility screening')
    parser.add_argument('--name', type=str, help='Client name')
    parser.add_argument('--income', type=float, help='Annual income')
    parser.add_argument('--household', type=int, help='Household size')
    parser.add_argument('--issue', type=str, help='Legal issue')
    parser.add_argument('--county', type=str, help='County')
    parser.add_argument('--search', type=str, help='Search query (optional, after screening)')
    parser.add_argument('query', nargs='?', type=str, help='Search query (positional)')
    
    args = parser.parse_args()
    
    if args.screen:
        # Require screening arguments
        if not all([args.name, args.income is not None, args.household, args.issue, args.county]):
            parser.error("--screen requires --name, --income, --household, --issue, and --county")
        
        result = screen_client(args.name, args.income, args.household, args.issue, args.county)
        print_screening_result(result)
        
        if result['eligible']:
            print("\n" + "="*50)
            print("PROCESS GUIDE AND SEARCH RESULTS")
            print("="*50)
            
            # Show process guide if issue matches
            guide = get_guide(args.issue)
            if guide:
                show_process_guide(args.issue, guide)
            
            # Always do semantic search if --search provided
            if args.search:
                print("\n" + "="*50)
                print(f"SEARCH RESULTS FOR: {args.search}")
                print("="*50)
                search_legal_docs(args.search)
        
    else:
        # Original behavior: treat all args as search query
        if len(sys.argv) > 1:
            search_query = " ".join(sys.argv[1:])
            search_legal_docs(search_query)
        else:
            index_legal_docs()

if __name__ == "__main__":
    main()
