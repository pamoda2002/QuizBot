"""
Chat Model
Represents a chat session
"""
from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field


class Chat(BaseModel):
    """Chat session model"""
    id: str = Field(..., description="Unique chat identifier")
    user_id: str = Field(..., description="User identifier")
    title: str = Field(default="New Chat", description="Chat title")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field(default_factory=lambda: datetime.now())
    is_active: bool = Field(default=True)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "chat_123",
                "user_id": "user_456",
                "title": "New Chat",
                "is_active": True
            }
        }
