"""
Intake form component for client information
"""
import streamlit as st

def show_intake_form():
    """Display the client intake form"""
    with st.form("client_intake", clear_on_submit=False):
        st.header("Client Information")

        # Basic info
        name = st.text_input("Full Name", placeholder="e.g., Jane Doe")

        # Numeric inputs
        income = st.number_input(
            "Annual Income ($)",
            min_value=0,
            max_value=200000,
            step=1000,
            placeholder="25000"
        )

        household = st.number_input(
            "Household Size",
            min_value=1,
            max_value=20,
            step=1,
            value=3
        )

        # Dropdowns and text
        county = st.text_input(
            "County",
            placeholder="e.g., Cook County"
        )

        issue = st.selectbox(
            "Legal Issue",
            options=["eviction", "divorce", "custody", "benefits"],
            help="Select the type of legal issue"
        )

        search_query = st.text_area(
            "Optional: What would you like to know?",
            placeholder="e.g., eviction process timeline",
            help="Ask a specific question about your legal issue"
        )

        submitted = st.form_submit_button("Check Eligibility", type="primary")

    return {
        'name': name,
        'income': income,
        'household': household,
        'county': county,
        'issue': issue,
        'search_query': search_query,
        'submitted': submitted,
    }
