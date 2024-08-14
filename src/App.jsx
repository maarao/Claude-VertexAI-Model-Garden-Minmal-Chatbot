import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }

  useEffect(scrollToBottom, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { text: input, user: true };
    setMessages([...messages, userMessage]);
    setInput('');

    try {
      const response = await axios.post('http://localhost:5000/chat', { message: input });
      const botMessage = { text: response.data.response, user: false };
      setMessages(messages => [...messages, botMessage]);
      console.log(response.data.response)
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="size-full">
      <div className="chat-container">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.user ? 'user' : 'bot'} bg-gray-800`} style={{ whiteSpace: 'pre-wrap', textAlign: 'left' }}>
            {message.user ? "You: " + message.text : "Claude: " + message.text}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSubmit}>
        <textarea
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default App;