from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from openai import AzureOpenAI

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from ..util import constants

# Secrets from keyvault
credential = DefaultAzureCredential()
client = SecretClient(vault_url=constants.KEY_VAULT_URL, credential=credential)

ai_client = AzureOpenAI(
    api_version=constants.OPEN_AI_API_VERSION,
    azure_endpoint=constants.OPEN_AI_ENDPOINT,
    api_key=client.get_secret(constants.VAULT_OPENAI_KEY).value,
)

def ai_answer(messages):
    # Get the chatbot's response
    try:
        # Call the OpenAI API to get a response
        response = ai_client.chat.completions.create(
            model=constants.GPT_MODEL_NAME,
            messages=messages  # Provide the chat history to maintain context
        )

        # Extract the assistant's reply
        return response.choices[0].message.content
    except Exception as e:
            return f"Error: {e}"