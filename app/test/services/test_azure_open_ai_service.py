import unittest
from unittest.mock import patch, MagicMock
from app.src.services.azure_open_ai_service import ai_answer

class TestAzureOpenAIService(unittest.TestCase):

    @patch('app.src.services.azure_open_ai_service.AzureOpenAI')
    @patch('app.src.services.azure_open_ai_service.SecretClient')
    @patch('app.src.services.azure_open_ai_service.DefaultAzureCredential')
    def test_ai_answer_success(self, mock_credential, mock_secret_client, mock_azure_openai):
        # Mock the secret client and AzureOpenAI client
        mock_secret_client_instance = mock_secret_client.return_value
        mock_secret_client_instance.get_secret.return_value.value = 'fake_api_key'
        
        mock_ai_client_instance = mock_azure_openai.return_value
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Test response"))]
        mock_ai_client_instance.chat.completions.create.return_value = mock_response

        messages = [{"role": "user", "content": "Hello"}]
        relevant_news_article = "Some news article content"
        
        response = ai_answer(messages, relevant_news_article)
        
        self.assertIsNotNone(response)

if __name__ == '__main__':
    unittest.main(verbosity=2)
