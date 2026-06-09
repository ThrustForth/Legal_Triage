content = '''"""
Results display components
"""
import streamlit as st

def show_eligibility_result(eligibility_data):
    """Display eligibility screening results"""

    if eligibility_data['eligible']:
        st.success("✅ Eligible: YES")
        st.markdown("**PASSED ALL CRITERIA**")

        priority_num = eligibility_data['priority_level']
        priority_desc = eligibility_data['priority_description']

        st.info(f"**Priority Level:** {priority_num} - {priority_desc}")

        # Show criteria passed
        with st.expander("Criteria Breakdown"):
            for criterion, passed in eligibility_data['criteria'].items():
                if passed:
                    st.success(f"✓ {criterion.capitalize()} Eligible")
                else:
                    st.error(f"✗ {criterion.capitalize()} Not Eligible")

    else:
        st.error("❌ Eligible: NO")
        st.markdown("**DID NOT MEET ALL REQUIREMENTS**")

        # Show which criteria failed
        with st.expander("Criteria Breakdown"):
            if not eligibility_data['criteria']['income']:
                st.error(f"✗ Income exceeds maximum (${eligibility_data['income_max']})")
            if not eligibility_data['criteria']['issue']:
                st.error("✗ Legal issue not supported")
            if not eligibility_data['criteria']['geographic']:
                st.error("✗ Geographic area not served")

        # Referral info
        st.warning("""
        **Referral Information:**

        Client may need to be referred to other legal services
        that specialize in their specific needs.
        """)

def show_process_guide(guide):
    """Display process guide in formatted markdown"""
    if not guide:
        st.markdown("None")
        return

    title = guide.get('title', 'Process Guide')
    timeline = guide.get('timeline', '')
    forms = guide.get('forms', [])
    steps = guide.get('steps', [])
    notes = guide.get('notes', '')

    markdown = f"**{title}**\n\n"

    if timeline:
        markdown += f"**Timeline:** {timeline}\n\n"

    if forms:
        markdown += f"**Forms needed:** {', '.join(forms)}\n\n"

    if steps:
        markdown += "**Steps:**\n\n"
        for i, step in enumerate(steps, 1):
            markdown += f"{i}. {step}\n\n"

    if notes:
        markdown += f"**Important notes:**\n • {notes}\n\n"

    markdown += "For detailed legal assistance, please contact a qualified attorney."

    st.markdown(markdown)

def show_search_results(results):
    """Display search results"""
    if not results:
        st.markdown("None")
        return

    if results.get('type') == 'error':
        st.error(results.get('message', 'Search error'))
        return

    documents = results.get('documents', [])

    if not documents:
        st.markdown("No documents found")
        return

    st.markdown(f"Found {len(documents)} documents:\n")

    for i, doc in enumerate(documents, 1):
        name = doc.get('name', 'Unknown')
        snippet = doc.get('snippet', '')
        distance = doc.get('distance', 0)

        filename = name.split('/')[-1] if '/' in name else name

        st.markdown(f"**{i}. {filename}**")
        if snippet:
            st.markdown(f"  {snippet}...")
        st.markdown(f"  Distance: {distance}\n")
'''

with open('components/results.py', 'w') as f:
    f.write(content)

print("Updated components/results.py!")
