"""
Authentication Routes
Handles authentication endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from app.models.user import UserCreate, UserLogin, AuthResponse
from app.services.auth_service import AuthService
from app.dependencies import get_auth_service

router = APIRouter()


@router.post("/signup", response_model=AuthResponse)
async def signup(
    user_create: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Register a new user
    
    - **email**: User's email address (must be unique)
    - **username**: User's display name
    - **password**: User's password (will be hashed)
    """
    try:
        return await auth_service.signup(user_create)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")


@router.post("/login", response_model=AuthResponse)
async def login(
    user_login: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Login an existing user
    
    - **email**: User's email address
    - **password**: User's password
    """
    try:
        return await auth_service.login(user_login)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")
