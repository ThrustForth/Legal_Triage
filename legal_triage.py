import lancedb
import ollama
import sys
from pathlib import Path
from bs4 import BeautifulSoup
import re

# Get the project root (parent of src directory)
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

def search_legal_docs(query, top_k=5):
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

if len(sys.argv) > 1:
    search_legal_docs(" ".join(sys.argv[1:]))
else:
    index_legal_docs()
