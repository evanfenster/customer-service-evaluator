// Feedback.js
import React from 'react';
import { Card } from 'react-bootstrap';
import ReactMarkdown from 'react-markdown';

const Feedback = ({feedback}) => {
  return (
    <Card>
      <Card.Body>
        <Card.Title>Feedback</Card.Title>
          <ReactMarkdown>{feedback}</ReactMarkdown>
      </Card.Body>
    </Card>
  );
};

export default Feedback;