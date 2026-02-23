/**
 * ChatBot Component
 * AI mentor chatbot interface with message history
 */

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import apiService from '../services/api';
import '../styles/chatbot.css';

const ChatBot = ({ recommendations }) => {
  const [messages, setMessages] = useState([
    {
      id: 0,
      sender: 'bot',
      content: "Hi! I'm your AI career mentor. Ask me anything about your recommended paths, learning strategies, or next steps. 🚀",
      timestamp: new Date(),
    },
  ]);

  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Load chat history
  useEffect(() => {
    const loadHistory = async () => {
      try {
        const response = await apiService.getChatHistory(10);
        if (response.data.success) {
          setMessages((prev) => [
            ...prev,
            ...response.data.messages.map((msg) => ({
              ...msg,
              timestamp: new Date(msg.created_at),
            })),
          ]);
        }
      } catch (err) {
        console.error('Error loading chat history:', err);
      }
    };

    loadHistory();
  }, []);

  const handleSendMessage = async (e) => {
    e.preventDefault();

    if (!inputValue.trim()) return;

    // Add user message
    const userMessage = {
      id: messages.length,
      sender: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);

    try {
      const response = await apiService.sendMessage(inputValue);

      if (response.data.success) {
        const botMessage = {
          id: messages.length + 1,
          sender: 'bot',
          content: response.data.response,
          sentiment: response.data.sentiment,
          timestamp: new Date(),
        };

        setMessages((prev) => [...prev, botMessage]);
      }
    } catch (err) {
      const errorMessage = {
        id: messages.length + 1,
        sender: 'bot',
        content:
          "I encountered an error processing your message. Please try again.",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const quickPrompts = [
    'Tell me about my top recommendation',
    'What skills should I focus on?',
    'How long will it take?',
    'What projects should I build?',
  ];

  const handleQuickPrompt = (prompt) => {
    setInputValue(prompt);
  };

  return (
    <div className="chatbot-container">
      {/* Header */}
      <div className="chat-header">
        <h2>🤖 Career Mentor Chat</h2>
        <p>Ask me anything about your career journey</p>
      </div>

      {/* Messages Area */}
      <div className="chat-messages">
        <AnimatePresence>
          {messages.map((msg, idx) => (
            <motion.div
              key={msg.id}
              className={`message ${msg.sender}-message`}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
            >
              <div className="message-bubble">
                <p>{msg.content}</p>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {loading && (
          <div className="message bot-message">
            <div className="message-bubble loading">
              <span className="typing-dot"></span>
              <span className="typing-dot"></span>
              <span className="typing-dot"></span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick Prompts - Show on first message */}
      {messages.length === 1 && !loading && (
        <div className="quick-prompts">
          <p>Quick start:</p>
          <div className="prompt-buttons">
            {quickPrompts.map((prompt, idx) => (
              <button
                key={idx}
                className="prompt-btn"
                onClick={() => handleQuickPrompt(prompt)}
              >
                {prompt}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input Area */}
      <form className="chat-input-form" onSubmit={handleSendMessage}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask me anything..."
          disabled={loading}
          className="chat-input"
        />
        <button
          type="submit"
          className="btn btn-primary"
          disabled={!inputValue.trim() || loading}
        >
          {loading ? '⏳' : '📤'}
        </button>
      </form>
    </div>
  );
};

export default ChatBot;
