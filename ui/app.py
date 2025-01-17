import streamlit as st
from openai import AzureOpenAI

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Set up the SecretClient
credential = DefaultAzureCredential()
vault_url = "https://kv-qna-news.vault.azure.net/"
secret_client = SecretClient(vault_url=vault_url, credential=credential)

# Open AI Section
api_version = "2024-08-01-preview"
endpoint = "https://cba.openai.azure.com"

ai_client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=secret_client.get_secret("OPENAI-KEY").value,
)

def show_chat_app():
    # Title and description of the app
    st.title("Chat with AI")
    st.write("This is a simple chat application where you can talk to a basic AI. Feel free to ask anything!")

    st.write("""Disclaimer:
    For your privacy and security, please do not share any personally identifiable information (PII), such as your full name, address, phone number, or financial details. This chatbot is not designed to store or process sensitive data, and sharing such information could compromise your privacy. Always exercise caution when interacting online.""")

    # Create a session state to store chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Input box for the user to enter their message
    user_input = st.text_input("You:", key="user_input")

    # Process the user input and respond when the user presses Enter (submit)
    if user_input:
        # Append the user's message to the chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get the chatbot's response
        try:
            # Call the OpenAI API to get a response
            response = ai_client.chat.completions.create(
                model="gpt-4o",  # You can change the model (e.g., gpt-4, gpt-3.5-turbo)
                messages=st.session_state.messages  # Provide the chat history to maintain context
            )

            # Extract the assistant's reply
            bot_reply = response.choices[0].message.content

            # Append the assistant's response to the chat history
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        except Exception as e:
                return f"Error: {e}"
        
        # **Don't reset the input field directly. Streamlit will clear the input box automatically.**
        # Just rely on Streamlit to clear it after each submission

    # Display the chat history
    for message in st.session_state.messages:
        st.write(message["role"],": ",message["content"])
show_chat_app()