import streamlit as st

# Title and description of the app
st.title("Chat with AI")
st.write("This is a simple chat application where you can talk to a basic AI. Feel free to ask anything!")

st.write("""Disclaimer:
For your privacy and security, please do not share any personally identifiable information (PII), such as your full name, address, phone number, or financial details. This chatbot is not designed to store or process sensitive data, and sharing such information could compromise your privacy. Always exercise caution when interacting online.""")


# Function to simulate the chatbot response
def chatbot_response(user_message):
    # Basic predefined responses
    responses = {
        "hi": "Hello! How can I assist you today?",
        "hello": "Hi there! How can I help you?",
        "how are you": "I'm just a bot, but I'm doing great! How about you?",
        "bye": "Goodbye! Have a great day!",
    }
    
    # Default response for unknown messages
    return responses.get(user_message.lower(), "I'm sorry, I didn't understand that. Can you ask something else?")

# Create a session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input box for the user to enter their message
user_input = st.text_input("You:", key="user_input")

# Process the user input and respond when the user presses Enter (submit)
if user_input:
    # Append the user's message to the chat history
    st.session_state.messages.append(f"You: {user_input}")
    
    # Get the chatbot's response
    bot_reply = chatbot_response(user_input)
    
    # Append the bot's response to the chat history
    st.session_state.messages.append(f"Bot: {bot_reply}")
    
    # **Don't reset the input field directly. Streamlit will clear the input box automatically.**
    # Just rely on Streamlit to clear it after each submission

# Display the chat history
for message in st.session_state.messages:
    st.write(message)
