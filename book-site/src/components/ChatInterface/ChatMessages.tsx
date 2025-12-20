import React from 'react';
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

interface ChatMessagesProps {
  messages: Message[];
  isLoading: boolean;
}

const ChatMessages: React.FC<ChatMessagesProps> = ({ messages, isLoading }) => {
  return (
    <div className="chat-messages">
      {messages.length === 0 ? (
        <div className="welcome-message">
          <h4>🤖 Hello! I'm your AI Assistant</h4>
          <p>Ask me anything about robotics, ROS 2, or the content in this documentation.</p>
          <p style={{marginTop: '10px', fontSize: '13px', color: '#6b7280'}}>
            <strong>Tip:</strong> I'll show you a single relevant source for each answer.
          </p>
        </div>
      ) : (
        messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}
          >
            <div className="message-content">
              {message.content}
            </div>
            {message.role === 'assistant' && message.primarySource && (
              <div className="sources-section">
                <h5>Source:</h5>
                <ul>
                  <li>
                    <a href={message.primarySource.url} target="_blank" rel="noopener noreferrer">
                      {message.primarySource.title}
                    </a>
                  </li>
                </ul>
              </div>
            )}
            {message.role === 'assistant' && message.isOutOfScope && (
              <div className="sources-section">
                <p className="out-of-scope-note">This content is not related to this book.</p>
              </div>
            )}
            <div className="message-timestamp">
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))
      )}
      {isLoading && (
        <div className="message assistant-message">
          <div className="typing-indicator">
            <div className="dot"></div>
            <div className="dot"></div>
            <div className="dot"></div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatMessages;