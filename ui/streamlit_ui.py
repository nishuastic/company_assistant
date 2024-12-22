import streamlit as st
import requests

BASE_API_URL = "http://localhost:8000"

st.title("LinkedIn Generator and Value App")

# Sidebar for navigation
option = st.sidebar.selectbox(
    "Choose Functionality", ["LinkedIn Generator", "Value App"]
)

# Initialize session state for `base_url` and `analysis_result`
if "base_url" not in st.session_state:
    st.session_state.base_url = ""
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# LinkedIn Generator functionality
if option == "LinkedIn Generator":
    st.subheader("Generate LinkedIn Note")
    # Input fields for LinkedIn note
    recipient_name = st.text_input("Recipient Name")
    recipient_headline = st.text_area("Recipient Headline")
    recipient_about = st.text_area("Recipient About Section")
    purpose = st.text_input("Purpose")
    sender_name = st.text_input("Sender Name")
    # Button to generate the note
    if st.button("Generate"):
        payload = {
            "recipient_name": recipient_name,
            "recipient_headline": recipient_headline,
            "recipient_about": recipient_about,
            "purpose": purpose,
            "sender_name": sender_name,
        }
        response = requests.post(f"{BASE_API_URL}/linkedin/generate_note", json=payload)
        if response.status_code == 200:
            st.success("Generated Note:")
            st.write(response.json()["note"])
        else:
            st.error(
                f"Failed to generate note: {response.json().get('detail', 'Unknown Error')}"
            )

# Value App functionality
elif option == "Value App":
    st.subheader("Analyze Competitor Website")
    # Input field for website URL
    base_url = st.text_input(
        "Website URL",
        value=st.session_state.base_url or "",
        placeholder="Enter competitor's website URL",
    )
    if st.button("Analyze"):
        st.session_state.base_url = base_url
        response = requests.get(
            f"{BASE_API_URL}/value/analyze", params={"base_url": base_url}
        )
        if response.status_code == 200:
            st.success("Website Analyzed Successfully!")
            st.session_state.analysis_result = response.json()
        else:
            st.error(
                f"Failed to analyze website: {response.json().get('detail', 'Unknown Error')}"
            )

    # Chat with the vectorstore
    if st.session_state.analysis_result:
        st.subheader("Chat with the Analyzed Content")
        query = st.text_input("Ask a Question")
        if st.button("Ask"):
            chat_payload = {
                "base_url": st.session_state.base_url,
                "query": query,
            }
            chat_response = requests.post(
                f"{BASE_API_URL}/value/chat", json=chat_payload
            )

            if chat_response.status_code == 200:
                st.success("Chatbot Response:")
                st.write(chat_response.json()["response"])
            else:
                st.error(
                    f"Failed to query the vectorstore: {chat_response.json().get('detail', 'Unknown Error')}"
                )
