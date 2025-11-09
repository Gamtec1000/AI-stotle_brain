// frontend/src/components/AristotleWidget.tsx
/**
 * AI-stotle Chat Widget
 * Embeddable on any page of carlsnewton.com
 */

import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Sparkles, X, Minimize2, Maximize2 } from 'lucide-react';
import './AristotleWidget.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface AristotleWidgetProps {
  apiUrl?: string;
  studentAge?: number;
  theme?: 'light' | 'dark';
  position?: 'bottom-right' | 'bottom-left';
}

const AristotleWidget: React.FC<AristotleWidgetProps> = ({
  apiUrl = 'http://localhost:8000',
  studentAge = 10,
  theme = 'dark',
  position = 'bottom-right'
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: '🏛️ Greetings, young scholar! I am AI-stotle, your wise science companion. Ask me anything about our experiments!',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${apiUrl}/ask`, {
        question: input,
        student_age: studentAge,
        use_knowledge_base: true
      });

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.data.answer,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);

      const errorMessage: Message = {
        role: 'assistant',
        content: 'Apologies, young scholar. I seem to have lost my train of thought. Please try again.',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  if (!isOpen) {
    return (
      <button
        className={`aristotle-fab ${position}`}
        onClick={() => setIsOpen(true)}
        aria-label="Open AI-stotle"
      >
        <Sparkles size={24} />
        <span className="fab-text">Ask AI-stotle</span>
      </button>
    );
  }

  return (
    <div className={`aristotle-widget ${position} ${theme} ${isMinimized ? 'minimized' : ''}`}>

      {/* Header */}
      <div className="widget-header">
        <div className="header-content">
          <div className="header-icon">
            <Sparkles size={20} />
          </div>
          <div className="header-text">
            <h3>AI-stotle</h3>
            <p>Your Wise Science Guide</p>
          </div>
        </div>

        <div className="header-actions">
          <button
            className="header-btn"
            onClick={() => setIsMinimized(!isMinimized)}
            aria-label="Minimize"
          >
            {isMinimized ? <Maximize2 size={18} /> : <Minimize2 size={18} />}
          </button>
          <button
            className="header-btn"
            onClick={() => setIsOpen(false)}
            aria-label="Close"
          >
            <X size={18} />
          </button>
        </div>
      </div>

      {/* Messages */}
      {!isMinimized && (
        <>
          <div className="widget-messages">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`message ${message.role}`}
              >
                {message.role === 'assistant' && (
                  <div className="message-avatar">🏛️</div>
                )}

                <div className="message-content">
                  <p>{message.content}</p>
                  <span className="message-time">
                    {message.timestamp.toLocaleTimeString([], {
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </span>
                </div>

                {message.role === 'user' && (
                  <div className="message-avatar">👤</div>
                )}
              </div>
            ))}

            {isLoading && (
              <div className="message assistant">
                <div className="message-avatar">🏛️</div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="widget-input">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask AI-stotle about science..."
              disabled={isLoading}
              rows={1}
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !input.trim()}
              className="send-btn"
              aria-label="Send message"
            >
              <Send size={20} />
            </button>
          </div>

          {/* Footer */}
          <div className="widget-footer">
            <p>Powered by AI-stotle • DeepSeek</p>
          </div>
        </>
      )}
    </div>
  );
};

export default AristotleWidget;
