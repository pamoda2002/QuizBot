/**
 * ChatWindow Component
 * Main chat interface
 */
'use client';

import { useEffect, useRef, useState } from 'react';
import { Message } from '@/types';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import SuccessNotification from './SuccessNotification';
import FileUpload from './FileUpload';
import { apiService } from '@/services/api';

interface ChatWindowProps {
  messages: Message[];
  onSendMessage: (content: string) => void;
  isLoading?: boolean;
  chatId?: string;
}

export default function ChatWindow({
  messages,
  onSendMessage,
  isLoading = false,
  chatId = 'default',
}: ChatWindowProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [showSuccess, setShowSuccess] = useState(false);
  const [uploadedPdf, setUploadedPdf] = useState<string | null>(null);
  const [isQuizActive, setIsQuizActive] = useState(false);
  const [suggestedTopics, setSuggestedTopics] = useState<string[]>([
    'Python', 'Data Science', 'Web Development', 
    'Cloud Computing', 'React', 'Databases'
  ]);
  const [loadingTopics, setLoadingTopics] = useState(true);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Fetch AI-generated topic suggestions on mount
  useEffect(() => {
    const fetchTopics = async () => {
      try {
        setLoadingTopics(true);
        const topics = await apiService.getSuggestedTopics();
        setSuggestedTopics(topics);
      } catch (error) {
        console.error('Error fetching topics:', error);
        // Keep default topics on error
      } finally {
        setLoadingTopics(false);
      }
    };
    
    fetchTopics();
  }, []);

  // Detect if quiz is active and correct answers
  useEffect(() => {
    if (messages.length > 0) {
      const lastMessage = messages[messages.length - 1];
      
      // Check if quiz is active (last bot message has quiz question format)
      if (lastMessage.role === 'assistant') {
        const hasQuizQuestion = /[A-D]\.\ .+/.test(lastMessage.content) && 
                               (lastMessage.content.includes('Assessment') || 
                                lastMessage.content.includes('Question'));
        const isQuizComplete = lastMessage.content.includes('Quiz Complete');
        setIsQuizActive(hasQuizQuestion && !isQuizComplete);
        
        // Detect correct answers for notification
        if (lastMessage.content.includes('✅ Correct!')) {
          setShowSuccess(true);
        }
      }
    } else {
      setIsQuizActive(false);
    }
  }, [messages]);

  const handleTopicClick = (topic: string) => {
    onSendMessage(`quiz ${topic}`);
  };

  const handleStopQuiz = () => {
    onSendMessage('stop');
  };

  const handleUploadSuccess = (filename: string) => {
    setUploadedPdf(filename);
    onSendMessage(`quiz pdf`);
  };

  return (
    <div className="chat-window">
      <SuccessNotification show={showSuccess} onHide={() => setShowSuccess(false)} />
      <div className="chat-window-header">
        <h1>Personal Assessment Platform</h1>
      </div>
      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="empty-chat">
            <h2>Personal Assessment Platform</h2>
            <p style={{ marginBottom: '48px', fontSize: '16px', color: '#94a3b8', fontWeight: '400', letterSpacing: '0.02em' }}>
              Advanced AI-Powered Knowledge Assessment System
            </p>
            <div style={{ 
              padding: '48px', 
              background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)', 
              borderRadius: '16px',
              maxWidth: '720px',
              textAlign: 'left',
              border: '1px solid #334155',
              boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(51, 65, 85, 0.5)',
            }}>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                marginBottom: '32px',
                paddingBottom: '24px',
                borderBottom: '1px solid #334155'
              }}>
                <div style={{
                  width: '4px',
                  height: '48px',
                  borderRadius: '2px',
                  background: 'linear-gradient(180deg, #3b82f6 0%, #1d4ed8 100%)',
                  marginRight: '20px',
                  boxShadow: '0 0 20px rgba(59, 130, 246, 0.4)'
                }}>
                </div>
                <h3 style={{ 
                  color: '#f1f5f9', 
                  fontSize: '20px', 
                  fontWeight: '600',
                  letterSpacing: '0.02em',
                  margin: 0,
                  textTransform: 'uppercase'
                }}>
                  Select Assessment Topic
                </h3>
              </div>
              <div style={{ 
                background: 'rgba(15, 23, 42, 0.6)', 
                padding: '32px', 
                borderRadius: '12px', 
                border: '1px solid #334155',
                boxShadow: 'inset 0 2px 4px rgba(0, 0, 0, 0.3)'
              }}>
                <p style={{ fontSize: '11px', color: '#94a3b8', fontWeight: '600', marginBottom: '20px', textTransform: 'uppercase', letterSpacing: '1.5px' }}>
                  {loadingTopics ? 'Loading AI Suggestions...' : 'Most Requested Topics (AI Generated)'}
                </p>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '14px' }}>
                  {suggestedTopics.map((topic, index) => {
                    const colors = [
                      { border: '#3b82f6', shadow: 'rgba(59, 130, 246, 0.2)', hover: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)', hoverShadow: 'rgba(59, 130, 246, 0.4)' },
                      { border: '#8b5cf6', shadow: 'rgba(139, 92, 246, 0.2)', hover: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)', hoverShadow: 'rgba(139, 92, 246, 0.4)' },
                      { border: '#10b981', shadow: 'rgba(16, 185, 129, 0.2)', hover: 'linear-gradient(135deg, #10b981 0%, #059669 100%)', hoverShadow: 'rgba(16, 185, 129, 0.4)' },
                      { border: '#06b6d4', shadow: 'rgba(6, 182, 212, 0.2)', hover: 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)', hoverShadow: 'rgba(6, 182, 212, 0.4)' },
                      { border: '#ec4899', shadow: 'rgba(236, 72, 153, 0.2)', hover: 'linear-gradient(135deg, #ec4899 0%, #db2777 100%)', hoverShadow: 'rgba(236, 72, 153, 0.4)' },
                      { border: '#f59e0b', shadow: 'rgba(245, 158, 11, 0.2)', hover: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)', hoverShadow: 'rgba(245, 158, 11, 0.4)' }
                    ];
                    const color = colors[index % colors.length];
                    
                    return (
                      <button 
                        key={index}
                        onClick={() => handleTopicClick(topic)}
                        disabled={loadingTopics}
                        style={{ 
                          background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)', 
                          color: '#e2e8f0', 
                          padding: '18px 14px', 
                          borderRadius: '8px', 
                          fontWeight: '500', 
                          textAlign: 'center', 
                          fontSize: '13px', 
                          border: `1px solid ${color.border}`, 
                          cursor: loadingTopics ? 'not-allowed' : 'pointer', 
                          transition: 'all 0.2s ease', 
                          boxShadow: `0 4px 12px ${color.shadow}`, 
                          letterSpacing: '0.5px', 
                          textTransform: 'uppercase',
                          opacity: loadingTopics ? 0.6 : 1
                        }}
                        onMouseOver={(e) => { 
                          if (!loadingTopics) {
                            e.currentTarget.style.transform = 'translateY(-2px)'; 
                            e.currentTarget.style.boxShadow = `0 6px 20px ${color.hoverShadow}`; 
                            e.currentTarget.style.background = color.hover; 
                            e.currentTarget.style.color = '#ffffff'; 
                          }
                        }}
                        onMouseOut={(e) => { 
                          e.currentTarget.style.transform = 'translateY(0)'; 
                          e.currentTarget.style.boxShadow = `0 4px 12px ${color.shadow}`; 
                          e.currentTarget.style.background = 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)'; 
                          e.currentTarget.style.color = '#e2e8f0'; 
                        }}
                      >
                        {topic}
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        ) : (
          messages.map((message, index) => (
            <ChatMessage 
              key={`${message.id}-${index}-${message.content.substring(0, 50)}`} 
              message={message} 
              onSendMessage={onSendMessage} 
            />
          ))
        )}
        {isLoading && (
          <div className="loading-indicator">
            <div className="typing-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      {uploadedPdf && (
        <div className="pdf-status">
          PDF Ready: <strong>{uploadedPdf}</strong>
        </div>
      )}
      {isQuizActive && (
        <div style={{
          padding: '12px 20px',
          background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)',
          borderTop: '1px solid #334155',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center'
        }}>
          <button
            onClick={handleStopQuiz}
            disabled={isLoading}
            style={{
              background: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
              color: '#ffffff',
              border: '1px solid #b91c1c',
              padding: '10px 32px',
              borderRadius: '8px',
              fontSize: '14px',
              fontWeight: '600',
              cursor: isLoading ? 'not-allowed' : 'pointer',
              textTransform: 'uppercase',
              letterSpacing: '0.5px',
              boxShadow: '0 4px 12px rgba(239, 68, 68, 0.3)',
              transition: 'all 0.2s ease',
              opacity: isLoading ? 0.6 : 1
            }}
            onMouseOver={(e) => {
              if (!isLoading) {
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow = '0 6px 20px rgba(239, 68, 68, 0.5)';
              }
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(239, 68, 68, 0.3)';
            }}
          >
            ⏹ STOP QUIZ
          </button>
        </div>
      )}
      <ChatInput 
        onSendMessage={onSendMessage} 
        disabled={isLoading}
        chatId={chatId}
        onUploadSuccess={handleUploadSuccess}
      />
    </div>
  );
}
