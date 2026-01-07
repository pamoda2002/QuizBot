"""
Message Controller
Handles message-related business logic
"""
from typing import List, Optional
import uuid
from app.models.message import Message, MessageRole
from app.services.database_service import DatabaseService
from app.services.chatbot_service import ChatbotService


class MessageController:
    """Controller for message operations"""
    
    def __init__(self, db_service: DatabaseService, chatbot_service: ChatbotService):
        self.db_service = db_service
        self.chatbot_service = chatbot_service
    
    async def send_message(self, chat_id: str, content: str) -> dict:
        """
        Send a user message and get bot response
        
        Args:
            chat_id: Chat identifier
            content: Message content
            
        Returns:
            dict: Contains user message and bot response
        """
        # Create user message
        user_message = Message(
            id=f"msg_{uuid.uuid4().hex[:12]}",
            chat_id=chat_id,
            role=MessageRole.USER,
            content=content
        )
        await self.db_service.save_message(user_message)
        
        # Get chat history for context
        history = await self.db_service.get_chat_messages(chat_id)
        
        # Find the last question message (for updating with markers)
        last_question_msg_id = None
        for msg in reversed(history):
            if msg.role == MessageRole.ASSISTANT and "Type your answer (A, B, C, or D)" in msg.content:
                last_question_msg_id = msg.id
                print(f"[CONTROLLER] Found last question message: {last_question_msg_id}")
                break
        
        if not last_question_msg_id:
            print(f"[CONTROLLER] No last question found in history of {len(history)} messages")
        
        # Generate bot response (pass chat_id for quiz session tracking)
        bot_response_content = await self.chatbot_service.generate_response(
            message=content,
            history=history,
            chat_id=chat_id,
            db_service=self.db_service,
            last_question_msg_id=last_question_msg_id
        )
        
        # Check if response contains FEEDBACK with NEXT_QUESTION
        if bot_response_content.startswith('FEEDBACK:') and '\n\nNEXT_QUESTION:' in bot_response_content:
            # Split feedback and next question
            parts = bot_response_content.split('\n\nNEXT_QUESTION:', 1)
            feedback_part = parts[0]
            next_question_part = parts[1]
            
            # Save FEEDBACK message (hidden from UI)
            feedback_msg = Message(
                id=f"msg_{uuid.uuid4().hex[:12]}",
                chat_id=chat_id,
                role=MessageRole.ASSISTANT,
                content=feedback_part
            )
            await self.db_service.save_message(feedback_msg)
            
            # Save next question as separate message (visible in UI)
            bot_message = Message(
                id=f"msg_{uuid.uuid4().hex[:12]}",
                chat_id=chat_id,
                role=MessageRole.ASSISTANT,
                content=next_question_part
            )
            await self.db_service.save_message(bot_message)
            
            # Return with flag to indicate quiz answer
            return {
                "user_message": user_message,
                "bot_message": bot_message,
                "is_quiz_answer": True
            }
        else:
            # Normal message - save as is
            bot_message = Message(
                id=f"msg_{uuid.uuid4().hex[:12]}",
                chat_id=chat_id,
                role=MessageRole.ASSISTANT,
                content=bot_response_content
            )
            await self.db_service.save_message(bot_message)
        
        return {
            "user_message": user_message,
            "bot_message": bot_message
        }
    
    async def get_chat_messages(self, chat_id: str) -> List[Message]:
        """
        Get all messages for a chat
        
        Args:
            chat_id: Chat identifier
            
        Returns:
            List[Message]: List of messages
        """
        return await self.db_service.get_chat_messages(chat_id)
    
    async def get_message(self, message_id: str) -> Optional[Message]:
        """
        Get a specific message
        
        Args:
            message_id: Message identifier
            
        Returns:
            Optional[Message]: Message object if found
        """
        return await self.db_service.get_message(message_id)
