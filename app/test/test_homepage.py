import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
from app.src.chat_bot import show_chat_app
from app.src.services.azure_aad_service import get_authorization_url, get_token_from_code, get_user_profile
from app.src.homepage import show_home_page

class TestHomePage(unittest.TestCase):
    
    @patch('streamlit.title')
    @patch('streamlit.write')
    @patch('streamlit.button')
    @patch('streamlit.markdown')
    @patch('streamlit.rerun')
    @patch('streamlit.session_state', new_callable=MagicMock)
    @patch('app.src.services.azure_aad_service.get_user_profile')
    @patch('app.src.services.azure_aad_service.get_authorization_url')
    @patch('app.src.services.azure_aad_service.get_token_from_code')
    def test_show_home_page_authenticated(self, mock_get_token_from_code, mock_get_authorization_url, mock_get_user_profile, mock_session_state, mock_rerun, mock_markdown, mock_button, mock_write, mock_title):
        # Simulate an authenticated user
        mock_session_state.access_token = "fake_access_token"
        
        # Mock the user profile function to return a mock profile
        mock_get_user_profile.return_value = {'displayName': 'John Doe', 'mail': 'john.doe@example.com'}
        
        # Call the function
        show_home_page()

        # Test if the UI elements are displayed
        mock_title.assert_called_with("Welcome to the Question and Answers Chatbot on news articles!!!")

        # Test that rerun is not triggered on successful authentication
        mock_rerun.assert_not_called()
    
    @patch('streamlit.title')
    @patch('streamlit.write')
    @patch('streamlit.button')
    @patch('streamlit.markdown')
    @patch('streamlit.rerun')
    @patch('streamlit.session_state', new_callable=MagicMock)
    @patch('app.src.services.azure_aad_service.get_user_profile')
    @patch('app.src.services.azure_aad_service.get_authorization_url')
    @patch('app.src.services.azure_aad_service.get_token_from_code')
    def test_show_home_page_error_in_token(self, mock_get_token_from_code, mock_get_authorization_url, mock_get_user_profile, mock_session_state, mock_rerun, mock_markdown, mock_button, mock_write, mock_title):
        # Simulate an error when retrieving the token
        mock_session_state.access_token = None
        mock_get_token_from_code.return_value = {'error_description': 'Invalid code'}
        st.query_params = {"code": "fake_code"}  # Simulating query params with a code
        
        # Call the function
        show_home_page()

        # Test error message is displayed
        mock_write.assert_called_once()
        
        # Test that rerun is not called due to error
        mock_rerun.assert_not_called()

if __name__ == '__main__':
    unittest.main()
