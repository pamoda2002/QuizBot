# QuizBot - Simple Chatbot Application

A full-stack chatbot application built with Python (FastAPI) backend following MVC architecture and Next.js (React) frontend.

## 🏗️ Project Structure

```
QuizBot/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── controllers/    # Business logic layer
│   │   │   ├── chat_controller.py
│   │   │   └── message_controller.py
│   │   ├── models/         # Data models
│   │   │   ├── chat.py
│   │   │   └── message.py
│   │   ├── routes/         # API endpoints
│   │   │   ├── chat_routes.py
│   │   │   └── message_routes.py
│   │   ├── services/       # Service layer
│   │   │   ├── database_service.py
│   │   │   └── chatbot_service.py
│   │   ├── utils/          # Utility functions
│   │   └── dependencies.py # Dependency injection
│   ├── config/             # Configuration
│   │   └── settings.py
│   ├── tests/              # Test files
│   ├── main.py             # Application entry point
│   └── requirements.txt    # Python dependencies
│
└── frontend/               # Next.js frontend
    ├── src/
    │   ├── app/           # Next.js app directory
    │   │   ├── page.tsx   # Main page
    │   │   ├── layout.tsx # Root layout
    │   │   └── globals.css
    │   ├── components/    # React components
    │   │   ├── ChatList.tsx
    │   │   ├── ChatWindow.tsx
    │   │   ├── ChatMessage.tsx
    │   │   └── ChatInput.tsx
    │   ├── services/      # API services
    │   │   └── api.ts
    │   ├── types/         # TypeScript types
    │   │   └── index.ts
    │   └── lib/           # Utilities
    │       └── utils.ts
    ├── public/            # Static assets
    ├── package.json
    └── tsconfig.json
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```powershell
   cd backend
   ```

2. Create a virtual environment:
   ```powershell
   python -m venv venv
   ```

3. Activate the virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

5. Create a `.env` file (copy from `.env.example`):
   ```powershell
   copy .env.example .env
   ```

6. Run the backend server:
   ```powershell
   python main.py
   ```

   The backend API will be available at `http://localhost:8000`
   API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
   ```powershell
   cd frontend
   ```

2. Install dependencies:
   ```powershell
   npm install
   ```

3. Create a `.env.local` file (copy from `.env.local.example`):
   ```powershell
   copy .env.local.example .env.local
   ```

4. Run the development server:
   ```powershell
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

## 📋 Features

- **Chat Management**: Create, view, update, and delete chat sessions
- **Real-time Messaging**: Send messages and receive bot responses
- **Chat History**: View all messages in a conversation
- **User Sessions**: Multiple chats per user
- **Responsive UI**: Clean and modern interface
- **MVC Architecture**: Clean separation of concerns in the backend
- **Type Safety**: Full TypeScript support in the frontend

## 🏛️ Architecture

### Backend (MVC Pattern)

- **Models**: Define data structures using Pydantic
- **Controllers**: Handle business logic and orchestrate services
- **Routes**: Define API endpoints and handle HTTP requests
- **Services**: Encapsulate reusable business logic
- **Dependencies**: Manage dependency injection

### Frontend

- **Components**: Reusable React components
- **Services**: API communication layer
- **Types**: TypeScript type definitions
- **Utilities**: Helper functions

## 🔌 API Endpoints

### Chats
- `POST /api/v1/chats/` - Create a new chat
- `GET /api/v1/chats/{chat_id}` - Get chat by ID
- `GET /api/v1/chats/user/{user_id}` - Get all user chats
- `PUT /api/v1/chats/{chat_id}` - Update chat title
- `DELETE /api/v1/chats/{chat_id}` - Delete chat

### Messages
- `POST /api/v1/messages/send` - Send a message
- `GET /api/v1/messages/chat/{chat_id}` - Get chat messages
- `GET /api/v1/messages/{message_id}` - Get message by ID

## 🛠️ Technologies Used

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation and settings management
- **Uvicorn** - ASGI server

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Axios** - HTTP client
- **CSS** - Custom styling

## 📝 Development Notes

- The backend uses in-memory storage for demonstration. Replace `DatabaseService` with a real database (PostgreSQL, MongoDB, etc.) for production.
- The chatbot responses are currently rule-based. Integrate with AI services (OpenAI, Anthropic, etc.) for smarter responses.
- User authentication is simplified. Implement proper auth (JWT, OAuth) for production.

## 🔜 Future Enhancements

- [ ] Add user authentication
- [ ] Integrate with LLM APIs (OpenAI, etc.)
- [ ] Add database persistence (PostgreSQL/MongoDB)
- [ ] Implement real-time updates with WebSockets
- [ ] Add message editing and deletion
- [ ] Support for file uploads
- [ ] Chat export functionality
- [ ] Dark mode support

## 📄 License

This project is open source and available under the MIT License.
