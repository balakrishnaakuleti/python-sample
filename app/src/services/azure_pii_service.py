
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from app.src.util import constants

# Secrets from keyvault
credential = DefaultAzureCredential()
client = SecretClient(vault_url=constants.KEY_VAULT_URL, credential=credential)
LANG_KEY = client.get_secret(constants.VAULT_LANG_KEY).value

# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(LANG_KEY)
    text_analytics_client = TextAnalyticsClient(
            endpoint=constants.LANG_END_POINT, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

# Example method for detecting sensitive information (PII) from text 
def redact_pii(query):
    result = client.recognize_pii_entities([query])
    docs = [doc for doc in result if not doc.is_error]
    #Only one document so, return the first document's redacted text
    return docs[0].redacted_text