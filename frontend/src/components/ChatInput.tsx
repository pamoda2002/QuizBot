/**
 * ChatInput Component
 * Input field for sending messages
 */
'use client';

import { useState, KeyboardEvent } from 'react';
import FileUpload from './FileUpload';

interface ChatInputProps {
  onSendMessage: (content: string) => void;
  disabled?: boolean;
  chatId?: string;
  onUploadSuccess?: (filename: string) => void;
}

export default function ChatInput({ 
  onSendMessage, 
  disabled = false,
  chatId = 'default',
  onUploadSuccess 
}: ChatInputProps) {
  const [message, setMessage] = useState('');

  const handleSend = () => {
    if (message.trim() && !disabled) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-input-container">
      {onUploadSuccess && (
        <FileUpload 
          chatId={chatId} 
          onUploadSuccess={onUploadSuccess}
        />
      )}
      <input
        type="text"
        className="chat-input"
        placeholder="Type your message..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={handleKeyPress}
        disabled={disabled}
      />
      <button
        className="send-button"
        onClick={handleSend}
        disabled={disabled || !message.trim()}
      >
        Send
      </button>
    </div>
  );
}
