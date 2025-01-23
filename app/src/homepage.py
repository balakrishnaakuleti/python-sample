import streamlit as st
from app.src.chat_bot import show_chat_app
from app.src.services.azure_aad_service import get_authorization_url, get_token_from_code, get_user_profile

def show_home_page():
    # Streamlit app UI
    st.title("Welcome to the Question and Answers Chatbot on news articles!!!")

    # Show the home page if the user is authenticated
    if 'access_token' in st.session_state:
        access_token = st.session_state.access_token
        try:
            user_profile = get_user_profile(access_token)
        except:
            st.write("Error: Unable to get user profile. Please try logging in again.")
            show_login_button()
            return
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
            show_login_button()
        else:
            # Handle the redirect (After login in Azure, Azure will redirect back to this URI with code)
            code = st.query_params.get("code")
            if code is not None:
                result = None
                try:
                    result = get_token_from_code(code)
                except:
                    st.write("Error: Unable to get token from code. Please try logging in again.")
                    show_login_button()
                    return
                if "access_token" in result:
                    st.session_state.access_token = result['access_token']
                    st.rerun()
                else:
                    st.write("Logout Successful !!")

def show_login_button():
    if st.button("Login with Azure AD"):
        auth_url = None
        try:
                auth_url = get_authorization_url()
        except:
            st.write("Error: Unable to get authorization URL. Please try again.")
            st.markdown(f'<a href="https://qna-news.azurewebsites.net/" target="_self">Please login using this link</a>', unsafe_allow_html=True)
            return
        st.markdown(f'<a href="{auth_url}" target="_self">Please login using this link</a>', unsafe_allow_html=True)
show_home_page()