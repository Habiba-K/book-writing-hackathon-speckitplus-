import React, { useState, useRef, useEffect } from 'react';
import ChatMessages from './ChatMessages';
import './ChatInterface.css';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  primarySource?: {
    url: string;
    title: string;
    chunk_index: number;
  };
  isOutOfScope?: boolean;
}

interface ChatWindowProps {
  isOpen: boolean;
  onClose: () => void;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ isOpen, onClose }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      role: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      // Call backend API
      const response = await fetch('https://khabiba17-deploy-chatbot.hf.space/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: inputValue,
          top_k: 5,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        let errorMessage = `API request failed with status ${response.status}`;

        if (response.status === 401) {
          errorMessage = 'API key configuration error. Please check backend settings.';
        } else if (response.status === 504) {
          errorMessage = 'Connection timeout to external service. Please try again later.';
        } else if (response.status === 404) {
          errorMessage = 'Backend API endpoint not found. Please ensure the backend service is running on port 8000.';
        } else if (response.status === 0) {
          errorMessage = 'Unable to connect to the backend service. Please ensure the backend is running and accessible.';
        } else if (errorData.detail) {
          errorMessage = errorData.detail;
        }

        throw new Error(errorMessage);
      }

      const data = await response.json();

      // Add assistant response
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: data.answer,
        role: 'assistant',
        timestamp: new Date(),
        primarySource: data.primary_source,
        isOutOfScope: data.is_out_of_scope,
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err: any) {
      console.error('Error:', err);
      const errorMessageText = err.message || 'Failed to get response. Please try again.';
      setError(errorMessageText);

      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: errorMessageText,
        role: 'assistant',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="chat-window">
      <div className="chat-header">
        <h3>AI Assistant</h3>
        <button className="close-button" onClick={onClose} aria-label="Close chat">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M6.2253 4.81109C5.83477 4.42056 5.20161 4.42056 4.81108 4.81109C4.42056 5.20161 4.42056 5.83477 4.81108 6.2253L10.5858 12L4.81109 17.7747C4.42056 18.1652 4.42056 18.7984 4.81109 19.1889C5.20161 19.5794 5.83477 19.5794 6.22529 19.1889L12 13.4142L17.7747 19.1889C18.1652 19.5794 18.7984 19.5794 19.1889 19.1889C19.5794 18.7984 19.5794 18.1652 19.1889 17.7747L13.4142 12L19.1889 6.2253C19.5794 5.83477 19.5794 5.20161 19.1889 4.81109C18.7984 4.42056 18.1652 4.42056 17.7747 4.81109L12 10.5858L6.2253 4.81109Z" fill="currentColor"/>
          </svg>
        </button>
      </div>

      <ChatMessages messages={messages} isLoading={isLoading} />

      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask a question about robotics, ROS 2, or AI..."
          disabled={isLoading}
          className="chat-input"
        />
        <button
          type="submit"
          disabled={!inputValue.trim() || isLoading}
          className="send-button"
          aria-label="Send message"
        >
          {isLoading ? (
            <div className="loading-spinner"></div>
          ) : (
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3.478 2.405A.75.75 0 0 0 1.97 3.75c0 5.291.009 9.095.009 13.368 0 1.194.321 2.33.978 3.232a.75.75 0 0 0 1.18.14l13.78-9.58a.75.75 0 0 0 0-1.244L4.15 2.405a.75.75 0 0 0-.672-.001Z" fill="currentColor"/>
            </svg>
          )}
        </button>
      </form>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatWindow;