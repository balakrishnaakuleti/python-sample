import streamlit as st
import msal
import requests
import json
import os
from app import show_chat_app
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.credentials import AccessTokenInfo

# Secrets from keyvault
key_vault_url = "https://kv-qna-news.vault.azure.net/"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=key_vault_url, credential=credential)

# Replace with the name of your secret
VAULT_CLIENT_ID = "CLIENT-ID"
VAULT_CLIENT_SECRET = "CLIENT-SECRET"
VAULT_TENTNT_ID = "TENANT-ID"


# Retrieve the secret
clientid = client.get_secret(VAULT_CLIENT_ID)
clientsecret = client.get_secret(VAULT_CLIENT_SECRET)
tenantid= client.get_secret(VAULT_TENTNT_ID)

# Replace these with your Azure AD details
CLIENT_ID = clientid.value #os.getenv("CLIENT_ID")  # Your Azure AD Application Client ID
CLIENT_SECRET = clientsecret.value #os.getenv("CLIENT_SECRET")  # Your Azure AD Application Client Secret
AUTHORITY = "https://login.microsoftonline.com/" + tenantid.value # os.getenv("TENANT_ID")  # Azure AD tenant ID
REDIRECT_URI = "https://qna-news.azurewebsites.net/"  # Redirect URI registered in Azure AD
SCOPE = ["User.Read"]

# MSAL app initialization
def _build_msal_app():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )

# Step 1: Authorization Code Flow
def get_authorization_url():
    msal_app = _build_msal_app()
    auth_url = msal_app.get_authorization_request_url(SCOPE, redirect_uri=REDIRECT_URI)
    return auth_url

# Step 2: Token Exchange
def get_token_from_code(code):
    msal_app = _build_msal_app()
    result = msal_app.acquire_token_by_authorization_code(
        code, 
        scopes=SCOPE, 
        redirect_uri=REDIRECT_URI
    )
    return result

# Step 3: Get User Profile
def get_user_profile(access_token):
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    profile_url = "https://graph.microsoft.com/v1.0/me"
    response = requests.get(profile_url, headers=headers)
    return response.json()

# Streamlit app UI
st.title("Azure AD Login")

# Check if the user is authenticated
if 'access_token' in st.session_state:
    access_token = st.session_state.access_token
    user_profile = get_user_profile(access_token)
    st.write(f"Welcome {user_profile['displayName']}")
    st.write(f"Email: {user_profile['mail']}")
    show_chat_app()
    # Logout button
    if st.button('Logout'):
        del st.session_state.access_token
        st.experimental_rerun()

else:
    # If not logged in, show login button
    if st.button("Login with Azure AD"):
        auth_url = get_authorization_url()
        st.markdown(f'<a href="{auth_url}" target="_self">Please login using this link</a>', unsafe_allow_html=True)

    # Handle the redirect (After login in Azure, Azure will redirect back to this URI with code)
    query_params = st.experimental_get_query_params()
    if 'code' in query_params:
        code = query_params['code'][0]
        result = get_token_from_code(code)
        
        if "access_token" in result:
            st.session_state.access_token = result['access_token']
            st.rerun()
        else:
            st.write("Error: " + result.get("error_description", "Unknown error"))
