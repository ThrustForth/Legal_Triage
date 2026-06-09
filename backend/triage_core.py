"""
Core legal triage functions - extracted from CLI for web app use
"""
import os
import sys
import pandas as pd

# Income eligibility threshold (can be adjusted)
INCOME_THRESHOLD = 32275

# Supported legal issues
SUPPORTED_ISSUES = ["eviction", "divorce", "custody", "benefits"]

# Priority levels
PRIORITY_MAP = {
    'eviction': (1, 'Critical'),
    'benefits': (1, 'Critical'),
    'divorce': (2, 'High'),
    'custody': (2, 'High'),
}

def check_eligibility(name, income, household, issue, county):
    """
    Check client eligibility for legal aid.
    Returns dict with eligibility status, priority, and criteria breakdown.
    """
    criteria = {
        'income': False,
        'issue': False,
        'geographic': False,
    }

    income_max = INCOME_THRESHOLD
    if income <= income_max:
        criteria['income'] = True

    if issue in SUPPORTED_ISSUES:
        criteria['issue'] = True

    # Basic geographic check (can be expanded)
    if county and len(county) > 0:
        criteria['geographic'] = True

    all_passed = all(criteria.values())

    # Determine priority
    if all_passed:
        priority_num, priority_desc = PRIORITY_MAP.get(issue, (3, 'Normal'))
    else:
        priority_num, priority_desc = (None, None)

    return {
        'eligible': all_passed,
        'name': name,
        'priority_level': priority_num,
        'priority_description': priority_desc,
        'criteria': criteria,
        'income_max': income_max,
    }

def search_legal_docs(query, top_k=5):
    """
    Search indexed legal documents for the given query.
    Returns formatted result dict with documents list.
    """
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
        from legal_triage import db, legal_dir
        from process_guide_handler import get_guide
        import ollama

        # Check if query is asking for a process guide
        guide = get_guide(query)
        if guide:
            return {'type': 'guide', 'guide': guide}

        # Proceed with regular semantic search
        table = db.open_table("legal_docs")

        resp = ollama.embed(model="nomic-embed-text", input=[query])
        query_embedding = resp["embeddings"][0]

        results = table.search(query_embedding).limit(top_k).to_pandas()

        documents = []
        for i, row in results.iterrows():
            snippet = row['text'][:500]
            documents.append({
                'name': str(row['path']),
                'snippet': snippet,
                'distance': row['_distance']
            })

        return {'type': 'search', 'documents': documents}

    except Exception as e:
        return {'type': 'error', 'message': f'Search not available: {str(e)}'}

def get_process_guide(issue):
    """
    Get process guide for a specific legal issue.
    Returns formatted guide dict.
    """
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
        from process_guide_handler import get_guide, format_guide

        guide = get_guide(f"{issue} process")
        if guide:
            return guide
        return None

    except:
        return None
