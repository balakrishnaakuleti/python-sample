from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType,VectorFilterMode
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from app.src.util import constants

# Secrets from keyvault
credential = DefaultAzureCredential()
client = SecretClient(vault_url=constants.KEY_VAULT_URL, credential=credential)

# Retrieve the secret
AI_SEARCH_API_KEY = client.get_secret(constants.VAULT_AI_SEARCH_API_KEY).value

# Create a SearchClient to perform search
search_client = SearchClient(endpoint=constants.AI_SEARCH_ENDPOINT, index_name=constants.AI_SEARCH_INDEX_NAME, credential=AzureKeyCredential(AI_SEARCH_API_KEY))

def ai_search(query):
    #Perform Hybrid search
    results= search_client.search(
    search_text= query,
    #Semantic Search Parameters
    search_fields=["chunk"],
    semantic_configuration_name= constants.SEMANTIC_SEARCH_CONFIG,
    query_type= QueryType.SEMANTIC,
    #Vector Search Parameters
    vector_filter_mode= VectorFilterMode.POST_FILTER ,    
    vector_queries=[
        {
            "kind": "text",
            "text": query,
            "fields": "text_vector",
            "k": 50
        }
    ],
    select=["chunk"],
    top=5)
    # Return first result if results is not None
    for result in results:
        return result["chunk"]
    return None
