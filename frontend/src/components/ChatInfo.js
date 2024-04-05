import React from 'react';
import { Row, Col, Card } from 'react-bootstrap';

const ChatInfo = ({ chatData }) => {
  const calculateDuration = (startTime, endTime) => {
    const start = new Date(startTime);
    const end = new Date(endTime);
    const duration = Math.floor((end - start) / 1000);
    return `${Math.floor(duration / 60)}m ${duration % 60}s`;
  };

  return (
    <Card className="mb-4">
      <Card.Body>
        <Row>
          <Col>
            <strong>Session ID:</strong> {chatData.session_id}
          </Col>
        </Row>
        <Row>
          <Col>
            <strong>Agent ID:</strong> {chatData.agent_id}
          </Col>
        </Row>
        <Row>
          <Col>
            <strong>Channel:</strong> {chatData.channel}
          </Col>
        </Row>
        <Row>
          <Col>
            <strong>Start Time:</strong> {chatData.start_time}
          </Col>
        </Row>
        <Row>
          <Col>
            <strong>End Time:</strong> {chatData.end_time}
          </Col>
        </Row>
        <Row>
          <Col>
            <strong>Duration:</strong> {calculateDuration(chatData.start_time, chatData.end_time)}
          </Col>
        </Row>
        <Row>
          <Col>
            <strong>Rating:</strong> {chatData.session_metadata?.rating || 'N/A'}
          </Col>
        </Row>
        <Row>
          <Col>
            <strong>Tags:</strong> {chatData.session_metadata?.tags?.join(', ') || 'N/A'}
          </Col>
        </Row>
      </Card.Body>
    </Card>
  );
};

export default ChatInfo;