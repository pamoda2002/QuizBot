"""
Application dependencies
Provides dependency injection for controllers and services
"""
from app.services.database_service import DatabaseService
from app.services.chatbot_service import ChatbotService
from app.services.auth_service import AuthService
from app.controllers.chat_controller import ChatController
from app.controllers.message_controller import MessageController

# Singleton instances
_db_service = None
_chatbot_service = None
_auth_service = None


def get_database_service() -> DatabaseService:
    """Get database service instance"""
    global _db_service
    if _db_service is None:
        _db_service = DatabaseService()
    return _db_service


def get_chatbot_service() -> ChatbotService:
    """Get chatbot service instance"""
    global _chatbot_service
    if _chatbot_service is None:
        _chatbot_service = ChatbotService()
    return _chatbot_service


def get_auth_service() -> AuthService:
    """Get auth service instance"""
    global _auth_service
    if _auth_service is None:
        _auth_service = AuthService(get_database_service())
    return _auth_service


def get_chat_controller() -> ChatController:
    """Get chat controller instance"""
    return ChatController(get_database_service())


def get_message_controller() -> MessageController:
    """Get message controller instance"""
    return MessageController(get_database_service(), get_chatbot_service())
