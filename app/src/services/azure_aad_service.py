import msal
import requests
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from ..util import constants

# Secrets from keyvault
credential = DefaultAzureCredential()
client = SecretClient(vault_url=constants.KEY_VAULT_URL, credential=credential)

# Retrieve the secret
clientid = client.get_secret(constants.AAD_VAULT_CLIENT_ID)
clientsecret = client.get_secret(constants.AAD_VAULT_CLIENT_SECRET)
tenantid= client.get_secret(constants.AAD_VAULT_TENTNT_ID)

# Replace these with your Azure AD details
AAD_CLIENT_ID = clientid.value
AAD_CLIENT_SECRET = clientsecret.value
AAD_AUTHORITY_TENANT = constants.AAD_AUTHORITY + tenantid.value

# MSAL app initialization
def _build_msal_app():
    return msal.ConfidentialClientApplication(
        AAD_CLIENT_ID,
        authority=AAD_AUTHORITY_TENANT,
        client_credential=AAD_CLIENT_SECRET
    )

# Step 1: Authorization Code Flow
def get_authorization_url():
    msal_app = _build_msal_app()
    auth_url = msal_app.get_authorization_request_url(constants.AAD_SCOPE, redirect_uri=constants.AAD_REDIRECT_URI)
    return auth_url

# Step 2: Token Exchange
def get_token_from_code(code):
    msal_app = _build_msal_app()
    result = msal_app.acquire_token_by_authorization_code(
        code, 
        scopes=constants.AAD_SCOPE, 
        redirect_uri=constants.AAD_REDIRECT_URI
    )
    return result

# Step 3: Get User Profile
def get_user_profile(access_token):
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    profile_url = constants.AAD_PROFILE_URL
    response = requests.get(profile_url, headers=headers)
    return response.json()