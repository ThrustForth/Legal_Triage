import streamlit as st
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import ollama
from legal_triage import search_legal_docs
from process_guide_handler import get_guide
from eligibility_screening import screen_client

def is_relevant_legal_query(prompt):
    legal_patterns = ['eviction', 'evicted', 'being evicted', 'landlord', 'tenant', 'housing', 'rent', 'lease', 'court', 'legal aid', 'qualify', 'eligible']
    prompt_lower = prompt.lower()
    return any(p in prompt_lower for p in legal_patterns)

def get_canned_off_topic_response():
    return "I'm a Legal Triage Agent for housing and eviction issues only.\n\nI can help with:\n\nEviction\nHousing rights\nLegal aid\nSearch\n\nWhat's your housing issue?"

def submit_legal_request(user_info, issue_type, description):
    import csv
    import random
    from datetime import datetime
    import os
    request_id = f"REQ-{random.randint(10000, 99999)}"
    csv_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'legal_requests.csv')
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)
    # Write to CSV
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            request_id,
            user_info.get('name', ''),
            user_info.get('income', ''),
            user_info.get('household', ''),
            user_info.get('is_illinois_resident', ''),
            user_info.get('county', ''),
            user_info.get('issue', ''),
            user_info.get('description', ''),
            user_info.get('preferred_contact', ''),
            user_info.get('contact_info', ''),
            user_info.get('priority_level', '')
        ])
    return {"success": True, "message": "Request saved to CSV!", "request_id": request_id}

st.set_page_config(page_title="Legal Triage Agent", layout="wide")
st.title("AI Legal Triage Agent")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! Are you facing eviction or have a landlord issue?"}]
if "conversation_state" not in st.session_state:
    st.session_state.conversation_state = "initial"
if "user_info" not in st.session_state:
    st.session_state.user_info = {}

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.empty()

        if st.session_state.conversation_state == "initial" and not is_relevant_legal_query(prompt):
            agent_response = get_canned_off_topic_response()
        else:
            user_context = ""
            if st.session_state.user_info.get('name'):
                user_context = f"\nName: {st.session_state.user_info['name']}, Income: ${st.session_state.user_info.get('income', 0)}"

            system_prompt = f"You are a Legal Triage Agent. ONLY: 1) Eviction, 2) Housing, 3) Legal aid eligibility. Route eligible users to (855) 601-9474."

            conversation = [{"role": "system", "content": system_prompt}]
            conversation.extend([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-3:]])

            resp = ollama.chat(model="llama3.2:3b", messages=conversation, options={"temperature": 0.3})
            agent_response = resp["message"]["content"]

            state = st.session_state.conversation_state
            prompt_lower = prompt.lower()

            if state == "initial" and any(w in prompt_lower for w in ['eviction', 'evicted', 'being evicted', 'help', 'qualify']):
                st.session_state.conversation_state = "collecting_name"
                agent_response = "Great! Let me check if you qualify. What's your name?"

            elif state == "collecting_name":
                st.session_state.user_info['name'] = prompt
                st.session_state.conversation_state = "collecting_income"
                agent_response = "What's your annual income? (e.g., 30000)"

            elif state == "collecting_income":
                try:
                    st.session_state.user_info['income'] = float(prompt.replace('$', '').replace(',', ''))
                    st.session_state.conversation_state = "collecting_household"
                    agent_response = "How many people in your household?"
                except:
                    agent_response = "Enter income as a number"

            elif state == "collecting_household":
                try:
                    st.session_state.user_info['household'] = int(prompt)
                    st.session_state.conversation_state = "collecting_residency"
                    agent_response = "Are you an Illinois resident? (yes/no)"
                except:
                    agent_response = "Enter number of people"

            elif state == "collecting_residency":
                is_illinois = prompt.lower().strip() in ['yes', 'illinois', 'il', 'yeah', 'y']
                st.session_state.user_info['county'] = 'Illinois'
                st.session_state.user_info['issue'] = 'eviction'
                st.session_state.user_info['is_illinois_resident'] = is_illinois

                result = screen_client(st.session_state.user_info['name'], st.session_state.user_info['income'], st.session_state.user_info['household'], 'eviction', 'Illinois')

                if result['eligible']:
                    agent_response = f"*Eligible!* Priority: {result['priority_level']}\n\nSubmit a request? Reply *yes* or *no*.\n\nHotline: (855) 601-9474"
                    st.session_state.conversation_state = "waiting_for_submit_decision"
                else:
                    agent_response = "Not eligible. Free resources: illinoislegalaid.org"
                    st.session_state.conversation_state = "initial"

            elif state == "waiting_for_submit_decision":
                if prompt_lower in ['yes', 'y', 'sure', 'ok']:
                    st.session_state.conversation_state = "collecting_description"
                    agent_response = "Describe your issue briefly:"
                elif prompt_lower in ['no', 'n']:
                    agent_response = "Hotline: (855) 601-9474. Any other questions?"
                    st.session_state.conversation_state = "initial"

            elif state == "collecting_description":
                st.session_state.user_info['description'] = prompt
                st.session_state.conversation_state = "collecting_contact_method"
                agent_response = "Contact method? phone, email, or text?"

            elif state == "collecting_contact_method":
                cm = prompt.lower().strip()
                if cm in ['phone', 'call']:
                    st.session_state.user_info['preferred_contact'] = 'Phone'
                elif cm in ['email']:
                    st.session_state.user_info['preferred_contact'] = 'Email'
                elif cm in ['text', 'sms']:
                    st.session_state.user_info['preferred_contact'] = 'Text Message'
                else:
                    agent_response = "phone, email, or text?"
                st.session_state.conversation_state = "collecting_contact_info"
                agent_response = f"What's your {st.session_state.user_info['preferred_contact']}?"

            elif state == "collecting_contact_info":
                st.session_state.user_info['contact_info'] = prompt
                result = submit_legal_request(st.session_state.user_info, 'eviction', st.session_state.user_info.get('description', ''))
                agent_response = f"Submitted! ID: {result['request_id']}\nRepresentative contacts you in 24-48 hours."
                st.session_state.conversation_state = "initial"

        response.markdown(agent_response)
        st.session_state.messages.append({"role": "assistant", "content": agent_response})
