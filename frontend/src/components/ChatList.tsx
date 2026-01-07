/**
 * ChatList Component
 * Displays list of user's chats
 */
'use client';

import { Chat } from '@/types';
import { truncateText, formatDate } from '@/lib/utils';
import { useState, useRef, useEffect } from 'react';

interface ChatListProps {
  chats: Chat[];
  activeChat: string | null;
  onSelectChat: (chatId: string) => void;
  onNewChat: () => void;
  onDeleteChat: (chatId: string) => void;
  onLogout?: () => void;
  username?: string;
}

export default function ChatList({
  chats,
  activeChat,
  onSelectChat,
  onNewChat,
  onDeleteChat,
  onLogout,
  username,
}: ChatListProps) {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogoutClick = () => {
    setIsDropdownOpen(false);
    onLogout?.();
  };

  return (
    <div className="chat-list">
      <div className="chat-list-header">
        <div className="header-content">
          <h2>QuizBot</h2>
        </div>
        <div className="header-actions">
          <button className="new-chat-button" onClick={onNewChat}>
            New Assessment
          </button>
          {onLogout && username && (
            <div className="user-profile-dropdown" ref={dropdownRef}>
              <button 
                className="user-profile-button" 
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              >
                <div className="user-avatar">
                  {username.charAt(0).toUpperCase()}
                </div>
                <span className="user-name">{username}</span>
                <svg 
                  className={`dropdown-arrow ${isDropdownOpen ? 'open' : ''}`}
                  width="12" 
                  height="12" 
                  viewBox="0 0 12 12" 
                  fill="none"
                >
                  <path 
                    d="M2 4L6 8L10 4" 
                    stroke="currentColor" 
                    strokeWidth="2" 
                    strokeLinecap="round" 
                    strokeLinejoin="round"
                  />
                </svg>
              </button>
              {isDropdownOpen && (
                <div className="dropdown-menu">
                  <div className="dropdown-header">
                    <div className="dropdown-user-info">
                      <div className="dropdown-avatar">
                        {username.charAt(0).toUpperCase()}
                      </div>
                      <div className="dropdown-user-details">
                        <div className="dropdown-username">{username}</div>
                        <div className="dropdown-user-role">User</div>
                      </div>
                    </div>
                  </div>
                  <div className="dropdown-divider"></div>
                  <button className="dropdown-item logout-item" onClick={handleLogoutClick}>
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <path 
                        d="M6 14H3C2.73478 14 2.48043 13.8946 2.29289 13.7071C2.10536 13.5196 2 13.2652 2 13V3C2 2.73478 2.10536 2.48043 2.29289 2.29289C2.48043 2.10536 2.73478 2 3 2H6M11 11L14 8M14 8L11 5M14 8H6" 
                        stroke="currentColor" 
                        strokeWidth="1.5" 
                        strokeLinecap="round" 
                        strokeLinejoin="round"
                      />
                    </svg>
                    <span>Sign Out</span>
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
      <div className="chat-list-items">
        {chats.length === 0 ? (
          <div className="empty-state">No chats yet. Start a new chat!</div>
        ) : (
          chats.map((chat) => (
            <div
              key={chat.id}
              className={`chat-list-item ${activeChat === chat.id ? 'active' : ''}`}
              onClick={() => onSelectChat(chat.id)}
            >
              <div className="chat-item-content">
                <div className="chat-item-title">
                  {truncateText(chat.title, 30)}
                </div>
                <div className="chat-item-date">
                  {formatDate(chat.updated_at)}
                </div>
              </div>
              <button
                className="delete-chat-button"
                onClick={(e) => {
                  e.stopPropagation();
                  onDeleteChat(chat.id);
                }}
              >
                ×
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
