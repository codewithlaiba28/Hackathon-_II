import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { user } = useAuth();

  // Function to send message to the backend API
  const sendMessage = async () => {
    if (!inputMessage.trim() || !user) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputMessage;
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch(`/api/${user.id}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${user.id}`
        },
        body: JSON.stringify({
          message: currentInput
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.response || data.message || "I've processed your request.",
        timestamp: new Date(),
        tool_calls: data.tool_calls || []
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: `Sorry, there was an error: ${error.message}`,
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-container">
      <div className="messages-list">
        {messages.length === 0 && (
          <div className="empty-state">
            <h3>How can I help you today?</h3>
            <p>Try saying "Add a task to buy groceries" or "Show my pending tasks"</p>
          </div>
        )}
        {messages.map((message) => (
          <div key={message.id} className={`message-wrapper ${message.role}`}>
            <div className={`message-bubble ${message.role} ${message.isError ? 'error' : ''}`}>
              <div className="content">{message.content}</div>
              {message.tool_calls && message.tool_calls.length > 0 && (
                <div className="tool-tags">
                  {message.tool_calls.map((tc, i) => (
                    <span key={i} className="tool-tag">🛠 {tc.name}</span>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message-wrapper assistant">
            <div className="message-bubble assistant typing">
              <span className="dot"></span>
              <span className="dot"></span>
              <span className="dot"></span>
            </div>
          </div>
        )}
      </div>

      <div className="input-container">
        <div className="input-wrapper">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Message Todo AI..."
            rows={1}
            disabled={isLoading}
          />
          <button onClick={sendMessage} disabled={isLoading || !inputMessage.trim()}>
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ width: '20px', height: '20px' }}>
              <path d="M7 11L12 6L17 11M12 18V7" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </button>
        </div>
        <p className="disclaimer">AI can make mistakes. Check important info.</p>
      </div>

      <style jsx>{`
        .chat-container {
          display: flex;
          flex-direction: column;
          height: calc(100vh - 150px);
          max-width: 800px;
          margin: 0 auto;
          position: relative;
        }
        .messages-list {
          flex: 1;
          overflow-y: auto;
          padding: 20px 0;
          display: flex;
          flex-direction: column;
          gap: 24px;
        }
        .empty-state {
          text-align: center;
          margin-top: 100px;
          color: #666;
        }
        .message-wrapper {
          display: flex;
          width: 100%;
        }
        .message-wrapper.user { justify-content: flex-end; }
        .message-bubble {
          max-width: 80%;
          padding: 12px 18px;
          border-radius: 18px;
          font-size: 15px;
          line-height: 1.5;
        }
        .message-bubble.user {
          background-color: #f4f4f4;
          color: #1a1a1a;
          border-bottom-right-radius: 4px;
        }
        .message-bubble.assistant {
          background-color: transparent;
          color: #1a1a1a;
          padding-left: 0;
        }
        .message-bubble.error {
          background-color: #fee2e2;
          color: #991b1b;
        }
        .tool-tags {
          display: flex;
          gap: 8px;
          margin-top: 8px;
          flex-wrap: wrap;
        }
        .tool-tag {
          font-size: 12px;
          background: #e5e7eb;
          padding: 2px 8px;
          border-radius: 4px;
          color: #4b5563;
        }
        .input-container {
          padding: 20px 0;
          background: white;
        }
        .input-wrapper {
          display: flex;
          align-items: center;
          background: #f4f4f4;
          border-radius: 24px;
          padding: 8px 16px;
          gap: 12px;
          border: 1px solid #e5e5e5;
        }
        textarea {
          flex: 1;
          background: transparent;
          border: none;
          outline: none;
          resize: none;
          padding: 8px 0;
          font-size: 15px;
          font-family: inherit;
        }
        button {
          background: #1a1a1a;
          color: white;
          border: none;
          border-radius: 50%;
          width: 32px;
          height: 32px;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          transition: transform 0.2s;
        }
        button:hover { transform: scale(1.05); }
        button:disabled { opacity: 0.3; cursor: not-allowed; }
        .disclaimer {
          font-size: 12px;
          color: #999;
          text-align: center;
          margin-top: 12px;
        }
        .typing { display: flex; gap: 4px; padding: 12px 0; }
        .dot {
          width: 6px;
          height: 6px;
          background: #ccc;
          border-radius: 50%;
          animation: bounce 1.4s infinite ease-in-out;
        }
        .dot:nth-child(1) { animation-delay: -0.32s; }
        .dot:nth-child(2) { animation-delay: -0.16s; }
        @keyframes bounce {
          0%, 80%, 100% { transform: scale(0); }
          40% { transform: scale(1); }
        }
      `}</style>
    </div>
  );
};

export default ChatInterface;