# Quickstart: Frontend RAG Integration with FastAPI

**Feature**: 006-frontend-rag-integration
**Time to complete**: ~15 minutes

## Prerequisites

- Python 3.10+
- Node.js 16+ and npm/yarn
- OpenAI API key
- Existing Qdrant vector database with embeddings
- Cohere API key
- Existing backend RAG agent (agent.py)

## Step 1: Update Backend Dependencies

```bash
cd backend
pip install fastapi uvicorn python-dotenv
# Or using uv:
uv add fastapi uvicorn python-dotenv
```

## Step 2: Create FastAPI Application

Create `backend/main.py` with the FastAPI application:

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from agent import RAGAgent

# Initialize FastAPI app
app = FastAPI(
    title="RAG Agent API",
    description="API for the RAG (Retrieval-Augmented Generation) Agent",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class Source(BaseModel):
    url: str
    title: str
    chunk_index: int

class Chunk(BaseModel):
    text: str
    similarity_score: float
    source: Source

class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]
    matched_chunks: List[Chunk]
    query_time: float
    success: bool
    error: Optional[str] = None

# Initialize RAG Agent
rag_agent = RAGAgent()

@app.post("/ask", response_model=QueryResponse)
async def ask_endpoint(request: QueryRequest):
    """
    Process a user query through the RAG agent.
    """
    try:
        # Validate query length
        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        if len(request.query) > 2000:  # MAX_QUERY_LENGTH
            raise HTTPException(status_code=400, detail="Query exceeds maximum length of 2000 characters")

        # Process query using existing RAG agent
        response = rag_agent.process_query(request.query)

        # Return response in expected format
        return QueryResponse(**response)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "healthy", "service": "RAG Agent API"}

# Run with: uvicorn main:app --reload --port 8000
```

## Step 3: Update Environment File

Ensure your `backend/.env` file contains:

```env
OPENAI_API_KEY=your_openai_api_key_here  # Format: sk-... followed by 48 characters
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=https://your-cluster-id.us-east4-0.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key_here
```

## Step 4: Create Chat Component for Docusaurus

Create `book-site/src/components/ChatInterface/ChatButton.tsx`:

```tsx
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
        {isHovered ? (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H16.585L19.293 19.708C19.4777 19.8928 19.585 20.1435 19.585 20.409C19.585 20.6745 19.4777 20.9252 19.293 21.11C19.1082 21.2947 18.8575 21.402 18.592 21.402C18.3265 21.402 18.0758 21.2947 17.891 21.11L15 18.219V21C15 21.5304 14.7893 22.0391 14.4142 22.4142C14.0391 22.7893 13.5304 23 13 23H5C4.46957 23 3.96086 22.7893 3.58579 22.4142C3.21071 22.0391 3 21.5304 3 21V9C3 8.46957 3.21071 7.96086 3.58579 7.58579C3.96086 7.21071 4.46957 7 5 7H13C13.5304 7 14.0391 7.21071 14.4142 7.58579C14.7893 7.96086 15 8.46957 15 9V12.764L17.208 15.011C17.3928 15.1957 17.6435 15.303 17.909 15.303C18.1745 15.303 18.4252 15.1957 18.61 15.011C18.7947 14.8262 18.902 14.5755 18.902 14.31C18.902 14.0445 18.7947 13.7938 18.61 13.609L15.729 10.728H19C20.0606 10.728 21 11.6674 21 12.728V15Z" fill="currentColor"/>
          </svg>
        ) : (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H16.585L19.293 19.708C19.4777 19.8928 19.585 20.1435 19.585 20.409C19.585 20.6745 19.4777 20.9252 19.293 21.11C19.1082 21.2947 18.8575 21.402 18.592 21.402C18.3265 21.402 18.0758 21.2947 17.891 21.11L15 18.219V21C15 21.5304 14.7893 22.0391 14.4142 22.4142C14.0391 22.7893 13.5304 23 13 23H5C4.46957 23 3.96086 22.7893 3.58579 22.4142C3.21071 22.0391 3 21.5304 3 21V9C3 8.46957 3.21071 7.96086 3.58579 7.58579C3.96086 7.21071 4.46957 7 5 7H13C13.5304 7 14.0391 7.21071 14.4142 7.58579C14.7893 7.96086 15 8.46957 15 9V12.764L17.208 15.011C17.3928 15.1957 17.6435 15.303 17.909 15.303C18.1745 15.303 18.4252 15.1957 18.61 15.011C18.7947 14.8262 18.902 14.5755 18.902 14.31C18.902 14.0445 18.7947 13.7938 18.61 13.609L15.729 10.728H19C20.0606 10.728 21 11.6674 21 12.728V15Z" fill="currentColor"/>
          </svg>
        )}
      </div>
    </button>
  );
};

export default ChatButton;
```

Create `book-site/src/components/ChatInterface/ChatWindow.tsx`:

```tsx
import React, { useState, useRef, useEffect } from 'react';
import ChatMessages from './ChatMessages';
import './ChatInterface.css';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  sources?: Array<{
    url: string;
    title: string;
    chunk_index: number;
  }>;
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
      const response = await fetch('http://localhost:8000/ask', {
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
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data = await response.json();

      // Add assistant response
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: data.answer,
        role: 'assistant',
        timestamp: new Date(),
        sources: data.sources,
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Error:', err);
      setError('Failed to get response. Please try again.');

      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'Sorry, I encountered an error processing your request. Please try again.',
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
            <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>

      <ChatMessages messages={messages} isLoading={isLoading} />

      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask a question about robotics..."
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
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M22 2L11 13M22 2L15 22L11 13M11 13L2 9L22 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
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
```

Create `book-site/src/components/ChatInterface/ChatMessages.tsx`:

```tsx
import React from 'react';
import './ChatInterface.css';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  sources?: Array<{
    url: string;
    title: string;
    chunk_index: number;
  }>;
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
          <h4>Hello! I'm your AI assistant.</h4>
          <p>Ask me anything about robotics, ROS 2, or the content in this documentation.</p>
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
            {message.role === 'assistant' && message.sources && message.sources.length > 0 && (
              <div className="sources-section">
                <h5>Sources:</h5>
                <ul>
                  {message.sources.slice(0, 3).map((source, index) => (
                    <li key={index}>
                      <a href={source.url} target="_blank" rel="noopener noreferrer">
                        {source.title}
                      </a>
                    </li>
                  ))}
                </ul>
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
```

Create `book-site/src/components/ChatInterface/ChatInterface.css`:

```css
.chat-button {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #2563eb;
  color: white;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.chat-button:hover {
  background-color: #1d4ed8;
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.chat-button:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.4);
}

.chat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-window {
  position: fixed;
  bottom: 100px;
  right: 30px;
  width: 380px;
  height: 500px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  display: flex;
  flex-direction: column;
  z-index: 1000;
  overflow: hidden;
  border: 1px solid #e5e7eb;
}

.chat-header {
  padding: 16px;
  background-color: #2563eb;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
}

.close-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background-color: #f9fafb;
  display: flex;
  flex-direction: column;
}

.welcome-message {
  text-align: center;
  padding: 20px 0;
  color: #6b7280;
}

.welcome-message h4 {
  margin: 0 0 8px 0;
  color: #1f2937;
}

.welcome-message p {
  margin: 0;
  font-size: 14px;
}

.message {
  margin-bottom: 16px;
  max-width: 85%;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.user-message {
  align-self: flex-end;
  background-color: #2563eb;
  color: white;
  padding: 12px 16px;
  border-radius: 18px 18px 4px 18px;
}

.assistant-message {
  align-self: flex-start;
  background-color: white;
  padding: 12px 16px;
  border-radius: 18px 18px 18px 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.message-content {
  line-height: 1.5;
}

.sources-section {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #e5e7eb;
}

.sources-section h5 {
  margin: 0 0 4px 0;
  font-size: 12px;
  color: #6b7280;
  font-weight: 600;
}

.sources-section ul {
  margin: 0;
  padding-left: 16px;
  font-size: 12px;
}

.sources-section li {
  margin-bottom: 4px;
}

.sources-section a {
  color: #2563eb;
  text-decoration: none;
}

.sources-section a:hover {
  text-decoration: underline;
}

.message-timestamp {
  font-size: 10px;
  color: #9ca3af;
  text-align: right;
  margin-top: 4px;
}

.typing-indicator {
  display: flex;
  align-items: center;
  padding: 8px 0;
}

.dot {
  width: 8px;
  height: 8px;
  background-color: #9ca3af;
  border-radius: 50%;
  margin: 0 2px;
  animation: bounce 1.5s infinite;
}

.dot:nth-child(2) {
  animation-delay: 0.2s;
}

.dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

.chat-input-form {
  display: flex;
  padding: 12px;
  background-color: white;
  border-top: 1px solid #e5e7eb;
}

.chat-input {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 20px;
  font-size: 14px;
  outline: none;
}

.chat-input:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.send-button {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #2563eb;
  color: white;
  border: none;
  margin-left: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-button:hover:not(:disabled) {
  background-color: #1d4ed8;
}

.send-button:disabled {
  background-color: #d1d5db;
  cursor: not-allowed;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #ffffff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  background-color: #fee2e2;
  color: #dc2626;
  padding: 8px 16px;
  font-size: 12px;
  text-align: center;
  border-top: 1px solid #fecaca;
}

/* Responsive design */
@media (max-width: 768px) {
  .chat-window {
    width: calc(100% - 30px);
    height: 50vh;
    bottom: 80px;
    right: 15px;
    left: 15px;
  }

  .chat-button {
    bottom: 20px;
    right: 20px;
    width: 50px;
    height: 50px;
  }
}
```

Create `book-site/src/components/ChatInterface/index.tsx`:

```tsx
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
```

## Step 5: Integrate Chat Component into Docusaurus

Update your Docusaurus layout to include the chat component. In `book-site/src/theme/Layout/index.js` or in the main App component:

```jsx
import React from 'react';
import Layout from '@theme-original/Layout';
import ChatInterface from '../components/ChatInterface';

export default function LayoutWrapper(props) {
  return (
    <>
      <Layout {...props}>
        {props.children}
        <ChatInterface />
      </Layout>
    </>
  );
}
```

## Step 6: Run the Applications

Start the backend FastAPI server:

```bash
cd backend
uvicorn main:app --reload --port 8000
```

In a new terminal, start the Docusaurus development server:

```bash
cd book-site
npm run start
# or if using yarn:
yarn start
```

## Expected Behavior

1. Visit your Docusaurus site and see a floating chat button in the bottom-right corner
2. Click the button to open the chat interface
3. Type a question and submit it
4. The backend processes the query using the RAG agent
5. The response with answer, sources, and matched chunks appears in the chat
6. Loading indicators show while processing
7. Error handling displays appropriate messages

## Verification

1. Check that the `/ask` endpoint returns properly formatted JSON responses
2. Verify that the chat UI displays messages correctly
3. Confirm that loading states are properly shown
4. Test error handling with invalid queries
5. Verify that sources are displayed as clickable links