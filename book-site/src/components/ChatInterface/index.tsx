import React, { useState } from 'react';
import ChatButton from './ChatButton';
import ChatWindow from './ChatWindow';
import './ChatInterface.css';

const ChatInterface: React.FC = () => {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  const closeChat = () => {
    setIsChatOpen(false);
  };

  return (
    <>
      <ChatButton onClick={toggleChat} />
      <ChatWindow isOpen={isChatOpen} onClose={closeChat} />
    </>
  );
};

export default ChatInterface;