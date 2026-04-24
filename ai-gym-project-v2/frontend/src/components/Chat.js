import React, { useState, useRef, useEffect } from 'react';

const API_URL = "https://ai-gym-project-ey72.onrender.com";

const SUGGESTIONS = [
  "How to build muscle fast?",
  "Best diet for weight loss",
  "Beginner workout routine",
  "How much protein do I need?",
  "Tips for better recovery",
  "What supplements should I take?",
];

const WELCOME_MESSAGE = {
  id: 'welcome',
  role: 'bot',
  text: "Hey there! 💪 I'm FitAI, your personal AI fitness coach. Ask me anything about workouts, nutrition, supplements, or training tips. I'm here to help you crush your goals!",
  time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
};

function Chat() {
  const [messages, setMessages] = useState([WELCOME_MESSAGE]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages, loading]);

  const sendMessage = async (text) => {
    const messageText = (text || input).trim();
    if (!messageText || loading) return;

    const userMsg = {
      id: Date.now(),
      role: 'user',
      text: messageText,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);
    setError('');

    try {
      const res = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: messageText }),
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.error || `Server error: ${res.status}`);
      }

      const data = await res.json();

      const botMsg = {
        id: Date.now() + 1,
        role: 'bot',
        text: data.response,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages(prev => [...prev, botMsg]);
    } catch (err) {
      setError(`Connection error: ${err.message}. Make sure the Flask backend is running on port 5000.`);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div>
      {/* Chat header */}
      <div className="chat-header">
        <div className="bot-avatar">🤖</div>
        <div className="bot-info">
          <h2>FitAI Coach</h2>
          <p><span className="online-dot" />Online — Ready to help</p>
        </div>
      </div>

      {/* Suggestion chips */}
      <div className="suggestions">
        {SUGGESTIONS.map((s, i) => (
          <button
            key={i}
            className="suggestion-chip"
            onClick={() => sendMessage(s)}
            disabled={loading}
          >
            {s}
          </button>
        ))}
      </div>

      {/* Messages area */}
      <div className="chat-container">
        <div className="messages-area">
          {messages.map((msg) => (
            <div key={msg.id} className={`message ${msg.role}`}>
              <div className={`msg-avatar ${msg.role}`}>
                {msg.role === 'bot' ? '🤖' : '👤'}
              </div>
              <div>
                <div className="msg-bubble">{msg.text}</div>
                <div className="msg-time">{msg.time}</div>
              </div>
            </div>
          ))}

          {/* Typing indicator */}
          {loading && (
            <div className="message bot">
              <div className="msg-avatar bot">🤖</div>
              <div className="typing-indicator">
                <div className="typing-dot" />
                <div className="typing-dot" />
                <div className="typing-dot" />
              </div>
            </div>
          )}

          {error && (
            <div className="error-msg">
              ⚠️ {error}
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input area */}
        <div className="chat-input-area">
          <textarea
            ref={inputRef}
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about workouts, diet, supplements..."
            rows={1}
            disabled={loading}
          />
          <button
            className="send-btn"
            onClick={() => sendMessage()}
            disabled={!input.trim() || loading}
          >
            ➤
          </button>
        </div>
      </div>
    </div>
  );
}

export default Chat;
