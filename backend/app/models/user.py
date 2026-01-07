"""
User Model
Represents a user in the system
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class User(BaseModel):
    """User model"""
    id: str
    email: EmailStr
    username: str
    hashed_password: str
    created_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "user_123",
                "email": "user@example.com",
                "username": "johndoe",
                "hashed_password": "$2b$12$...",
                "created_at": "2024-01-01T00:00:00"
            }
        }


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    email: EmailStr
    username: str
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "securepassword123"
            }
        }


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }


class UserResponse(BaseModel):
    """Schema for user response (without password)"""
    id: str
    email: EmailStr
    username: str
    created_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "user_123",
                "email": "user@example.com",
                "username": "johndoe",
                "created_at": "2024-01-01T00:00:00"
            }
        }


class AuthResponse(BaseModel):
    """Schema for authentication response"""
    user: UserResponse
    token: str
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "id": "user_123",
                    "email": "user@example.com",
                    "username": "johndoe",
                    "created_at": "2024-01-01T00:00:00"
                },
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "message": "Login successful"
            }
        }
