
import unittest
from unittest.mock import patch, MagicMock
from app.src.services.azure_pii_service import redact_pii, authenticate_client

class TestAzurePiiService(unittest.TestCase):

    @patch('app.src.services.azure_pii_service.authenticate_client')
    def setUp(self, mock_authenticate_client):
        self.mock_client = MagicMock()
        mock_authenticate_client.return_value = self.mock_client

    @patch('app.src.services.azure_pii_service.client')
    def test_redact_pii(self, mock_client):
        mock_response = MagicMock()
        mock_response.is_error = False
        mock_response.redacted_text = "REDACTED"
        mock_client.recognize_pii_entities.return_value = [mock_response]

        query = "My email is example@example.com"
        redacted_text = redact_pii(query)

        mock_client.recognize_pii_entities.assert_called_once_with(documents=[query], categories_filter=[
            "Email", "URL", "Age", "PhoneNumber", "IPAddress", "Person", "Address"
        ])
        self.assertEqual(redacted_text, "REDACTED")

if __name__ == '__main__':
    unittest.main()
