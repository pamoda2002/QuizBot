"""
Message Model
Represents a chat message
"""
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class MessageRole(str, Enum):
    """Message role enumeration"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):
    """Chat message model"""
    id: str = Field(..., description="Unique message identifier")
    chat_id: str = Field(..., description="Associated chat ID")
    role: MessageRole = Field(..., description="Message role (user/assistant/system)")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=lambda: datetime.now())
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "msg_123",
                "chat_id": "chat_456",
                "role": "user",
                "content": "Hello, how are you?",
            }
        }
