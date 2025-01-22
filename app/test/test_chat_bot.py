import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
from app.src.chat_bot import show_chat_app
from app.src.services.azure_aad_service import get_user_profile

class TestChatBotApp(unittest.TestCase):
    
    @patch('streamlit.title')
    @patch('streamlit.write')
    @patch('app.src.services.azure_aad_service.get_user_profile')
    @patch('app.src.chat_bot.show_chat_app')
    @patch('streamlit.session_state', new_callable=MagicMock)
    def test_authenticated_user(self, mock_session_state, mock_show_chat_app, mock_get_user_profile, mock_write, mock_title):
        
        # Simulate the app logic
        show_chat_app()
        
        # Test if Streamlit's title was set correctly
        mock_title.assert_called_once_with("Intelligent QnA Chatbot on the news articles")