/**
 * Home Page - Main Chat Interface
 */
'use client';

import { useState, useEffect } from 'react';
import { Chat, Message, MessageRole } from '@/types';
import { apiService } from '@/services/api';
import { getUserId } from '@/lib/utils';
import ChatList from '@/components/ChatList';
import ChatWindow from '@/components/ChatWindow';
import AuthForm from '@/components/AuthForm';

export default function Home() {
  const [chats, setChats] = useState<Chat[]>([]);
  const [activeChat, setActiveChat] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [userId, setUserId] = useState<string>('');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);

  // Check authentication on mount
  useEffect(() => {
    const checkAuth = () => {
      const authenticated = apiService.isAuthenticated();
      setIsAuthenticated(authenticated);
      
      if (authenticated) {
        const user = apiService.getCurrentUser();
        if (user) {
          setUserId(user.id);
        }
      }
      setIsCheckingAuth(false);
    };
    
    checkAuth();
  }, []);

  // Load user's chats on mount
  useEffect(() => {
    if (userId && isAuthenticated) {
      loadChats();
    }
  }, [userId, isAuthenticated]);

  // Load messages when active chat changes
  useEffect(() => {
    if (activeChat) {
      loadMessages(activeChat);
    }
  }, [activeChat]);

  const loadChats = async () => {
    try {
      const userChats = await apiService.getUserChats(userId);
      setChats(userChats);
    } catch (error) {
      console.error('Failed to load chats:', error);
    }
  };

  const loadMessages = async (chatId: string) => {
    try {
      const chatMessages = await apiService.getChatMessages(chatId);
      console.log('[loadMessages] Received messages:', chatMessages.length);
      // Sanitize all message contents to ensure they're strings
      // Filter out FEEDBACK protocol messages - they're not for display
      const sanitized = chatMessages
        .filter(msg => {
          const content = typeof msg.content === 'string' ? msg.content : JSON.stringify(msg.content);
          return !content.startsWith('FEEDBACK:');
        })
        .map(msg => ({
          ...msg,
          content: typeof msg.content === 'string' ? msg.content : JSON.stringify(msg.content),
          // Add a render key to force React to re-render when content changes
          _renderKey: `${msg.id}-${Date.now()}`
        }));
      console.log('[loadMessages] Setting messages, sanitized count:', sanitized.length);
      setMessages(sanitized);
    } catch (error) {
      console.error('Failed to load messages:', error);
    }
  };

  const handleNewChat = async () => {
    try {
      const newChat = await apiService.createChat({
        user_id: userId,
        title: 'New Chat',
      });
      setChats([newChat, ...chats]);
      setActiveChat(newChat.id);
      setMessages([]);
    } catch (error) {
      console.error('Failed to create chat:', error);
    }
  };

  const handleSelectChat = (chatId: string) => {
    setActiveChat(chatId);
  };

  const handleDeleteChat = async (chatId: string) => {
    try {
      await apiService.deleteChat(chatId);
      setChats(chats.filter((chat) => chat.id !== chatId));
      if (activeChat === chatId) {
        setActiveChat(null);
        setMessages([]);
      }
    } catch (error) {
      console.error('Failed to delete chat:', error);
    }
  };

  const handleSendMessage = async (content: string) => {
    if (!activeChat) {
      // Create a new chat if none is active
      await handleNewChat();
      return;
    }

    setIsLoading(true);
    try {
      const response = await apiService.sendMessage({
        chat_id: activeChat,
        content,
      });

      console.log('[Quiz Debug] is_quiz_answer flag:', response.is_quiz_answer);

      // Check if this is a quiz answer response
      const isFeedback = response.bot_message.content.startsWith('FEEDBACK:') || response.is_quiz_answer;
      
      if (isFeedback) {
        console.log('[Quiz Debug] Detected quiz answer, reloading messages immediately...');
        // For quiz answers, reload all messages from database immediately
        // This ensures we get the updated question with markers
        await loadMessages(activeChat);
      } else {
        // Sanitize response messages before adding to state
        const sanitizedUserMsg = {
          ...response.user_message,
          content: typeof response.user_message.content === 'string' 
            ? response.user_message.content 
            : JSON.stringify(response.user_message.content)
        };
        const sanitizedBotMsg = {
          ...response.bot_message,
          content: typeof response.bot_message.content === 'string' 
            ? response.bot_message.content 
            : JSON.stringify(response.bot_message.content)
        };
        // Normal message flow
        setMessages([...messages, sanitizedUserMsg, sanitizedBotMsg]);
      }

      // Update chat's updated_at timestamp
      await loadChats();
    } catch (error: any) {
      console.error('Failed to send message:', error);
      
      // Format error for display
      let errorText = 'Unknown error occurred';
      if (error.response?.data?.detail) {
        const detail = error.response.data.detail;
        if (Array.isArray(detail)) {
          // Pydantic validation errors
          errorText = detail.map((e: any) => 
            `${e.loc ? e.loc.join('.') : 'field'}: ${e.msg || 'validation error'}`
          ).join('; ');
        } else if (typeof detail === 'string') {
          errorText = detail;
        } else {
          errorText = JSON.stringify(detail);
        }
      } else if (error.message) {
        errorText = error.message;
      }
      
      // Show error message to user
      const errorMsg: Message = {
        id: `error-${Date.now()}`,
        chat_id: activeChat,
        role: MessageRole.ASSISTANT,
        content: `Error: ${errorText}`,
        timestamp: new Date().toISOString(),
      };
      setMessages([...messages, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAuthSuccess = () => {
    const user = apiService.getCurrentUser();
    if (user) {
      setUserId(user.id);
      setIsAuthenticated(true);
    }
  };

  const handleLogout = () => {
    apiService.logout();
    setIsAuthenticated(false);
    setUserId('');
    setChats([]);
    setMessages([]);
    setActiveChat(null);
  };

  // Show loading state while checking authentication
  if (isCheckingAuth) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-600">Loading...</div>
      </div>
    );
  }

  // Show auth form if not authenticated
  if (!isAuthenticated) {
    return <AuthForm onAuthSuccess={handleAuthSuccess} />;
  }

  return (
    <div className="app-container">
      <ChatList
        chats={chats}
        activeChat={activeChat}
        onSelectChat={handleSelectChat}
        onNewChat={handleNewChat}
        onDeleteChat={handleDeleteChat}
        onLogout={handleLogout}
        username={apiService.getCurrentUser()?.username}
      />
      <ChatWindow
        messages={messages}
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
        chatId={activeChat || 'default'}
      />
    </div>
  );
}
