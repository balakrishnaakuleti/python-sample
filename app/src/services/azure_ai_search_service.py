from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import constants
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import constants

# Secrets from keyvault
credential = DefaultAzureCredential()
client = SecretClient(vault_url=constants.KEY_VAULT_URL, credential=credential)

# Retrieve the secret
AI_SEARCH_API_KEY = client.get_secret(constants.VAULT_AI_SEARCH_API_KEY).value

# Create a SearchClient to perform search
search_client = SearchClient(endpoint=constants.AI_SEARCH_ENDPOINT, index_name=constants.AI_SEARCH_INDEX_NAME, credential=AzureKeyCredential(AI_SEARCH_API_KEY))

def ai_search(query):
    # Perform a search query
    results = search_client.search(search_text=query, top=1)

    for page in results.by_page():
        for result in page:
            return result["content"]["article"]
    return None