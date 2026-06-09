from process_guide_templates import templates

def get_guide(query):
    """Match query to template topic (eviction, divorce, custody, debt collection, identity theft)"""
    query_lower = query.lower()
    topic_mappings = {
        'eviction': ['eviction', 'rent', 'tenant', 'sheriff'],
        'divorce': ['divorce', 'marriage', 'spouse', 'dissolution'],
        'custody': ['custody', 'child', 'parent', 'allocation'],
        'debt collection': ['debt', 'collection', 'creditor'],
        'identity theft': ['identity theft', 'fraud', 'stolen']
    }
    for topic, keywords in topic_mappings.items():
        if any(keyword in query_lower for keyword in keywords):
            return templates.get(topic)
    return None


def format_guide(template):
    """Format template as a nicely-formatted string with numbered steps, deadlines, forms"""
    if not template:
        return None
    output = []
    output.append(f"## {template['title']}")
    output.append(f"\n**Timeline:** {template['timeline']}")
    output.append(f"**Forms needed:** {', '.join(template['forms'])}")
    output.append("\n**Steps:**\n")

    for i, step in enumerate(template['steps'], 1):
        # Handle both string steps and dict steps
        if isinstance(step, dict):
            output.append(f"{i}. **{step['title']}**")
            output.append(f"   {step['description']}")
            if step.get('deadline'):
                output.append(f"   **Deadline:** {step['deadline']}")
        else:
            output.append(f"{i}. {step}")
        output.append("")

    if template.get('notes'):
        output.append("\n**Important notes:**")
        notes = template['notes']
        if isinstance(notes, list):
            for note in notes:
                output.append(f"  • {note}")
        else:
            output.append(f"  • {notes}")

    return '\n'.join(output)
