"""
Legal Triage System - Streamlit Frontend
Main entry point for the web application
"""
import streamlit as st
import sys
import os

# Add backend to path (go up one level from frontend to find backend)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from components.intake_form import show_intake_form
from components.results import show_eligibility_result, show_process_guide, show_search_results
from triage_core import check_eligibility, get_process_guide, search_legal_docs

# App configuration
st.set_page_config(
    page_title="Legal Triage System",
    page_icon="⚖️",
    layout="wide",
)

# App header
st.title("⚖️ Legal Triage System")
st.markdown("""
**Eligibility Screening & Legal Process Guides**

This system helps legal aid organizations screen clients for eligibility
and provides instant access to legal process information.
""")

# Show intake form
form_data = show_intake_form()

# Handle form submission
if form_data['submitted']:
    # Validate required fields
    if not form_data['name'] or not form_data['county']:
        st.error("Please fill in Name and County")
        st.stop()

    # Check eligibility

    eligibility = check_eligibility(
        name=form_data['name'],
        income=form_data['income'],
        household=form_data['household'],
        issue=form_data['issue'],
        county=form_data['county']
    )

    # Display results
    st.divider()
    st.header("Screening Results")
    show_eligibility_result(eligibility)

    # If eligible, show process guide and search
    if eligibility['eligible']:
        st.divider()
        st.header("Process Guide")

        guide = get_process_guide(form_data['issue'])
        show_process_guide(guide)

        # Show search if query provided
        if form_data['search_query']:
            st.divider()
            st.header(f"Search: {form_data['search_query']}")

            results = search_legal_docs(form_data['search_query'])
            show_search_results(results)

# Footer
st.divider()
st.markdown("""
**Legal Triage System** | Built for Legal Aid Organizations
*For detailed legal assistance, please contact a qualified attorney.*
""")
