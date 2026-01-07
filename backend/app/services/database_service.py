"""
Database Service
Handles data persistence with SQLite
"""
from typing import List, Optional, Dict
import aiosqlite
import os
from datetime import datetime
from app.models.chat import Chat
from app.models.message import Message
from app.models.user import User


class DatabaseService:
    """Service for database operations"""
    
    def __init__(self):
        # In-memory storage (replace with actual database in production)
        self.chats: Dict[str, Chat] = {}
        self.messages: Dict[str, Message] = {}
        self.chat_messages: Dict[str, List[str]] = {}  # chat_id -> [message_ids]
        self.user_chats: Dict[str, List[str]] = {}  # user_id -> [chat_ids]
        
        # SQLite database path
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "users.db")
        self._initialized = False
    
    async def initialize(self):
        """Initialize database tables"""
        if self._initialized:
            return
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    username TEXT NOT NULL,
                    hashed_password TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            await db.commit()
        
        self._initialized = True
    
    async def save_chat(self, chat: Chat) -> Chat:
        """Save a chat to the database"""
        self.chats[chat.id] = chat
        if chat.user_id not in self.user_chats:
            self.user_chats[chat.user_id] = []
        if chat.id not in self.user_chats[chat.user_id]:
            self.user_chats[chat.user_id].append(chat.id)
        return chat
    
    async def get_chat(self, chat_id: str) -> Optional[Chat]:
        """Get a chat by ID"""
        return self.chats.get(chat_id)
    
    async def get_user_chats(self, user_id: str) -> List[Chat]:
        """Get all chats for a user"""
        chat_ids = self.user_chats.get(user_id, [])
        return [self.chats[chat_id] for chat_id in chat_ids if chat_id in self.chats]
    
    async def delete_chat(self, chat_id: str) -> bool:
        """Delete a chat"""
        if chat_id in self.chats:
            chat = self.chats[chat_id]
            del self.chats[chat_id]
            
            # Remove from user's chat list
            if chat.user_id in self.user_chats:
                self.user_chats[chat.user_id] = [
                    cid for cid in self.user_chats[chat.user_id] if cid != chat_id
                ]
            
            # Delete associated messages
            if chat_id in self.chat_messages:
                for msg_id in self.chat_messages[chat_id]:
                    if msg_id in self.messages:
                        del self.messages[msg_id]
                del self.chat_messages[chat_id]
            
            return True
        return False
    
    async def save_message(self, message: Message) -> Message:
        """Save a message to the database"""
        self.messages[message.id] = message
        if message.chat_id not in self.chat_messages:
            self.chat_messages[message.chat_id] = []
        self.chat_messages[message.chat_id].append(message.id)
        return message
    
    async def get_message(self, message_id: str) -> Optional[Message]:
        """Get a message by ID"""
        return self.messages.get(message_id)
    
    async def get_chat_messages(self, chat_id: str) -> List[Message]:
        """Get all messages for a chat"""
        message_ids = self.chat_messages.get(chat_id, [])
        return [self.messages[msg_id] for msg_id in message_ids if msg_id in self.messages]
    
    async def update_message_content(self, message_id: str, new_content: str) -> Optional[Message]:
        """Update the content of an existing message"""
        message = self.messages.get(message_id)
        if message:
            print(f"[DB] Updating message {message_id}")
            print(f"[DB] Old content length: {len(message.content)}")
            print(f"[DB] New content length: {len(new_content)}")
            message.content = new_content
            print(f"[DB] Message updated successfully. Content now: {new_content[:200]}...")
            return message
        else:
            print(f"[DB] Message {message_id} not found!")
        return None
    
    # User authentication methods
    async def create_user(self, user: User) -> User:
        """Create a new user in the database"""
        await self.initialize()
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO users (id, email, username, hashed_password, created_at) VALUES (?, ?, ?, ?, ?)",
                (user.id, user.email, user.username, user.hashed_password, user.created_at.isoformat())
            )
            await db.commit()
        
        return user
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        await self.initialize()
        
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM users WHERE email = ?", (email,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return User(
                        id=row['id'],
                        email=row['email'],
                        username=row['username'],
                        hashed_password=row['hashed_password'],
                        created_at=datetime.fromisoformat(row['created_at'])
                    )
        return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by ID"""
        await self.initialize()
        
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM users WHERE id = ?", (user_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return User(
                        id=row['id'],
                        email=row['email'],
                        username=row['username'],
                        hashed_password=row['hashed_password'],
                        created_at=datetime.fromisoformat(row['created_at'])
                    )
        return None
