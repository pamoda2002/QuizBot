"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    APP_NAME: str = "QuizBot API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ]
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Groq API settings
    GROQ_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
