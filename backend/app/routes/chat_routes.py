"""
Chat Routes
API endpoints for chat operations
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from app.controllers.chat_controller import ChatController
from app.models.chat import Chat
from app.dependencies import get_chat_controller
from app.services.chatbot_service import ChatbotService
from app.services.database_service import DatabaseService

router = APIRouter()


class CreateChatRequest(BaseModel):
    """Request model for creating a chat"""
    user_id: str
    title: str = "New Chat"


class UpdateChatRequest(BaseModel):
    """Request model for updating a chat"""
    title: str


@router.get("/topics")
async def get_suggested_topics():
    """Get AI-generated topic suggestions based on actual user demand"""
    try:
        # Get all user chats from database to analyze trends
        db_service = DatabaseService()
        
        # Collect all chats across all users (for aggregate analysis)
        all_chat_titles = []
        for user_id, chat_ids in db_service.user_chats.items():
            for chat_id in chat_ids:
                chat = db_service.chats.get(chat_id)
                if chat:
                    all_chat_titles.append({
                        'title': chat.title,
                        'created_at': chat.created_at.isoformat()
                    })
        
        # Sort by most recent and limit to last 100 chats for analysis
        all_chat_titles.sort(key=lambda x: x['created_at'], reverse=True)
        recent_chats = all_chat_titles[:100]
        
        # Generate topics using AI based on actual user data
        chatbot_service = ChatbotService()
        topics = await chatbot_service.get_suggested_topics(recent_chats if recent_chats else None)
        
        return {"topics": topics}
    except Exception as e:
        print(f"Error in get_suggested_topics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=Chat)
async def create_chat(
    request: CreateChatRequest,
    controller: ChatController = Depends(get_chat_controller)
):
    """Create a new chat session"""
    try:
        chat = await controller.create_chat(request.user_id, request.title)
        return chat
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{chat_id}", response_model=Chat)
async def get_chat(
    chat_id: str,
    controller: ChatController = Depends(get_chat_controller)
):
    """Get a specific chat by ID"""
    chat = await controller.get_chat(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.get("/user/{user_id}", response_model=List[Chat])
async def get_user_chats(
    user_id: str,
    controller: ChatController = Depends(get_chat_controller)
):
    """Get all chats for a user"""
    try:
        chats = await controller.get_user_chats(user_id)
        return chats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{chat_id}", response_model=Chat)
async def update_chat(
    chat_id: str,
    request: UpdateChatRequest,
    controller: ChatController = Depends(get_chat_controller)
):
    """Update a chat's title"""
    chat = await controller.update_chat(chat_id, request.title)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.delete("/{chat_id}")
async def delete_chat(
    chat_id: str,
    controller: ChatController = Depends(get_chat_controller)
):
    """Delete a chat"""
    success = await controller.delete_chat(chat_id)
    if not success:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"message": "Chat deleted successfully"}
