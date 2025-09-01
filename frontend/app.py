import streamlit as st
import requests
import json
from typing import Dict

# Configure the page
st.set_page_config(
    page_title="Smart Librarian AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"


def call_chat_api(message: str) -> Dict:
    """Call the chat API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={"message": message},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API Error: {str(e)}"}


def get_available_books():
    """Get list of available books"""
    try:
        response = requests.get(f"{API_BASE_URL}/books", timeout=10)
        response.raise_for_status()
        return response.json().get("books", [])
    except requests.exceptions.RequestException:
        return []


def main():
    # Title and description
    st.title("📚 Smart Librarian AI")
    st.markdown("### Your AI-powered book recommendation assistant")
    st.markdown("Ask me for book recommendations based on your interests, themes, or genres!")

    # Sidebar with information
    with st.sidebar:
        st.header("📖 Available Books")

        with st.spinner("Loading books..."):
            books = get_available_books()

        if books:
            st.write(f"**{len(books)} books** in our database:")
            for book in sorted(books):
                st.write(f"• {book}")
        else:
            st.warning("Could not load book list. Make sure the API is running.")

        st.markdown("---")
        st.markdown("### 💡 Example Queries")
        st.markdown("""
        • *"I want a book about freedom and social control"*
        • *"What do you recommend if I love fantasy stories?"*
        • *"I'm looking for war stories"*
        • *"Books about friendship and magic"*
        • *"What is 1984?"*
        """)

        st.markdown("---")
        st.markdown("### 🔧 API Status")
        try:
            health_response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if health_response.status_code == 200:
                st.success("✅ API Connected")
            else:
                st.error("❌ API Issues")
        except:
            st.error("❌ API Offline")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello! I'm your Smart Librarian AI. I can help you discover amazing books based on your interests. What kind of book are you in the mood for today?"
        })

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What kind of book are you looking for?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_data = call_chat_api(prompt)

            if "error" in response_data:
                response = f"Sorry, I encountered an error: {response_data['error']}"
                st.error(response)
            else:
                response = response_data.get("response", "I'm sorry, I couldn't generate a response.")

                # Check for inappropriate content warning
                if response_data.get("inappropriate_content", False):
                    st.warning("⚠️ Please keep our conversation respectful!")

                st.markdown(response)

                # Show recommended books if available
                if response_data.get("recommended_books"):
                    st.success("📚 **Recommended Books:**")
                    for book in response_data["recommended_books"]:
                        st.write(f"• **{book}**")

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Clear chat button
    if st.button("🗑️ Clear Chat", type="secondary"):
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello! I'm your Smart Librarian AI. I can help you discover amazing books based on your interests. What kind of book are you in the mood for today?"
        })
        st.rerun()


if __name__ == "__main__":
    main()