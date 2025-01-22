import unittest
from unittest.mock import patch, MagicMock
from app.src.services.azure_ai_search_service import ai_search

class TestAzureAiSearchService(unittest.TestCase):

    @patch('app.src.services.azure_ai_search_service.SearchClient')
    @patch('app.src.services.azure_ai_search_service.AzureKeyCredential')
    @patch('app.src.services.azure_ai_search_service.SecretClient')
    @patch('app.src.services.azure_ai_search_service.DefaultAzureCredential')
    def test_ai_search_returns_chunk(self, mock_default_credential, mock_secret_client, mock_key_credential, mock_search_client):
        # Mock the secret client to return a fake API key
        mock_secret_instance = mock_secret_client.return_value
        mock_secret_instance.get_secret.return_value.value = 'fake_api_key'

        # Mock the search client to return a fake search result
        mock_search_instance = mock_search_client.return_value
        mock_search_instance.search.return_value = iter([{'chunk': 'test_chunk'}])

        # Call the function
        result = ai_search('test_query')

        # Assert the result
        self.assertIsNotNone(result)