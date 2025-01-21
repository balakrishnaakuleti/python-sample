import streamlit as st
from chat_bot import show_chat_app
from services.azure_aad_service import get_authorization_url, get_user_profile

# Streamlit app UI
st.title("Welcome to the Question and Answers Chatbot on news articles!!!")

# Show the home page if the user is authenticated
if 'access_token' in st.session_state:
    access_token = st.session_state.access_token
    user_profile = get_user_profile(access_token)
    st.write(f"Welcome {user_profile['displayName']}")
    st.write(f"Email: {user_profile['mail']}")
    # Display the chat application
    show_chat_app()
    # Logout button
    if st.button('Logout'):
        del st.session_state.access_token
        st.rerun()
else:
    # If not logged in, show login button
    if st.button("Login with Azure AD"):
        auth_url = get_authorization_url()
        st.markdown(f'<a href="{auth_url}" target="_self">Please login using this link</a>', unsafe_allow_html=True)

