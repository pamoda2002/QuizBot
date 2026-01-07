/**
 * API Service
 * Handles all API communication with the backend
 */
import axios, { AxiosInstance } from 'axios';
import {
  Chat,
  Message,
  SendMessageRequest,
  SendMessageResponse,
  CreateChatRequest,
  UpdateChatRequest,
  SignupRequest,
  LoginRequest,
  AuthResponse,
} from '@/types';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add interceptor to include auth token
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('auth_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  // Authentication endpoints
  async signup(data: SignupRequest): Promise<AuthResponse> {
    const response = await this.api.post<AuthResponse>('/auth/signup', data);
    // Store token in localStorage
    if (response.data.token) {
      localStorage.setItem('auth_token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  }

  async login(data: LoginRequest): Promise<AuthResponse> {
    const response = await this.api.post<AuthResponse>('/auth/login', data);
    // Store token in localStorage
    if (response.data.token) {
      localStorage.setItem('auth_token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  }

  logout(): void {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem('auth_token');
  }

  getCurrentUser(): any {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  }

  // Chat endpoints
  async createChat(data: CreateChatRequest): Promise<Chat> {
    const response = await this.api.post<Chat>('/chats/', data);
    return response.data;
  }

  async getChat(chatId: string): Promise<Chat> {
    const response = await this.api.get<Chat>(`/chats/${chatId}`);
    return response.data;
  }

  async getUserChats(userId: string): Promise<Chat[]> {
    const response = await this.api.get<Chat[]>(`/chats/user/${userId}`);
    return response.data;
  }

  async updateChat(chatId: string, data: UpdateChatRequest): Promise<Chat> {
    const response = await this.api.put<Chat>(`/chats/${chatId}`, data);
    return response.data;
  }

  async deleteChat(chatId: string): Promise<void> {
    await this.api.delete(`/chats/${chatId}`);
  }

  async getSuggestedTopics(): Promise<string[]> {
    const response = await this.api.get<{ topics: string[] }>('/chats/topics');
    return response.data.topics;
  }

  // Message endpoints
  async sendMessage(data: SendMessageRequest): Promise<SendMessageResponse> {
    const response = await this.api.post<SendMessageResponse>('/messages/send', data);
    return response.data;
  }

  async getChatMessages(chatId: string): Promise<Message[]> {
    const response = await this.api.get<Message[]>(`/messages/chat/${chatId}`);
    return response.data;
  }

  async getMessage(messageId: string): Promise<Message> {
    const response = await this.api.get<Message>(`/messages/${messageId}`);
    return response.data;
  }
}

export const apiService = new ApiService();
