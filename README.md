## 📋 Project Overview

**QuizBot** is a comprehensive full-stack conversational AI quiz platform designed to revolutionize the way people learn and practice. Built with a modern tech stack and powered by Groq's cutting-edge LLM technology, QuizBot delivers real-time, intelligent assessments across multiple knowledge domains including Programming, DevOps, and General Knowledge.

### 🌟 What Makes QuizBot Special?

The system provides a complete solution for managing learning assessments through:

- **Intelligent Question Generation** - AI-powered quiz creation tailored to user skill levels
- **Real-time Feedback System** - Instant answer evaluation 
- **Conversational Interface** - Natural chat-based learning experience
- **Session Management** - Persistent chat history and multi-assessment tracking
- **User Authentication** - Secure role-based access with JWT tokens
- **Streaming Responses** - Ultra-fast AI responses using Groq's LPU technology

Whether you're an individual learner, educator, or organization looking to assess skills, QuizBot adapts to your workflow and allows you to focus on what truly matters: **effective learning and skill development**.

---

## ✨ Key Features

### 🔐 Authentication & User Management
- **Secure User Registration** - Password hashing with bcrypt
- **JWT Token Authentication** - Stateless session management
- **User Profile Dropdown** - Quick access to account settings
- **Session Persistence** - Automatic login state retention
- **Role-Based Access** - Future support for different user roles

### 💬 Conversational AI Interface
- **Natural Chat Experience** - Intuitive message-based interaction
- **Real-time Streaming** - Live response generation from AI
- **Message History** - Complete conversation tracking
- **Context Awareness** - AI remembers previous interactions

### 🎨 User Experience
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- **Loading States** - Visual feedback during AI processing
- **Error Handling** - Graceful degradation with user-friendly messages
- **Empty States** - Helpful prompts when no data exists
- **Smooth Animations** - Polished transitions and interactions

### 🔒 Security & Privacy
- **Password Encryption** - Industry-standard bcrypt hashing
- **HTTPS Ready** - Secure data transmission
- **SQL Injection Protection** - ORM-based database queries
- **CORS Configuration** - Controlled cross-origin requests
- **Token Expiration** - Automatic session timeout
- **Data Validation** - Pydantic models for input sanitization

---

## 🛠️ Tech Stack

### Frontend

* **TypeScript** – Type-safe development
* **React** – Component-based UI library
* **Next.js** – App Router framework for routing, SSR, and performance
* **Axios** – HTTP client for API communication
* **Custom CSS** – Handcrafted styling (no CSS framework)

### Backend

* **Python** – Core backend language
* **FastAPI** – High-performance async web framework
* **Pydantic** – Data validation and schema management
* **Uvicorn** – ASGI server for FastAPI
* **python-jose** – JWT authentication (**not PyJWT**)
* **Passlib with bcrypt** – Secure password hashing
* **python-dotenv** – Environment variable management
* **python-multipart** – File upload support
* **aiosqlite** – Async SQLite driver (database layer present; implementation evolving)

### AI / LLM

* **Groq API** – High-speed LLM inference platform
* **Llama 3.3 70B Versatile** – Primary language model 
* **PyPDF2** – PDF parsing for quiz/question generation
* **Non-streaming responses** – Standard request/response inference pattern

## 💡 Closing Note

**QuizBot** was created with a heartfelt mission to democratize learning and make quality education accessible to everyone, everywhere. By offering an intuitive and comprehensive platform powered by cutting-edge AI technology, our goal is to empower learners, educators, and organizations to collaborate effortlessly and achieve their educational objectives with confidence.

Powered by modern web technologies and state-of-the-art language models, the system delivers a smooth and reliable experience—managing everything from simple knowledge checks to complex technical assessments—while ensuring strong security and data integrity at every step.

Whether you're an individual learner looking to upskill, an educator managing student assessments, or an organization conducting technical interviews, QuizBot adapts to your workflow and allows you to focus on what truly matters: **effective learning and meaningful skill development**.


###  Mission

Make Learning Fun with QuizBot ❤️
QuizBot is more than just a quiz platform—it’s your personal companion for smarter, more engaging learning. Explore, practice, and challenge yourself across multiple domains, all with instant feedback and interactive AI-powered quizzes. Thank you for checking out QuizBot—let’s make learning fun, accessible, and rewarding for everyone!
