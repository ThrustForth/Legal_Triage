# Legal Triage System

A semantic search system for legal aid documents using LanceDB and Ollama.

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Ollama (if not running)
ollama pull nomic-embed-text

# Index legal documents
python src/legal_triage.py

# Search
python src/legal_triage.py "eviction"
```

## Structure

- `src/` - Python scripts
- `data/` - Legal document HTML files
- `db/` - LanceDB index (generated)
- `docs/` - Documentation

## Dependencies

- LanceDB
- Ollama (with nomic-embed-text model)
- BeautifulSoup4
- Requests
- pandas

cd ~/projects/legal_triage
./venv/bin/pip install -r requirements.txt
./venv/bin/python src/legal_triage.py  # Index documents

Use it:

bash
./venv/bin/python src/legal_triage.py "eviction help"
./venv/bin/python src/legal_triage.py "custody divorce"
./venv/bin/python src/legal_triage.py "identity theft"

Add more legal pages:

bash
./venv/bin/python src/scrape_legal.py  # Scrape more pages
./venv/bin/python src/legal_triage.py  # Re-index

Port to another system:

bash
tar -czf legal_triage.tar.gz src data db README.md requirements.txt venv
