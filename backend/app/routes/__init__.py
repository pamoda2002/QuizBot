"""
Routes package initialization
"""
from fastapi import APIRouter
from .chat_routes import router as chat_router
from .message_routes import router as message_router
from .auth_routes import router as auth_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(chat_router, prefix="/chats", tags=["chats"])
api_router.include_router(message_router, prefix="/messages", tags=["messages"])

__all__ = ['api_router']
