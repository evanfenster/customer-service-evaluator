// ChatInfo.js
import React from 'react';
import { Row, Col, Card, ListGroup } from 'react-bootstrap';

const ChatInfo = ({ chatData }) => {
  const calculateDuration = (startTime, endTime) => {
    const start = new Date(startTime);
    const end = new Date(endTime);
    const duration = Math.floor((end - start) / 1000); // Duration in seconds
    return `${Math.floor(duration / 60)}m ${duration % 60}s`; // Format as "Xm Ys"
  };

  return (
    <Card>
    <Card.Body>
        <Row>
        <Col>
            <strong>Session ID:</strong> {chatData.session_id}
        </Col>
        <Col>
            <strong>Start Time:</strong> {chatData.start_time}
        </Col>
        <Col>
            <strong>End Time:</strong> {chatData.end_time}
        </Col>
        <Col>
            <strong>Duration:</strong> {calculateDuration(chatData.start_time, chatData.end_time)}
        </Col>
        </Row>
        <Row>
        <Col>
            <strong>Agent ID:</strong> {chatData.agent_id}
        </Col>
        <Col>
            <strong>Channel:</strong> {chatData.channel}
        </Col>
        <Col>
            <strong>Rating:</strong> {chatData.session_metadata?.rating || 'N/A'}
        </Col>
        <Col>
            <strong>Tags:</strong> {chatData.session_metadata?.tags?.join(', ') || 'N/A'}
        </Col>
        </Row>
    </Card.Body>
    </Card>
  );
};

export default ChatInfo;