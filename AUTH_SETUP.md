# Authentication Setup Guide

## Overview
This chatbot application now includes a complete authentication system with:
- User signup (registration)
- User login  
- SQLite database for secure user storage
- JWT token-based authentication
- Password hashing with bcrypt

## Backend Implementation

### Database
- **Location**: `backend/data/users.db`
- **Type**: SQLite database
- **Table**: `users` with columns:
  - `id` - Unique user identifier
  - `email` - User email (unique)
  - `username` - Display name
  - `hashed_password` - Bcrypt hashed password
  - `created_at` - Registration timestamp

### API Endpoints

#### Signup
```bash
POST http://localhost:8000/api/v1/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "yourpassword"
}
```

Response:
```json
{
  "user": {
    "id": "user_xxx",
    "email": "user@example.com",
    "username": "johndoe",
    "created_at": "2026-01-01T00:00:00"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Signup successful"
}
```

#### Login
```bash
POST http://localhost:8000/api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

Response: Same as signup

## Frontend Implementation

### Features
- Beautiful authentication form with toggle between signup/login
- Form validation
- Error handling
- Token storage in localStorage
- Automatic redirect after successful authentication
- Session persistence

### User Flow
1. User opens the application
2. If not authenticated, sees the AuthForm
3. Can choose to:
   - **Sign Up**: Enter email, username, and password
   - **Log In**: Enter email and password
4. On success:
   - Token and user info saved to localStorage
   - Redirected to chat interface
5. Subsequent visits: Automatically logged in if token exists

## Security Features

### Password Security
- Passwords are hashed using bcrypt before storage
- Never stored in plain text
- Salt automatically generated per password

### Token Security
- JWT tokens with 30-day expiration
- Tokens include user ID and email
- Stored in browser localStorage
- Sent with every API request via Authorization header

### API Security
- Axios interceptor adds token to all requests
- Backend validates tokens (can be implemented as needed)
- CORS configured for frontend access

## Running the Application

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```
Backend runs on: http://localhost:8000

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on: http://localhost:3000

## Testing Authentication

Run the test script:
```bash
cd backend
python tests/test_auth.py
```

This will:
- Create a test user
- Test login
- Verify password validation
- Check database creation

## Files Modified/Created

### Backend
- `backend/requirements.txt` - Added auth dependencies
- `backend/app/models/user.py` - User models and schemas
- `backend/app/services/auth_service.py` - Authentication logic
- `backend/app/services/database_service.py` - SQLite user operations
- `backend/app/routes/auth_routes.py` - Auth API endpoints
- `backend/app/dependencies.py` - Added auth service dependency
- `backend/tests/test_auth.py` - Authentication tests

### Frontend
- `frontend/src/types/index.ts` - Auth type definitions
- `frontend/src/services/api.ts` - Auth API methods
- `frontend/src/components/AuthForm.tsx` - Authentication UI
- `frontend/src/app/page.tsx` - Auth state management

## Environment Variables

For production, create a `.env` file:

```env
# Backend
SECRET_KEY=your-secret-key-here-use-strong-random-string
DATABASE_URL=sqlite:///./data/users.db

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation (Swagger UI).

## Troubleshooting

### "User already exists" error
- The email is already registered
- Try logging in instead or use a different email

### "Invalid email or password" error  
- Check credentials are correct
- Password is case-sensitive

### Database locked error
- Close any other processes accessing the database
- Restart the backend server

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check CORS settings in backend
- Verify NEXT_PUBLIC_API_URL in frontend
