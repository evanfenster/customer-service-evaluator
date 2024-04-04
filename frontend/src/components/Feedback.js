// Feedback.js
import React from 'react';
import { Card } from 'react-bootstrap';

export const placeholderFeedback = [
  'The agent provided helpful and informative responses throughout the conversation.',
  'The customer\'s issue was resolved in a timely manner.',
  'The agent maintained a friendly and professional tone.',
];

const Feedback = () => {
  return (
    <Card>
      <Card.Body>
        <Card.Title>Feedback</Card.Title>
        <ul>
          {placeholderFeedback.map((feedback, index) => (
            <li key={index}>{feedback}</li>
          ))}
        </ul>
      </Card.Body>
    </Card>
  );
};

export default Feedback;