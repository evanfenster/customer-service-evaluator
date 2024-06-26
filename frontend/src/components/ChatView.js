import React from 'react';
import { Card } from 'react-bootstrap';
import './ChatView.css';

const ChatView = ({ messages }) => {
  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case 'negative':
        return 'red';
      case 'neutral':
        return 'yellow';
      case 'positive':
        return 'green';
      default:
        return '';
    }
  };

  return (
    <Card className="chat-card">
      <Card.Body>
        <Card.Title className="text-center mb-4">Chat History</Card.Title>
        <div className="chat-container">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`chat-message ${message.sender === 'customer' ? 'customer' : 'agent'}`}
            >
              <div className={`message-bubble ${getSentimentColor(message.sentiment)}`}>
                <div className="message-text">{message.text}</div>
                <div className="message-time">{new Date(message.timestamp).toLocaleString()}</div>
              </div>
            </div>
          ))}
        </div>
      </Card.Body>
    </Card>
  );
};

export default ChatView;