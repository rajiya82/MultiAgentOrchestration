
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# from IntentClassifier.classifier import intent_classifier_endpoint

load_dotenv()

import streamlit as st

st.set_page_config(page_title="Chatbot", layout="wide")

st.title("Chatbot")
st.caption("Basic chatbot application")

model = st.sidebar.selectbox(
    "Choose a model", ["amazon.nova-micro-v1:0"]
)

if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

# Capture user query from chat bar input container
user_query = st.chat_input("Ask something...")

# 🎯 FIX 1: Enforce encapsulation.
# Absolutely no code should float loosely underneath this conditional block!
if user_query:
    # Append and render user question bubble layout
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query, unsafe_allow_html=True)

    # Open assistant container with a loading spinner while API fetches tokens
    with st.chat_message("assistant"):
        with st.spinner("Invoking remote routing engine..."):

            api_url = "https://rfqefkbrqa.execute-api.us-east-1.amazonaws.com/intent-classifier"
            payload = {"user_query": user_query}
            headers = {"Content-Type": "application/json"}

            try:
                response = requests.post(api_url, json=payload, headers=headers, timeout=30)

                if response.status_code == 200:
                    # Parse out the JSON payload return string safely
                    detected_intent = response.json()

                    # 🎯 FIX 2: Defensive Python Slicing
                    # If the stop sequence fails on AWS, we chop off "REASONING" right here in Python!
                    if isinstance(detected_intent, str):
                        if "REASONING" in detected_intent:
                            detected_intent = detected_intent.split("REASONING")[0]

                    # Strip out any remaining template headers cleanly
                    detected_intent = detected_intent.replace("USER_INTENT:", "").strip()

                    # 🎯 FIX 3: Multi-Agent Logic Branching Distribution Tree
                    if "GENERAL_INFO" in detected_intent:
                        agent_output = "🌐 **Routed to Knowledge Agent:** Commencing public internet query checks via LangChain Wikipedia..."
                    elif "FINANCIAL_INFO" in detected_intent:
                        agent_output = "📈 **Routed to Finance Agent:** Connecting to deployed AWS Lambda microservice endpoint..."
                    elif "APPOINTMENT_BOOKING" in detected_intent:
                        agent_output = "📅 **Routed to Scheduler Agent:** Reviewing available time slots..."
                    else:
                        agent_output = f"🎯 **Routing Coordinator:** Clear intent label identified: `{detected_intent}`"

                    # Save and print the target agent text layout to the screen
                    st.session_state.messages.append({"role": "assistant", "content": agent_output})
                    st.write(agent_output)

                else:
                    st.error(f"API Gateway Error ({response.status_code}): {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"Network transport error connecting to AWS endpoint: {e}")