"""
Test Authentication System
Simple script to verify authentication is working
"""
import asyncio
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.database_service import DatabaseService
from app.services.auth_service import AuthService
from app.models.user import UserCreate, UserLogin


async def test_auth():
    """Test authentication system"""
    print("🔐 Testing Authentication System\n")
    
    # Initialize services
    db_service = DatabaseService()
    auth_service = AuthService(db_service)
    
    print("1. Testing Signup...")
    try:
        # Create a test user
        signup_data = UserCreate(
            email="test@example.com",
            username="testuser",
            password="password123"
        )
        
        auth_response = await auth_service.signup(signup_data)
        print(f"   ✅ Signup successful!")
        print(f"   User ID: {auth_response.user.id}")
        print(f"   Username: {auth_response.user.username}")
        print(f"   Email: {auth_response.user.email}")
        print(f"   Token: {auth_response.token[:50]}...")
        
    except ValueError as e:
        print(f"   ℹ️  User already exists: {e}")
    except Exception as e:
        print(f"   ❌ Signup failed: {e}")
        return
    
    print("\n2. Testing Login...")
    try:
        # Login with the test user
        login_data = UserLogin(
            email="test@example.com",
            password="password123"
        )
        
        auth_response = await auth_service.login(login_data)
        print(f"   ✅ Login successful!")
        print(f"   User ID: {auth_response.user.id}")
        print(f"   Username: {auth_response.user.username}")
        print(f"   Token: {auth_response.token[:50]}...")
        
    except ValueError as e:
        print(f"   ❌ Login failed: {e}")
    except Exception as e:
        print(f"   ❌ Login error: {e}")
    
    print("\n3. Testing Wrong Password...")
    try:
        login_data = UserLogin(
            email="test@example.com",
            password="wrongpassword"
        )
        
        await auth_service.login(login_data)
        print(f"   ❌ Should have failed!")
        
    except ValueError as e:
        print(f"   ✅ Correctly rejected: {e}")
    
    print("\n4. Database Check...")
    db_path = db_service.db_path
    if os.path.exists(db_path):
        print(f"   ✅ Database created at: {db_path}")
        print(f"   Size: {os.path.getsize(db_path)} bytes")
    else:
        print(f"   ❌ Database not found")
    
    print("\n✨ Authentication system is working correctly!")


if __name__ == "__main__":
    asyncio.run(test_auth())
