import React, { useState } from 'react';
import './ChatInterface.css';

interface ChatButtonProps {
  onClick: () => void;
}

const ChatButton: React.FC<ChatButtonProps> = ({ onClick }) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <button
      className="chat-button"
      onClick={onClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      aria-label="Open chat"
    >
      <div className="chat-icon">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2C6.48 2 2 6.48 2 12C2 13.54 2.36 15.02 3.01 16.35L2 22L7.65 20.99C8.98 21.64 10.46 22 12 22C17.52 22 22 17.52 22 12S17.52 2 12 2Z" fill="#2563eb"/>
          <circle cx="8.5" cy="9.5" r="1.1" fill="white"/>
          <circle cx="15.5" cy="9.5" r="1.1" fill="white"/>
          <path d="M9 14.5C9 14.5 11 16 12 16C13 16 15 14.5 15 14.5" stroke="white" strokeWidth="1.1" strokeLinecap="round"/>
        </svg>
      </div>
    </button>
  );
};

export default ChatButton;