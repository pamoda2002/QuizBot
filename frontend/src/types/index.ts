/**
 * Type definitions for the chatbot application
 */

export enum MessageRole {
  USER = 'user',
  ASSISTANT = 'assistant',
  SYSTEM = 'system',
}

export interface Message {
  id: string;
  chat_id: string;
  role: MessageRole;
  content: string;
  timestamp: string;
}

export interface Chat {
  id: string;
  user_id: string;
  title: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface SendMessageRequest {
  chat_id: string;
  content: string;
}

export interface SendMessageResponse {
  user_message: Message;
  bot_message: Message;
}

export interface CreateChatRequest {
  user_id: string;
  title?: string;
}

export interface UpdateChatRequest {
  title: string;
}

// Authentication types
export interface User {
  id: string;
  email: string;
  username: string;
  created_at: string;
}

export interface SignupRequest {
  email: string;
  username: string;
  password: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  user: User;
  token: string;
  message: string;
}
