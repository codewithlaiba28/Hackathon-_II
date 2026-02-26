import React, { useState } from 'react';

interface ChatbotMessage {
  id: number;
  sender: 'user' | 'bot';
  text: string;
}

interface ChatbotProps {
  // Function to send message to backend and receive response
  onSendMessage: (message: string) => Promise<ChatbotMessage>;
}

const Chatbot: React.FC<ChatbotProps> = ({ onSendMessage }) => {
  const [messages, setMessages] = useState<ChatbotMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (input.trim() === '') return;

    const newMessage: ChatbotMessage = { id: messages.length + 1, sender: 'user', text: input };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
    setInput('');
    setLoading(true);

    try {
      // Simulate sending to backend and getting a response
      // In a real application, this would call your FastAPI backend endpoint
      // which would then use the ChatbotNLPService.
      const botResponse = await onSendMessage(input);
      setMessages((prevMessages) => [...prevMessages, botResponse]);
    } catch (error) {
      console.error("Error sending message:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { id: prevMessages.length + 1, sender: 'bot', text: 'Sorry, I encountered an error.' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !loading) {
      handleSend();
    }
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '10px', width: '400px', height: '500px', display: 'flex', flexDirection: 'column' }}>
      <div style={{ flexGrow: 1, overflowY: 'auto', marginBottom: '10px' }}>
        {messages.map((message) => (
          <div key={message.id} style={{ textAlign: message.sender === 'user' ? 'right' : 'left', margin: '5px 0' }}>
            <span style={{
              display: 'inline-block',
              padding: '8px 12px',
              borderRadius: '15px',
              backgroundColor: message.sender === 'user' ? '#007bff' : '#f1f1f1',
              color: message.sender === 'user' ? 'white' : 'black',
            }}>
              {message.text}
            </span>
          </div>
        ))}
      </div>
      <div style={{ display: 'flex' }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
          style={{ flexGrow: 1, padding: '8px', border: '1px solid #ddd', borderRadius: '5px' }}
          disabled={loading}
        />
        <button onClick={handleSend} disabled={loading} style={{ marginLeft: '10px', padding: '8px 15px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '5px' }}>
          Send
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
