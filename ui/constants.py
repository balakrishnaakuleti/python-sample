# KEY_VAULT Section
KEY_VAULT_ACCOUNT_NAME="kv-qna-news"
KEY_VAULT_URL = F"https://{KEY_VAULT_ACCOUNT_NAME}.vault.azure.net/"
AAD_VAULT_CLIENT_ID = "CLIENT-ID"
AAD_VAULT_CLIENT_SECRET = "CLIENT-SECRET"
AAD_VAULT_TENTNT_ID = "TENANT-ID"
VAULT_OPENAI_KEY= "OPENAI-KEY"
VAULT_AI_SEARCH_API_KEY = "ACS-KEY" 

# AAD SECTION
AAD_AUTHORITY = "https://login.microsoftonline.com/"
AAD_REDIRECT_URI = "https://qna-news.azurewebsites.net/"
AAD_SCOPE = ["User.Read"]
AAD_PROFILE_URL = "https://graph.microsoft.com/v1.0/me"


#Open AI
OPEN_AI_API_VERSION = "2024-08-01-preview"
OPEN_AI_ENDPOINT = "https://cba.openai.azure.com"
GPT_MODEL_NAME="gpt-4o"

#AI SEARCH
AI_SEARCH_ACCOUNT_NAME="qna-news-ai-search"
AI_SEARCH_ENDPOINT = f"https://{AI_SEARCH_ACCOUNT_NAME}.search.windows.net"
AI_SEARCH_INDEX_NAME="qna-news"