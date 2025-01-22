import unittest
from unittest.mock import patch, MagicMock
from app.src.services.azure_aad_service import get_token_from_code
from app.src.services.azure_aad_service import get_authorization_url, get_user_profile, _build_msal_app
from app.src.util import constants


class TestAzureAADService(unittest.TestCase):

    @patch('app.src.services.azure_aad_service._build_msal_app')
    def test_get_token_from_code(self, mock_build_msal_app):
        # Create a mock MSAL app
        mock_msal_app = MagicMock()
        mock_build_msal_app.return_value = mock_msal_app
        
        # Mock the acquire_token_by_authorization_code method
        mock_token_response = {
            'access_token': 'fake_access_token',
            'id_token': 'fake_id_token'
        }
        mock_msal_app.acquire_token_by_authorization_code.return_value = mock_token_response
        
        # Call the function to test
        code = 'fake_code'
        result = get_token_from_code(code)
        
        # Assert the function returns the expected token response
        self.assertEqual(result, mock_token_response)
        mock_msal_app.acquire_token_by_authorization_code.assert_called_once_with(
            code, 
            scopes=constants.AAD_SCOPE, 
            redirect_uri=constants.AAD_REDIRECT_URI
        )

    @patch('app.src.services.azure_aad_service._build_msal_app')
    def test_get_authorization_url(self, mock_build_msal_app):
        # Create a mock MSAL app
        mock_msal_app = MagicMock()
        mock_build_msal_app.return_value = mock_msal_app
        
        # Mock the get_authorization_request_url method
        mock_auth_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
        mock_msal_app.get_authorization_request_url.return_value = mock_auth_url
        
        # Call the function to test
        result = get_authorization_url()
        
        # Assert the function returns the expected authorization URL
        self.assertEqual(result, mock_auth_url)
        mock_msal_app.get_authorization_request_url.assert_called_once_with(
            constants.AAD_SCOPE, 
            redirect_uri=constants.AAD_REDIRECT_URI
        )

    @patch('requests.get')
    def test_get_user_profile(self, mock_requests_get):
        # Mock the response from the requests.get call
        mock_response = MagicMock()
        mock_response.json.return_value = {'id': 'user_id', 'displayName': 'User Name'}
        mock_requests_get.return_value = mock_response
        
        # Call the function to test
        access_token = 'fake_access_token'
        result = get_user_profile(access_token)
        
        # Assert the function returns the expected user profile
        self.assertEqual(result, {'id': 'user_id', 'displayName': 'User Name'})
        mock_requests_get.assert_called_once_with(
            constants.AAD_PROFILE_URL, 
            headers={'Authorization': 'Bearer fake_access_token'}
        )

    @patch('app.src.services.azure_aad_service.msal.ConfidentialClientApplication')
    @patch('app.src.services.azure_aad_service.AAD_CLIENT_ID', 'fake-client-id')
    @patch('app.src.services.azure_aad_service.AAD_CLIENT_SECRET', 'fake-client-secret')
    @patch('app.src.services.azure_aad_service.AAD_AUTHORITY_TENANT', 'https://login.microsoftonline.com/fake-tenant-id')
    def test_build_msal_app(self, MockConfidentialClientApplication):
        mock_app = MagicMock()
        MockConfidentialClientApplication.return_value = mock_app

        msal_app = _build_msal_app()

        MockConfidentialClientApplication.assert_called_once_with(
            'fake-client-id',
            authority='https://login.microsoftonline.com/fake-tenant-id',
            client_credential='fake-client-secret'
        )
        self.assertEqual(msal_app, mock_app)

if __name__ == '__main__':
    unittest.main()
if __name__ == '__main__':
    unittest.main()