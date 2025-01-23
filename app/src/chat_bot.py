import streamlit as st

from app.src.services.azure_ai_search_service import ai_search
from app.src.services.azure_open_ai_service import ai_answer
from app.src.services.azure_pii_service import redact_pii

system_prompt ="You are an intelligent language assistant who can answer questions from the provided news article. You can greet them back politey if they greet you saying hi. You can briefly explain your purpose. Once the user asks the question, you should strictly asnswer the questions only from the news article provided. If you are unable to understand the user query, you can ask for clarification. If you are unable to find the apt answer from the article below, please say that you would be unable to help. Some samples question and answers Question 1 : How to prepare dosa? Answer: Sorry this question doesn't seem to be related to news. Would be unable to answer. Please ask some relevant question on news. News article starts here: "

def show_chat_app():
    # Title and description of the app
    st.title("Intelligent QnA Chatbot on the news articles")
    st.write("This is a simple chat application where you can ask questions on the news articles. Feel free to ask anything!")

    st.write("""Disclaimer:
    For your privacy and security, please do not share any personally identifiable information (PII), such as your full name, address, phone number, or financial details. This chatbot is not designed to store or process sensitive data, and sharing such information could compromise your privacy. Always exercise caution when interacting online.""")

    # Create a session state to store chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Input box for the user to enter their message
    user_input = st.text_input("You:", key="user_input")

    # Process the user input and respond when the user presses Enter (submit)
    st.session_state.messages.append({"role": "system", "content": system_prompt})
    if user_input:
        # Length restricted to 1000 character
        if len(user_input) > 1000:
            st.write("Please keep your message under 1000 characters.")
            return
        # Get the chatbot's response
        try:
            relevant_news_article = None
            # PII detection and redaction
            try:
                user_input = redact_pii(user_input)
            except:
                st.write("Error: Unable to redact PII. Please make sure No PII is shared as part of your query.")
            # AI Search
            try:
                relevant_news_article = ai_search(user_input)
            except:
                st.write("Error: Unable to get relevant news article. Please try again.")
                return

            #Add redacted user utterance to the history
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Append the user's message to the chat history
            # Call the OpenAI API to get a response
            bot_reply = None
            try:
                bot_reply = ai_answer(st.session_state.messages,relevant_news_article)
            except:
                st.write("Error: Unable to get answer from the news article. Please try again.")
                return

            # Append the assistant's response to the chat history
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        except Exception as e:
                return f"Error: {e}"
        
        # **Don't reset the input field directly. Streamlit will clear the input box automatically.**
        # Just rely on Streamlit to clear it after each submission

    # Display the chat history
    for message in st.session_state.messages:
        role = message["role"]
        if role != "system":
            st.write(role,": ",message["content"])