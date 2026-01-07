"""
App package initialization
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import api_router
from config.settings import settings


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        description="A simple chatbot API with MVC architecture"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(api_router, prefix="/api/v1")
    
    @app.get("/")
    async def root():
        return {
            "message": "Welcome to QuizBot API",
            "version": settings.VERSION,
            "docs": "/docs"
        }
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
    
    return app
