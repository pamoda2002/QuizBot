"""
Chat Controller
Handles chat-related business logic
"""
from typing import List, Optional
from datetime import datetime
import uuid
from app.models.chat import Chat
from app.services.database_service import DatabaseService


class ChatController:
    """Controller for chat operations"""
    
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service
    
    async def create_chat(self, user_id: str, title: Optional[str] = None) -> Chat:
        """
        Create a new chat session
        
        Args:
            user_id: User identifier
            title: Optional chat title
            
        Returns:
            Chat: Created chat object
        """
        chat = Chat(
            id=f"chat_{uuid.uuid4().hex[:12]}",
            user_id=user_id,
            title=title or "New Chat"
        )
        await self.db_service.save_chat(chat)
        return chat
    
    async def get_chat(self, chat_id: str) -> Optional[Chat]:
        """
        Get a chat by ID
        
        Args:
            chat_id: Chat identifier
            
        Returns:
            Optional[Chat]: Chat object if found
        """
        return await self.db_service.get_chat(chat_id)
    
    async def get_user_chats(self, user_id: str) -> List[Chat]:
        """
        Get all chats for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            List[Chat]: List of user's chats
        """
        return await self.db_service.get_user_chats(user_id)
    
    async def update_chat(self, chat_id: str, title: str) -> Optional[Chat]:
        """
        Update chat title
        
        Args:
            chat_id: Chat identifier
            title: New title
            
        Returns:
            Optional[Chat]: Updated chat object
        """
        chat = await self.db_service.get_chat(chat_id)
        if chat:
            chat.title = title
            chat.updated_at = datetime.utcnow()
            await self.db_service.save_chat(chat)
        return chat
    
    async def delete_chat(self, chat_id: str) -> bool:
        """
        Delete a chat
        
        Args:
            chat_id: Chat identifier
            
        Returns:
            bool: True if deleted successfully
        """
        return await self.db_service.delete_chat(chat_id)
