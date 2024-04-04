import React from 'react';
import { Card } from 'react-bootstrap';
import './ChatView.css';

const ChatView = ({ messages }) => {
  return (
    <Card>
      <Card.Body>
        <Card.Title>Chat History</Card.Title>
        <div className="chat-container">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`chat-message ${message.sender === 'customer' ? 'customer' : 'agent'}`}
            >
              <div className="message-bubble">
                <div className="message-text">{message.text}</div>
                <div className="message-time">{new Date(message.timestamp).toLocaleTimeString()}</div>
              </div>
            </div>
          ))}
        </div>
      </Card.Body>
    </Card>
  );
};

export default ChatView;