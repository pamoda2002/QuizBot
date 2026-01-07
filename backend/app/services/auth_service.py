"""
Authentication Service
Handles user authentication, registration, and token management
"""
from datetime import datetime, timedelta
from typing import Optional
import uuid
import bcrypt
from jose import JWTError, jwt
from app.models.user import User, UserCreate, UserLogin, UserResponse, AuthResponse
from app.services.database_service import DatabaseService


# JWT configuration
SECRET_KEY = "your-secret-key-change-this-in-production"  # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30


class AuthService:
    """Service for authentication operations"""
    
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def get_password_hash(self, password: str) -> str:
        """Generate password hash"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def create_access_token(self, user_id: str, email: str) -> str:
        """Create JWT access token"""
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        to_encode = {
            "sub": user_id,
            "email": email,
            "exp": expire
        }
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def decode_token(self, token: str) -> Optional[dict]:
        """Decode and verify JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None
    
    async def signup(self, user_create: UserCreate) -> AuthResponse:
        """Register a new user"""
        # Check if user already exists
        existing_user = await self.db_service.get_user_by_email(user_create.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Create new user
        user_id = f"user_{uuid.uuid4().hex[:12]}"
        hashed_password = self.get_password_hash(user_create.password)
        
        user = User(
            id=user_id,
            email=user_create.email,
            username=user_create.username,
            hashed_password=hashed_password,
            created_at=datetime.utcnow()
        )
        
        await self.db_service.create_user(user)
        
        # Generate token
        token = self.create_access_token(user.id, user.email)
        
        # Return response
        user_response = UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            created_at=user.created_at
        )
        
        return AuthResponse(
            user=user_response,
            token=token,
            message="Signup successful"
        )
    
    async def login(self, user_login: UserLogin) -> AuthResponse:
        """Login an existing user"""
        # Get user from database
        user = await self.db_service.get_user_by_email(user_login.email)
        
        if not user:
            raise ValueError("Invalid email or password")
        
        # Verify password
        if not self.verify_password(user_login.password, user.hashed_password):
            raise ValueError("Invalid email or password")
        
        # Generate token
        token = self.create_access_token(user.id, user.email)
        
        # Return response
        user_response = UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            created_at=user.created_at
        )
        
        return AuthResponse(
            user=user_response,
            token=token,
            message="Login successful"
        )
    
    async def get_current_user(self, token: str) -> Optional[UserResponse]:
        """Get current user from token"""
        payload = self.decode_token(token)
        
        if not payload:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        user = await self.db_service.get_user_by_id(user_id)
        if not user:
            return None
        
        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            created_at=user.created_at
        )
